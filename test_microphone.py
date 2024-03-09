import speech_recognition as sr
from speech_recognition.recognizers import google


recognizer = sr.Recognizer()


with sr.Microphone() as source:
	print('Listening...')
	
	recognizer.adjust_for_ambient_noise(source)
	
	audio = recognizer.listen(source)
	
	print('Processing...')
	
	
text = recognizer.recognize_google(audio)

print(f'You said {text}')
