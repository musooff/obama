%% PSOLA with Audio System Toolbox

% Initialization
addpath(genpath('yin'));

% Hop / Window Size / Sampling Rate for YIN
P.hop = 64;
P.wsize = 128;
P.sr = 44100;
fs=44100;

% Loop ????
toc_length = 6;

% Pitch tracking memory
pitch_tracker = ones(1,10000);
pitch_modified_tracker = ones(1,10000);
i = 1;

x = zeros(fs*toc_length,1);
R2 = yin(x,P);

f0_midi = midi_reader('yeah(C-D-C).mid',x,fs,R2.f0);

%% Audio System Toolbox System objects
% AR: audioDeviceReader, where the records the sound from input device with
% given frame number ==> 2048
%
% AP: audioDeviceWriter, where the recorded sound is written into output
% device (speaker)
% Samples per frame = 2048

AR = audioDeviceReader('SamplesPerFrame',2048);
AP = audioDeviceWriter('SampleRate',AR.SampleRate, 'SupportVariableSizeInput', true);


% Device Setting --> Default (???? ??????/??????)
AP.Device = 'Default';
AR.Device = 'Default';


% Device Setting --> ASIO Device
%   AP.Driver = 'ASIO';
%   AR.Driver = 'ASIO';

%   AP.Device = 'ASIO4ALL v2';
%   AR.Device = 'ASIO4ALL v2';

%   PSOLA
%       ALPHA + BETA Value (In this case --> fixed beta: 1.1)
alpha = 1.0;
beta = 1.1;

%   Storage for recorded sound + modified sound
x_store = 0;
x_store2 = 0;
y_store = 0;

tic             % tic start for the loop

prev_en = 2048;


y = 0;             % Modified frame storage

% Frame Processing (Pitch Shifting)
while toc < toc_length

    audioIn = record(AR);
    
    
    % Pitch Detection of input sound
    warning off;
    R = yin(audioIn,P);
    warning on;
    f0 = 440.0 * 2.^R.f0;
    f0(isnan(f0)) = 0;
    
    pitch = median(f0);
    
    % Target pitch according to recording position
    midi_pos = ceil(toc*fs/P.hop);
    midi_target = f0_midi(midi_pos);

    % Pitch marking + Pitch shifting by PSOLA
    %   
    if((max(audioIn)) > 0.002)
        marks = findpitchmarks(audioIn, fs, f0, R.hop, R.wsize);
        %y = psola_midi_real(audioIn, marks, alpha, beta,midi_target);
        y = psola(audioIn, marks, alpha, beta);
        %[y, prev_en] = psola_modified(audioIn,marks,alpha,beta);
    else
        
        y = audioIn';
    end
    

    y = y';
    
    R = yin(y,P);
    f0_modified = 440.0 * 2.^R.f0;
    f0_modified(isnan(f0_modified)) = 1;
    
    pitch_modified = median(f0_modified);
    
    
    % Pitch ?????? ?????? ???????? (INPUT / OUTPUT) 
    pitch_tracker(i) = pitch;
    pitch_modified_tracker(i) = pitch_modified;
    
    
    i = i+1;

    % Device?? ???? ?????? frame ????
    numunderrun = play(AP,y);
    
    % ???? input ?? ???? ?? 
    % numunderrun = play(AP, audioIn);
    
    
    x_store = [x_store ; audioIn];
    %x_store2 = [x_store2 ; audioIn2];
    y_store = [y_store ; y];
    
end

x_axis = 1:length(pitch_tracker);

disp('End Signal Input');

% Release the system objects
release(AR);
release(AP);


%%   ???? Device to Device mic playback via Audio System Toolbox

% Audio System Toolbox System objects
% AR: audioDeviceReader, where the records the sound from input device with
% given frame number ==> 2048
%
% AP: audioDeviceWriter, where the recorded sound is written into output
% device (speaker)
% Samples per frame = 2048

AR = audioDeviceReader('SamplesPerFrame',2048);
AP = audioDeviceWriter('SampleRate',AR.SampleRate, 'SupportVariableSizeInput', true);


% Device Setting --> Default (???? ??????/??????)
AP.Device = 'Default';
AR.Device = 'Default';


% Device Setting --> ASIO Device --> ?????? ???? latency ????
%   AP.Driver = 'ASIO';
%   AR.Driver = 'ASIO';

%   AP.Device = 'ASIO4ALL v2';
%   AR.Device = 'ASIO4ALL v2';

tic;

while toc < 5

    audioIn = record(AR);
    numunderrun = play(AP,audioIn);

end



disp('End Signal Input');

% Release the system objects
release(AR);
release(AP);
