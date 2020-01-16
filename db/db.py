from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///smb.db')
# use session_factory() to get a new Session
_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    # Base.metadata.create_all(engine)
    return _SessionFactory()


if __name__ == "__main__":
    # create scheme
    Base.metadata.create_all(engine)

    # add flowers
