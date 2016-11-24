# -*- coding: utf-8 -*-
from PyPDF2 import PdfFileWriter, PdfFileReader
import StringIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
import datetime
import locale
import calendar
import subprocess
from datetime import timedelta
import os
import sys
import warnings
warnings.filterwarnings("ignore")

locale.setlocale(locale.LC_ALL, 'fr_FR')


lignes = {0:160, 1:192, 2:226, 3:258, 4:292, 'total':390, 'heures':420}
colonnes = {'arrivee':60, 'pause_debut':160, 'pause_fin':200, 'depart':350, 'duree':460}


data_pdf = {}

def read_config():
    name = os.path.dirname(sys.argv[0])+"/../config/config.txt"
    with open(name, "r") as myfile:
        for line in myfile:
            line_splited = line.split("---")
            data_pdf[line_splited[0]] = line_splited[1].replace("\n","")

def write_texte(c, x, y,texte):
    c.drawString(x, -y, str(texte))

def initialisation(can):
    from reportlab.lib.units import inch
    can.translate(inch,inch)
    can.setFont("Helvetica", 10)
    can.rotate(90)

def write_semaine(can,numero):
    d = "2016-W"+str(numero)
    r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    write_texte(can, -10, 115, r.strftime('%d/%m'))
    
    r = datetime.datetime.strptime(d + '-5', "%Y-W%W-%w")
    write_texte(can, -10, 130, r.strftime('%d/%m'))

def write_Etablissement(can, etablissement):
    write_texte(can, 60, 25, str(etablissement))

def write_mois(can, semaine):
    d = "2016-W"+str(semaine)
    r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    write_texte(can, 30, 60, str(calendar.month_name[int(r.month)]))

def write_annee(can, semaine):
    d = "2016-W"+str(semaine)
    r = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
    write_texte(can, 210, 60, str(r.year))

def write_identification(can, identification):
    write_texte(can, 450, 25, str(identification))

def write_emploi(can, emploi):
    write_texte(can, 350, 45, str(emploi))

def days_hours_minutes(td):
    return (td.days, td.seconds//3600, (td.seconds//60)%60)

def makePDF(semaine):
    packet = StringIO.StringIO()
    can = canvas.Canvas(packet, pagesize=landscape(letter))
    initialisation(can)

    read_config()

    write_Etablissement(can,data_pdf['NOM_ORGANISME'])
    
    write_semaine(can,semaine)
    write_mois(can,semaine)
    write_annee(can,semaine)
    write_identification(can, data_pdf['IDENTIFICATION'])
    write_emploi(can, data_pdf['EMPLOI'])
    
    name = os.path.dirname(sys.argv[0])+"/../fichiers/semaine"+"_"+str(semaine)+".txt"
    with open(name, "r") as myfile:
        data = []
        for line in myfile:
            line_splited = line.split("---")

            minute_entree = int(line_splited[2])
            if minute_entree <10:
                minute_entree = "0"+str(minute_entree)
            else:
                minute_entree = str(minute_entree)
                
            write_texte(can, colonnes['arrivee'], lignes[int(line_splited[0])],line_splited[1]+":"+minute_entree)
            write_texte(can, colonnes['pause_debut'], lignes[int(line_splited[0])],"12:00")
            write_texte(can, colonnes['pause_fin'], lignes[int(line_splited[0])],"13:00")

            minute_sortie = int(line_splited[4].replace("\n",""))
            if minute_sortie <10:
                minute_sortie = "0"+str(minute_sortie)
            else:
                minute_sortie = str(minute_sortie)
            
            
            write_texte(can, colonnes['depart'], lignes[int(line_splited[0])],line_splited[3]+":"+minute_sortie)
            t1 = timedelta(hours=int(line_splited[1]), minutes=int(line_splited[2]))
            t2 = timedelta(hours=int(line_splited[3]), minutes=int(line_splited[4].replace("\n","")))
            t3 = timedelta(hours=1, minutes=0)
            
            heure = t2-t1-t3
            heure_delta = days_hours_minutes(heure)
            heure = heure_delta[1]

            minute_sortie = int(heure_delta[2])
            if minute_sortie <10:
                minute_sortie = "0"+str(minute_sortie)
            else:
                minute_sortie = str(minute_sortie)
                
            write_texte(can, colonnes['duree'], lignes[int(line_splited[0])],str(heure_delta[1])+":00")

            data.append(timedelta(hours=heure_delta[1], minutes=0))

        if(len(data) >0):
            temps_semaine = data[0]
            for i in range(len(data)-1):
                temps_semaine = temps_semaine + data[i+1]
            heure_delta = days_hours_minutes(temps_semaine)
            
            minute_sortie = int(heure_delta[2])
            if minute_sortie <10:
                minute_sortie = "0"+str(minute_sortie)
            else:
                minute_sortie = str(minute_sortie)
                
            write_texte(can, colonnes['duree'], lignes['total'],str(heure_delta[0]*24+heure_delta[1])+":"+minute_sortie)

            if heure_delta[0]*24+heure_delta[1]-35 >= 0:
                write_texte(can, colonnes['duree'], lignes['heures'],str(heure_delta[0]*24+heure_delta[1]-35))


    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    existing_pdf = PdfFileReader(file(os.path.dirname(sys.argv[0])+"/../config/"+data_pdf['NOM_FICHIER'], "rb"))
    output = PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = file(os.path.dirname(sys.argv[0])+"/../fichiers/semaine"+"_"+str(semaine)+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    subprocess.Popen("open "+os.path.dirname(sys.argv[0])+"/../fichiers/semaine"+"_"+str(semaine)+".pdf",shell=True)



