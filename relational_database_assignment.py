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

Base.metadata.drop_all(engine) #Drops the database so you can start over again, eachtime you run the code.  Comment this out if you don't want to drop the database everytime.
Base.metadata.create_all(engine)

session = Session()



user1 = User(name='Lanae', email='naenae@example.com')
user2 = User(name='Riley', email='ridawg@example.com')
product1 = Product(name='Ball', price = 50)
product2 = Product(name='Claw', price = 150)
product3 = Product(name='Widget', price = 100)

#Adds users and products to the database -->> comment out after initial commit so you don't duplicate --> Actually since, we have the drop_all at the top, we can leave this because the database resets each time, which stops the database from creating duplicates.
session.add_all([user1, user2, product1, product2, product3]) #Must wrap all items in a bracket
session.commit()

order1 = Order(user_id=1, product_id=1, quantity=2, is_shipped=False)
order2 = Order(user_id=1, product_id=3, quantity=3, is_shipped=True)
order3 = Order(user_id=2, product_id=2, quantity=4, is_shipped=True)
order4 = Order(user_id=2, product_id=3, quantity=1, is_shipped=True)

#Commented out so it doesn't run again and try to create a duplicate --> Actually since, we have the drop_all at the top, we can leave this because the database resets each time, which stops the database from creating duplicates.
session.add_all([order1, order2, order3, order4])
session.commit()

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

users = session.query(User).all()

for user in users:
    print(user.name, user.email)

products = session.query(Product).all()

for product in products:
    print(product.name, product.price)

orders = session.query(Order).all()

for order in orders:
    print(order.user.name, order.product.name, order.quantity) #added order.x.x so the statements would print correctly

#quer for orders that have not been shipped
print('Unshipped Orders:')
for order in orders:
    if not order.is_shipped:
        print(f'Orders awaiting shipment: {order.user.name}, Product: {order.product.name}, Qty: {order.quantity}')

#Alternate way to query for orders that have not been shipped
print('Unshipped Orders:')
unshipped_orders = session.query(Order).filter_by(is_shipped=False).all()
for orders in unshipped_orders:
    print(f'Orders awaiting shipment: {orders.user.name}, Product: {orders.product.name}, Qty: {orders.quantity}')

#Count the number of unshipped orders
unshipped_count = session.query(Order).filter_by(is_shipped=False).count()
print(f'Total unshipped orders: {unshipped_count}')

#Updating a price - enter a different price each time you run the code

product = session.query(Product).filter_by(name='Widget').first()
product.price = 120
session.commit()

for product in products:
    print(product.name, product.price)

# # # #Deleting a user by id - this works for single use purposes
user = session.query(User).filter_by(id=1).first()

if user:
    session.delete(user)
    session.commit()
    print(f'User {user.name} deleted')
else:
    print('User not found')




# I was trying to figure out how to add a the use back in after I deleted them.  I tried a bunch of different ways,
# but since the user email was linked to an order and because the table incremented each time, the user wouldn't ever
# add back to user_id 1.  So we can still delet, but I added the drop_all at the top to set the code.  Some of the comments
# are from trying to figure out how to add the user back in after deletion, but I couldn't get it to work because of the 
# relationships and the fact that the id's increment each time.  So I just added the drop_all at the top to reset the database each time.

# #Delete the 'old' user to get rid of the email

# # old_user = session.query(User).filter_by(email='naenae@example.com').first()
# # if old_user:
# #     session.delete(old_user)
# #     session.commit()
# #     session.expunge(old_user)


# # # ##Un comment to add user back in, then re-comment out so you can delete them
# # user1 = User(name='Lanae', email='naenae@example.com')
# # session.add(user1)
# # session.commit()



