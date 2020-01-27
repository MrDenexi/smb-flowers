from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


engine = create_engine('sqlite:///db/database.sqlite3', convert_unicode=True, echo=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

def session_factory():
    # Base.metadata.create_all(engine)
    return db_session()

def init_db():
    from models import User, Access, Flower, Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = session_factory()

    # add flowers
    for count, port in enumerate([3,5,6,9,10,11]):
        flower = Flower(port, True, count)
        session.add(flower)

    session.commit()


if __name__ == "__main__":
    init_db()
