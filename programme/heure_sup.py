#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import createPDF
import os

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('--semaine', nargs='?', help='Numéro de semaine')

args = parser.parse_args()
entree = str(args.semaine)

if entree.isdigit():
    createPDF.makePDF(int(entree))
