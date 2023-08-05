# ngChat Speech to Text and Text to Speech SDK

### Welcome to ngChat, Next Generation Chat, a revolutionary enterprise conversational platform that aims to:

1. addressing issues from the first version of NLU/ChatFlow, and
2. adding significant new features that support enterprise dialogue applications for the next 5 years.

### To know more, please visit [Seasalt.ai](https://seasalt.ai/)

## Example to use ngChat Speech to Text SDK:

### Prerequisites
You'll need a ngchat speech-to-text server url to run this example. Please contact Seasalt.ai to have one.

### Install and import the Speech SDK
First you'll need to install the Speech SDK.
```pip install ngchat-speech-sdk```

After the Speech SDK is installed, import it inot your Python project with this.
```import ngchat_speech.speech as speechsdk```

### Create a speech configuration
To call the Speech service using the Speech SDK, you need to create a SpeechConfig.
You'll need a ngchat speech-to-text server url to run this example. Please contact Seasalt.ai to have one.
```
    speech_config = speechsdk.SpeechConfig(
        host="ws://NGCHAT_STT_SERVER/client/ws/speech"
    )
```

### Recognize from a file
In this example, we'll show how to recognize speech from an audio file, if you want to recognize a stream, you'll need to use SpeechRecognizer.start_continuous_recognition_async() instead of SpeechRecognizer.recognize_once().
Create an AudioConfig and use the `filename` parameter.
```
    audio_stream = speechsdk.audio.PushAudioInputStream()
    audio_config = speechsdk.audio.AudioConfig(
        filename="test.wav"
    )
```

### Initialize a recognizer
After you've created a SpeechConfig and an AudioConfig, the next step is to initialize a SpeechRecognizer.
```
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )
```

### Connect callbacks to recognizer
SpeechRecognizer has 5 kinds of callbacks.
- Recognizing - called when some words were recognized, but not finished recognizing a single utterance.
- Recognized - called when a single utterance was recognized.
- Canceled - called when a continuous recognition was interrupted.
- Session_started - called when a recognition sesstion was started.
- Session_stopped - called when a recognition sesstion was stopped.
```
    speech_recognizer.recognizing.connect(
        lambda evt: print(f"Recognizing: {evt.result.text}"))
    speech_recognizer.recognized.connect(
        lambda evt: print(f'Recognized: {evt.result.text}'))
    speech_recognizer.canceled.connect(
        lambda evt: print(f'Canceled: {evt}'))
    speech_recognizer.session_started.connect(
        lambda evt: print(f'Session_started: {evt}'))
    speech_recognizer.session_stopped.connect(
        lambda evt: print(f'Session_stopped: {evt}'))
```

### Recognize speech
Now you're ready to run SpeechRecognizer. SpeechRecognizer has two ways for speech recognition.
- Single-shot recognition - Performs recognition once. This is to recognize a single audio file. Stop recognizing after a single utterance is recognized.
- Continuous recognition (async) - Asynchronously initiates continuous recognition operation. Connect to Recognizing and Recognized callbacks to receive recognition results. To stop asynchronous continuous recognition, call stop_continuous_recognition_async().
```speech_recognizer.recognize_once()```

### Put all together
We put all these steps together, the example code to test ngChat Speech SDK will look like this.
```
import speech as speechsdk
import audio as audio
import asyncio
import threading
import sys
import time

if __name__=="__main__":
    # this is an example to show how to use the ngChat Speech SDK to recognize once

    try:
        speech_config = speechsdk.SpeechConfig(
            host="ws://NGCHAT_STT_SERVER/client/ws/speech"
        )
        audio_stream = audio.PushAudioInputStream()
        audio_config = audio.AudioConfig(filename="test.wav")
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        speech_recognizer.recognizing.connect(
            lambda evt: print(f"Recognizing: {evt.result.text}"))
        speech_recognizer.recognized.connect(
            lambda evt: print(f'Recognized: {evt.result.text}'))
        speech_recognizer.canceled.connect(
            lambda evt: print(f'Canceled: {evt}'))
        speech_recognizer.session_started.connect(
            lambda evt: print(f'Session_started: {evt}'))
        speech_recognizer.session_stopped.connect(
            lambda evt: print(f'Session_stopped: {evt}'))

        speech_recognizer.recognize_once()
        time.sleep(3)

    except KeyboardInterrupt:
        print("Caught keyboard interrupt. Canceling tasks...")
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        sys.exit()
```
