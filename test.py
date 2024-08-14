import chromadb
from chromadb.config import Settings
anonymous_settings = Settings(anonymized_telemetry=False)

# setup Chroma in-memory, for easy prototyping. Can add persistence easily!
# client = chromadb.Client(anonymous_settings)

# persistent chromadb
client = chromadb.PersistentClient(settings=anonymous_settings)

COLLECTION_NAME = "all-my-documents"

# Create collection. get_collection, get_or_create_collection, delete_collection also available!
# collection = client.create_collection(COLLECTION_NAME)
collection = client.get_or_create_collection(COLLECTION_NAME)

# Add docs to the collection. Can also update and delete. Row-based API coming soon!
# will not insert to the db if the id is duplicated
collection.add(
    documents=["This is document1", "This is document2"], # we handle tokenization, embedding, and indexing automatically. You can skip that and add your own embeddings as well
    metadatas=[{"source": "notion"}, {"source": "google-docs"}], # filter on these!
    ids=["doc1", "doc2"], # unique for each doc
)

# Query/search 2 most similar results. You can also .get by id
results = collection.query(
    query_texts=["This is a query document"],
    n_results=2,
    # where={"metadata_field": "is_equal_to_this"}, # optional filter
    # where_document={"$contains":"search_string"}  # optional filter
)

print("results:", results)