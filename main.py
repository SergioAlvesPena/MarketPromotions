import os
from dotenv import load_dotenv
from Infrastructure.PamphletRepository import PamphletRepository
from Domain.Product import Product
from Domain.Pamphlet import Pamphlet
from Services import DataExtractionService as DES

load_dotenv()

# Caminho da imagem
image_path = os.getenv("IMAGE_PATH") 
# Chamar a função
extract_text_from_image(image_path)

if __name__ == "__main__":
    db = PamphletRepository()

    # Criar um panfleto com produtos
    #products = [Product(name="Apple", price=0.5), Product(name="Bread", price=1.5)]
    #pamphlet = Pamphlet(supermarket="SuperMarket A", address="123 Main St", products=products)

    
    #Extraction with json
    #pamphlets = DES.extract_data_from_json(json)

    pamphlets = DES.extract_text_from_image(image_path)

    # Inserir o panfleto no banco de dados
    for pamphlet in pamphlets:
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
