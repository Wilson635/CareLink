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


class Medecin(db.Model):
    __tablename__ = 'Medecins'

    id_medecin = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    specialite_id = db.Column(db.Integer, db.ForeignKey('Speciality.id'), nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image = db.Column(db.String(255), nullable=True)

    specialite = db.relationship('Speciality', backref=db.backref('medecins', lazy=True))

    def __repr__(self):
        return f"{self.nom} {self.prenom}"


class Consultation(db.Model):
    __tablename__ = 'Consultations'

    id_consultation = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_consultation = db.Column(db.DateTime, nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('Medecins.id_medecin'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.id_patient'), nullable=False)
    observations = db.Column(db.Text, nullable=True)
    ordonnance = db.Column(db.Text, nullable=True)

    medecin = db.relationship('Medecin', backref=db.backref('consultations', lazy=True))
    patient = db.relationship('Patients', backref=db.backref('consultations', lazy=True))

    def __repr__(self):
        return f"Consultation {self.id_consultation} - {self.patient.nom} {self.patient.prenom}"


class Hospitalisation(db.Model):
    __tablename__ = 'Hospitalisations'

    id_hospitalisation = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_entree = db.Column(db.DateTime, nullable=False)
    date_sortie = db.Column(db.DateTime, nullable=True)
    chambre_id = db.Column(db.Integer, db.ForeignKey('Chambres.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.id_patient'), nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('Medecins.id_medecin'), nullable=False)
    motif = db.Column(db.Text, nullable=True)

    chambre = db.relationship('Chambres', backref=db.backref('hospitalisations', lazy=True))
    patient = db.relationship('Patients', backref=db.backref('hospitalisations', lazy=True))
    medecin = db.relationship('Medecin', backref=db.backref('hospitalisations', lazy=True))

    def __repr__(self):
        return f"Hospitalisation {self.id_hospitalisation} - {self.patient.nom} {self.patient.prenom}"


class Medicaments(db.Model):
    __tablename__ = 'Medicaments'

    id_medicament = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom_medicament = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    stock = db.Column(db.Integer, nullable=False)
    prix = db.Column(db.Float, nullable=False)
    date_creation = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"{self.nom_medicament}"


class Traitements(db.Model):
    __tablename__ = 'Traitements'

    id_traitement = db.Column(db.Integer, primary_key=True, autoincrement=True)
    medicament_id = db.Column(db.Integer, db.ForeignKey('Medicaments.id_medicament'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.id_patient'), nullable=False)
    consultation_id = db.Column(db.Integer, db.ForeignKey('Consultations.id_consultation'), nullable=False)
    posologie = db.Column(db.String(100), nullable=False)
    duree = db.Column(db.Integer, nullable=False)

    patient = db.relationship('Patients', backref=db.backref('traitements', lazy=True))
    medicament = db.relationship('Medicaments', backref=db.backref('traitements', lazy=True))
    consultation = db.relationship('Consultation', backref=db.backref('traitements', lazy=True))

    def __repr__(self):
        return f"Traitement {self.id_traitement} - {self.medicament.nom_medicament}"


class Rapports(db.Model):
    __tablename__ = 'Rapports'

    id_rapport = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_rapport = db.Column(db.DateTime, nullable=False)
    medecin_id = db.Column(db.Integer, db.ForeignKey('Medecins.id_medecin'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('Patients.id_patient'), nullable=False)
    contenu = db.Column(db.Text, nullable=True)

    medecin = db.relationship('Medecin', backref=db.backref('rapports', lazy=True))
    patient = db.relationship('Patients', backref=db.backref('rapports', lazy=True))

    def __repr__(self):
        return f"Rapport {self.id_rapport} - {self.patient.nom} {self.patient.prenom}"



@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None
