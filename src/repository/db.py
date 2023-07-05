from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

connection_string = "mysql+mysqlconnector://root:password@mysql:3306/db"
engine = create_engine(connection_string, echo=True)

Base = declarative_base()


def is_connected_to_db():
    try:
        engine = create_engine(connection_string)
        with engine.connect():
            return True
    except:
        return False
