import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Experience:
    '''
    This class represents an experience
    '''

    def __init__(self, experience_id, verb, modifiers):
        '''
        Args:
            experience_id: int
            verb: str
            modifiers: list[str]
        '''
        self.__experience_id = experience_id
        self.__verb = verb
        self.__modifiers = modifiers

    @property
    def experience_id(self):
        return self.__experience_id

    @property
    def verb(self):
        return self.__verb

    @property
    def modifiers(self):
        return  self.__modifiers


class Experiences:
    '''
    This class represents a list of Experiences.
    '''

    def __init__(self):
        self.__experiences = []

    @property
    def experiences(self):
        return self.__experiences

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

    def read_experiences_from_database(self, label):
        '''
        Args:
            label: str
        '''
        self.__init__()

        try:
            db_connection = self.get_db_connection()
            cursor = db_connection.cursor()
            sql = 'SELECT id, verb, modifier, label FROM experiences where label ="' + label + '";'
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                experience = Experience(int(row[0]), row[1], [row[2]])
                self.__experiences.append(experience)

        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)

        except Exception as e:
            traceback.print_exc()
            print(e)

        cursor.close()
        db_connection.close()

    def get_index(self, verb, modifiers):
        '''
        Get index of Experience

        Args:
            verb: str
            modifiers: list[str]

        Return:
            int or None
        '''
        for i, experience in enumerate(self.experiences):
            if experience.verb == verb and len(experience.modifiers) == len(modifiers):
                flg = True
                for modifier in modifiers:
                    if modifier not in experience.modifiers:
                        flg = False
                        break
                if flg == True:
                    return i


    def append(self, another_experience):
        '''
        append a Experience to the Experiences

        Args:
            another_experience: Experience
        Returns:
            None
        '''
        self.__experiences.append(another_experience)

    def extend(self, another_experiences):
        '''
        extend the Experiences by another Experiences

        Args:
            another_experiences: Experiences
        Returns:
            None
        '''
        self.__experiences.extend(another_experiences.experiences)
