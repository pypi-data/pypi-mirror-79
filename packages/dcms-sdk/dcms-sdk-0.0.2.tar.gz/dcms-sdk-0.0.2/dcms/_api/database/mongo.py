from ..init import PROJECT_ID, mongo_client


def get_mongo_collection(collection_name, project_id=PROJECT_ID):
    return mongo_client.get_database("crawldata").get_collection("%s:%s" % (project_id, collection_name))


def get_database(db_name="crawldata"):
    return mongo_client.get_database(db_name)


def get_mongo_client():
    return mongo_client


def get_system_database():
    return mongo_client.get_database('ssti')
