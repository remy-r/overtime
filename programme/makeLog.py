#!/usr/bin/env python

import datetime
import calcul
import sys
import os

date_now = datetime.datetime.now()
ic = date_now.isocalendar()

calcul.write_day(ic[1], date_now.weekday(), date_now.hour, date_now.minute, date_now.hour, date_now.minute)

