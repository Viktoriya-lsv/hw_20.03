import os
import json
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

DSN = 'postgresql://postgres:vika7333@localhost:5432/bookstore'
sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

# Определение базового класса
Base = declarative_base()

# Определение моделей
class Publisher(Base):
    _tablename_ = 'publisher'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False, unnique = True)
    books = relationship("Book", back_populates = "publisher")

class Book(Base):
    _tablename_ = 'publisher'
    id = Column(Integer, primary_key = True)
    title = Column(String, nullable = False, unnique = True)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)
    publisher = relationship("Publisher", back_populates = "books")
    stocks = relationship("Stock", back_populates = "book")

class Shop(Base):
    _tablename_ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unnique=True)
    stocks = relationship("Stock", back_populates="shop")

class Stock(Base):
    _tablename_ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable = False)
    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")
    sales = relationship("Sale", back_populates="stock")

class Sale(Base):
    _tablename_ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable = False)
    date_sale = Column(Date, nullable = False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable = False)
    count = Column(Integer, nullable=False)
    stock = relationship("Stock", back_populates = "sales")

Base.metadata.create_all(engine)

# Функция поиска магазинов, продающих книги издателя
def find_shops(publisher_name):
    result = session.query(Book.title, Shop.name, Sale.price, Sale.data_sale)
    result.join(Publisher).join(Stock).join(Shop).join(Sale)
    result.filter(Publisher.name == publisher_name)
    result.all()

    for title, shop, price, date in result:
        print(f"{title} | {shop} | {price} | {date}")

def load_test_data(json_path = 'fixtures/tests_data.json'):
    with open(json_path, 'r', encoding = 'utf-8') as f:
        data = json.load(f)
    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale
        }[record['model']]
        session.add(model(id=record['pk'], **record['fields']))

    session.commit()

if _name_ == "_main_":
    publisher_name= input("Введите имя издателя: ")
    find_shops(publisher_name)

session.close()