#!/usr/bin/python

from json import loads
from time import strftime, gmtime
from datetime import datetime, time

json_file = open('sms.txt')
commtool = open('import.json', 'w')
isfirst = True

commtool.write('[\n')

def escape(s):
	s = repr(s)
	s = s.replace('\\', '\\\\')
	s = s.replace("\\\\x", "\\x")
	s = s.replace('\'', '\\\'')
	s = s.replace('\n', '\\n')
	return s.decode('string_escape')[2:-1]

for line in json_file:
	# Remove IndexedDB key to get the plain JSON data
	line = line.split(':', 1)[1]

	sms_entry = loads(line)
	if sms_entry['type'] == 'mms':
		continue

	if not isfirst:
		commtool.write('\t},\n')
	isfirst = False
	commtool.write('\t{\n')
	commtool.write('\t\t"type": "' + sms_entry['type'] + '",\n')

	if sms_entry['sender']:
		commtool.write('\t\t"to": "' + sms_entry['sender'] + '",\n')
		direction = 'in'
	if sms_entry['receiver']:
		commtool.write('\t\t"to": "' + sms_entry['receiver'] + '",\n')
		direction = 'out'

	commtool.write('\t\t"events": [\n')
	commtool.write('\t\t\t{\n')

	commtool.write('\t\t\t\t"direction": "' + direction + '",\n')
	commtool.write('\t\t\t\t"date": "' + datetime.utcfromtimestamp(sms_entry['timestamp'] / 1000).strftime('%Y-%m-%dT%H:%M:%S') + '",\n')
	if sms_entry['read'] == False:
		commtool.write('\t\t\t\t"unread": true,\n')
	commtool.write('\t\t\t\t"text": "' + escape(sms_entry['body']) + '"\n')

	commtool.write('\t\t\t}\n')
	commtool.write('\t\t]\n')

commtool.write('\t}\n')
commtool.write(']\n')
