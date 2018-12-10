%% Real-Time Audio Stream Processing
%
% The Audio System Toolbox provides real-time, low-latency processing of
% audio signals using the System objects audioDeviceReader and
% audioDeviceWriter.
%
% This example shows how to acquire an audio signal using your microphone,
% perform basic signal processing, and play back your processed
% signal.
%

%% Create input and output objects

clear all;
close all;

AR = audioDeviceReader;
deviceWriter = audioDeviceWriter('SampleRate',AR.SampleRate);

P.hop = 64;
P.wsize = 256;
P.sr = 44100;
P.minf0 = 100;

ap_acc = [];
% Device Setting --> ASIO Device
   deviceWriter.Driver = 'ASIO';
   AR.Driver = 'ASIO';

   deviceWriter.Device = 'ASIO4ALL v2';
   AR.Device = 'ASIO4ALL v2';

%% Specify an audio processing algorithm
% PROCESSING ALGORITHM GOES HERE... INPUT SIGNAL CHANGES HERE
process = @(x) x.*2;

%% Code for stream processing
% Place the following steps in a while loop for continuous stream
% processing:
%   1. Use the record method of your audio device reader to acquire one input frame.
%   2. Perform your signal processing operation on the input frame. 
%   3. Use the play method of your audio device writer to listen to your processed frame. 

disp('Begin Signal Input...')
tic
while toc<10
    mySignal = record(AR);
    
    
    warning off;
    R = yin(mySignal,P);
    warning on;
    
    f0 = 440.0 * 2.^R.f0;
    ap = R.ap;
    median(ap)
    
    ap_acc = [ap_acc ap];
    
    amp = max(abs(mySignal));
    myProcessedSignal = process(mySignal);
    play(deviceWriter, myProcessedSignal);
end
disp('End Signal Input')

release(deviceReader)
release(deviceWriter)