from geo import Geo, Geos
import csv
import codecs

def read_experiment_results(result_file):
    '''
    Read results of experiments from csv

    Args:
        result_file: str

    Returns:
        dict{str: dict{int: float}}
    '''
    correct_dict_dict = {}
    with codecs.open(result_file, 'r', 'utf-8-sig') as f:
        data = csv.reader(f)

        for line in data:
            top = line[0]
            if top == '' or top == '正誤':
                continue

            elif top != '1':
                label = top
                correct_dict_dict[label] = {}

            else:
                url = line[1]
                geo_id = int(url.split('/')[6])
                correct_dict_dict[label][geo_id] = float(top)

    return correct_dict_dict

def merge_correct_dict_dicts(dict1, dict2):
    '''
    Merge correct dictionaries.
    Same keys are added.

    Args:
        dict1, dict2:
    '''
    merged_dict = dict1.copy()
    for label, correct_dict in dict2.items():
        if label in merged_dict:
            for k, v in correct_dict.items():
                if k in merged_dict[label]:
                    merged_dict[label][k] += v
                else:
                    merged_dict[label][k] = v
        else:
            merged_dict[k] = correct_dict

    return merged_dict

class Experimenter:
    '''
    This class does some experiments
    '''

    def __init__(self, label):
        self.__geos = Geos()
        self.correct_dict, self.__label = self.__init_correct_dict(label)
        self.__label = label
    @property
    def geos(self):
        return self.__geos

    @property
    def label(self):
        return self.__label

    def __init_correct_dict(self, label):
        '''
        Initialize correct_dict

        Returns:
            dict{id: float}
        '''
        self.geos.read_geos_from_database()
        correct_dict = {}
        for geo in self.geos.geos:
            correct_dict[geo.geo_id] = 0.0
        return correct_dict, label

    def update_correct_dict(self, correct_dict):
        '''
        Args:
            correct_dict: dict{int: float}
        Returns:
            None
        '''
        self.correct_dict.update(correct_dict)


    def get_value_of_dcg(self, result_list):
        '''
        Args:
            result_list[tuple(int, float)]
        Returns:
            float
        '''

        val = 0.0
        for i in range(0, len(result_list)):
            geo_id = result_list[i][0]
            if self.correct_dict[geo_id]:
                if i == 0:
                    val += result_list[i][1]
                else:
                    val += result_list[i][1] / np.log2(i + 1)
            else:
                pass
            i += 1

        return val

    def get_value_of_ap(self, result_list):
        '''
        Args:
            result_list[tuple(int, float)]
        Returns:
            float
        '''
        val = 0.0
        correct_num = 0
        for i in range(0, len(result_list)):
            geo_id = result_list[i][0]
            if self.correct_dict[geo_id]:
                correct_num += 1
                p = 1 / (i + 1)
                val += p
            else:
                pass
            i += 1

        if correct_num > 0:
            ap = val /correct_num
        else:
            ap = 0

        return ap


class Experimenters:
    '''
    This class is a list of Experimenters.
    '''

    def __init__(self):
        self.__experimenters = []

    @property
    def experimenters(self):
        return self.__experimenters

    def append(self, another_experimenter):
        self.__experimenters.append(another_experimenter)

    def extend(self, another_experimenters):
        self.__experimenters.extend(another_experimenters.experimenters)
