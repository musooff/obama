function y = expTrans( source, target, sr, mixRate, phoneS, phoneT )


if nargin < 5
    useLPC = true;
end

if nargin < 4
    mixRate = 0.7;
end

if nargin < 3
    sr = 44100;
end

if nargin < 2
    error('Please specify source and target.');
end

addpath('./MATLAB_TSM-Toolbox_1.0');
addpath('./MATLAB-Chroma-Toolbox_2.0');
addpath('./yin_audioread');
addpath('./PSOLA(Tae)');

%% Normalize source and target %%
source = source/max(abs(source));

target = target/max(abs(target));

%% Set Parameters %%
blockSize = 2048;

parameter.anaHop = 1024;
parameter.win = win(blockSize,2);
parameter.zeroPad = 0;
parameter.fsAudio = sr;
parameter.numOfFrames = -1;
parameter.fftShift = 0;

%% Get STFT and Formant for Similarity Matrix %%

specS = abs(stft(source,parameter));specS = specS(1:256,:);%specS = filterbank'*specS;%specS = specS(1:256,:);
specS = max_filter(specS,2);
specT = abs(stft(target,parameter));specT = specT(1:256,:);%specT = filterbank'*specT;%specT = specT(1:256,:);
specT = max_filter(specT,2);
AS = getFormantViaLPC(source,parameter);
AT = getFormantViaLPC(target,parameter);

shiftFBS = estimateTuning(source);
shiftFBT = estimateTuning(target);

paramPitchS.winLenSTMSP = 4410;
paramPitchS.shiftFB = shiftFBS;
paramPitchS.visualize = 0;
paramPitchT.winLenSTMSP = 4410;
paramPitchT.shiftFB = shiftFBT;
paramPitchT.visualize = 0;
[f_pitchS,~] = ...
    audio_to_pitch_via_FB(source,paramPitchS);
[f_pitchT,~] = ...
    audio_to_pitch_via_FB(target,paramPitchT);
f_pitchS_new = resample(f_pitchS',size(specS,2),size(f_pitchS,2))';
f_pitchT_new = resample(f_pitchT',size(specT,2),size(f_pitchT,2))';
f_pitchS_new = f_pitchS_new(41:end,:);
f_pitchT_new = f_pitchT_new(41:end,:);
f_pitchS_log = log10(1+1*max(f_pitchS_new,0));
f_pitchT_log = log10(1+1*max(f_pitchT_new,0));
f_pitchS_log = max_filter(f_pitchS_log, 3);
f_pitchT_log = max_filter(f_pitchT_log, 3);

if ~useLPC
    phoneS = resample(phoneS',size(specS,2),size(phoneS,2))';
    phoneT = resample(phoneT',size(specT,2),size(phoneT,2))';
end

%% Make Similarity Matrix %%
SMspec = simmx(specS,specT);
SMfor = simmx(AS, AT);
SMq = simmx(f_pitchS_log,f_pitchT_log);
if ~useLPC
    SMp = simmx(phoneS,phoneT);
end
%SMceps = simmx(cepsS,cepsT);
%SMpitch = simmx(pitchS,pitchT);
if useLPC
    SM = SMq*mixRate + SMfor*(1-mixRate);
else
    SM = SMp*mixRate + SMq*(1-mixRate);
end
%SMfor*0.5 + SMq*0.5;
%SM = SMceps*0.25 + SMfor*0.25 + SMspec*0.5;
%SM(SM == 1) = 0;
%SM(SM > 0.9) = 1;

[p,q,~] = dp(1-SM);

%p = p(1:5:end);q = q(1:5:end);
%% Make Time-Varying Time-stretch rate s %%

s = q(1);
for i = 2:length(p)
    if p(i) ~= p(i-1)
        s = [s; q(i)];
    end
end

s_mod = sgolayfilt(s,3,11);
N = length(s_mod);

s_new = [1,1];
s_new = [s_new;(1:N)',s_mod];
s_new = round((s_new-1)*parameter.anaHop + 1);
s_new = s_new(1:end-2,:);
s_new = [s_new; length(source), length(target)];

s_newnew = s_new(1,:);
for i = 3:size(s_new,1)
    if s_new(i,2) > s_newnew(end,2) && s_new(i,1) <= length(source) && s_new(i,2) <= length(target)
        s_newnew = [s_newnew;s_new(i,:)];
    end
end
%s_newnew = s_newnew(1:5:end,:);

%% Time-matching %%
ss = hpTSM(source,s_newnew);

if length(ss) > length(target)
    ss = ss(1:length(target));
end
if length(ss) < length(target)
    target = target(1:length(ss));
end

%% Pitch Tracking with YIN for Both Signals %%
par.sr = sr;
par.hop = 512;

par.thresholds = 0.01:0.01:1;
par.relflag = 1;

parHps.maskingMode = 'binary';
[ssHarm,~,~] = hpSep(ss,parHps);

yin_ss = yin(ssHarm,par);
freq_ss = 2.^(yin_ss.f0).*440;
freq_ss_best = 2.^(yin_ss.best).*440;
yin_tar = yin(target,par);
yin_tar.best = yin_tar.best - nanmean(yin_tar.best) + nanmean(yin_ss.best);
freq_tar_best = 2.^(yin_tar.best).*440;

%% Set Beta and matching Pitch %%

f0 = freq_ss;
f0(isnan(f0)) = 0;
m = findpitchmarks(ss,sr,f0,yin_ss.hop,yin_ss.wsize);
ss_pitch = psola_contBeta(ss, m, 1, freq_ss_best, freq_tar_best)';


% beta = freq_tar./freq_ss;beta(isnan(beta)) = 1;
% beta = [(512:512:512*length(beta))', beta'];
% ss_pitch = pitchShiftContViaTSM(ss,beta);
% ss_pitch = ss_pitch(1:length(target));
% % freq_diff = freq_tar./freq_ss;
% % ss_pitch = pitchShiftContViaTSM(ss,beta);

%% Matching Volume Envelope %%
env_ss = envelope(ss_pitch,2048,'rms');env_ss(env_ss<0.005) = 0.005;
env_tar = envelope(target,2048,'rms');
env = env_tar./env_ss;

ss_pitch_env = ss_pitch.*env;


y = ss;

end

