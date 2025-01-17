from PIL import Image
from dotenv import load_dotenv
import os
import base64
import pytesseract
import numpy as np
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

pytesseract.pytesseract.tesseract_cmd = os.getenv("PYTESSERACT_PATH")

def extract_text_from_image(image_path):
    try:

        # Extrair texto com vision
        text = openAI_get_text(image_path)
        
        # Exibir o texto extraídob v
        print("Texto extraído:")
        print(text)
        
        return text
    except Exception as e:
        print(f"Erro ao obter a imagem: {e}")

def openAI_get_text(image_path):
    base64_image = encode_image(image_path)

    prompt = f"""
                Assuma que você é um assistente e que provavelmente o usuário está enviado a foto de
                um folheto de ofertas de supermercados

                Sua função é ver esse folheto de ofertas de supermercados e extrair desse folheto as seguintes informações:
                1- O nome do supermercado
                2- Os nomes dos produtos desse supermercado
                3- O preço dos produtos
                4- a validade dessas ofertas

                # FORMATO DA RESPOSTA
                O supermercado: (Nome do supermercado) da Localidade (Endereço ou Local). Tem disponivel (Uma Lista de produtos e seus valores). Até o dia: (Data de validade). Contato (Contatos fornecidos)
                
                """

    response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
    max_tokens= 300
    )

    resposta = response.choices[0].message.content

    return resposta


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")



# Caminho da imagem
image_path = os.getenv("IMAGE_PATH") 

# Chamar a função
extract_text_from_image(image_path)


