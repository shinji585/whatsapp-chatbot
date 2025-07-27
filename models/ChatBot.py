from typing import override
from models.Bot import Bot
from models.Message import Message
from models.NPLModel import NPLmodel
from models.DummyModel import DummyModel
from models.ProhibitedWords import ProhibitedWordsError
from api.model_service import generar_respuestas
import re


# definimos lo que viene siendo la clase del chatbot
class ChatBot(Bot):
    __model: NPLmodel
    __history: list[Message]

    # definimos el constructor
    def __init__(self, name: str = "ChatBot") -> None:
        super().__init__(name)
        self.__history = []
        self.__model = DummyModel()

    # implementar los metodos de la clase abstracta

    @override
    def receive_message(self, msg: str) -> str:
        # ahora eliminamos palabras prohidas
        # limpiamos el texto eliminando los espacios que este tenga
        msg = msg.strip()

        # luego de eso pasamos msg a una funcion interna que nos devuelve el texto de forma limpia
        def remove_emojis_and_symbols(msg: str) -> str:
            emoji_pattern = re.compile(
                "["
                "\U0001f600-\U0001f64f"  # emoticons
                "\U0001f300-\U0001f5ff"  # symbols & pictographs
                "\U0001f680-\U0001f6ff"  # transport & map symbols
                "\U0001f1e0-\U0001f1ff"  # flags (iOS)
                "\U00002702-\U000027b0"
                "\U000024c2-\U0001f251"
                "]+",
                flags=re.UNICODE,
            )
            return emoji_pattern.sub(r"", msg)

        # pasamos nuestros texto y lo volvemos a capturar
        msg = remove_emojis_and_symbols(msg=msg)

        # ahora creamos una funcion que procesa las entradas a el chatbot y que las limpia y lanza excepciones si esta contiene alguna palabra prohibidad
        def process_chatbot_input(msg: str) -> bool:
            palabras_prohibidas = {
                "puto",
                "mierda",
                "cabrón",
                "joder",
                "fuck",
                "shit",
                "negro",
                "maricón",
                "zorra",
                "porno",
                "sexo",
                "orgasmo",
                "matar",
                "suicidio",
                "bomba",
                "tarjeta de crédito",
                "contraseña",
                "drogas",
                "hackear",
                "robo",
            }
            frases_prohibidas = [
                "hijo de puta",
                "vete a la mierda",
                "no te quiero"
            ]
            
            # verificamos las palabras individuales 
            for palabra_prohibida in palabras_prohibidas: 
                if palabra_prohibida in msg: 
                    raise ProhibitedWordsError(
                        f"La entrada contiene una palabra prohibidad: {palabra_prohibida}",
                        found_word=palabra_prohibida
                    )    
                
            # buscamos en las frases prohibidas
            for frase in frases_prohibidas: 
                if frase in msg:
                    raise ProhibitedWordsError(
                        f"La entrada contiene una frase prohibidad: {frase}",
                        found_word=frase
                    )  
            # en caso de que no se haya encontrado ninguna           
            return True
        
        # verificamos que si devuelve true devuelva el texto si no que no devuelva nada 
        
        if process_chatbot_input(msg=msg):
            return msg
        else: 
            return f""

    @override
    def process_message(self, msg: str) -> str:
        # retornamos la respuesta 
        return self.__model.analyze(msg)

  

   