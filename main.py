from dotenv import dotenv_values
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
from models import Publisher, Shop, Book, Stock, Sale, create_tables
import json


LOGIN = dotenv_values(".env")["LOGIN"]
PASSWORD = dotenv_values(".env")["PASSWORD"]
DB = dotenv_values(".env")["NAME_DB"]
DSN = f"postgresql://{LOGIN}:{PASSWORD}@localhost:5432/{DB}"


def get_query_publisher(sess, publisher):
    
    q = sess.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    
    if publisher.isdigit():
        fin = q.filter(Publisher.id == publisher).all()
        print(fin)
    else:
        fin = q.filter(Publisher.name == publisher).all()
        print(fin)
    for title, name, price, date in fin:
        print(f"{title: <40} | {name: <10} | {price: <8} | {date.strftime('%d-%m-%Y')}")


def add_test_data(sess, file="tests_data.json"):
    model = {
    'publisher': Publisher,
    'shop': Shop,
    'book': Book,
    'stock': Stock,
    'sale': Sale
    }

    with open('tests_data.json', 'r') as file:
        data = json.load(file)

        for record in data:
            sess.add(model[record.get('model')](id=record.get('pk'), **record.get('fields')))
            sess.commit()
            

if __name__ == "__main__":
    engine = sq.create_engine(DSN)
    create_tables(engine)

    Session = sessionmaker(engine)
    session = Session()

    add_test_data(session)

    publisher_input = input('Введите автора: ')
    get_query_publisher(session, publisher_input)
    