from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Table 
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

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
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    is_shipped = Column(Boolean, default=True)

    #Creates a many to many relationship -->> Only need a one to many relationship updated to reflect this
    product = relationship('Product', back_populates='orders')
    user = relationship('User', back_populates='orders')

Base.metadata.create_all(engine)

session = Session()

user1 = User(name='Lanae', email='naenae@example.com')
user2 = User(name='Riley', email='ridawg@example.com')
product1 = Product(name='Ball', price = 50)
product2 = Product(name='Claw', price = 150)
product3 = Product(name='Widget', price = 100)

# old_user = session.query(User).filter_by(email='naenae@example.com').first()
# if old_user:
#     session.delete(old_user)
#     session.commit()
#     # session.expunge(old_user)


# ##Un comment to add user back in, then re-comment out so you can delete them
# user1 = User(name='Lanae', email='naenae@example.com')
# session.add(user1)
# session.commit()

#Adds users and products to the database -->> comment out after initial commit so you don't duplicate
# session.add_all([user1, user2, product1, product2, product3]) #Must wrap all items in a bracket
# session.commit()

order1 = Order(user_id=1, product_id=1, quantity=2, is_shipped=False)
order2 = Order(user_id=1, product_id=3, quantity=3, is_shipped=True)
order3 = Order(user_id=2, product_id=2, quantity=4, is_shipped=True)
order4 = Order(user_id=2, product_id=3, quantity=1, is_shipped=True)

#Commented out so it doesn't run again and try to create a duplicate
# session.add_all([order1, order2, order3, order4])
# session.commit()

# user=session.query(User).filter_by(name='Lanae').first() #not necessary
# product = session.query(Product).filter_by(name='Widget').first() #not necessary

#Not using, there is a simpler but repetitive way to do this
# new_order = Order(
#     user = user1,
#     product = product1,
#     quantity=3,
#     is_shipped=False
# )

# session.add(new_order)
# session.commit()

#Retreive users and print their information

# users = session.query(User).all()

# for user in users:
#     print(user.name, user.email)

# products = session.query(Product).all()

# for product in products:
#     print(product.name, product.price)

# orders = session.query(Order).all()

# for order in orders:
#     print(order.user.name, order.product.name, order.quantity) #added order.x.x so the statements would print correctly

#Updating a price

# product = session.query(Product).filter_by(name='Widget').first()
# product.price = 120
# session.commit()

# for product in products:
#     print(product.name, product.price)

# #Deleting a user by id
# user = session.query(User).filter_by(id=1).first()

# if user:
#     session.delete(user)
#     session.commit()
#     print(f'User {user.name} deleted')
# else:
#     print('User not found')

#Delete the 'old' user to get rid of the email

# old_user = session.query(User).filter_by(email='naenae@example.com').first()
# if old_user:
#     session.delete(old_user)
#     session.commit()
#     session.expunge(old_user)


# ##Un comment to add user back in, then re-comment out so you can delete them
# user1 = User(name='Lanae', email='naenae@example.com')
# session.add(user1)
# session.commit()