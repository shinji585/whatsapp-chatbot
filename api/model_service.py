# en este sera el modulo donde se caragara el modelo y se define la logica del modelo 
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import requests
# Cargamos el modelo y tokenizador
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)

def generar_respuestas(input_text: str) -> str:
    # Formato correcto para OpenChat
    inputs = tokenizer(input_text, return_tensors='pt').to(model.device)
    
    # configuramos la salida
    outputs = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7
    )
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# generamremos la respuestas utilizando ollama sera mas lento pero seria mas inteligente 
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"

def generar_respuestas2(input_text: str) -> str: 
    payload = {
        "model": MODEL,
        "prompt": input_text,
        "stream": False
    }
    response = requests.post(OLLAMA_URL,json=payload)
    response_data = response.json()
    return response_data.get("response","")