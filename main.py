from os import access
import json
import pyaudio
import speech_recognition as speech
from wit import Wit
import sys


def get_intents(response):
	intents = []

	for intent in response['intents']:
		intents.append(intent['name'])
		
	return intents


def get_entities_values(response):
	entities_values = []

	for entity in response['entities']:
		for item in response['entities'][entity]:
			entities_values.append(item['value'])

	return entities_values


def main():

	if len(sys.argv) != 2:
		print('Error: you entered the wrong amount of sys args')
		exit(1)
	
	recognizer = speech.Recognizer()
	audio = None
	
	with speech.Microphone() as mic:
		print('Speak now')
		recognizer.adjust_for_ambient_noise(mic)
		audio = recognizer.listen(mic)

	ACCESS_CODE = sys.argv[1]
	client = Wit(ACCESS_CODE)
	google_understanding = recognizer.recognize_google(audio)
	response = client.message(google_understanding)

	print('Google heard: ', google_understanding, '\n')
	print('Wit\'s resopnse: ', response)
	print('Intent(s): ', get_intents(response))
	print('Entities(s): ', get_entities_values(response))


if __name__ == '__main__':
	main()