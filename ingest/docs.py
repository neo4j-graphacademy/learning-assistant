from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
from utils import current_mapping, extract_docs, batch
from db import import_pages
from math import ceil

def read_docs_directory():
    data = []

    # Get the current working directory
    current_dir = os.getcwd()

    # Build the relative path to the parent directory
    parent_dir = os.path.join(current_dir, 'docs-prod')

    # for subdir, dirs, files in os.walk(parent_dir):
    for mapping in current_mapping.values():
        for name, version in mapping.items():
            # Define the target directory path
            target_dir = os.path.join(parent_dir, name, version)

            # Find all .html files recursively in directory
            for subdir, dirs, files in os.walk(target_dir):
                for file in files:
                    if file.endswith('.html'):
                        file_path = os.path.join(subdir, file)
                        url = file_path.replace(parent_dir, "https://neo4j.com/docs").replace(f'/{version}/', "/current/").rstrip("index.html")

                        data.append({"path": file_path, "url": url})

    return data

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


    # Get files from directory
    files = read_docs_directory()

    batch_no = 0
    batch_size = 100
    batches = ceil(len(files) / batch_size)

    with driver.session() as session:
        for rows in batch(files, batch_size):
            batch_no += 1
            print(batch_no)

            extracted = [ extract_docs(file['path'], file['url']) for file in rows ]

            res = session.execute_write(import_pages, rows=[r for r in rows if r is not None])

    driver.close()
