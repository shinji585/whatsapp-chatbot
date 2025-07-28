from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from models.ChatBot import ChatBot
from models.ProhibitedWords import ProhibitedWordsError
import uvicorn
import logging

# Configuración básica del logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="WhatsApp ChatBot API",
    description="API para chatbot de WhatsApp",
    version="2.0.0"
)

# Inicializar chatbot
try:
    chatbot = ChatBot()
    logger.info("✅ ChatBot inicializado correctamente")
except Exception as e:
    logger.error(f"❌ Error inicializando ChatBot: {e}")
    chatbot = None

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputMessage(BaseModel):
    text: str

class OutputMessage(BaseModel):
    response: str

class StatusResponse(BaseModel):
    status: str
    service: str
    chatbot_ready: bool

# Endpoint raíz para verificar estado
@app.get("/", response_model=StatusResponse)
async def root():
    return StatusResponse(
        status="active", 
        service="WhatsApp Bot Backend",
        chatbot_ready=chatbot is not None
    )

# Endpoint de salud
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "chatbot_status": "ready" if chatbot else "error",
        "timestamp": logging.Formatter().formatTime(logging.LogRecord(
            name="", level=0, pathname="", lineno=0, msg="", args=(), exc_info=None
        ))
    }

@app.post("/chat", response_model=OutputMessage)
def chat_with_bot(message: InputMessage):
    try:
        logger.info(f"📨 Mensaje recibido: {message.text}")
        
        # Verificar que el chatbot esté disponible
        if not chatbot:
            logger.error("❌ ChatBot no está disponible")
            raise HTTPException(
                status_code=503, 
                detail="ChatBot no está disponible en este momento"
            )
        
        # Verificar que el mensaje no esté vacío
        if not message.text or not message.text.strip():
            logger.warning("⚠️ Mensaje vacío recibido")
            return OutputMessage(response="Por favor, envía un mensaje con contenido.")
        
        # Procesar mensaje
        clean_msg = chatbot.receive_message(message.text.strip())
        response = chatbot.process_message(clean_msg)
        
        logger.info(f"📤 Respuesta generada: {response}")
        return OutputMessage(response=response)
        
    except ProhibitedWordsError as e:
        logger.warning(f"🚫 Palabra prohibida detectada: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"💥 Error inesperado: {str(e)}")
        # En caso de error, devolver respuesta genérica
        return OutputMessage(
            response="Disculpa, ocurrió un error procesando tu mensaje. Intenta nuevamente."
        )

# Endpoint para probar la conexión
@app.post("/test")
def test_connection():
    return {"message": "Conexión exitosa con FastAPI", "status": "ok"}

# Función principal
if __name__ == "__main__":
    logger.info("🚀 Iniciando servidor FastAPI...")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",  # Cambié de "0.0.0.0." a "127.0.0.1"
        port=8000,
        reload=True,
        log_level="info"
    )