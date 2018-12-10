function y = pitchShiftContViaTSM( x, beta, parameter )
%PITCHSHIFTCONTVIATSM Summary of this function goes here
%   Detailed explanation goes here

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% check parameters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if nargin < 3
    parameter = [];
end

if ~isfield(parameter,'interp')
    parameter.interp = @linInterp;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% some pre calculations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
interp = parameter.interp;
numOfChan = size(x,2);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% pitch modification
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if isscalar(beta)
    betas = [size(x,1) beta];
else
    betas = beta;
end
%outputLength = anchorPoints(end,2);

yResamp = [];
for c = 1:numOfChan
    xC = x(:,c);
    yResamp = [yResamp, interp(xC,betas)];
end

s = [1;betas(1,1)/betas(1,2)];
for i = 2:size(betas,1)
    s = [s;(betas(i,1)-betas(i-1,1))/betas(i,2) + s(i)];
end

y = wsolaTSM(yResamp,[s,[1;betas(:,1)]]);

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% linear interpolation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function y = linInterp(x,betas)
    y = [];
    pointer = 1;
    rateCounter = 1;
    while pointer <= length(x)
        pf = floor(pointer);
        pc = ceil(pointer);
        pmid = pointer - floor(pointer);
        y = [y; (1-pmid)*x(pf) + pmid*x(pc)];
        if pointer > betas(rateCounter,1)
            rateCounter = rateCounter + 1;
        end
        pointer = pointer + (1-pmid)*betas(rateCounter,2)+pmid*betas(rateCounter,2);
    end
end

