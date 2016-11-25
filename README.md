# overtime

Python script (Python 2.7) to fill out an hour extra form in PDF

This program works with a CRON file 'programme/makeLog.py' which write in a directory 'fichiers' your logs hours of the week.
The script heure_sup.py in command line 'programme/heure_sup.py --semaine 47' read your logs for the week 47 and create a completed PDF.


0 - INSTALL

sudo pip install reportlab

sudo pip install PyPDF2

1 - CONFIG

The config file for your PDF information 'config/config.txt'

2 - CRON

The CRON file to be executed every 'x' minutes (5 for me)
programme/makeLog.py

3 - COMMAND LINE GENERATION FOR PDF

'programme/heure_sup.py --semaine [number of the week]'


