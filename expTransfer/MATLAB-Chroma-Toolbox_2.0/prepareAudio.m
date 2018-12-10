function [filterBankResponse, dlnco] = prepareAudio(dirAudio, demandSampleRate, useChroma)
% [filterBankResponse] = prepareAudio(dirAudio) 
% Load Audiofile and return Filter Bank Response of it.
% 
% dirAudio : string that indicate absolute directory of target Audiofile
% demandSampleRate : double. nSample per second (demanding). 
% Default is 50 (1 sample : 20ms)

%	Version 1.00
%	06.07.2016
%	Copyright (c) by Taegyun Kwon
%	ilcobo2@kaist.ac.kr

if nargin<2; demandSampleRate = 50; end;
if nargin<3; useChroma = false; end;


if ~useChroma
    [wavAudio,wavSampleRate] = audioread(dirAudio);

    filterBankResponse = computeFilterBankResponse(wavAudio,wavSampleRate,demandSampleRate); % this response contains unexpected negative values
    filterBankResponse(filterBankResponse<0)=0; % for temporal correction for this problem
    filterBankResponse(109:120,:) = zeros(12, size(filterBankResponse,2));
    
    paramCLP.applyLogCompr = 1;
    paramCLP.factorLogCompr = 10;
    paramCLP.applyNormalization =0 ;


    [~,~,dlnco] = onsetDetection(filterBankResponse, demandSampleRate, paramCLP);
    
    
    filterBankResponse=log(1+5000*filterBankResponse);
    filterBankResponse=filterBankResponse(21:108,:);

else    
    
    [f_audio,sideinfo.fs] = audioread(dirAudio);
    if size(f_audio,2) ==2
        f_audio = (f_audio(:,1) + f_audio(:,2)) /2;
    end
    shiftFB = estimateTuning(f_audio);
    
    paramPitch.winLenSTMSP = 44100 / demandSampleRate;
    paramPitch.shiftFB = shiftFB;
    %[f_pitch,sideinfo] = audio_to_pitch_via_FB(f_audio,paramPitch,sideinfo);
    
    [wavAudio,wavSampleRate] = audioread(dirAudio);
    f_pitch = computeFilterBankResponse(wavAudio,wavSampleRate,demandSampleRate); % this response contains unexpected negative values
    f_pitch(f_pitch<0)=0; 
    f_pitch(109:120,:) = zeros(12, size(f_pitch,2));
    
    
    
    
%     paramCP.applyLogCompr = 0;
%     paramCP.inputFeatureRate = sideinfo.pitch.featureRate;
    
    paramCLP.applyLogCompr = 1;
    %paramCLP.factorLogCompr = 3100;
    paramCLP.factorLogCompr = 50000;
    paramCLP.applyNormalization =0 ;
%     paramCLP.inputFeatureRate = sideinfo.pitch.featureRate;
%     paramCLP.inputFeatureRat = demandSampleRate /2;
    
%     paramCENS.winLenSmooth = 21;
%     paramCENS.downsampSmooth = 5;
%     paramCENS.inputFeatureRate = sideinfo.pitch.featureRate;

    [~,~,dlnco] = onsetDetection(f_pitch, demandSampleRate, paramCLP);

    [filterBankResponse, sideinfo] = pitch_to_chroma(f_pitch,paramCLP,sideinfo);
%     filterBankResponse = f_pitch;
    
%     filterBankResponse(filterBankResponse<0)=0; % for temporal correction for this problem
%     filterBankResponse=log(1+5000*filterBankResponse);
%     filterBankResponse=filterBankResponse(21:108,:);
end


end

