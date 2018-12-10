%% TRYOUT WITH INPUT OF MIC

clear all;

% Initialization
addpath(genpath('yin'));

% Select SONG

%file_name = 'yeah(C-C-C).wav';
%file_name = 'way(BAD).wav';
file_name = 'Falling(BAD).wav';

frameLength = 1024;

AR = audioDeviceReader('SamplesPerFrame', frameLength);

fileReader = dsp.AudioFileReader(file_name, 'SamplesPerFrame',frameLength);
deviceWriter = audioDeviceWriter('SampleRate',fileReader.SampleRate);

file_length = zeros(1,441000);

% % Device Setting --> Default 
% AP.Device = 'Default';
% AR.Device = 'Default';


% Device Setting --> ASIO Device
   deviceWriter.Driver = 'ASIO';
   AR.Driver = 'ASIO';

   deviceWriter.Device = 'ASIO4ALL v2';
   AR.Device = 'ASIO4ALL v2';

    
% time stretching ratio
alpha = 1;
% pitch shifting ratio
beta = 1.2;

% parameters 
pitch_hop = 64;
pitch_win = 256;
pitch_thres = 0.1;
sr = fileReader.SampleRate;

% Hop / Window Size / Sampling Rate for YIN
P.hop = pitch_hop;
P.wsize = pitch_win;
P.sr = sr;
P.minf0 = 100;



%f0_midi = midi_reader('yeah(C-D-C).mid',sr);
%f0_midi = midi_reader('way.mid',sr);
f0_midi = midi_reader('Falling.mid',sr);

tick = 0;

f0_acc = [];
ap_acc = [];
f0_2_acc = [];
pitch_mark_acc = [];

energy_acc = [];

x = [];
y = [];

pitch_offset = 0;

out_init = zeros(1, frameLength);
last_tk = frameLength;
last_pit = 100;
first_call = 1;
beta_out = 1;
beta_coef = 0.2;

while ~isDone(fileReader)
    offset = frameLength*tick+1;
    
    if(offset > length(f0_midi))
       break; 
    end
    
    % audio input 
    %signal = step(fileReader);
    signal = record(AR);
    
    
    
    if tick == 0
        pitch_analysis_buffer = signal;
    else
        pitch_analysis_buffer = [untouched_samples; signal];
    end
%    pitch_analysis_buffer = signal;

    %%%%% pitch detection %%%%%
    warning off;
    R = yin(pitch_analysis_buffer, P);
    warning on;
        
    f0 = 440.0 * 2.^R.f0;
    ap = R.ap;
    
    
    
    
    % unvoiced if aperiodicity is greater than pitch_thres
    f0(ap > pitch_thres) = 100;
    f0(median(f0) > 1000) = 100;
    
                
    f0_acc = [f0_acc median(f0)];
    ap_acc = [ap_acc ap];

    untouched_samples = pitch_analysis_buffer(length(f0)*pitch_hop+1:end);


    %%%%% pitch marks %%%%%
    pitch_mark = findpitchmarks(pitch_analysis_buffer, sr, f0, pitch_hop, pitch_win);

    
    pitch_mark2 = pitch_mark(pitch_mark <= length(f0)*pitch_hop);
    pitch_mark_acc = [pitch_mark_acc pitch_mark2+pitch_offset];
    pitch_offset = pitch_offset + length(f0)*pitch_hop;
    beta = f0_midi(offset)/median(f0);
    
    beta
    max(abs(signal));
    % change pitch when all frames are voiced!!!
    if tick >= 4 && max(abs(signal)) > 0.05 && f0(1) ~= 100 && median(f0) < 500 && median(f0) > 140 && beta > 0.5 && beta < 2.0
%         if (tick > 80) & (tick < 160)
%             beta = power(2, 2/12);            
%         else
%             beta = 1;
%         end
        
        %disp('VOICING');
        
        
        beta_out = beta_coef*beta + (1-beta_coef)*beta_out;
        
        [psola_out, last_tk, last_pit] = psola(pitch_analysis_buffer, out_init, last_tk, last_pit, frameLength, pitch_mark, 1, beta_out, first_call);
        first_call = 0;        
        

        processedSignal = psola_out(1:frameLength)';
        out_init = psola_out(frameLength+1:last_tk+last_pit);
    else
%        processedSignal = [zeros(frameLength-length(f0)*pitch_hop,1); pitch_analysis_buffer(1:length(f0)*pitch_hop)];
        processedSignal = signal;           % Input
    end

% if 0
%     figure(1);
%     subplot(2,1,1);
%     plot(pitch_analysis_buffer);
%     hold on;
%     ll = max(abs(pitch_analysis_buffer));
%     for jj=1:length(pitch_mark)
%         plot([pitch_mark(jj), pitch_mark(jj)], [-ll, ll], '--k')
%     end
%     hold off;
% 
%     subplot(2,1,2);
%     plot(psola_out);
%     hold on;
%     plot([last_tk, last_tk], [-ll, ll], '--k');
%     hold off;
% end

    
    %%%%% processing %%%%%
    %processedSignal = signal;    
    
    R2 = yin(processedSignal, P);
    f0_2 = 440.0 * 2.^R2.f0;
    ap2 = R2.ap;
    
    
    play(deviceWriter, 2*processedSignal);

    tick = tick + 1;


    
    
    % Changed Pitch Storage
    
    if(median(f0_2) < 1000)
        f0_2_acc = [f0_2_acc median(f0_2)];
    else
        f0_2_acc = [f0_2_acc median(f0)];
        
    end
    
    x = [x; signal];
    y = [y; processedSignal];
    
    energy_acc = [energy_acc max(signal)];
    
    %pause;
end

f0_midi_mod = resample(f0_midi,1,1000);
f0_midi_mod = f0_midi_mod(1:length(f0_acc));

%plot(1:length(f0_acc),f0_acc,1:length(f0_acc),f0_2_acc,1:length(f0_acc),f0_midi_mod);
% ylim([0,500]);

release(AR);
release(fileReader);
release(deviceWriter);
