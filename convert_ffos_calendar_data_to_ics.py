#!/usr/bin/python

from json import loads
from time import strftime, gmtime
from datetime import datetime, time
from ast import literal_eval

json_file = open("events.txt")
ics_file = open("import.ics", "w")

ics_file.write("BEGIN:VCALENDAR\n")
ics_file.write("PRODID:-//digitalimagecorp.de//Firefox OS calendar converter//EN\n")
ics_file.write("VERSION:2.0\n")

def escape(s):
	s = repr(s)
	s = s.replace("\\", "\\\\")
	s = s.replace("\\\\x", "\\x")
	s = s.replace(";", "\\;")
	s = s.replace(",", "\\,")
	s = s.replace("\n", "\\n")
	return s.decode("string_escape")[2:-1]

for line in json_file:
	# Only convert Offline Calendar data
	if not line.startswith("local-"):
		continue
	# Remove IndexedDB key to get the plain JSON data
	line = line.split(":", 1)[1]

	cal_entry = loads(line)
	ics_file.write("BEGIN:VEVENT\n")
	ics_file.write("DTSTAMP:" + strftime("%Y%m%dT%H%M%SZ", gmtime()) + "\n")
	ics_file.write("UID:" + cal_entry["remote"]["id"] + "\n")
	ics_file.write("SUMMARY:" + escape(cal_entry["remote"]["title"]) + "\n")
	if cal_entry["remote"]["location"]:
		ics_file.write("LOCATION:" + escape(cal_entry["remote"]["location"]) + "\n")
	if cal_entry["remote"]["description"]:
		ics_file.write("DESCRIPTION:" + escape(cal_entry["remote"]["description"]) + "\n")

	start = datetime.utcfromtimestamp(cal_entry["remote"]["start"]["utc"] / 1000)
	end = datetime.utcfromtimestamp(cal_entry["remote"]["end"]["utc"] / 1000)
	# All day events can be either saved with the corresponding attribute "isDate"(FFOS 1.1)
	# or just span the whole day (FFOS 1.3)
	if "isDate" in cal_entry["remote"]["start"] or (start.time() == end.time() == time(0)):
		ics_file.write("DTSTART;VALUE=DATE:" + start.strftime("%Y%m%d") + "\n")
		ics_file.write("DTEND;VALUE=DATE:" + end.strftime("%Y%m%d") + "\n")
	else:
		ics_file.write("DTSTART:" + start.strftime("%Y%m%dT%H%M%S") + "\n")
		ics_file.write("DTEND:" + end.strftime("%Y%m%dT%H%M%S") + "\n")

	ics_file.write("TRANSP:OPAQUE\n")
	for alarm in cal_entry["remote"]["alarms"]:
		ics_file.write("BEGIN:VALARM\n")
		ics_file.write("DESCRIPTION:\n")
		ics_file.write("ACTION:DISPLAY\n")
		if str(alarm["trigger"]).startswith("-"):
			alarm["trigger"] = "-PT" + str(alarm["trigger"])[1:] + "S"
		else:
			alarm["trigger"] = "PT" + str(alarm["trigger"]) + "S"
		ics_file.write("TRIGGER;VALUE=DURATION:" + alarm["trigger"] + "\n")
		ics_file.write("END:VALARM\n")
	ics_file.write("END:VEVENT\n")
ics_file.write("END:VCALENDAR\n")
