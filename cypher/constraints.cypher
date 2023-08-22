CREATE CONSTRAINT FOR (p:Page) REQUIRE p.url IS UNIQUE;
CREATE CONSTRAINT FOR (p:Section) REQUIRE p.url IS UNIQUE;
CREATE CONSTRAINT FOR (p:Image) REQUIRE p.src IS UNIQUE;
CREATE CONSTRAINT FOR (p:CodeBlock) REQUIRE p.code IS UNIQUE;

CALL db.index.vector.createNodeIndex(
  'chatbot-embeddings',  // The name of the index
  'Chunk',               // The label
  'embedding',           // The property
  1536,                  // The dimensions of the embedding, OpenAI uses 1536
  'cosine'               // Function to calculate similarity
);