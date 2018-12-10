function y = pitchTimeViaTSM( x, fsAudio, n, alpha )
%PITCHTIMEVIATSM 이 함수의 요약 설명 위치
%   자세한 설명 위치

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% time-stretching
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear parameter
yHP = hpTSM(x,alpha);
%yHP = pvTSM(x,alpha);
%yHP = wsolaTSM(x,alpha);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% pitch-shifting
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear parameter
parameter.fsAudio = fsAudio;
parameter.algTSM = @hpTSM;
%parameter.algTSM = @pvTSM;
%parameter.algTSM = @wsolaTSM;
y = pitchShiftViaTSM(yHP,n,parameter);

end

