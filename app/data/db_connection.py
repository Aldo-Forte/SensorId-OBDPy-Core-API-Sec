from pymongo import MongoClient

class DbConnection:

    _client = None
    _database = None

    """ 
    @staticmethod
    def connection():

        if DbConnection._client is None or DbConnection._database is None:
            DbConnection._client = MongoClient('mongodb://sensoridAdmin:10T53nsor.2010!@siddev.dnsalias.net:17027/?authSource=admin')
            DbConnection._database = DbConnection._client['obd']

        return DbConnection._database
    """




