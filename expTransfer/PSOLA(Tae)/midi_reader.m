function f0_midi = midi_reader(file_name,fs)

% This function reads MIDI file and returns the array of MIDI file's note
% sequence in terms of Hertz

% Calculate length of the 


% Read midi file
midi = readmidi(file_name);     
Notes = midiInfo(midi,0);       

endTime = ceil(Notes(end,6));

          % Sync the length of INPUT pitch info 
midi_num = zeros(1,fs*endTime);   % MIDI number sequence storage Initialize



% Recalculate onset/offset timing of each note in terms of pitch length
% wise
ttp = ceil(fs.*(Notes(:,5:6)));   
ttp(1) = 1;

% Extract MIDI number and organize to MIDI number sequence
for i=1:size(ttp,1)
    for j = ttp(i,1):ttp(i,2)
        midi_num(j) = Notes(i,3);
    end
end

% Translate to frequency
f0_midi = round(2.^((midi_num-69)/12)*440);

% Median Filter (Getting rid off gaps between notes)
f0_midi = medfilt1(f0_midi,30);


end

