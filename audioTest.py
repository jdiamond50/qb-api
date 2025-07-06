from gtts import gTTS # google text to speech

text = "This is test audio."
lang = "en"

audio = gTTS(text=text, lang=lang, slow=False)
audio.save("test-audio.mp3")
