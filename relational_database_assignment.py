from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///shop.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    
    orders = relationship(
        'Order', secondary=product_order, back_populates='users'
    )

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    is_shipped = Column(Boolean, default=True)

    #Creates a many to many relationship
    orders = relationship(
        'Order', secondary=product_order, back_populates='products'
    )

class Order(Base):
    __tablename__= 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey=User.id)
    product_id = Column(Integer, ForeignKey=Product.id)
    quantity = Column(Integer, nullable=False)
    
    #Creates a many to many relationship
    products = relationship(
        'Product', secondary=product_order, back_populates='orders'
        )
    users = relationship(
        'User', secondary=product_table, back_populates='orders'
    )

session = Session()