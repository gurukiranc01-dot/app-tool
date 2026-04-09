from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    role = db.Column(db.String(20))


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    rc = db.Column(db.String(50))
    chassis = db.Column(db.String(100))
    engine = db.Column(db.String(100))
    owner = db.Column(db.String(100))
    received_on = db.Column(db.String(20))
    inertia = db.Column(db.String(50))
    cc = db.Column(db.String(50))
    gears = db.Column(db.String(50))
    road_a = db.Column(db.String(50))
    road_b = db.Column(db.String(50))
    road_c = db.Column(db.String(50))
    fuel = db.Column(db.String(50))
    oil = db.Column(db.String(50))
    coolant = db.Column(db.String(50))
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    image = db.Column(db.String(200))
    bike = db.Column(db.String(100))
    insurance = db.Column(db.String(200))
    number_plate = db.Column(db.String(50))
    reg_date = db.Column(db.String(20))
    mfg_date = db.Column(db.String(20))
    rc_card = db.Column(db.String(200))
    insurance_file = db.Column(db.String(200))
    return_image = db.Column(db.String(200))
    status = db.Column(db.String(50), default="In Testing")
    
    # Vehicle Condition Checklist
    number_of_keys = db.Column(db.Integer, default=1)
    scratches_present = db.Column(db.Boolean, default=False)
    scratches_details = db.Column(db.String(500))
    scratches_image = db.Column(db.String(200))
    dents_present = db.Column(db.Boolean, default=False)
    dents_details = db.Column(db.String(500))
    dents_image = db.Column(db.String(200))
    glass_damage_present = db.Column(db.Boolean, default=False)
    glass_damage_details = db.Column(db.String(500))
    glass_damage_image = db.Column(db.String(200))
    tire_condition = db.Column(db.String(50))  # Good, Fair, Poor
    battery_status = db.Column(db.String(50))  # Good, Weak, Dead
    lights_issue_present = db.Column(db.Boolean, default=False)
    lights_details = db.Column(db.String(500))
    lights_image = db.Column(db.String(200))
    engine_status = db.Column(db.String(100))  # Starts Smoothly, Starts with Difficulty, Won't Start
    condition_notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Instrumentation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer)
    type = db.Column(db.String(50))
    activity = db.Column(db.String(200))
    request_date = db.Column(db.String(20))
    completion_date = db.Column(db.String(20))
    details = db.Column(db.String(200))


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer)
    description = db.Column(db.String(500))
    date = db.Column(db.String(20))
    performed_by = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)