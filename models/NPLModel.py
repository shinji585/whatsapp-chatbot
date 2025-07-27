from abc import ABC, abstractmethod

# deinimos una clase abstracta que tendra el texto que se analizara por el modelo 

class NPLmodel(ABC): 
    
    # definimos el metodo analyze()
    @abstractmethod
    def analyze(self, text: str) -> str:
        raise NotImplementedError("Subclasses must implement this method")