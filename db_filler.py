from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Base, Category, Item, User

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


User1 = User(name="Fancy Phill", email="fancypants@example.com",
			picture="htttp://www.placehold.it/300x300")
session.add(User1)
session.commit()

cat1 = Category(name="Engine", user=User1)
session.add(cat1)
session.commit()

item1 = Item(name="Piston", price="$44.99", category=cat1, user=User1)
session.add(item1)
session.commit()

item2 = Item(name="Valves", price="$69.99",category=cat1, user=User1)
session.add(item2)
session.commit()


item3 = Item(name="Cam", price="89.99", category=cat1, user=User1)
session.add(item3)
session.commit()

item4 = Item(name="Valve Cover", price="$34.99", category=cat1, user=User1)
session.add(item4)
session.commit()

item5 = Item(name="Timing Chain", price="$79.99", category=cat1, user=User1)
session.add(item5)
session.commit()

cat2 = Category(name="Exterior", user=User1)
session.add(cat2)
session.commit()

item6 = Item(name="Front Fender", price="$49.99", category=cat2, user=User1)
session.add(item6)
session.commit()

item7 = Item(name="Rear Fender", price="$59.99", category=cat2, user=User1)
session.add(item7)
session.commit()

item8 = Item(name="Hood", price="$99.99", category=cat2, user=User1)
session.add(item8)
session.commit()

item9 = Item(name="Bumper", price="$89.99", category=cat2, user=User1)
session.add(item9)
session.commit()

item10 = Item(name="Door", price="$129.99", category=cat2, user=User1)
session.add(item10)
session.commit()

cat3 = Category(name="Interior", user=User1)
session.add(cat3)
session.commit()

item11 = Item(name="Seat Cover", price="$39.99", category=cat3, user=User1)
session.add(item11)
session.commit()

item12 = Item(name="Steering Wheel", price="$54.99", category=cat3, user=User1)
session.add(item12)
session.commit()

item13 = Item(name="Rearview Mirror", price="$12.99", category=cat3, user=User1)
session.add(item13)
session.commit()

item14 = Item(name="Carpet", price="$29.99", category=cat3, user=User1)
session.add(item14)
session.commit()

item15 = Item(name="Floor Mats", price="$34.99", category=cat3, user=User1)
session.add(item15)
session.commit()

cat4 = Category(name="Accessories", user=User1)
session.add(cat4)
session.commit()

item16 = Item(name="Keychain", price="$4.99", category=cat4, user=User1)
session.add(item16)
session.commit()

item17 = Item(name="Bumper Sticker", price="$6.99", category=cat4, user=User1)
session.add(item16)
session.commit()

item18 = Item(name="Shifter Knob", price="$14.99", category=cat4, user=User1)
session.add(item18)
session.commit()

item19 = Item(name="License Plate Frame", price="$19.99", category=cat4, user=User1)
session.add(item18)
session.commit()

item20 = Item(name="Air Freshener", price="$4.99", category=cat4, user=User1)
session.add(item20)
session.commit()

cat5 = Category(name="Electrical", user=User1)
session.add(cat5)
session.commit()

item21 = Item(name="Stereo", price="$99.99", category=cat5, user=User1)
session.add(item21)
session.commit()

item22 = Item(name="Phone Charger", price="$19.99", category=cat5, user=User1)
session.add(item22)
session.commit()

item23 = Item(name="Heated Seat Cushion", price="$34.99", category=cat5, user=User1)
session.add(item23)
session.commit()

item24 = Item(name="Driving Gloves", price="$29.99", category=cat5, user=User1)
session.add(item24)
session.commit()

item25 = Item(name="Sun Shade", price="$19.99", category=cat5, user=User1)
session.add(item25)
session.commit()

print "Items added!!!"