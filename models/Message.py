from datetime import datetime

# definimos la clase de los mensajes 
class Message:
    __content: str
    __sender: str
    __timestamp: datetime
    
    # definimos el constructor 
    
    def __init__(self,content: str,timestamp: datetime,sender: str) -> None:
        self.__content = content
        self.__timestamp = timestamp
        self.__sender = sender
        
        
    # generamos el metodo to_dict()
    def to_dict(self) -> dict: 
        return {
            "sender": self.__sender,
            "content": self.__content,
            "timestamp": self.__timestamp
        }