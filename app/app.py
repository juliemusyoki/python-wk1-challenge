#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return ''

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [{'id': hero.id, 'name': hero.name, 'super_name': getattr(hero, 'super_name', '')} for hero in heroes]
    return jsonify(hero_data)

# GET /heroes/:id
@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)

    if not hero:
        return jsonify({'error': 'Hero not found'}), 404

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': getattr(hero, 'super_name', ''),
        'powers': [{'id': power.id, 'name': power.name, 'description': getattr(power, 'description', '')} for power in hero.powers]
    }

    return jsonify(hero_data)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [{'id': power.id, 'name': power.name, 'description': getattr(power, 'description', '')} for power in powers]
    return jsonify(power_data)

# GET /powers/:id
@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)

    if not power:
        return jsonify({'error': 'Power not found'}), 404

    power_data = {
        'id': power.id,
        'name': power.name,
        'description': getattr(power, 'description', '')
    }

    return jsonify(power_data)

# PATCH /powers/:id
@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)

    if not power:
        return jsonify({'error': 'Power not found'}), 404

    try:
        data = request.get_json()
        power.description = data['description']
        db.session.commit()
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    except KeyError:
        return jsonify({'errors': ['validation errors']}), 400

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data = request.get_json()
        strength = data['strength']
        power_id = data['power_id']
        hero_id = data['hero_id']

        # Validate strength
        if strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Invalid strength value")

        hero_power = HeroPower(strength=strength, power_id=power_id, hero_id=hero_id)
        db.session.add(hero_power)
        db.session.commit()

        hero = Hero.query.get(hero_id)
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': getattr(hero, 'super_name', ''),
            'powers': [{'id': power.id, 'name': power.name, 'description': getattr(power, 'description', '')} for power in hero.powers]
        }

        return jsonify(hero_data)
    except (KeyError, ValueError):
        return jsonify({'errors': ['validation errors']}), 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
