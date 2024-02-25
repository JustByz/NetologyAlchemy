import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


BASE = declarative_base()


class Publisher(BASE):
    __tablename__ = "publisher"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=80), unique=True)


class Book(BASE):
    __tablename__ = "book"
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=300))
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"))
    publisher = relationship(Publisher, backref="book")


class Shop(BASE):
    __tablename__ = "shop"
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=100), unique=True)


class Stock(BASE):
    __tablename__ = "stock"
    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"))
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"))
    count = sq.Column(sq.Integer)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")


class Sale(BASE):
    __tablename__ = "sale"
    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.String(length=80))
    date_sale = sq.Column(sq.Date)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"))
    count = sq.Column(sq.Integer)
    stock = relationship(Stock, backref="stock")
    
    
def create_tables(engine):
    BASE.metadata.drop_all(engine)
    BASE.metadata.create_all(engine)