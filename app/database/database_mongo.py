from pymongo import MongoClient


class DatabaseMongo:

    __connection_string = None
    __client = None
    __db = None

    @staticmethod
    def database_connection(connection_string:str, database:str):
        if DatabaseMongo.__client is None or DatabaseMongo.__db is None:
            DatabaseMongo.__client = MongoClient(connection_string)
            DatabaseMongo.__db = DatabaseMongo.__client[database]


        print(DatabaseMongo.__connection_string)
        return DatabaseMongo.__db

    @staticmethod
    def get_database():
        return DatabaseMongo.__db