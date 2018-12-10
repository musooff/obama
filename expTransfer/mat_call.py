import matlab.engine
eng = matlab.engine.start_matlab()
source= eng.audioread('/home/muso/Desktop/obama/karaoke/split_parts/Shape Of You/obama/1.wav')
#print source
target = eng.audioread('/home/muso/Desktop/obama/karaoke/split_parts/Shape Of You/prof/1.wav')
y = eng.expTrans(source, target, 44100)