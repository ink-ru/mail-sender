#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
cron mail sender
'''

import sys, os, argparse, time, random
from email.mime.text import MIMEText
from email.header import Header

try:
	import smtplib
except ImportError:
	print("smtp module havn't been found. Use - pip3 install smtplib")

version = "1.0.0"

# /srv/social/sender.py -t test@test.ru -s 'Test mail'

def createParser (): # http://jenyay.net/Programming/Argparse
	parser = argparse.ArgumentParser(
				prog = sys.argv[0],
				description = '''cron mail sender''',
				epilog = '''george.a.wise@gmail.com'''
				)
	parser.add_argument ('-t', '-to',   required=True, default='test@test.ru', help = 'Адрес получателя')
	parser.add_argument ('-f', '-from', required=False, default='test@test.ru', help = 'Адрес отправителя')
	parser.add_argument ('-c', '-copy', required=False, default='test@test.ru', help = 'Копия письма')
	parser.add_argument ('-s', '-subj', required=True, help = 'Тема письма')
	parser.add_argument ('-b', '-body', required=False, default=' ', help = 'Текст письма')
	parser.add_argument ('-r', '-random', action='store_true', default=False, help = 'Случайная пауза перед отправкой')
 
	return parser

def main():
	parser = createParser()
	namespace = parser.parse_args()
	
	if namespace.r:
		random.seed( random.randint(1,512) )
		r_val = int(random.randrange(1, 512)) + random.randint(1,512)
		#print('sleep for ' + str(r_val))
		time.sleep(r_val)

	receiver = str(namespace.t) # sys.argv[1]
	sender = str(namespace.f) # sys.argv[2]
	cc = str(namespace.f) # sys.argv[3]
	subject = str(namespace.s) # sys.argv[4]
	message = MIMEText(str(namespace.b), 'html', 'utf-8')
	
	password = ''
	
	message['From'] = sender
	message['To'] = receiver
	message['Cc'] = cc

	message['Subject'] = Header(subject, 'utf-8')
	receiver = [receiver] + [cc]

	try:
		smtpObj = smtplib.SMTP("smtp.mastermail.ru", 25)
		smtpObj.starttls()
		smtpObj.login(sender, password)
		smtpObj.sendmail(sender, receiver, message.as_string())
		smtpObj.close()
	except smtplib.SMTPException as e:
		print(str(e))
		sys.exit(os.EX_UNAVAILABLE)

	sys.exit(os.EX_OK) # code 0, all ok

def local():

	#with open(textfile) as fp:
	#    msg = MIMEText(fp.read())
	msg = MIMEText('cron msg')

	msg['Subject'] = 'Test'
	msg['From'] = 'test@test.ru'
	msg['To'] = 'test@test.ru'

	# Send the message via our own SMTP server.
	try:
		s = smtplib.SMTP('localhost')
		s.send_message(msg)
		s.quit()
	except smtplib.SMTPException as e:
		print(str(e))
		sys.exit(os.EX_UNAVAILABLE)

	sys.exit(os.EX_OK) # code 0, all ok

if __name__ == '__main__':
	main()
else:
	sys.exit(os.EX_USAGE) # https://docs.python.org/2/library/os.html
