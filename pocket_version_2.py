from pocketsphinx import AudioFile
import os

model_path = "en-us/"
config = {
    'verbose': False,
	'audio_file': os.path.join("../test", 'about.wav'),
    'buffer_size': 2048,
    'no_search': False,
    'full_utt': False,
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(model_path, 'en-us.lm.bin'),
    'dict': os.path.join(model_path, 'cmudict-en-us.dict')
}
audio = AudioFile(*config)
for phrase in audio:
    print(phrase.segments())