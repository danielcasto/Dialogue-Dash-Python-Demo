import speech_recognition as speech
from wit import Wit
import sys

def main():
	recognizer = speech.Recognizer()
	audio = ''
	
	with speech.Microphone() as mic:
		print('Speak now')
		audio = recognizer.listen(mic)

	ACCESS_CODE = sys.argv[1]

	client = Wit(ACCESS_CODE)
	response = client.message(audio)
	print(str(response))

if __name__ == '__main__':
	main()