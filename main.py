from PIL import Image
from dotenv import load_dotenv
import os
import base64
import pytesseract
import numpy as np
from openai import OpenAI
from Infrastructure.PamphletRepository import PamphletRepository
from Domain.Product import Product
from Domain.Pamphlet import Pamphlet

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
                2- Os nomes de 5 produtos desse supermercado
                3- O preço desses 5 produtos
                4- a validade dessas ofertas

                # FORMATO DA RESPOSTA
                (Nome do supermercado); (Endereço ou Local); (Uma Lista de produtos e seus valores); (Data de validade); (Contatos fornecidos);
                
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
#image_path = os.getenv("IMAGE_PATH") 
# Chamar a função
#extract_text_from_image(image_path)

if __name__ == "__main__":
    db = PamphletRepository()

    product1 = Product(name="Apple", price=0.5)

    # Criar um panfleto com produtos
    products = [Product(name="Apple", price=0.5), Product(name="Bread", price=1.5)]
    pamphlet = Pamphlet(supermarket="SuperMarket A", address="123 Main St", products=products)

    # Inserir o panfleto no banco de dados
    db.create_pamphlet(pamphlet)

    # Recuperar o panfleto
    retrieved = db.get_pamphlet(2)
    print(retrieved)

    # Atualizar o panfleto
    updated_products = [Product(name="Milk", price=1.0)]
    updated_pamphlet = Pamphlet(supermarket="SuperMarket B", address="456 Elm St", products=updated_products)
    db.update_pamphlet(1, updated_pamphlet)

    # Deletar o panfleto
    db.delete_pamphlet(1)
