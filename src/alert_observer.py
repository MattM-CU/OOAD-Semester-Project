# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi

from twilio.rest import Client

class AlertObserver():


	def __init__(self):

		# Twilio API keys
		self.account_sid = 'AC277acee6c034434de95b728161ac91e4'
		self.auth_token = 'e04eab2b310c8bbc1f921ccd61ef9847'
		
		# Init Twilio REST client
		self.client = Client(self.account_sid, self.auth_token)
		
		# Init list of observer numbers
		self.observers = list()


	def addObserver(self, observer_number):
		if observer_number:
			self.observers.append(observer_number)
		else:
			print("Could not add number to the list of observers")


	def alertObserver(self, observer_number):
		self.client.messages.create(
								body="An unknown face has been detected at your home!",
                     			from_='+13342922914',
                     			to=observer_number
							)

	def alertObservers(self):
		if len(self.observers) >= 1:
			for observer_number in self.observers:
				#alertObserver(observer_number)
				print("PRETENDING TO SEND SMS TO {}".format(observer_number))
		else:
			print("There are currently no observers to alert")