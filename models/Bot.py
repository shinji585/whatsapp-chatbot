from abc import ABC,abstractmethod

# creamos la clase ChatBot la cual es de tipo abstracto 

class Bot(ABC): 
    
    # este debe tener un nombre 
    __name: str
    
    # definimos el constructor 
    def __init__(self,name: str = '') -> None:
        self.__name = name
        
    @property
    def name(self) -> str: 
        return self.__name
        
    # definimos lo que viene siendo los metodos de nuestra clase abstracta 
    @abstractmethod
    def receive_message(self,msg: str) -> str:
        raise NotImplementedError("Subclasses must implement this method")
     
    @abstractmethod
    def process_message(self,msg: str) -> str: 
        raise NotImplementedError("Subclasses must implement this method")
        
   
    