# Matthew Menten
# Eli Jacobshagen
# CSCI 5/4448 - OOAD - Montgomery
# Fall 2019
# Semester Project - Facial Recognition w. Raspberry Pi


from twilio.rest import Client


class AlertObserver:
	"""
	AlertObserver class

	INPUTS:  None
	OUTPUTS: None

	Notes: Used by the AppEngine to send SMS messages to current observers.
	"""

	# SOURCE/CREDIT: https://www.twilio.com/docs/sms/quickstart/python
	def __init__(self):
		"""Initialize the AlertObserver

		Input:  None
		Output: Creates an instance of the AlertObserver.
		"""

		# Twilio API keys
		self.account_sid = 'AC277acee6c034434de95b728161ac91e4'
		self.auth_token = 'e04eab2b310c8bbc1f921ccd61ef9847'
		
		# Init Twilio REST client
		self.client = Client(self.account_sid, self.auth_token)
		
		# Init list of observer numbers
		self.observers = list()

	def addObserver(self, observer_number):
		"""
		AlertObserver - addObserver
		:param observer_number: str - phone number to add
		:return:

		NOTES: add a new phone number to the list of observers
		"""

		# make sure observer number is not empty
		if observer_number:
			# make sure it's not a duplicate
			if observer_number not in self.observers:	
				self.observers.append(observer_number)
			else:
				print("Number already registered!")
		else:
			print("Could not add number to the list of observers")

	def alertObserver(self, observer_number):
		"""
		AlertObserver - alertObserver
		:param observer_number: str - number to send the SMS to
		:return:

		NOTES: send an SMS to the given phone number
		"""

		# create the new SMS message and send it to the specified number
		self.client.messages.create(
								body="An unknown face has been detected at your home!",
                     			from_='+13342922914',
                     			to=observer_number
								)

	def alertObservers(self):
		"""
		AlertObserver - alertObservers
		:return:

		NOTES: send an SMS to each registered observer
		"""

		# make sure there are registered observers
		if len(self.observers) >= 1:

			# loop over observers and alert each one
			for observer_number in self.observers:
				self.alertObserver(observer_number)
				#print("PRETENDING TO SEND SMS TO {}".format(observer_number))
		else:
			print("There are currently no observers to alert")