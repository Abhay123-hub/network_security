import pymongo

# Replace with your MongoDB URI
uri = uri = "mongodb+srv://genai3002:abhay@cluster0.lziqa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = pymongo.MongoClient(uri)

# List all databases
print("Databases:")
for db_name in client.list_database_names():
    print(f"- {db_name}")

    # List all collections in each database
    db = client[db_name]
    print("  Collections:")
    for collection_name in db.list_collection_names():
        print(f"  - {collection_name}")