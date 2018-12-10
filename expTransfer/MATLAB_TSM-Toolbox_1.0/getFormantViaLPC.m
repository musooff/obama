function [ A, e, sideinfo ] = getFormantViaLPC( x,parameter,sideinfo )
%GETFORMANTVIALPC 이 함수의 요약 설명 위치
%   자세한 설명 위치

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% check parameters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if nargin < 3
    sideinfo = [];
end
if nargin < 2
    parameter = [];
end
if nargin < 1
    error('Please specify input data x.');
end

if ~isfield(parameter,'anaHop')
    parameter.anaHop = 2048;
end
if ~isfield(parameter,'win')
    parameter.win = win(4096,2); % hann window
    %parameter.win = ones(4096,1);
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
if ~isfield(parameter,'ncoef')
    parameter.ncoef = 2 + round(parameter.fsAudio / 1000); % rule of thumb for human speech
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
ncoef = parameter.ncoef;
numOfChan = size(x,2);

xPadded = [zeros(winLenHalf,numOfChan);x;zeros(winLen+anaHop,numOfChan)];

if parameter.numOfFrames >= 0
    numOfFrames = parameter.numOfFrames;
else
    numOfFrames = floor((size(xPadded,1) - winLen)/anaHop + 1);
end
winPos = (0:numOfFrames-1) * anaHop + 1;



A = zeros(ncoef + 1,numOfFrames,numOfChan);
e = zeros(size(xPadded));
for c = 1 : numOfChan
    for i = 1 : numOfFrames
        xi = xPadded(winPos(i):winPos(i) + winLen - 1,c) .* w;
        ai = lpc(xi, ncoef);
        A(:,i,c) = ai;
        ei = xi - filter([0 -ai(2:end)],1,xi);
        e(winPos(i):winPos(i) + winLen - 1,c) = e(winPos(i):winPos(i) + winLen - 1,c) + ei;
    end
end
e = e(winLenHalf+1:end-winLenHalf,:);
e(isnan(e)) = 0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% update sideinfo
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sideinfo.formLPC.anaHop = anaHop;
sideinfo.formLPC.winPos = winPos;
sideinfo.formLPC.numOfFrames = numOfFrames;
sideinfo.formLPC.win = parameter.win;

end

