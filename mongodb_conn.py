import pymongo
import logging_file


def save_to_mongodb(data):
    try:
        client = pymongo.MongoClient(
            "mongodb+srv://JAISWA_B:Bikoo1996@clusterbik.2grbd0c.mongodb.net/?retryWrites=true&w=majority")

        db = client.test

        database = client['flipkart_scrapper']
        collection = database['flipkart_comments']
        #db.collection.remove()
        collection.insert_many(data)
        logging_file.info("data insertion successful into mongodb")
        return collection.find()

    except Exception as e:
        logging_file.error(f"{e}: failed to load data into mongodb")
