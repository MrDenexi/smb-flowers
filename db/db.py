from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True, echo=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def session_factory():
    # Base.metadata.create_all(engine)
    return db_session()

def init_db():
    from models import User, Access, Flower, Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    

    # add flowers
    # flower = Flower(12, True, 1)
    # db_session.add(flower)
    # db_session.commit()
    


if __name__ == "__main__":
    init_db()
