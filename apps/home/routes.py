# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
from datetime import datetime

from apps import db
from apps.authentication.models import Chambres, Speciality
from apps.home import blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.forms import RoomForm


@blueprint.route('/index')
@login_required
def index():
    return render_template('pages/index.html', segment='index')


@blueprint.route('/chambres', methods=['GET', 'POST'])
@login_required
def chambres():
    form = RoomForm(request.form)

    if request.method == 'POST' and form.validate():
        new_room = Chambres(
            name=form.numbers.data,
            description=form.description.data,
            speciality_id=form.speciality.data,
            type=form.type.data,
            capacity=form.capacity.data,
            statut=form.etat.data,
            date_creation=datetime.utcnow()
        )
        db.session.add(new_room)
        db.session.commit()
        flash("Chambre enregistrée avec succès.", "success")
        return redirect(url_for('home_blueprint.chambres'))

    chambres_list = Chambres.query.all()
    return render_template('pages/chambres.html', form=form, chambres=chambres_list)



@blueprint.route('/hospitalisation')
@login_required
def hospitalisation():
    return render_template('pages/hospitalisation.html')


@blueprint.route('/consultation')
@login_required
def consultation():
    return render_template('pages/consultation.html')


@blueprint.route('/medecin')
@login_required
def medecin():
    return render_template('pages/medecin.html')


@blueprint.route('/infirmière')
@login_required
def infirmiere():
    return render_template('pages/infirmiere.html')


@blueprint.route('/patients')
@login_required
def patients():
    return render_template('pages/patients.html')


@blueprint.route('/accounts/password-reset/')
def password_reset():
    return render_template('accounts/password_reset.html')


@blueprint.route('/accounts/password-reset-done/')
def password_reset_done():
    return render_template('accounts/password_reset_done.html')


@blueprint.route('/accounts/password-reset-confirm/')
def password_reset_confirm():
    return render_template('accounts/password_reset_confirm.html')


@blueprint.route('/accounts/password-reset-complete/')
def password_reset_complete():
    return render_template('accounts/password_reset_complete.html')


@blueprint.route('/accounts/password-change/')
def password_change():
    return render_template('accounts/password_change.html')


@blueprint.route('/accounts/password-change-done/')
def password_change_done():
    return render_template('accounts/password_change_done.html')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
