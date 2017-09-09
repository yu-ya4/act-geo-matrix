class Experiment:
    '''
    This class represents an experiment
    '''

    def __init__(self, verb, modifiers):
        '''
        Args:
            verb: str
            modifiers: list[str]
        '''
        self.__verb = verb
        self.__modifiers = modifiers

    @property
    def verb(self):
        return self.__verb

    @property
    def modifiers(self):
        return  self.__modifiers
