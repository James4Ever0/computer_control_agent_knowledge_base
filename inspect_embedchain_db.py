from lib import EmbedApp
# from embedchain.app import DataSource
# import json

app = EmbedApp()
# print("[*] DB count:", app.app.db.count())
# serialized_db = app.app.db.serialize()
# print("[*] Serialized DB:")
# print(serialized_db)  # just connection configs.

# data_sources = app.app.get_data_sources()
# print("[*] Data sources:")
# print(data_sources)

# all_data = app.app.db_session.query(DataSource).all()

# print("[*] All data:")
# for it in all_data:
#     data = dict(
#         id=it.id,
#         app_id=it.app_id,
#         hash=it.hash,
#         type=it.type,
#         value=it.value,
#         meta_data=it.meta_data,
#         is_uploaded=it.is_uploaded,
#     )
#     print(data)

print('[*] Chroma Embeddings:')
embed_data = app.app.db.get()
# print(json.dumps(embed_data, indent=4, ensure_ascii=True))
# breakpoint()

for metadata, document in zip(embed_data['metadatas'], embed_data['documents']):
    url = metadata['url']
    
