import pyodbc
import os
from dotenv import load_dotenv
from Domain.Product import *
from Domain.Pamphlet import * 

load_dotenv()

# Configurações de conexão
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USERNAME")
password = os.getenv("SQL_PASSWORD")
connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=YES"

class PamphletRepository:
    def __init__(self):
        self.connection = pyodbc.connect(connection_string)

    def create_tables(self):
        cursor = self.connection.cursor()

        # Tabela de Product
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Product' AND xtype='U')
            CREATE TABLE Product (
                id INT IDENTITY(1,1) PRIMARY KEY,
                name NVARCHAR(255) NOT NULL,
                price FLOAT NOT NULL
            )
        ''')

        # Tabela de Pamphlet
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Pamphlet' AND xtype='U')
            CREATE TABLE Pamphlet (
                id INT IDENTITY(1,1) PRIMARY KEY,
                supermarket NVARCHAR(255) NOT NULL,
                address NVARCHAR(255) NOT NULL
            )
        ''')

        # Tabela de relação entre Pamphlet e Product
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='PamphletProduct' AND xtype='U')
            CREATE TABLE PamphletProduct (
                pamphlet_id INT NOT NULL,
                product_id INT NOT NULL,
                FOREIGN KEY (pamphlet_id) REFERENCES Pamphlet(id),
                FOREIGN KEY (product_id) REFERENCES Product(id)
            )
        ''')

        self.connection.commit()

    def create_pamphlet(self, pamphlet: Pamphlet):

        cursor = self.connection.cursor()

        # Inserir o panfleto
        cursor.execute(
            "INSERT INTO Pamphlet (supermarket, address) OUTPUT INSERTED.id VALUES (?, ?)",
            (pamphlet.supermarket, pamphlet.address)
        )
        pamphlet_id = cursor.fetchone()[0]

        # Inserir os produtos relacionados
        for product in pamphlet.products:
            cursor.execute(
                "INSERT INTO Product (name, price) OUTPUT INSERTED.id VALUES (?, ?)",
                (product.name, product.price)
            )
            product_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO PamphletProduct (pamphlet_id, product_id) VALUES (?, ?)",
                (pamphlet_id, product_id)
            )

        self.connection.commit()

    def get_pamphlet(self, pamphlet_id: int) -> Pamphlet:
        cursor = self.connection.cursor()

        # Buscar o panfleto
        cursor.execute("SELECT supermarket, address FROM Pamphlet WHERE id = ?", (pamphlet_id,))
        pamphlet_row = cursor.fetchone()
        if not pamphlet_row:
            return None

        supermarket, address = pamphlet_row

        # Buscar os produtos relacionados
        cursor.execute('''
            SELECT Product.name, Product.price
            FROM Product
            INNER JOIN PamphletProduct ON Product.id = PamphletProduct.product_id
            WHERE PamphletProduct.pamphlet_id = ?
        ''', (pamphlet_id,))

        products = [Product(name=row[0], price=row[1]) for row in cursor.fetchall()]

        return Pamphlet(supermarket=supermarket, address=address, products=products)

    def update_pamphlet(self, pamphlet_id: int, updated_pamphlet: Pamphlet):
        cursor = self.connection.cursor()

        # Atualizar o panfleto
        cursor.execute(
            "UPDATE Pamphlet SET supermarket = ?, address = ? WHERE id = ?",
            (updated_pamphlet.supermarket, updated_pamphlet.address, pamphlet_id)
        )

        # Remover os produtos antigos
        cursor.execute("DELETE FROM PamphletProduct WHERE pamphlet_id = ?", (pamphlet_id,))

        # Inserir os produtos atualizados
        for product in updated_pamphlet.products:
            cursor.execute(
                "INSERT INTO Product (name, price) OUTPUT INSERTED.id VALUES (?, ?)",
                (product.name, product.price)
            )
            product_id = cursor.fetchone()[0]

            cursor.execute(
                "INSERT INTO PamphletProduct (pamphlet_id, product_id) VALUES (?, ?)",
                (pamphlet_id, product_id)
            )

        self.connection.commit()

    def delete_pamphlet(self, pamphlet_id: int):
        cursor = self.connection.cursor()

        # Remover as relações com produtos
        cursor.execute("DELETE FROM PamphletProduct WHERE pamphlet_id = ?", (pamphlet_id,))

        # Remover o panfleto
        cursor.execute("DELETE FROM Pamphlet WHERE id = ?", (pamphlet_id,))

        self.connection.commit()
