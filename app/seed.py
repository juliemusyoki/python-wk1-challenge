import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
from models import db, Hero, HeroPower, Power
import random

# Set the current directory to the script's directory
current_dir = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(current_dir, '..'))  # Add the parent directory to the Python path

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance/app.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# ... rest of the script remains unchanged ...

# Seeding powers
power_list = [
    {"name": "super strength", "description": "gives the wielder super-human strengths"},
    {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
    {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
    {"name": "elasticity", "description": "can stretch the human body to extreme lengths"},
]

# Seeding heroes
hero_list = [
    {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
    {"name": "Doreen Green", "super_name": "Squirrel Girl"},
    {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
    {"name": "Janet Van Dyne", "super_name": "The Wasp"},
    {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
    {"name": "Carol Danvers", "super_name": "Captain Marvel"},
    {"name": "Jean Grey", "super_name": "Dark Phoenix"},
    {"name": "Ororo Munroe", "super_name": "Storm"},
    {"name": "Kitty Pryde", "super_name": "Shadowcat"},
    {"name": "Elektra Natchios", "super_name": "Elektra"},
]

# Adding powers to heroes
strength_list = ["Strong", "Weak", "Average"]

with app.app_context():
    Power.query.delete()
    Hero.query.delete()
    HeroPower.query.delete()

    heroes = []
    for hero in hero_list:
        ahero = Hero(name=hero["name"], super_name=hero["super_name"])
        heroes.append(ahero)
    db.session.add_all(heroes)

    powers = []
    for power in power_list:
        apower = Power(name=power["name"], description=power["description"])
        powers.append(apower)
    db.session.add_all(powers)

    # Associate each hero with all available powers
    hero_powers = []
    for hero in heroes:
        for power in powers:
            astrength = HeroPower(
                strength=random.choice(strength_list),
                hero=hero,
                power=power,
            )
            hero_powers.append(astrength)
    db.session.add_all(hero_powers)

    db.session.commit()

print("🦸‍♀️ Done seeding!")
