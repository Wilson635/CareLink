# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin

from apps import db, login_manager

from apps.authentication.util import hash_pass


class Users(db.Model, UserMixin):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    role = db.Column(db.String(64), unique=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


class Speciality(db.Model):
    __tablename__ = 'Speciality'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(64), unique=False)
    category = db.Column(
        db.Enum('Médecine', 'Chirurgie', 'Pédiatrie et Gynécologie', 'Urgences et Soins Intensifs', 'Médico-Technique',
                'Psychiatrie et Rééducation'), unique=False)
    date_creation = db.Column(db.DateTime, unique=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)


class Chambres(db.Model):
    __tablename__ = 'Chambres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(64), unique=False)
    date_creation = db.Column(db.DateTime, unique=False)
    capacity = db.Column(db.Integer, unique=False)
    type = db.Column(db.Enum('Standard', 'VIP', 'Privée'), unique=False)
    statut = db.Column(db.Enum('Disponible', 'Occupée', 'Maintenance'), unique=False)
    speciality_id = db.Column(db.Integer, db.ForeignKey('Speciality.id'))

    speciality = db.relationship('Speciality',
                                 backref=db.backref('chambres', lazy='dynamic'))

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return str(self.name)


class Patients(db.Model):
    __tablename__ = 'Patients'

    id_patient = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code_patient = db.Column(db.String(50), unique=True, nullable=False)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    date_naissance = db.Column(db.Date, nullable=False)
    sexe = db.Column(db.Enum('M', 'F'), nullable=False)
    adresse = db.Column(db.Text, nullable=True)
    telephone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    groupe_sanguin = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-'), nullable=True)
    historique_medical = db.Column(db.Text, nullable=True)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            setattr(self, property, value)

    def __repr__(self):
        return f"{self.nom} {self.prenom} ({self.code_patient})"


@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
