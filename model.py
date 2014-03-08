from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref


ENGINE = create_engine("sqlite:///ratings.db", echo=True)
Session = scoped_session(sessionmaker(bind=ENGINE,
                                        autocommit = False,
                                        autoflush = False))

Base = declarative_base()
Base.query = Session.query_property()

### Class declarations go here
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable = True)
    gender = Column(String(10), nullable = True)

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key = True)
    title = Column(String(64))
    release_date = Column(DateTime, nullable = True)
    imdb_url = Column(String(90), nullable = True)

class Rating(Base):
    __tablename__="ratings"
    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)

    user = relationship("User",
        backref=backref("ratings", order_by=id))

### End class declarations


def createTables():
    #make a funciton to recreate the tables in the db
    Base.metadata.create_all(ENGINE)
    print "all our base are recreated!!!"

def authenticate(email, password):
# If a row matches 
    row = Session.query(User).filter_by(email = email, password = password).one()
    if row:       
        return row
    else:
        return -1


def main():
    """In case we need this for something"""
    # connect()
    #createTables()


if __name__ == "__main__":
    main()
