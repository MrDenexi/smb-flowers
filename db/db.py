from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# create global database variables
engine = create_engine('sqlite:///db/database.sqlite3', convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()

# get session
def session_factory():
    # Base.metadata.create_all(engine)
    return db_session()


# run this to create the database
def init_db():
    # create all tables
    from models import User, Access, Flower, Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = session_factory()

    # add flowers
    for count, port in enumerate([3,5,6]):
        flower = Flower(port, True, count)
        session.add(flower)

    # commit all
    session.commit()


if __name__ == "__main__":
    # run this to create the database
    init_db()
