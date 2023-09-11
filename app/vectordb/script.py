from provider import VectorDBProvider
from dotenv import load_dotenv

load_dotenv()

foo = VectorDBProvider()

foo.connect()

# collections = foo.list_collections()
# print(collections)

# response = foo.create_collection('test_collection', 'test description')
# print(response)

# collections = foo.list_collections()
# print(collections)

# foobar = foo.get_collections([1, 2, 3])
# print(foobar)

# bar = foo.create_collection('test_collection', 'test description')
# print(bar)

# yeet = foo.list_collections()
# print(yeet)

# tear = foo.update_collection(7, 'test_collection_update', 'test description')
# print(tear)

# print(foo.delete_collection(7))

# print(foo.create_file(
#     3,
#     1,
#     'test_file',
#     'test description',
#     "Bananananananananananananana",
#     'https://www.google.com'
# ))

# print(foo.get_file(5))

# print(foo.update_file(
#     file_id=5,
#     contents='foooooobar'
# ))

# print(foo.get_file(5))

print(foo.get_file_class(1))


foo.disconnect()