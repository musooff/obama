function [ y ] = formantRecover( A, e, parameter, sideinfo )
%FORMANTRECOVER 이 함수의 요약 설명 위치
%   자세한 설명 위치

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% check parameters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if nargin < 4
    sideinfo = [];
end
if nargin < 3
    parameter = [];
end
if nargin < 2
    error('Please specify input data A and e.');
end

if ~isfield(parameter,'anaHop')
    parameter.anaHop = 2048;
end
if ~isfield(parameter,'win')
    %parameter.win = win(4096,2); % hann window
    parameter.win = ones(4096,1);
end
if ~isfield(parameter,'zeroPad')
    parameter.zeroPad = 0;
end
if ~isfield(parameter,'fsAudio')
    parameter.fsAudio = 22050;
end
if ~isfield(parameter,'numOfFrames')
    parameter.numOfFrames = -1;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% some pre calculations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
anaHop = parameter.anaHop;
w = parameter.win;
zp = parameter.zeroPad;
w = [zeros(floor(zp/2),1);w;zeros(floor(zp/2),1)];
winLen = length(w);
winLenHalf = round(winLen/2);
numOfChan = size(e,2);

numOfFrames = parameter.numOfFrames;
winPos = parameter.winPos;

ePadded = [zeros(winLenHalf,numOfChan);e;zeros(winLen+anaHop,numOfChan)];

y = zeros(size(ePadded));
for c = 1:numOfChan
    for i = 1 : numOfFrames
        ei = ePadded(winPos(i):winPos(i) + winLen - 1,c) .* w;
        reci = filter(1,A(:,i),ei);
        y(winPos(i):winPos(i) + winLen - 1,c) = y(winPos(i):winPos(i) + winLen - 1,c) + reci;
    end
end
y = y(winLenHalf+1:end-winLenHalf,:);
y(isnan(y)) = 0;

end

