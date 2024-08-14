import os
from secret import OLLAMA_EXTERNAL_BASEURL
# import litellm
# litellm.supports_function_calling = lambda _: True
# os.environ["OLLAMA_HOST"] = "http://127.0.0.1:11434"
os.environ["OLLAMA_HOST"] = OLLAMA_EXTERNAL_BASEURL

os.environ['OPENAI_API_KEY'] = 'dummykey'
# os.environ['OPENAI_API_BASE'] = ''
# os.environ['OPENAI_MODEL_NAME'] = 'mixtral'

from mem0 import Memory

config = {
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "",
            # "model": "mxbai-embed-large",
        }
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
        }
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
        }
    }
}

m = Memory.from_config(config)

# 1. Add: Store a memory from any unstructured text
uploaded_memory = m.add("I am working on improving my tennis skills. Suggest some online courses.", user_id="alice", metadata={"category": "hobbies"}) # {"message": "ok"}

# print(uploaded_memory)
breakpoint()

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

