import os
from secret import OLLAMA_EXTERNAL_BASEURL

# os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
os.environ["OLLAMA_HOST"] = OLLAMA_EXTERNAL_BASEURL

os.environ["OPENAI_API_KEY"] = "dummykey"
from mem0 import Memory

config = {
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "mxbai-embed-large",
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            # "model": "codegemma:2b",
            # "model": "llama3.1:8b",
            "model": "mistral:v0.3",
            # "model": "internlm/internlm2.5:1.8b-chat", # does not support tools
            "temperature": 0.5,
            "max_tokens": 2000,
        },
    },
    # "llm": {
    #     "provider": "litellm",
    #     "config": {
    #         "model": "ollama/codegemma:2b",
    #         "temperature": 0.2,
    #         "max_tokens": 1500,
    #     }
    # },
    "embedding_model_dims": 1024,
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "test",
            "path": "test_db",
            # "embedding_model_dims": 1536,
        },
    },
}

m = Memory.from_config(config)

# 1. Add: Store a memory from any unstructured text
uploaded_memory = m.add(
    "I am working on improving my tennis skills. Suggest some online courses.",
    user_id="alice",
    metadata={"category": "hobbies"},
)  # {"message": "ok"}

# print(uploaded_memory)
# breakpoint()

# m.get_all()
# memory_id = uploaded_memory['id']
# # Created memory --> 'Improving her tennis skills.' and 'Looking for online suggestions.'

# # 2. Update: update the memory
# result = m.update(memory_id=memory_id, data="Likes to play tennis on weekends")

# Updated memory --> 'Likes to play tennis on weekends.' and 'Looking for online suggestions.'

# 3. Search: search related memories
related_memories = m.search(query="What are Alice's hobbies?", user_id="alice")

# Retrieved memory --> 'Likes to play tennis on weekends'
print("[*] Retrieved memory:")
print(related_memories)
# [{'id': '24c76f9e-ac4d-42a2-9f09-6b1ccd5a2465', 'memory': 'Improving tennis skills (current activity): Interested in online courses for tennis improvement (preference)', 'hash': 'd9be5aede3f0dab28f3ba19fdeade599', 'metadata': {'category': 'hobbies'}, 'score': 375.0532211123522, 'created_at': '2024-08-14T07:10:34.622102-07:00', 'updated_at': None, 'user_id': 'alice'}]
