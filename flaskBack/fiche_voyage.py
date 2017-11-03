import os
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.units import inch
from Fiche.mail import Mail
from random import randint
import datetime

LogoTrain='./Data/Img/train.png'
LogoHotel='./Data/Img/hotel.png'
logoMNT = "./Data/Img/MNT_logo.png"

class FicheVoyage :
    """Classe définissant la fiche voyage caractérisée par :
        - Les caracéristiques utilisateurs
        - Les infos Voyage
        - L'hôtel
    """

    date = datetime.datetime.now()

    def __init__(self, infos_perso : dict):
        self.infos_perso = infos_perso
        self.mail = Mail(self.infos_perso)
        self.voyage = {}
        self.complement = {}
        self.numbertrain = randint(0, 500000)
        self.numberhotel = randint(0, 500000)

    def add_item_to_voyage(self, key : str, item : dict):
        self.voyage[key] = item

    def add_voyage(self, voyage : dict, complement : dict):
        self.voyage = voyage
        self.complement = complement

    def createFiche_Train(self):
        """
            Fonction qui créé une fiche liée uniquement à la réservation d'un train.
            Dans l'ordre sur la fiche :
            - le demandeur (avec la date de la demande) et le 1er voyageur (saut de page).
            - la liste des voyageurs (saut de page a chaque voyageur ajouté).
            - les détails de la réservation et les compléments (dont le lien avec fiche hôtel ou non).
            Les informations viennent de différents dictionnaires : infos_perso (ConvNameInfo)pour le demandeur, voyage pour les voyageurs (ConvVoyage),
            voyage (et a l'intérieur les dictionnaires aller et retour) pour les détails de réservation de train (ConvVoyage), complement pour motif et commentaires (ConvVoyage).
            La fonction parcout tous ses dictionnaires.
            Utilisation du module python reportlab pour la création de fichier.
            Le fichier est créé et stocké dans le dossier stockagefiche. La fonction sendmail permet ensuite de détruire ce fichier.
        """

        outfilename ='fichetrain'+self.infos_perso.get('nom')+self.infos_perso.get('prenom')+str(self.numbertrain)+'.pdf'
        outfiledir = './Fiche/stockagefiche/train'
        outfilepath = os.path.join(outfiledir, outfilename )
        doc = SimpleDocTemplate(outfilepath,pagesize=A4,
                            rightMargin=60,leftMargin=50,
                            topMargin=50,bottomMargin=25)

        Story=[]
        styles=getSampleStyleSheet()

        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName="Times-Roman"))
        texte = '<font size=34><strong>Fiche Voyage n°' + str(self.numbertrain)+ '</strong></font>'
        Story.append(Paragraph(texte, styles["Justify"]))
        Story.append(Spacer(1, 32))
        texte = 'Catégorie : Billeterie et Réservation'
        texte2 = '<font size=14>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,10))
        if 'hotel' in self.voyage.keys() :
            texte = "Information complémentaire : Lien avec la fiche hotel n° " + str.capitalize(str(self.numberhotel))
            texte2 = "<font size=14>"+texte+"</font>"
            Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,30))
        im = Image(logoMNT, 2*inch, 2*inch)
        Story.append(im)
        Story.append(Spacer(1, 16))
        texte = '<font size=14><strong>Catégorie : Information Demandeur</strong></font>'
        Story.append(Paragraph(texte,styles["Justify"]))
        Story.append(Spacer(1, 10))
        texte = 'Nom : ' + str.capitalize(self.infos_perso.get('nom'))
        texte2 = '<font size=11>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        texte = 'Prénom : ' + str.capitalize(self.infos_perso.get('prenom'))
        texte2 = '<font size=11>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        texte = 'E-mail : ' + self.infos_perso.get('mail')
        texte2 = '<font size=11>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        date_today = str(self.date.day) + '/' + str(self.date.month) + '/'+ str(self.date.year)
        texte = 'Date de la demande : ' + str(date_today)
        texte2 = '<font size=11>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,10))
        if 'voyageurs' in self.voyage.keys():
            texte = '<font size=14><strong>Catégorie : Information Voyageur(s) </strong></font>'
            Story.append(Paragraph(texte,styles["Justify"]))
            Story.append(Spacer(1, 10))
            voyageur = self.voyage.get('voyageurs')
            i=0
            while i < len(voyageur):
                texte = '<font size=12><strong> Voyageur n°' + str(i+1)+'</strong></font>'
                Story.append(Paragraph(texte,styles["Justify"]))
                Story.append(Spacer(1, 10))
                voyageur_i = voyageur[i]
                if 'nom' in voyageur_i.keys() and 'prenom' in voyageur_i.keys() and 'mail' in voyageur_i.keys():
                    texte = "Nom : " + str.capitalize(voyageur_i.get('nom'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte =" Prénom : " + str.capitalize(voyageur_i.get('prenom'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = "E-Mail : " + voyageur_i.get('mail')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Numéro de téléphone : ' + voyageur_i.get('telephone')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Statut : ' + str.capitalize(voyageur_i.get('statut'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Lieu de travail : ' + str.capitalize(voyageur_i.get('lieu_de_travail'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Section ou service : ' + voyageur_i.get('section_service')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Date de naissance : ' + voyageur_i.get('date_de_naissance')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Grand Voyageur : ' + str.capitalize(voyageur_i.get('grand_voyageur'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Carte de réduction : ' + str.capitalize(voyageur_i.get('reductions'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    Story.append(Spacer(1, 10))
                    i +=1
                    Story.append(PageBreak())
                    Story.append(im)
                    Story.append(Spacer(1, 20))
        texte= '<font size=14><strong>Catégorie : Détails du voyage </strong></font>'
        Story.append(Paragraph(texte,styles["Justify"]))
        Story.append(Spacer(1, 10))
        if 'aller' in self.voyage.keys():
            texte = '<font size=11><strong> Catégorie : Aller </strong></font>'
            Story.append(Paragraph(texte, styles["Justify"]))
            Story.append(Spacer(1,7))
            aller = self.voyage.get('aller')
            if 'départ' in aller.keys() and 'arrivée' in aller.keys() and 'jour' in aller.keys():
                texte = "Départ : " + str.capitalize(aller.get('départ'))
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
                texte =" Arrivée : " + str.capitalize(aller.get('arrivée'))
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
                texte = "Date : " + aller.get('jour')
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
                if 'heure' in aller.keys():
                    texte = "Horaires : "+ aller.get('heure')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
            Story.append(Spacer(1,10))
        if 'retour' in self.voyage.keys():
            texte = '<font size=11><strong> Catégorie : Retour </strong></font>'
            Story.append(Paragraph(texte, styles["Justify"]))
            Story.append(Spacer(1,7))
            retour = self.voyage.get('retour')
            if 'départ' in retour.keys() and 'arrivée' in retour.keys() and 'jour' in retour.keys():
                texte = "Départ : " + str.capitalize(retour.get('départ'))
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
                texte =" Arrivée : " + str.capitalize(retour.get('arrivée'))
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
                texte = "Date : " + retour.get('jour')
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
                if 'heure' in retour.keys():
                    texte = "Horaires : "+ retour.get('heure')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
            Story.append(Spacer(1,10))
        Story.append(Spacer(1,10))
        texte= '<font size=14><strong>Catégorie : Complément </strong></font>'
        Story.append(Paragraph(texte, styles["Justify"]))
        Story.append(Spacer(1,7))
        motif = self.complement.get('motif')
        commentaires = self.complement.get('commentaires')
        texte = "Motif : " + str.capitalize(motif)
        texte2 = "<font size=11>"+texte+"</font>"
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        texte = "Commentaires : " + str.capitalize(commentaires)
        texte2 = "<font size=11>"+texte+"</font>"
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        if 'hotel' in self.voyage.keys() :
            texte = "Autre : Lien avec la fiche hotel n° " + str.capitalize(str(self.numberhotel))
            texte2 = "<font size=11>"+texte+"</font>"
            Story.append(Paragraph(texte2, styles["Justify"]))
        else :
            texte = "Autre : Pas de fiche hôtel liée."
            texte2 = "<font size=11>"+texte+"</font>"
            Story.append(Paragraph(texte2, styles["Justify"]))
        if 'retour' in self.voyage.keys() or 'aller' in self.voyage.keys():
            doc.build(Story, onFirstPage=self.addPageInfo, onLaterPages = self.addPageInfo)
        else :
            return None

    def createFiche_Hotel(self):
        """
            Fonction qui créé une fiche liée uniquement à la réservation d'un hotel.
            (il a été explicitement demandé de distinguer les fiches.)
            Dans l'ordre sur la fiche :
            - le demandeur (avec la date de la demande) et le 1er voyageur (saut de page).
            - la liste des voyageurs (saut de page a chaque voyageur ajouté).
            - les détails de la réservation et les compléments (dont le lien avec fiche hôtel ou non).
            Les informations viennent de différents dictionnaires : infos_perso (ConvNameInfo)pour le demandeur, voyage pour les voyageurs (ConvVoyage),
            voyage (et à l'intérieur le dictionnaire hotel) pour les détails de l'hotel (ConvVoyage), complement pour motif et commentaires (ConvVoyage).
            La fonction parcout tous ses dictionnaires.
            Utilisation du module python reportlab pour la création de fichier.
            Le fichier est créé et stocké dans le dossier stockagefiche. La fonction sendmail permet ensuite de détruire ce fichier.
        """

        outfilename ='fichehotel'+self.infos_perso.get('nom')+self.infos_perso.get('prenom')+str(self.numberhotel)+'.pdf'
        outfiledir = './Fiche/stockagefiche/hotel'
        outfilepath = os.path.join(outfiledir, outfilename )
        doc = SimpleDocTemplate(outfilepath,pagesize=A4,
                            rightMargin=60,leftMargin=50,
                            topMargin=50,bottomMargin=25)

        Story=[]
        styles=getSampleStyleSheet()

        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, fontName="Times-Roman"))
        texte = '<font size=34><strong>Fiche Hotel n°' + str(self.numberhotel)+ '</strong></font>'
        Story.append(Paragraph(texte, styles["Justify"]))
        Story.append(Spacer(1, 32))
        texte = 'Catégorie : Billeterie et Réservation'
        texte2 = '<font size=14>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,10))
        if 'hotel' in self.voyage.keys() :
            texte = "Information complémentaire : Lien avec la fiche train n° " + str.capitalize(str(self.numbertrain))
            texte2 = "<font size=14>"+texte+"</font>"
            Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,30))
        im = Image(logoMNT, 2*inch, 2*inch)
        Story.append(im)
        Story.append(Spacer(1, 16))
        texte = '<font size=14><strong>Catégorie : Information Demandeur</strong></font>'
        Story.append(Paragraph(texte,styles["Justify"]))
        Story.append(Spacer(1, 10))
        texte = 'Nom : ' + str.capitalize(self.infos_perso.get('nom'))
        texte2 = '<font size=11>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        texte = 'Prénom : ' + str.capitalize(self.infos_perso.get('prenom'))
        texte2 = '<font size=11>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        texte = 'E-mail : ' + self.infos_perso.get('mail')
        texte2 = '<font size=11>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        date_today = str(self.date.day) + '/' + str(self.date.month) + '/'+ str(self.date.year)
        texte = 'Date de la demande :' + str(date_today)
        texte2 = '<font size=11>'+ texte +'</font>'
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,10))
        if 'voyageurs' in self.voyage.keys():
            texte = '<font size=14><strong>Catégorie : Information Voyageur(s) </strong></font>'
            Story.append(Paragraph(texte,styles["Justify"]))
            Story.append(Spacer(1, 10))
            voyageur = self.voyage.get('voyageurs')
            i=0
            while i < len(voyageur):
                texte = '<font size=12><strong> Voyageur n°' + str(i+1)+'</strong></font>'
                Story.append(Paragraph(texte,styles["Justify"]))
                Story.append(Spacer(1, 10))
                voyageur_i = voyageur[i]
                if 'nom' in voyageur_i.keys() and 'prenom' in voyageur_i.keys() and 'mail' in voyageur_i.keys():
                    texte = "Nom : " + str.capitalize(voyageur_i.get('nom'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte =" Prénom : " + str.capitalize(voyageur_i.get('prenom'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = "E-Mail : " + voyageur_i.get('mail')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Numéro de téléphone : ' + voyageur_i.get('telephone')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Statut : ' + str.capitalize(voyageur_i.get('statut'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Lieu de travail : ' + str.capitalize(voyageur_i.get('lieu_de_travail'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Section ou service : ' + voyageur_i.get('section_service')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Date de naissance : ' + voyageur_i.get('date_de_naissance')
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Grand Voyageur : ' + str.capitalize(voyageur_i.get('grand_voyageur'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    texte = 'Carte de réduction : ' + str.capitalize(voyageur_i.get('reductions'))
                    texte2 = "<font size=11>"+texte+"</font>"
                    Story.append(Paragraph(texte2, styles["Justify"]))
                    Story.append(Spacer(1,4))
                    Story.append(Spacer(1, 10))
                    i +=1
                    Story.append(PageBreak())
                    Story.append(im)
                    Story.append(Spacer(1, 20))
        texte= '<font size=14><strong>Catégorie : Détails Hotel </strong></font>'
        Story.append(Paragraph(texte, styles["Justify"]))
        Story.append(Spacer(1,7))
        if 'hotel' in self.voyage.keys():
            hotel = self.voyage.get('hotel')
            if 'ville' in hotel.keys() and 'date_arrivee' in hotel.keys() and 'date_depart' in hotel.keys():
                texte = "Lieu : " + str.capitalize(hotel.get('ville'))
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
                texte =" Date d'arrivée : " + hotel.get('date_arrivee')
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
                texte = "Date de départ : " + hotel.get('date_depart')
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
            if 'nights' in hotel.keys():
                texte = " Préférence Hotel : " + str.capitalize(hotel.get('nights'))
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
            if 'hotel_wanted' in hotel.keys():
                texte = " Préférence Hotel : " + str.capitalize(hotel.get('hotel_wanted'))
                texte2 = "<font size=11>"+texte+"</font>"
                Story.append(Paragraph(texte2, styles["Justify"]))
                Story.append(Spacer(1,4))
        Story.append(Spacer(1,10))
        texte= '<font size=14><strong>Catégorie : Complément </strong></font>'
        Story.append(Paragraph(texte, styles["Justify"]))
        Story.append(Spacer(1,7))
        motif = self.complement.get('motif')
        commentaires = self.complement.get('commentaires')
        texte = "Motif : " + str.capitalize(motif)
        texte2 = "<font size=11>"+texte+"</font>"
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        texte = "Commentaires : " + str.capitalize(commentaires)
        texte2 = "<font size=11>"+texte+"</font>"
        Story.append(Paragraph(texte2, styles["Justify"]))
        Story.append(Spacer(1,4))
        if 'aller' in self.voyage.keys() or 'retour' in self.voyage.keys() :
            texte = "Autre : Lien avec la fiche train n° " + str.capitalize(str(self.numbertrain))
            texte2 = "<font size=11>"+texte+"</font>"
            Story.append(Paragraph(texte2, styles["Justify"]))
        else :
            texte = "Autre : Pas de fiche train liée. "
            texte2 = "<font size=11>"+texte+"</font>"
            Story.append(Paragraph(texte2, styles["Justify"]))
        if 'hotel' in self.voyage.keys():
            doc.build(Story, onFirstPage=self.addPageInfo, onLaterPages = self.addPageInfo)
        else :
            return None

    def sendFiche(self, voyage):
        self.mail.sendmail(self, voyage)

    def addPageInfo(self, canvas, doc):
        """
            Fonction qui permet d'ajouter des infos en bas de page sur le pdf.
            Ajoute le logo de la MNT, le numéro de page, et un logo de train ou d'hotel.
        """
        page_num = canvas.getPageNumber()
        text = 'Page %s'% page_num
        canvas.drawRightString(180*mm, 10*mm, text)
        if 'aller' in self.voyage.keys() or 'retour' in self.voyage.keys():
            text = "Fiche Voyage - MNT"
            canvas.drawRightString(180*mm, 14*mm, text)
            canvas.drawImage(LogoTrain,25,13,width=65,height=55,mask='auto')
        if 'hotel' in self.voyage.keys():
            text = "Fiche Hotel - MNT"
            canvas.drawRightString(180*mm, 14*mm, text)
            canvas.drawImage(LogoHotel,25,13,width=65,height=55,mask='auto')
        canvas.setStrokeColorCMYK(0.68,0.44,0,0.41)
        canvas.setLineWidth(3)
        canvas.line(20,80,570,80)
