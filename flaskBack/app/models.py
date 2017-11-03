"""
    Création d'une base de données SQLAlchemy.
    User : définit tous les utilisateurs.

    Fichier qui répertorie également différentes fonctions liées à la base de données.
"""

from app import database as db

class User(db.Model):
    """"
        Définition de la classe User qui comprend tous les champs nécessaires pour réserver un
        voyage à la MNT.
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    mail = db.Column(db.String(200), unique = True)
    telephone = db.Column(db.String(100))
    statut = db.Column(db.String(100))
    section_service = db.Column(db.String(100))
    lieu_de_travail = db.Column(db.String(50))
    date_de_naissance = db.Column(db.String(70))
    grand_voyageur = db.Column(db.String(70))
    reductions = db.Column(db.String(80))

    def __repr__(self):
      return '<User %r>' % (self.mail)

    def user_dict(self):
        """
            Fonction qui permet de lister les informations utilisateurs.
        """
        return {
                'nom' : self.nom,
                'prenom' : self.prenom,
                'mail' :self.mail,
                'telephone' : self.telephone,
                'statut' : self.statut,
                'lieu_de_travail' : self.lieu_de_travail,
                'section_service' : self.section_service,
                'date_de_naissance' : self.date_de_naissance,
                'grand_voyageur' : self.grand_voyageur,
                'reductions' : self.reductions
                }

    def save_to_bdd(self, infos):
        """
            Fonction qui permet d'ajouter un utilisateur dans la table User.
        """
        user_to_add= User(nom = infos.get('nom'),
            prenom = infos.get('prenom'),
            mail = infos.get('mail'),
            telephone = infos.get('telephone'),
            statut = infos.get('statut'),
            section_service = infos.get('section_service'),
            lieu_de_travail = infos.get('lieu_de_travail'),
            date_de_naissance = infos.get('date_de_naissance'),
            grand_voyageur = infos.get('grand_voyageur'),
            reductions = infos.get('reductions'))
        db.session.add(user_to_add)
        db.session.commit()
