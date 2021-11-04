from os import access
import pyaudio
import speech_recognition as speech
from wit import Wit
import sys

def main():
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

	print('Google heard: ', google_understanding)
	print('Wit\'s resopnse: ', str(response))

if __name__ == '__main__':
	main()