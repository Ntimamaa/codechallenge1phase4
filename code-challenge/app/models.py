from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import ValidationError

db = SQLAlchemy()

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(150), nullable=False)

    def validate(self):
        if self.strength not in ['Strong', 'Weak', 'Average']:
            raise ValidationError("Invalid strength value")

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('power.id'), nullable=False)
    strength = db.Column(db.String(50), nullable=False)

    def validate(self):
        if self.strength not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Invalid strength value")

    hero = db.relationship('Hero', backref=db.backref('hero_powers', lazy=True))
    power = db.relationship('Power', backref=db.backref('hero_powers', lazy=True))

