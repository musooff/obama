function [filterBankResponseMatrix] = computeFilterBankResponse(wavAudio,sr,demandSampleRate)
% [filterBankResponse] = computeFilterBankResponse(wavAudio,sr)
% Compute Filter Bank Response of given Audio(waveform format)
% Method and codes are diffectly influenced by Chroma Toolbox 2.0 by Meinard Mueller, Sebastian Ewert
% Need to be rewriten.

if nargin<3; demandSampleRate = 50; end;

% Resampling to 22050 Hz to use Chroma toolbox
[~,nchannel]=size(wavAudio);
if nchannel ~= 1
    wavAudio = sum(wavAudio,nchannel)./nchannel;
end
audio_wav = resample(wavAudio, 22050, sr);

% Downsampling frequency
fs_low = 882;
fs_mid = 4410;
fs_high = 22050;

fs_pitch(21:59) = fs_low;
fs_pitch(60:95) = fs_mid;
fs_pitch(96:108) = fs_high;

fs_index = zeros(1,108);
fs_index(21:59) = 1;
fs_index(60:95) = 2;
fs_index(96:108) = 3;

pcm_ds = cell(3,1);
% y = resample(x,p,q,n) uses an antialiasing filter of order 2 ¡¿ n ¡¿ max(p,q).
pcm_ds{1} = resample(audio_wav, fs_low, 22050, 100);
pcm_ds{2} = resample(audio_wav, fs_mid, 22050, 100);
pcm_ds{3} = audio_wav;
load MIDI_FB_ellip_pitch_60_96_22050_Q25.mat
% compute STRMS for all 88 subbands

fprintf('Computing subbands and STMSP for all pitches: (21-108):  21');
filterBankResponse=cell(108,1);
for p=21:108;
    fprintf('\b\b\b\b');fprintf('%4i',p);
    index = fs_index(p);
    Subband = filtfilt(h(p).b, h(p).a, pcm_ds{index});
    filterBankResponse{p} = Subband.^2*(fs_high/fs_pitch(p));
end
fprintf('\n')

% convert to Metrix and Downsampling
% win_hann=[21 41 101];
win_rect=[21 41 101];
fbrLength=floor(length(audio_wav)*demandSampleRate/22050);
filterBankResponseMatrix=zeros(108,fbrLength);
fprintf('Downsampling subbands : (21-108):  21');
for p=21:108;
    fprintf('\b\b\b\b');fprintf('%4i',p);
    stat_window = rectwin(win_rect(fs_index(p)));
    stat_window = stat_window/sum(stat_window);
    filterBankResponse{p}=conv(filterBankResponse{p},stat_window,'same');
    tempfbr=resample(filterBankResponse{p},demandSampleRate, fs_pitch(p));
    filterBankResponseMatrix(p,:) = tempfbr(1:fbrLength);
end
fprintf('\n');

end

