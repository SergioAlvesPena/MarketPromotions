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
#extract_text_from_image(image_path)

if __name__ == "__main__":
    db = PamphletRepository()

    # Criar um panfleto com produtos
    #products = [Product(name="Apple", price=0.5), Product(name="Bread", price=1.5)]
    #pamphlet = Pamphlet(supermarket="SuperMarket A", address="123 Main St", products=products)

    json = """
[
  {
    "supermarket": "Supermarket A",
    "address": "123 Main St",
    "products": [
      {"name": "Apple", "price": 0.5},
      {"name": "Banana", "price": 0.3},
      {"name": "Orange Juice", "price": 2.5}
    ]
  },
  {
    "supermarket": "Supermarket B",
    "address": "456 Elm St",
    "products": [
      {"name": "Milk", "price": 1.2},
      {"name": "Bread", "price": 1.5},
      {"name": "Eggs", "price": 2.0}
    ]
  },
  {
    "supermarket": "Supermarket C",
    "address": "789 Oak Ave",
    "products": [
      {"name": "Chicken Breast", "price": 5.0},
      {"name": "Rice", "price": 1.0},
      {"name": "Beans", "price": 1.5}
    ]
  },
  {
    "supermarket": "Supermarket Y",
    "address": "987 Maple Rd",
    "products": [
      {"name": "Cheese", "price": 3.0},
      {"name": "Ham", "price": 2.8},
      {"name": "Butter", "price": 1.8}
    ]
  },
  {
    "supermarket": "Supermarket Z",
    "address": "654 Pine Blvd",
    "products": [
      {"name": "Fish Fillet", "price": 6.0},
      {"name": "Shrimp", "price": 8.0},
      {"name": "Squid", "price": 7.5}
    ]
  }
]
"""

    pamphlets = DES.extract_data_from_json(json)

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
