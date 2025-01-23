from Domain.Product import *
from typing import List

class Pamphlet:
    def __init__(self, supermarket: str, address:str, products: List[Product]):
        
        self.supermarket = supermarket
        self.address = address
        self.products = products

    def __str__(self):
        return (f"Supermarket: {self.supermarket}, Address: {self.address})")

    def to_dict(self):
        return {
            "name": self.name,
            "price": self.price,
            "supermarket": self.supermarket,
            "address": self.address
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Product(
            name=data.get("name"),
            price=data.get("price"),
            supermarket=data.get("supermarket"),
            address=data.get("address")
        )

