# definimos la clase que lanza las excepciones si encuentra una palabra prohibidad 

class ProhibitedWordsError(Exception): 
    
    def __init__(self, message="Prohibited words detected in the text.", found_word = None) -> None:
        self.__message = message
        self.__found_word = found_word
        super().__init__(self.__message)