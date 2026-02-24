from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///shop.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

#Association table to link relationships -->> Removed because, I didn't need many to many relationships. Only one to many
# # user_product = Table(
# #     'user_product',
# #     Base.metadata,
# #     Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
# #     Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
# #     Column('quantity', Integer),
# #     Column('is_shipped', Boolean, default=False)
# )

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    
    #One to many relationship
    orders = relationship('Order', back_populates='user')

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    

    #Creates a many to many relationship -->> Corrected to one to many, removed secondary=user_product
    orders = relationship('Order', back_populates='product')

class Order(Base):
    __tablename__= 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey='users.id')
    product_id = Column(Integer, ForeignKey='products.id')
    quantity = Column(Integer, nullable=False)
    is_shipped = Column(Boolean, default=True)

    #Creates a many to many relationship -->> Only need a one to many relationship updated to reflect this
    product = relationship('Product', back_populates='orders')
    user = relationship('User', back_populates='orders')

session = Session()