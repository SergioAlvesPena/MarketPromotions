class Product:
    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def __str__(self):
        """
        Representação textual do objeto Product.

        :return: String formatada com os detalhes do produto.
        """
        return (f"Product(Name: {self.name}, Price: {self.price}")

    def to_dict(self):
        """
        Converte o objeto Product para um dicionário.

        :return: Dicionário com os atributos do produto.
        """
        return {
            "name": self.name,
            "price": self.price,
        }
    
    @staticmethod
    def from_dict(data: dict):
        """
        Cria um objeto Product a partir de um dicionário.

        :param data: Dicionário com os atributos do produto.
        :return: Objeto Product.
        """
        return Product(
            name=data.get("name"),
            price=data.get("price")
        )

