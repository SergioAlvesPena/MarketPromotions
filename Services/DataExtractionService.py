from PIL import Image
import os
import base64
import pytesseract
import numpy as np
from openai import OpenAI
import json
from types import SimpleNamespace

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
pytesseract.pytesseract.tesseract_cmd = os.getenv("PYTESSERACT_PATH")

def extract_text_from_image(image_path):
    try:

        # Tenta extrair a imagem com pytesseract
        img = Image.open(image_path)
        pix = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                if pix[x, y][0] < 102 or pix[x, y][1] < 102 or pix[x, y][2] < 102:
                    pix[x, y] = (0, 0, 0, 255)
                else:
                    pix[x, y] = (255, 255, 255, 255)
        text = pytesseract.image_to_string(img)
        print(text)

        if(not text):
            # Extrair texto com vision
            text = openAI_get_text(image_path)
            # Exibir o texto extraído
            print("Texto extraído:")
            print(text)
            
        return extract_data_from_json(text)
    except Exception as e:
        # Extrair texto com vision
        text = openAI_get_text(image_path)
        # Exibir o texto extraído
        print("Texto extraído:")
        print(text)
        return extract_data_from_json(text)

def openAI_get_text(image_path):
    base64_image = encode_image(image_path)

    prompt = f"""
                Assuma que você é um assistente e que provavelmente o usuário está enviado a foto de
                um folheto de ofertas de supermercados

                Sua função é ver esse folheto de ofertas de supermercados e extrair desse folheto as seguintes informações:
                1- O nome do supermercado
                2- Os nomes de 5 produtos desse supermercado
                3- O preço desses 5 produtos
                4- a validade dessas ofertas

                # FORMATO DA RESPOSTA
                O formato da resposta deve ser um json com a seguinte formatação

                #IMPORTANTE
                Priorize as ofertas de cervejas presentes no folheto
                
                { "supermarket": Nome do supermercado, "address":Endereço ou Local, "products": Uma Lista de produtos e seus valores }

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

def extract_data_from_json(text):
    try:
         
        pamphlets = json.loads(text, object_hook=lambda d: SimpleNamespace(**d))

        return pamphlets
    except Exception as e:
        print(f"Erro ao obter a imagem: {e}")