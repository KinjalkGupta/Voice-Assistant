from neuralintents import GenericAssistant  # pip install neuralintents
import speech_recognition  # pip install speechrecognition
import pyttsx3 as tts  # pip install pyttsx3
import sys


# Instantiating the Recognizer class
recognizer = speech_recognition.Recognizer()

speaker = tts.init()  # this method creates a new engine instance for the driver's name
# Setting the speech rate to 105 words per minute
speaker.setProperty("rate", 105)

todo_list = ["Go to shopping", "Clean room"]


def create_note():
    global recognizer

    speaker.say("What do you want to write onto your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again")
            speaker.runAndWait()

        else:
            with open(filename, "a") as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()


def add_todo():

    global recognizer

    speaker.say("What todo do you want to add?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:  # Creates a new Microphone instance

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand. Please try again")
            speaker.runAndWait()

        else:
            todo_list.append(item)
            done = True

            speaker.say(f'I added {item} to the todo list')
            speaker.runAndWait()


def show_todo():

    speaker.say("The items on your todo list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("Hello. What can I do for you? ")
    speaker.runAndWait()


def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit()


mappings = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todo": show_todo,
    "exit": quit
}


assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()

while True:
    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.5)
            audio = recognizer.listen(mic)

            message = recognizer.recognize_google(audio)
            message = message.lower()

        print(message)
        assistant.request(message)

    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
        print("retrying")
