import MySQLdb
import os
from .dbconnection import get_db_connection
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

class Experience:
    '''
    This class represents an experience
    '''

    def __init__(self, experience_id, verb, modifier):
        '''
        Args:
            experience_id: int
            verb: str
            modifier: str
        '''
        self.__experience_id = experience_id
        self.__verb = verb
        self.__modifier = modifier

    @property
    def experience_id(self):
        return self.__experience_id

    @property
    def verb(self):
        return self.__verb

    @property
    def modifier(self):
        return  self.__modifier


class Experiences:
    '''
    This class represents a list of Experiences.
    '''

    def __init__(self):
        self.__experiences = []

    @property
    def experiences(self):
        return self.__experiences

    def read_experiences_from_database(self, label):
        '''
        Args:
            label: str
        '''
        self.__init__()
        db_connection = get_db_connection()
        cursor = db_connection.cursor()

        try:
            sql = 'SELECT id, verb, modifier, label FROM experiences where label ="' + label + '";'
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                experience = Experience(int(row[0]), row[1], row[2])
                self.__experiences.append(experience)

        except MySQLdb.Error as e:
            print('MySQLdb.Error: ', e)

        except Exception as e:
            traceback.print_exc()
            print(e)

        cursor.close()
        db_connection.close()

    def get_index(self, verb, modifier):
        '''
        Get index of Experience

        Args:
            verb: str
                '飲む'
            modifier: str
                'ちょっと'

        Return:
            int or None
        '''
        index = None

        for i, experience in enumerate(self.experiences):
            if experience.verb == verb and experience.modifier == modifier:
                index = i
                break

        return index


    def append(self, another_experience):
        '''
        append a Experience to the Experiences

        Args:
            another_experience: Experience
        Returns:
            None
        '''
        if self.has_id(another_experience.experience_id):
            print('erorr: duplicate id: ' + str(another_experience.experience_id))
        else:
            self.__experiences.append(another_experience)

    def extend(self, another_experiences):
        '''
        extend the Experiences by another Experiences

        Args:
            another_experiences: Experiences
        Returns:
            None
        '''
        for another_experience in another_experiences.experiences:
            if self.has_id(another_experience.experience_id):
                print('erorr: duplicate id: ' + str(another_experience.experience_id))
                return
        self.__experiences.extend(another_experiences.experiences)

    def has_id(self, e_id):
        return e_id in [ex.experience_id for ex in self.experiences]
