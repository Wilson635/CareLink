# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import os
from datetime import datetime

from werkzeug.utils import secure_filename

from apps import db
from apps.authentication.models import Chambres, Speciality, Patients, Medecin, Hospitalisation, Consultation, \
    Infirmiere
from apps.home import blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from jinja2 import TemplateNotFound
from apps.home.forms import RoomForm, PatientForm, MedecinForm, HospitalisationForm, InfirmiereForm, ConsultationForm


@blueprint.route('/index')
@login_required
def index():
    # Count all patients
    patients_count = Patients.query.count()
    # Count all doctors
    doctors_count = Medecin.query.count()
    # Count all rooms
    rooms_count = Chambres.query.count()
    # Count all hospitalisations
    hospitalisations_count = Hospitalisation.query.count()
    # Count all specialties
    specialties_count = Speciality.query.count()
    # Count all hospitalisations by doctor
    hospitalisations_by_doctor = db.session.query(Medecin, db.func.count(Hospitalisation.id_hospitalisation)).join(
        Hospitalisation).group_by(Medecin).all()
    # Count all hospitalisations by patient
    hospitalisations_by_patient = db.session.query(Patients, db.func.count(Hospitalisation.id_hospitalisation)).join(
        Hospitalisation).group_by(Patients).all()
    # Count all hospitalisations by room
    hospitalisations_by_room = db.session.query(Chambres, db.func.count(Hospitalisation.id_hospitalisation)).join(
        Hospitalisation).group_by(Chambres).all()
    # Count all Consultations
    consultations_count = Consultation.query.count()
    # Count all infirmieres
    infirmieres_count = Infirmiere.query.count()
    return render_template('pages/index.html', segment='index',
                           patients_count=patients_count,
                           doctors_count=doctors_count,
                           rooms_count=rooms_count,
                           hospitalisations_count=hospitalisations_count,
                           specialties_count=specialties_count,
                           consultations_count=consultations_count,
                           infirmieres_count=infirmieres_count,
                           hospitalisations_by_doctor=hospitalisations_by_doctor,
                           hospitalisations_by_patient=hospitalisations_by_patient,
                           hospitalisations_by_room=hospitalisations_by_room)


@blueprint.route('/chambres', methods=['GET', 'POST'])
@login_required
def chambres():
    form = RoomForm(request.form)
    # Récupérer les spécialités depuis la base de données
    form.speciality.choices = [(s.id, s.name) for s in Speciality.query.all()]
    # form.speciality.choices = [("", "-- Sélectionner une spécialité --")] + [(s.id, s.name) for s in Speciality.query.all()]

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


@blueprint.route('/hospitalisation', methods=['GET', 'POST'])
@login_required
def hospitalisation():
    form = HospitalisationForm()
    form.patient.choices = [(p.id_patient, f"{p.nom} {p.prenom}") for p in Patients.query.all()]
    form.medecin.choices = [(m.id_medecin, f"{m.nom} {m.prenom}") for m in Medecin.query.all()]
    form.chambre.choices = [(c.id, c.name) for c in Chambres.query.all()]

    if request.method == 'POST' and form.validate():
        # Traitement de l'hospitalisation ici

        new_hospitalisation = Hospitalisation(
            patient_id=form.patient.data,
            medecin_id=form.medecin.data,
            chambre_id=form.chambre.data,
            date_entree=form.date_entree.data,
            date_sortie=form.date_sortie.data if form.date_sortie.data else None,
            motif=form.motif.data
        )
        db.session.add(new_hospitalisation)
        db.session.commit()
        # Envoi d'un message flash pour indiquer le succès de l'opération
        flash("Hospitalisation enregistrée avec succès.", "success")

        # Redirection vers la page d'hospitalisation
        return redirect(url_for('home_blueprint.hospitalisation'))

    # Récupération de la liste des hospitalisations
    hospitalisations_list = Hospitalisation.query.all()
    return render_template('pages/hospitalisation.html', form=form, hospitalisations=hospitalisations_list)


@blueprint.route('/hospitalisation/delete/<int:id_hospitalisation>', methods=['POST'])
def delete_hospitalisation(id_hospitalisation):
    hospitalisation = Hospitalisation.query.get_or_404(id_hospitalisation)
    db.session.delete(hospitalisation)
    db.session.commit()
    flash("Hospitalisation supprimée avec succès.", "success")
    return redirect(url_for('home_blueprint.hospitalisation'))


@blueprint.route('/hospitalisation/edit/<int:id_hospitalisation>', methods=['GET', 'POST'])
@login_required
def edit_hospitalisation(id_hospitalisation):
    form = HospitalisationForm()
    form.patient.choices = [(p.id_patient, f"{p.nom} {p.prenom}") for p in Patients.query.all()]
    form.medecin.choices = [(m.id_medecin, f"{m.nom} {m.prenom}") for m in Medecin.query.all()]
    form.chambre.choices = [(c.id, c.name) for c in Chambres.query.all()]

    hospitalisation = Hospitalisation.query.get_or_404(id_hospitalisation)

    if request.method == 'POST' and form.validate():
        hospitalisation.patient_id = form.patient.data
        hospitalisation.medecin_id = form.medecin.data
        hospitalisation.chambre_id = form.chambre.data
        hospitalisation.date_entree = form.date_entree.data
        hospitalisation.date_sortie = form.date_sortie.data if form.date_sortie.data else None
        hospitalisation.motif = form.motif.data

        db.session.commit()
        flash("Hospitalisation mise à jour avec succès.", "success")
        return redirect(url_for('home_blueprint.hospitalisation'))

    return render_template('pages/hospitalisation.html', form=form, hospitalisation=hospitalisation)


@blueprint.route('/hospitalisation/show/<int:id_hospitalisation>', methods=['GET'])
@login_required
def show_hospitalisation(id_hospitalisation):
    hospitalisation = Hospitalisation.query.get_or_404(id_hospitalisation)
    return render_template('pages/hospitalisation.html', hospitalisation=hospitalisation)


@blueprint.route('/consultation', methods=['GET', 'POST'])
@login_required
def consultation():
    form = ConsultationForm()

    form.patient.choices = [(p.id_patient, f"{p.nom} {p.prenom}") for p in Patients.query.all()]
    form.medecin.choices = [(m.id_medecin, f"{m.nom} {m.prenom}") for m in Medecin.query.all()]

    if request.method == 'POST' and form.validate():
        new_consultation = Consultation(
            patient_id=form.patient.data,
            medecin_id=form.medecin.data,
            date_consultation=form.date_consultation.data,
            observations=form.observations.data,
            ordonnance=form.ordonnance.data
        )
        db.session.add(new_consultation)
        db.session.commit()
        flash("Consultation enregistrée avec succès.", "success")
        return redirect(url_for('home_blueprint.consultation'))

    # Récupération de la liste des consultations
    consultations_list = Consultation.query.all()
    return render_template('pages/consultation.html', form=form, consultations=consultations_list)


@blueprint.route('/consultation/delete/<int:id_consultation>', methods=['POST'])
def delete_consultation(id_consultation):
    consultation = Consultation.query.get_or_404(id_consultation)
    db.session.delete(consultation)
    db.session.commit()
    flash("Consultation supprimée avec succès.", "success")
    return redirect(url_for('home_blueprint.consultation'))


@blueprint.route('/rendez-vous')
@login_required
def visit():
    return render_template('pages/visit.html')


@blueprint.route('/messages')
@login_required
def messages():
    return render_template('pages/messages.html')


@blueprint.route('/medecins', methods=['GET', 'POST'])
@login_required
def medecin():
    form = MedecinForm()
    form.specialite.choices = [(s.id, s.name) for s in Speciality.query.all()]

    if request.method == 'POST' and form.validate():
        # Gestion de l'image
        if form.image.data:
            # Création du répertoire 'uploads' si nécessaire
            upload_folder = os.path.join('apps\static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(upload_folder, filename)
            form.image.data.save(filepath)
            image_url = f"/{filepath}"  # URL pour afficher l'image
        else:
            image_url = None  # Aucune image fournie

        # Création du médecin
        new_medecin = Medecin(
            nom=form.nom.data,
            prenom=form.prenom.data,
            specialite_id=form.specialite.data,
            telephone=form.telephone.data,
            email=form.email.data,
            image=image_url  # Stocke l'URL dans la BD
        )
        db.session.add(new_medecin)
        db.session.commit()
        flash("Médecin enregistré avec succès.", "success")
        return redirect(url_for('home_blueprint.medecin'))

    medecins_list = Medecin.query.all()
    return render_template('pages/medecin.html', form=form, medecins=medecins_list)


@blueprint.route('/medecins/delete/<int:id_medecin>', methods=['POST'])
def delete_medecin(id_medecin):
    medecin = Medecin.query.get_or_404(id_medecin)
    db.session.delete(medecin)
    db.session.commit()
    flash("Médecin supprimé avec succès.", "success")
    return redirect(url_for('home_blueprint.medecin'))


@blueprint.route('/infirmière', methods=['GET', 'POST'])
@login_required
def infirmiere():
    form = InfirmiereForm()

    form.specialite.choices = [(s.id, s.name) for s in Speciality.query.all()]
    if request.method == 'POST' and form.validate():
        # Gestion de l'image
        if form.image.data:
            # Création du répertoire 'uploads' si nécessaire
            upload_folder = os.path.join('apps\static', 'uploads')
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)

            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(upload_folder, filename)
            form.image.data.save(filepath)
            image_url = f"/{filepath}"
        else:
            image_url = None
        # Création de l'infirmière
        new_infirmiere = Infirmiere(
            nom=form.nom.data,
            prenom=form.prenom.data,
            telephone=form.telephone.data,
            email=form.email.data,
            image=image_url,
            specialite_id=form.specialite.data
        )
        db.session.add(new_infirmiere)
        db.session.commit()
        flash("Infirmière enregistrée avec succès.", "success")
        return redirect(url_for('home_blueprint.infirmiere'))

    infirmieres_list = Infirmiere.query.all()
    return render_template('pages/infirmiere.html', form=form, infirmieres=infirmieres_list)


@blueprint.route('/infirmière/delete/<int:id_infirmiere>', methods=['POST'])
def delete_infirmiere(id_infirmiere):
    infirmiere = Infirmiere.query.get_or_404(id_infirmiere)
    db.session.delete(infirmiere)
    db.session.commit()
    flash("Infirmière supprimée avec succès.", "success")
    return redirect(url_for('home_blueprint.infirmiere'))


def generate_patient_code(nom, prenom, date_naissance):
    """ Génère un code unique basé sur les premières lettres du nom et prénom + date de naissance """
    return f"{nom[:2].upper()}{prenom[:2].upper()}{date_naissance.strftime('%d%m%Y')}"


@blueprint.route('/patients', methods=['GET', 'POST'])
@login_required
def patients():
    form = PatientForm()

    if request.method == 'POST' and form.validate():
        # Générer automatiquement le code patient
        code_patient = generate_patient_code(form.nom.data, form.prenom.data, form.date_naissance.data)

        new_patient = Patients(
            code_patient=code_patient,
            nom=form.nom.data,
            prenom=form.prenom.data,
            date_naissance=form.date_naissance.data,
            sexe=form.sexe.data,
            adresse=form.adresse.data,
            telephone=form.telephone.data,
            email=form.email.data,
            groupe_sanguin=form.groupe_sanguin.data,
            historique_medical=form.historique_medical.data
        )

        db.session.add(new_patient)
        db.session.commit()
        flash(f"Patient enregistré avec succès. Code: {code_patient}", "success")
        return redirect(url_for('home_blueprint.patients'))

    patients_list = Patients.query.all()
    return render_template('pages/patients.html', form=form, patients=patients_list)


@blueprint.route('/patients/delete/<int:id_patient>', methods=['POST'])
def delete_patient(id_patient):
    patient = Patients.query.get_or_404(id_patient)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient supprimé avec succès.", "success")
    return redirect(url_for('home_blueprint.patients'))


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
