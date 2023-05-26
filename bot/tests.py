# from django.test import TestCase

# # Create your tests here.
# # importing the module

# import speech_recognition as sr
# import pyttsx3
# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)
# engine.setProperty('rate', '50')

# keywords = {
#     'hai':'hello',
#     'buy':'sure, please wait, let me contact the seller'
# }

# recognizer = sr.Recognizer()
# while True:
#     try:
#         with sr.Microphone() as source:
#             print('listening...')
#             listner = recognizer.listen(source)
#             data = recognizer.recognize_google(listner)
#             print(data)
            
    
#             for k in keywords:
#                 for d in str(data).split(' '):
#                     if k == d :
#                         engine.say(keywords[k])
#                         engine.runAndWait()
#     except Exception as e:
#         print(e)
#         pass
            
        