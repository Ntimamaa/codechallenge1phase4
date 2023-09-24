from flask import Flask, jsonify, request, abort
from models import db, Hero, Power, HeroPower, ValidationError
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database_name.db'
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name
    } for hero in heroes]), 200


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404
    
    powers = [{"id": hp.power.id, "name": hp.power.name, "description": hp.power.description} for hp in hero.hero_powers]
    return jsonify({
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": powers
    }), 200


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([{
        "id": power.id,
        "name": power.name,
        "description": power.description
    } for power in powers]), 200


@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404
    
    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    }), 200


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.json
    description = data.get('description', '')
    
    if not description or len(description) < 20:
        return jsonify({"errors": ["Description must be present and at least 20 characters long"]}), 400
    
    power.description = description
    db.session.commit()
    
    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    }), 200


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.json
    hero_id = data.get('hero_id')
    power_id = data.get('power_id')
    strength = data.get('strength')
    
    if strength not in ['Strong', 'Weak', 'Average']:
        return jsonify({"errors": ["Invalid strength value"]}), 400
    
    hero_power = HeroPower(hero_id=hero_id, power_id=power_id, strength=strength)
    
    try:
        hero_power.validate()
        db.session.add(hero_power)
        db.session.commit()
    except ValidationError as e:
        return jsonify({"errors": [str(e)]}), 400
    
    hero = Hero.query.get(hero_id)
    powers = [{"id": hp.power.id, "name": hp.power.name, "description": hp.power.description} for hp in hero.hero_powers]
    
    return jsonify({
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "powers": powers
    }), 201


if __name__ == '__main__':
    app.run(debug=True)
