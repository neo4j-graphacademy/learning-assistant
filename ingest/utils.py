import os
import openai
import bs4
import re
from urllib.parse import urljoin, urlparse, urlunparse
from neo4j import GraphDatabase

# Dictionary containing folder mapping
current_mapping = {
  "current": {
     "api-java-driver": "5.8",
     "api-javascript-driver": "5.8",
     "api-dotnet-driver": "5.8",
     "api-python-driver": "5.8",
     "apoc": "5",
     "aura": "current",
     "bloom-user-guide": "2.7",
     "bolt": "1.0",
     "browser-manual":"5",
     "cypher-cheat-sheet": "5",
     "cypher-manual": "5",
     "cypher-refcard": "5",
     "desktop-manual":"1.5",
     "dotnet-manual": "5",
     "driver-manual": "4.2",
     "getting-started": "5",
     "go-manual": "5",
     "graph-algorithms": "3.5",
     "graph-data-science": "2.3",
     "graph-data-science-client": "1.6",
     "graphql-manual":"3.0",
     "http-api": "5",
     "java-manual": "5",
     "java-reference": "5",
     "javascript-manual": "5",
     "kerberos-add-on": "4.0",
     "migration-guide": "current",
     "ogm-manual": "4.0",
     "operations-manual": "5",
     "ops-manager": "1.5",
     "python-manual":"5",
     "rest-docs": "3.5",
     "spark": "5.0",
     "spring-data-neo4j-rx": "1.0",
     "status-codes": "5",
#      "upgrade-migration-guide": "current"
 }
}

def absolute_url(url, link):
    url = urljoin(url, link.get('href'))
    parsed = urlparse(url)

    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, '', ''))


def cleaned_link(url, link):
    text = link.text.strip()
    url = urljoin(url, link.get('href'))
    parsed = urlparse(url)

    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ''))

    return {
            "text": text,
            "url": clean_url,
            "fragment": parsed.fragment
        }


def cleaned_image(url, img):
    text = img.get('alt')
    url = urljoin(url, img.get('src'))
    parsed = urlparse(url)

    clean_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, parsed.query, ''))

    return {
            "alt": text,
            "src": clean_url,
        }


def batch(iterable, number=1):
    l = len(iterable)
    for ndx in range(0, l, number):
        yield iterable[ndx:min(ndx + number, l)]
