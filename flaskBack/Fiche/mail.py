"""
Fichier écrit pour l'envoi de mail
"""
#-*- coding: utf-8 -*-
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
#from getpass import getpass
import time
import datetime as datetime
import pythonconfig


class Mail :
    """ Classe pour envoyer des mails"""

    date=datetime.date.today()

    def __init__(self, infos_perso):
        self.infos_perso = infos_perso

    def sendmail(self, f, voyage):
        """
            Fonction pour envoyer le mail
        """

        print('Envoi du mail...')
        mail_port = 587
        msg = MIMEMultipart()
        #Envoi a tous les destinataires concernés : le demandeur, les voyageurs et l'expéditeur en copie
        to = []
        mail_demandeur = self.infos_perso.get('mail')
        to.append(mail_demandeur)
        voyageur = voyage.get('voyageurs')
        i=0
        while i < len(voyageur):
            voyageur_i = voyageur[i]
            mail_i = voyageur_i.get('mail')
            if mail_i == self.infos_perso.get('mail'):
                print('Email déjà dans les destinataires')
            else :
                to.append(mail_i)
            i +=1
        msg['To']=",".join(to)
        msg['From'] = pythonconfig.adressfrom
        msg['cc']=",".join(pythonconfig.cc)
        listDes = to + pythonconfig.cc
        msg['Subject'] = 'Réservation Voyage - Fiche n°' + str(f.numbertrain)
        date_today = str(self.date.day) + '/' + str(self.date.month) + '/'+ str(self.date.year)
        body = 'Ceci est votre fiche voyage pour votre réservation du '+ str(date_today) + '. \n Bon voyage ! \n \n Albert le robot. \n'
        msg.attach(MIMEText(body, 'plain'))

        #Pour le chemin de la pièce jointe
        cwd = os.getcwd()

        #Piece jointe train : envoyer uniquement dans le cas où on a créé une fiche train.
        if 'aller' in voyage.keys() or 'retour' in voyage.keys():
            filename_train = "fichetrain"+self.infos_perso.get('nom')+self.infos_perso.get('prenom')+str(f.numbertrain)+".pdf"
            path_fichetrain = cwd + '/Fiche/stockagefiche/train/'+ filename_train
            attachment = open(path_fichetrain, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename_train)
            msg.attach(part)

        #Piece jointe hotel : envoyer uniquement dans le cas où on a créé une fiche hôtel.
        if 'hotel' in voyage.keys():
            filename_hotel = "fichehotel"+self.infos_perso.get('nom')+self.infos_perso.get('prenom')+str(f.numberhotel)+".pdf"
            path_fichehotel = cwd + '/Fiche/stockagefiche/hotel/'+ filename_hotel
            attachment = open(path_fichehotel, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename_hotel)
            msg.attach(part)

        #Envoi du mail.
        mailserver = smtplib.SMTP('smtp.gmail.com', 587)
        mailserver.ehlo()
        mailserver.starttls()
        mailserver.ehlo()
        mailserver.login(pythonconfig.adressfrom, pythonconfig.mot_de_passe)
        mailserver.sendmail(pythonconfig.adressfrom,listDes, msg.as_string())
        mailserver.quit()
        #Suppression des fiches qui étaient stockées jusqu'ici (si elles existent)
        if 'aller' in voyage.keys() or 'retour' in voyage.keys():
            os.remove(path_fichetrain)
        if 'hotel' in voyage.keys():
            os.remove(path_fichehotel)
