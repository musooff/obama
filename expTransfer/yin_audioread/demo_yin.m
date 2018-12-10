%file = '../../data/speech/LDC93S1.wav';
%file = 'clarinet.au';

%file = '/Users/juhannam/Google Drive/GCT731 MIR/samples/cello_arp.wav';
%file = '/Users/juhannam/Google Drive/GCT731 MIR/samples/jobs.wav';
file = 'A-01.wav';

% run YIN
yin(file);
%r=yin(file);

% 
% 
% [x,sr] = wavread(file);
% %[x,sr] = audioread(file);
% 
% % FFT parameters
% win = hann(floor(0.04*sr));
% hop = floor(length(win)/2);
% N = 1024;
% 
% % display
% xf = stft(x, N, win, hop, sr);
% 
% M = size(xf,2);
% t = [0:M-1]*hop/sr;
% f = [0:N/2]/N*sr;
% figure; imagesc(t,f,20*log10(abs(xf)));
% axis xy;
% xlabel('time [sec]');
% ylabel('freq. [Hz]');
