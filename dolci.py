"""
dolci.py

Reads information from names.txt and submits it
to the next upcoming Dolci ticket sign up form
just after 9PM (when the form begins accepting
entries).

Created by Daniel Trauner on 2013-02-01.
Copyright (c) 2013 Daniel Trauner. All rights reserved.
"""

import mechanize as m
import datetime as d
import time as t
import random as r
from urllib2 import HTTPError

# global variables

successful = []

# helper methods
	
def get_all_students():
	'''
	Returns an array containing the names, emails and mailbox
	Numbers (in order) contained within the file 'names.txt'
	located in the same directory as this script.
	'''
	all_students = []
	column_header = ['name', 'email', 'mailbox_number']
	f = open("names.txt", "r")
	for line in f:
		student = []
		if '#' not in line:
			temp_list = line.split(',')
			for s in temp_list:
				student.append(s.strip())
			all_students.append(student)

	return all_students

def dolci_batch_submit(students):
	'''
	Fills out the Dolci signup form using the given array
	of students (each with a name, email, and box number)
	and returns an array containing an entry corresponding
	to the (successful) submission time of that student's
	information or False if the student's information was
	not successfully submitted.
	'''
	br = m.Browser()
	
	# search dolci page for current signup form url
	br.open("http://dolcimidd.blogspot.com/")
	current_dolci = br.find_link(text="Get tickets here!").url

	# open the current signup form
	br.open(current_dolci)

	# for each entry in students submit information
	global successful
	successful = [False]*len(students)
	for i, student in enumerate(students):
		br.form = list(br.forms())[0]
		br.form.controls[0].value = student[0]
		br.form.controls[1].value = student[1]
		br.form.controls[2].value = student[2]
		response = br.submit()

		if '24 hours' in response.read():
			successful[i] = str(d.datetime.now()-d.timedelta(seconds=1))[11:19]

		# handle error 301 (infinite redirect) by re-opening page
		try:
			# if not on last student, hit the back button to enter next student
			if student is not students[-1]:
				br.back()
		except HTTPError, e:
			print 'Handing error code ' +  str(e.code) + '...\n'
			br.open(current_dolci)

def next_weekday(current_date, weekday):
	'''
	Given a current_date, determines the date of the 
	next occurrence of weekday where the days of the 
	week are given as follows: 0=Monday, 1=Tuesday...
	Original source: http://bit.ly/1dTnMUj.
	'''
	return current_date + d.timedelta(weekday - current_date.weekday())

def wait_until_9pm_wednesday():
	'''
	When called, delays the script until 9PM on the
	next occurrence of Wednesday.
	'''
	# get current time
	now = d.datetime.now()

	# get date of next wednesday
	today = d.datetime.today()
	next_wednesday = next_weekday(today, 2)

	wednesday_9pm = now.replace(year=next_wednesday.year, month=next_wednesday.month, day=next_wednesday.day, hour=21, minute=0, second=0, microsecond=0)

	time_diff = wednesday_9pm - now

	while wednesday_9pm > now:
		now = d.datetime.now()
		time_diff = wednesday_9pm - now
		if wednesday_9pm > now:
			remaining = d.datetime(1,1,1) + time_diff if time_diff else d.datetime(0,0,0)
			print chr(27) + "[2J"
			print("%02d:%02d:%02d:%02d until the Dolci ticket sign up opens..." % (remaining.day - 1, remaining.hour, remaining.minute, remaining.second))
			t.sleep(0.001)

def main():
	# wait until 9PM on Wednesday
	wait_until_9pm_wednesday()

	print chr(27) + "[2J"

	print '\nExtracting student info from names.txt...\n'
	students = get_all_students()

	print 'Attempting to submit (after delay) starting at exactly ' + str(d.datetime.now())[11:] + '...\n'

	# insert a 3-4 second delay to look less robotic
	t.sleep(r.randint(3,4))

	# submit the students' info
	dolci_batch_submit(students)

	for i, student in enumerate(students):
		if successful[i]:
			print str(student[0]) + ' was submitted successfully at ' + str(successful[i]) + '!'
		else:
			print 'Oh no!  It looks like there was a problem submitting ' + str(student[0]) + '!'

	print

if __name__ == '__main__':
    main()