import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import pyjokes
import os
import webbrowser
from pycaw.pycaw import AudioUtilities

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# Speak function
def talk(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Voice command function
def take_command():
    listener = sr.Recognizer()

    try:
        with sr.Microphone() as source:

            print("Listening...")

            listener.adjust_for_ambient_noise(source, duration=1)

            voice = listener.listen(
                source,
                timeout=5,
                phrase_time_limit=5
            )

            command = listener.recognize_google(voice)

            command = command.lower()

            print("You said:", command)

            return command

    except sr.WaitTimeoutError:
        print("Listening timeout")
        return ""

    except sr.UnknownValueError:
        print("Could not understand audio")
        return ""

    except Exception as e:
        print("Error:", e)
        return ""

# Volume control function
def set_volume(level):

    try:
        devices = AudioUtilities.GetSpeakers()

        interface = devices.EndpointVolume

        volume = interface

        volume.SetMasterVolumeLevelScalar(level, None)

    except Exception as e:

        print("Volume control error:", e)

        talk("Unable to control volume")

# Main assistant function
def run_assistant():

    command = take_command()

    # Play song on YouTube
    if 'play' in command:

        song = command.replace('play', '')

        if song.strip() != "":

            talk('Playing ' + song)

            pywhatkit.playonyt(song)

        else:
            talk("Please tell the song name")

    # Tell time
    elif 'time' in command:

        current_time = datetime.datetime.now().strftime('%I:%M %p')

        talk('Current time is ' + current_time)

    # Wikipedia search
    elif 'who is' in command or 'what is' in command:

        person = command.replace('who is', '')
        person = person.replace('what is', '')

        try:

            info = wikipedia.summary(person, sentences=2)

            print(info)

            talk(info)

        except:

            talk("Sorry, I could not find information")

    # Tell joke
    elif 'joke' in command:

        joke = pyjokes.get_joke()

        print(joke)

        talk(joke)

    # Open Google
    elif 'open google' in command:

        talk("Opening Google")

        webbrowser.open("https://www.google.com")

    # Open YouTube
    elif 'open youtube' in command:

        talk("Opening YouTube")

        webbrowser.open("https://www.youtube.com")

    # Open Notepad
    elif 'open notepad' in command:

        talk("Opening Notepad")

        os.system("notepad")

    # Volume up
    elif 'volume up' in command:

        talk("Increasing volume")

        set_volume(0.8)

    # Volume down
    elif 'volume down' in command:

        talk("Decreasing volume")

        set_volume(0.2)

    # Mute volume
    elif 'mute' in command:

        talk("Muting volume")

        set_volume(0.0)

    # Shutdown system
    elif 'shutdown' in command:

        talk("Shutting down system")

        os.system("shutdown /s /t 1")

    # Restart system
    elif 'restart' in command:

        talk("Restarting system")

        os.system("shutdown /r /t 1")

    # Exit assistant
    elif 'exit' in command or 'stop' in command:

        talk("Goodbye")

        exit()

    # Empty command
    elif command == "":

        pass

    # Unknown command
    else:

        talk("Please say the command again")

# Start assistant
talk("AI Voice Assistant Started")

# Run continuously
while True:

    run_assistant()