from os import access
import pyaudio
import speech_recognition as speech
import sounddevice as sd
import wavio
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
	
	ACCESS_CODE = sys.argv[1]
	client = Wit(ACCESS_CODE)
	response = None
	recognizer = speech.Recognizer()
	audio = None
	
	print('Options: ','\t1. Record audio file and send to wit',
		'\t2. Use google speech recognition and send send resulting string to wit', sep='\n', end='\n')
	
	user_input = input()

	if user_input == '1':
		print()
		frequency = 44100
		duration = 10
		
		audio_arr = sd.rec(int(duration*frequency), samplerate=frequency, channels=2)
		sd.wait()

		wavio.write('voice_recording.wav', audio_arr, frequency, sampwidth=2)

		with open('voice_recording.wav', 'rb') as file:
			response = client.speech(file, {'Content-Type': 'audio/wav'})
			print(str(response))
	elif user_input == '2':
		with speech.Microphone() as mic:
			print('\n----- Speak now -----\n')
			recognizer.adjust_for_ambient_noise(mic)
			audio = recognizer.listen(mic)

		google_understanding = recognizer.recognize_google(audio)
		response = client.message(google_understanding)

		print('Google heard, \'', google_understanding, '\'\n', sep='')
	else:
		print('Error: that wasn\'t one of the options')
		return

	

	user_input = input('Print raw data from wit? Enter \'Y\' for yes, anything else for no')

	if user_input == 'Y':
		print('\nWit\'s response: ', response,)

	print('\nIntent(s): ', get_intents(response))
	print('Entities(s): ', get_entities_values(response))
	# TODO add traits as well

if __name__ == '__main__':
	main()