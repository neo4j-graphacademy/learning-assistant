def import_pages(tx, rows):
    res = tx.run("""
        UNWIND $rows AS row
        MERGE (p:Page {url: row.url})
        SET p.title = row.title,
            p.text = row.text

        FOREACH (link in row.links |
            MERGE (p2:Page {url: link.url})
            MERGE (p)-[r:LINKS_TO]->(p2)
            SET r.fragment = link.fragment, r.text = link.text
        )

        FOREACH (section in row.sections |
            MERGE (s:Section {url: section.url})
            SET s.title = section.title, s.text = section.text, s.anchor = section.anchor

            FOREACH (link in section.links |
                MERGE (p2:Page {url: link.url})
                MERGE (s)-[r:LINKS_TO]->(p2)
                SET r.fragment = link.fragment, r.text = link.text
            )

            FOREACH (image IN section.images |
                MERGE (i:Image {src: image.src})
                MERGE (s)-[r:INCLUDES_IMAGE]->(i)
                SET r.alt = image.alt
            )

            FOREACH (code IN section.code |
                MERGE (i:CodeBlock {code: code.code})
                SET i.language = code.language
                MERGE (s)-[r:INCLUDES_CODE]->(i)
                SET r.title = code.title
            )

            MERGE (p)-[:HAS_SECTION]->(s)
        )
        RETURN count(*) AS count
    """, rows=rows)

    return res.single().get('count')
