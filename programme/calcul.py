#!/usr/bin/env python

import datetime
import collections
import os
import sys
import os.path
from datetime import timedelta


def days_hours_minutes(td):
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60


def write_day(semaine, dayweek, start_h, start_m, end_h, end_m):
    name = os.path.dirname(sys.argv[0]) + "/../fichiers/semaine" + "_" + str(semaine) + ".txt"
    print name
    with open(name, "a") as myfile:
        None

    with open(name, "r") as myfile:
        data = {}
        for line in myfile:
            line_splited = line.split("---")
            data[int(line_splited[0])] = line

        if dayweek in data:
            line_splited = data[dayweek].split("---")
            lanceur = os.path.dirname(sys.argv[0]) + "/.lanceur"
            start_to_write_h = line_splited[1]
            start_to_write_m = line_splited[2]

            if not os.path.isfile(lanceur):
                star_pause_h = int(line_splited[6])
                star_pause_m = int(line_splited[7])
                end_pause_h = int(line_splited[8])
                end_pause_m = int(line_splited[9])

                t1 = timedelta(hours=star_pause_h, minutes=star_pause_m)
                t2 = timedelta(hours=end_pause_h, minutes=end_pause_m)
                t3 = t2 - t1
                delta = days_hours_minutes(t3)
                pause = int(line_splited[5]) + abs(delta[0] * 24 * 60 + delta[1] * 60 + delta[2])
                data[int(dayweek)] = str(dayweek) + "---" + str(start_to_write_h) + "---" + str(
                    start_to_write_m) + "---" + str(end_h) + "---" + str(end_m) + "---" + str(
                    pause) + "---0---0---0---0\n"
            else:
                star_pause_h = int(line_splited[6])
                star_pause_m = int(line_splited[7])
                pause = int(line_splited[5])

                if star_pause_h == 0 and star_pause_m == 0:
                    star_pause_h = end_h
                    star_pause_m = end_m

                end_pause_h = end_h
                end_pause_m = end_m

                data[int(dayweek)] = str(dayweek) + "---" + str(start_to_write_h) + "---" + str(
                    start_to_write_m) + "---" + str(end_h) + "---" + str(end_m) + "---" + str(pause) + "---" + str(
                    star_pause_h) + "---" + str(star_pause_m) + "---" + str(end_pause_h) + "---" + str(
                    end_pause_m) + "\n"


        else:
            start_to_write_h = start_h
            start_to_write_m = start_m
            data[int(dayweek)] = str(dayweek) + "---" + str(start_to_write_h) + "---" + str(
                start_to_write_m) + "---" + str(end_h) + "---" + str(end_m) + "---0---0---0---0---0\n"

        od = collections.OrderedDict(sorted(data.items()))

    with open(name, "w") as myfile:
        for key, value in od.iteritems():
            myfile.write(value)
