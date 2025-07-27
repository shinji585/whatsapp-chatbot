# en este sera el modulo donde se caragara el modelo y se define la logica del modelo 
from transformers.pipelines import pipeline

generador = pipeline("text-generation",model="gpt2")
print(generador("que sabes sobre algebra",max_length=20)[0]['generated_text'])