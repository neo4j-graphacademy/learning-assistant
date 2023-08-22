from neo4j import GraphDatabase
import os
import requests
from urllib.parse import urlparse, urlunparse
import bs4
from dotenv import load_dotenv
from utils import batch, cleaned_image, cleaned_link
from db import import_pages
from math import ceil
import json

def get_indexable_pages(driver):
    records, summary, keys = driver.execute_query("""
        MATCH (c:Course)-[:HAS_MODULE]->(m)-[:HAS_LESSON]->(l)
        WHERE NOT c.status IN $negative + ['redirect']
        UNWIND [ m.link, l.link ] AS link
        RETURN distinct link
    """, negative = ['disabled', 'deleted'])

    return [ record['link'] for record in records ]

def graphacademy_url(url, fragment = ''):
    parsed = urlparse(url)
    return urlunparse(("https", "graphacademy.neo4j.com", parsed.path, parsed.params, '', fragment))


def fetch_and_parse(url):
    url = graphacademy_url(url)

    # Send a GET request to the URL
    response = requests.get(url, headers={
        "User-Agent": os.getenv('GA_USER_AGENT')
    })

    # Check if the request was successful
    if response.status_code == 200:
        return extract_graphacademy(url, response.content)



def extract_graphacademy(url, html):
    url = graphacademy_url(url)

    soup = bs4.BeautifulSoup(html, features="lxml")

    title_element = soup.find("h1", class_="module-title")
    title =  " ".join([text for text in title_element.stripped_strings])


    article = soup.find('article', class_='doc')
    links = article.find_all('a')

    cleaned_links = []

    for link in links:
        if link.get('href') != None and not link.get('href').startswith('#'):
            cleaned_links.append(cleaned_link(url, link))

    sections = []

    for index, section in enumerate(soup.select('#preamble, .section')):
        header = section.find('h2')
        section_links = [ cleaned_link(url, link) for link in section.find_all('a') if link.text != "" ]

        anchor = section.find('a', class_='anchor')
        section_url = graphacademy_url(url, 'section-'+ str(index))


        code_blocks = []
        for pre in section.find_all('pre'):
            language = pre.find('div', class_="code-language")
            code_title = pre.find('div', class_='code-title')
            code = pre.find('code')

            if code:
                code_blocks.append({
                    "language": language.text.strip() if language is not None else None,
                    "title": code_title.text.strip() if code_title is not None else None,
                    "code": code.text
                })

        section_title = header.text.strip() if header is not None else ""

        sections.append({
            "url": section_url,
            "title": section_title,
            "text": section.text.strip().replace(section_title, f"{section_title} - "),
            "anchor": anchor.get('href') if anchor else None,
            "links": section_links,
            "images": [ cleaned_image(url, img) for img in section.find_all('img') ],
            "code": code_blocks
        })

    return {
        "url": graphacademy_url(url),
        "title": title,
        "links": cleaned_links,
        "sections": sections
    }


if __name__ == "__main__":
    load_dotenv()

    # Connect to Chatbot Neo4j
    driver = GraphDatabase.driver(
        os.getenv('NEO4J_URI'),
        auth=(
            os.getenv('NEO4J_USERNAME'),
            os.getenv('NEO4J_PASSWORD')
        )
    )
    driver.verify_connectivity()

    # Connect to GraphAcademy Neo4j
    ga_driver = GraphDatabase.driver(
        os.getenv('GA_NEO4J_URI'),
        auth=(
            os.getenv('GA_NEO4J_USERNAME'),
            os.getenv('GA_NEO4J_PASSWORD')
        )
    )
    ga_driver.verify_connectivity()

    indexable = get_indexable_pages(ga_driver)

    batch_no = 0
    batch_size = 100
    batches = ceil(len(indexable) / batch_size)

    with driver.session() as session:
        for urls in batch(indexable, batch_size):
            batch_no += 1
            print(batch_no)

            rows = [ fetch_and_parse(url) for url in urls ]

            res = session.execute_write(import_pages, rows=[r for r in rows if r is not None])

    driver.close()
    ga_driver.close()
