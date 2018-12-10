func = @pitchTimeViaTSM;

BPM = [80,100,120];
pitchShift = [-2,0,2];

for i = pitchShift
    for j = BPM
        output = func(data,fs,i*100,100/j);
        audiowrite(sprintf('outputBPM %d pitch %d .wav',j,i),output,fs);
    end
end