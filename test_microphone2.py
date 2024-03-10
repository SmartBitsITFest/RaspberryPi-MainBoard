import speech_recognition as sr

r = sr.Recognizer()

speech = sr.Microphone()

#print(sr.Microphone.list_microphone_names())

with speech as source:
    print("say something!…")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source,10,3)
    print("the audio has been recorded")
    print("api is enabled")
    try:
        recog = r.recognize_sphinx(audio, language = 'en-US')
        print("You said: " + recog)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
