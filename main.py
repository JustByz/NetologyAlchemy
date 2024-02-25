from dotenv import dotenv_values
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import BASE, Publisher, Shop, Book, Stock, Sale
import json


LOGIN = dotenv_values(".env")["LOGIN"]
PASSWORD = dotenv_values(".env")["PASSWORD"]
DB = dotenv_values(".env")["NAME_DB"]
DSN = f"postgresql://{LOGIN}:{PASSWORD}@localhost:5432/{DB}"


def create_tables(engine):
    BASE.metadata.drop_all(engine)
    BASE.metadata.create_all(engine)


def get_query_publisher(sess, publisher="O'Reilly"):
    q_book = sess.query(Book).all()
    q_shop = sess.query(Shop).all()
    book_len = 0
    for b in q_book:
        if len(b.title) > book_len:
            book_len = len(b.title)
    shop_len = 0
    for b in q_shop:
        if len(b.name) > shop_len:
            shop_len = len(b.name)
    q = sess.query(Publisher).join(Book).join(Stock).join(Sale).filter(Publisher.name == publisher).all()
    for pub in q:
        for book in pub.book:
            for stock in book.stock:
                for sale in stock.stock:
                    print(f'{pub.name} | '
                          f'{book.title:<{book_len}} | '
                          f'{stock.shop.name:<{shop_len}} | '
                          f'{float(sale.price) * sale.count:>5} | '
                          f'{sale.date_sale}'
                          )


def add_test_data(sess, file="tests_data.json"):
    with open(file, "r") as file:
        data = json.load(file)
    for d in data:
        if d['model'] == 'publisher':
            model = Publisher
        elif d['model'] == 'book':
            model = Book
        elif d['model'] == 'shop':
            model = Shop
        elif d['model'] == 'stock':
            model = Stock
        elif d['model'] == 'sale':
            model = Sale
        sess.add(model(id=d.get('pk'), **d.get('fields')))
        sess.commit()


if __name__ == "__main__":
    engine = sq.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(engine)
    session = Session()

    add_test_data(session)

    publisher_input = "O'Reilly"
    get_query_publisher(session, publisher_input)