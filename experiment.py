import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Experiment:
    '''
    This class represents an experiment
    '''

    def __init__(self, experiment_id, verb, modifiers):
        '''
        Args:
            experiment_id: int
            verb: str
            modifiers: list[str]
        '''
        self.__experiment_id = experiment_id
        self.__verb = verb
        self.__modifiers = modifiers

    @property
    def experiment_id(self):
        return self.__experiment_id

    @property
    def verb(self):
        return self.__verb

    @property
    def modifiers(self):
        return  self.__modifiers


class Experiments:
    '''
    This class represents a list of Experiments.
    '''

    def __init__(self):
        self.__experiments = []

    @property
    def experiments(self):
        return self.__experiments

    def get_db_connection(self, db='local'):
        '''
        Get database connection

        Args:
            db: str
                local
                ieyasu
                ieyasu-berry
        '''
        try:
            if db == 'local':
                return MySQLdb.connect(host=os.environ.get('LOCAL_DB_HOST'), user=os.environ.get('LOCAL_DB_USER'), passwd=os.environ.get('LOCAL_DB_PASSWD'), db=os.environ.get('LOCAL_DB_DATABASE'), charset=os.environ.get('CHARSET'))
            elif db == 'ieyasu':
                return MySQLdb.connect(host=os.environ.get('IEYASU_DB_HOST'), user=os.environ.get('IEYASU_DB_USER'), passwd=os.environ.get('IEYASU_DB_PASSWD'), db=os.environ.get('IEYASU_DB_DATABASE'), charset=os.environ.get('CHARSET'), port=int(os.environ.get('IEYASU_DB_PORT')))
            elif db == 'ieyasu-berry':
                return MySQLdb.connect(host=os.environ.get('IEYASU_DB_HOST'), user=os.environ.get('IEYASU_DB_USER'), passwd=os.environ.get('IEYASU_DB_PASSWD'), db=os.environ.get('IEYASU_DB_DATABASE'), charset=os.environ.get('CHARSET'), port=int(os.environ.get('IEYASU_BERRY_DB_PORT')))
            elif db == 'ieyasu-local':
                return MySQLdb.connect(host=os.environ.get('IEYASU_DB_HOST'), user=os.environ.get('IEYASU_DB_USER'), passwd=os.environ.get('IEYASU_DB_PASSWD'), db=os.environ.get('IEYASU_DB_DATABASE'), charset=os.environ.get('CHARSET'))
            else:
                print('Error: please select correct database')
                exit()
        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)
            exit()

    def read_experiments_from_database(self, label):
        '''
        Args:
            label: str
        '''
        self.__init__()

        try:
            db_connection = self.get_db_connection()
            cursor = db_connection.cursor()
            sql = 'SELECT id, verb, modifier, label FROM experiments where label ="' + label + '";'
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)
            for row in result:
                experiment = Experiment(int(row[0]), row[1], [row[2]])
                self.__experiments.append(experiment)

        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)

        except Exception as e:
            traceback.print_exc()
            print(e)

        cursor.close()
        db_connection.close()
