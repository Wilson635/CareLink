# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class RoomForm(FlaskForm):
    numbers = StringField('Numéro de chambre',
                          id='number_create',
                          validators=[DataRequired()])

    speciality = StringField('Specialité de chambre',
                             id='speciality_create',
                             validators=[DataRequired()])

    description = StringField('Description de chambre',
                             id='description_create',
                             validators=[DataRequired()])

    type = StringField('Type de chambre',
                       id='type_create',
                       validators=[DataRequired()])

    capacity = StringField('Capacité de la chambre',
                           id='capacity_create',
                           validators=[DataRequired()])

    etat = StringField('Etat de la chambre',
                       id='etat_create',
                       validators=[DataRequired()])
