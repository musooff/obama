function y = pitchTimeViaTSM( x, fsAudio, n, alpha )
%PITCHTIMEVIATSM �� �Լ��� ��� ���� ��ġ
%   �ڼ��� ���� ��ġ

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

