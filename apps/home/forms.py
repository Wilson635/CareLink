# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.fields.simple import TextAreaField, FileField
from wtforms.validators import DataRequired, Email


class RoomForm(FlaskForm):
    numbers = StringField('Numéro de chambre',
                          id='number_create',
                          validators=[DataRequired()])

    speciality = SelectField('Spécialité de chambre',
                             id='speciality_create',
                             choices=[],  # La liste sera remplie dynamiquement
                             coerce=int,  # Convertir l'ID en entier
                             validators=[DataRequired()])

    description = StringField('Description de chambre',
                              id='description_create',
                              validators=[DataRequired()])

    type = SelectField('Type de chambre',
                       id='type_create',
                       choices=[('VIP', 'VIP'), ('Standard', 'Standard'), ('Privée', 'Privée')],
                       validators=[DataRequired()])

    capacity = StringField('Capacité de la chambre',
                           id='capacity_create',
                           validators=[DataRequired()])

    etat = SelectField('Etat de la chambre',
                       id='etat_create',
                       choices=[('Disponible', 'Disponible'), ('Occupée', 'Occupée'), ('Maintenance', 'Maintenance')],
                       validators=[DataRequired()])


class PatientForm(FlaskForm):
    nom = StringField('Nom',
                      id='nom',
                      validators=[DataRequired()])
    prenom = StringField('Prénom',
                         id='prenom',
                         validators=[DataRequired()])
    date_naissance = DateField('Date de naissance',
                               id='date_naissance',
                               format='%Y-%m-%d',
                               validators=[DataRequired()])
    sexe = SelectField('Sexe',
                       id='sexe',
                       choices=[('M', 'Masculin'), ('F', 'Féminin')],
                       validators=[DataRequired()])
    adresse = TextAreaField('Adresse',
                            id='adresse')
    telephone = StringField('Téléphone',
                            id='telephone')
    email = StringField('Email',
                        id='email',
                        validators=[Email()])
    groupe_sanguin = SelectField('Groupe Sanguin',
                                 id='groupe_sanguin',
                                 choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('O+', 'O+'),
                                          ('O-', 'O-'), ('AB+', 'AB+'), ('AB-', 'AB-')])
    historique_medical = TextAreaField('Historique Médical',
                                       id='historique_medical')


class MedecinForm(FlaskForm):
    nom = StringField('Nom', id='nom', validators=[DataRequired()])
    prenom = StringField('Prénom', id='prenom', validators=[DataRequired()])
    specialite = SelectField('Spécialité', id='specialite', coerce=int, validators=[DataRequired()])
    telephone = StringField('Téléphone', id='telephone', validators=[DataRequired()])
    email = StringField('Email', id='email', validators=[DataRequired(), Email()])
    image = FileField('Image', id='image')  # Utilisation de FileField pour l'upload de l'image