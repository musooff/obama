from pydub import AudioSegment
from pydub.silence import split_on_silence, detect_silence

sound_file = AudioSegment.from_wav("someFolder/I know that some are skeptical about the size and scale .wav")
audio_chunks = split_on_silence(sound_file, silence_thresh=sound_file.dBFS-1, min_silence_len=30)

from pydub.playback import play

#play(sound_file)
print detect_silence(sound_file,  silence_thresh=sound_file.dBFS-1, min_silence_len=30)

print len(sound_file)
print sound_file.dBFS
print audio_chunks

def orig_code():
	for i, chunk in enumerate(audio_chunks):
		out_file = "splitAudio/chunk{0}.wav".format(i)
		print "exporting", out_file
		chunk.export(out_file, format="wav")

orig_code()