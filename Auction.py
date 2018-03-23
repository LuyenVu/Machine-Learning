import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,ForeignKey,Float,DateTime

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)

class Item(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String,nullable= False)
    description = Column(String,nullable=False)
    start_time = Column(DateTime)
    users = db.relationship('User', secondary='place_bids', backref='User')

    def __init__(self,name,description,starttime):
        self.name = name
        self.description = description
        self.start_time = starttime

    def __repr__(self):
        return '<Item {}>'.format(self.name)

class User(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String,nullable=False)
    password = Column(String,nullable=False)
    items = db.relationship('Item', secondary='place_bids', backref='Item')

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Bid(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)
    price = Column(Float,nullable=False)

    def __init__(self,price):
        self.price = price


class Auction(db.Model):
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True,nullable=False)
    item_id = Column(Integer, ForeignKey('item.id'), primary_key=True,nullable=False)

    def __init__(self,userid,itemid):
        self.user_id = userid
        self.item_id = itemid


class PlaceBids(db.Model):
    id = Column(Integer, primary_key=True,autoincrement=True)
    userBid_id = Column(Integer, ForeignKey('user.id'), primary_key=True,nullable=False)
    itemBid_id = Column(Integer, ForeignKey('item.id'), primary_key=True,nullable=False)
    bid_id = Column(Integer,ForeignKey('bid.id'),primary_key=True,nullable=False)

    def __init__(self,userId,itemId,bidId):
        self.userBid_id = userId
        self.itemBid_id = itemId
        self.bid_id = bidId

db.create_all()

# Create 3 users: an Auction, 2 bids
newuser1 = User('Auction user 1','123')
newuser2 = User('Bid user 1','123')
newuser3 = User('Bid user 2','123')
db.session.add(newuser1)
db.session.add(newuser2)
db.session.add(newuser3)

#Create 2 items
newItem1 = Item('Baseball','Basball use in Olimpic 2018',datetime.datetime(2018,3,1,8,15,00))
newItem2 = Item('Huyndai Elantra auto','Huyndai Elatra 2018 AT 2.0',datetime.datetime(2018,3,21,00,0,00))
db.session.add(newItem1)
db.session.add(newItem2)

db.session.commit()

#Make one user auction a baseball
newAuction1= Auction(1,1)
db.session.add(newAuction1)
db.session.commit()

#Each other user place 2 bids on baseball: crate new bid and new a place bid together
newBid1= Bid('400')
db.session.add(newBid1)
db.session.commit()

newPlaceBids_01 = PlaceBids(2,1,1)
db.session.add(newPlaceBids_01)
db.session.commit()

newBid2= Bid('600')
db.session.add(newBid2)
db.session.commit()

newPlaceBids_02 = PlaceBids(3,1,2)
db.session.add(newPlaceBids_02)
db.session.commit()

#Perform a query to findout which user placed the highest bid
def highestBid(itemid):
    q = db.session.query(PlaceBids,User,Bid).filter(PlaceBids.userBid_id == User.id).\
       filter(PlaceBids.bid_id == Bid.id).filter(PlaceBids.itemBid_id == itemid).\
       order_by(Bid.price.desc()).first() #all()

    #just test to show list PlaceBids
    # for c in q:
    #   print(c.User.username,c.Bid.price)

    item = db.session.query(Item).filter(Item.id == q.PlaceBids.itemBid_id).first()

    print('Item Name:', item.name, "\nPerson highest bid:" , q.User.username,"\nPrice:" , q.Bid.price)

highestBid(1)  # item = 1 with Baseball item
