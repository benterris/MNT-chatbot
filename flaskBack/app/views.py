"""
    Script qui répertorie les fonctions du Back en Flask.
    Script lié au fichier hhtp_helper.py
"""

from flask import render_template, flash, redirect
import json
import Parser_general.parse as p
# from controller import Controller
from app import app
from app import database as db
from app.models import User
from flask import request

@app.route('/')
def hello():
    return 'Accueil ! '

# ATTENTION : quand on met un keyword qui peut contenir des '/',
# on met <path:...> devant comme pour msg ci-dessous
@app.route('/parser/<to_classify>/<path:msg>')
def parser(msg : str, to_classify : str) :
    """
        Route pour rediriger vers le parser.
    """
    return json.dumps(p.parse_message(msg, to_classify))

@app.route('/add_bdd', methods=['POST'])
def register_user():
    """
        Fonction qui utilise la fonction save_to_bdd pour ajouter un utilisateur.
        Permet de faire le lien entre base de données et Front.
    """
    if request.method == 'POST':
        data = request.get_json()
        a = User()
        a.save_to_bdd(data)
    return 'ok'

@app.route('/users/<path:user_id>')
def user_in_bdd(user_id : str):
    """
        Fonction qui permet de vérifier si un utilisateur est en base de données ou non.
        Utilisation d'une fonction SLQAlchemy : User.query.filter_by.
        Choix du mail comme identifiant unique.
    """
    user = User.query.filter_by(mail=user_id).first()
    if user == None :
        return json.dumps(False)
    else :
        return json.dumps(user.user_dict())

@app.route('/delete_bdd/<path:user_id>')
def delete_bdd_user(user_id: str):
    """
        Fonction qui permet de supprimer un utilisateur de la base de données.
        Utilisation de la fonction query.filter_by pour trouver l'utilisateur en questions dans la BDD et le supprimer.
    """
    user_in_bdd = User.query.filter_by(mail=user_id).first()
    if user_in_bdd == None :
        print("Error : user not found in database")
        return json.dumps(False)
    else :
        db.session.delete(user_in_bdd)
        db.session.commit()
        return 'ok'
