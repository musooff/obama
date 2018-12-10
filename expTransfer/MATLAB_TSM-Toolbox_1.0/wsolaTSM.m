function [y,sideinfo] = wsolaTSM(x,s,parameter,sideinfo)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name: wsolaTSM
% Date: 03-2014
% Programmer: Jonathan Driedger
% http://www.audiolabs-erlangen.de/resources/MIR/TSMtoolbox/
%
% WSOLA (Waveform Similarity Overlap-add) is a time-scale modification 
% algorithm. It rescales the time-axis of the input signal x according to 
% the time-stretch function s without altering the pitch of x. For more
% information see the paper "An Overlap-Add Technique Based on Waveform
% Similarity (WSOLA) for High Quality Time-Scale Modification of Speech" by
% Verhelst and Roelands.
%
% Input:    x               input signal.
%           s               time-stretch function. Either a constant
%                           scaling factor or a n x 2 matrix representing a
%                           set of n anchorpoints relating sample positions
%                           in the input signal with sample positions in
%                           the output signal.
%           parameter.
%               synHop      hop size of the synthesis window.
%               win         the analysis and synthesis window for the stft.
%               tolerance   number of samples the window positions in the
%                           input signal may be shifted to avoid phase
%                           discontinuities when overlap-adding them to
%                           form the output signal (given in samples).
%
% Output:   y               the time-scale modified output signal.
%           sideinfo.
%               wsolaTSM.synHop
%               wsolaTSM.win
%               wsolaTSM.tolerance
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Reference: 
% If you use the 'TSM toolbox' please refer to:
% [DM14] Jonathan Driedger, Meinard Mueller
%        TSM Toolbox: MATLAB Implementations of Time-Scale Modification 
%        Algorithms
%        Proceedings of the 17th International Conference on Digital Audio  
%        Effects, Erlangen, Germany, 2014.
%
% License:
% This file is part of 'TSM toolbox'.
% 
% 'TSM toolbox' is free software: you can redistribute it and/or modify it
% under the terms of the GNU General Public License as published by the
% the Free Software Foundation, either version 3 of the License, or (at
% your option) any later version.
% 
% 'TSM toolbox' is distributed in the hope that it will be useful, but
% WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
% Public License for more details.
% 
% You should have received a copy of the GNU General Public License along
% with 'TSM toolbox'. If not, see http://www.gnu.org/licenses/.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% check parameters
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if nargin < 4
    sideinfo = [];
end
if nargin < 3
    parameter = [];
end
if nargin<2
    error('Please specify input data x and s.');
end

if ~isfield(parameter,'synHop')
    parameter.synHop = 512;
end
if ~isfield(parameter,'win')
    parameter.win = win(1024,2); % hann window
end
if ~isfield(parameter,'tolerance')
    parameter.tolerance = 512;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% some pre calculations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
synHop = parameter.synHop;
w = parameter.win;
winLen = length(w);
winLenHalf = round(winLen/2);
tol = parameter.tolerance;
numOfChan = size(x,2);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% time-stretch function
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if isscalar(s)
    anchorPoints = [1 1; size(x,1) ceil(s*size(x,1))];
else
    anchorPoints = s;
end
outputLength = anchorPoints(end,2);
synWinPos = 1:synHop:outputLength + ... % Positions of the synthesis
    winLenHalf;                         % windows in the output
anaWinPos = ...                         % Positions of the analysis windows
    round(interp1(anchorPoints(:,2),... % in the input
    anchorPoints(:,1),synWinPos,...
    'linear','extrap'));
anaHop = [0 anaWinPos(2:end)-...        % Analysis hopsizes
    anaWinPos(1:end-1)];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% wsola
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
y = zeros(outputLength,numOfChan);      % Initialize output

% To avoid that we access x outside its range, we need to zero pad it
% appropreately
minFac = min(synHop ./ anaHop);         % The minimal local stretching 
                                        % factor
x = [zeros(winLenHalf + ...             % Zero pad
    tol,numOfChan);... 
    x;...
    zeros(ceil(1/minFac) * ...
    winLen+tol,numOfChan)];
anaWinPos = anaWinPos + tol;            % Compensate for the extra 'tol' 
                                        % padded zeros at the beginning of
                                        % x

for c = 1 : numOfChan                   % loop over channels
xC = x(:,c);

yC = zeros(outputLength + 2*winLen,1);  % Initialize the output signal
ow = zeros(outputLength + 2*winLen,1);  % Keep track of overlapping windows

del = 0;                                % Shift of the current analysis  
                                        % window position
for i = 1 : length(anaWinPos)-1
    % OLA
    currSynWinRan = ...                 % The range of the current 
     synWinPos(i):synWinPos(i)+winLen-1;% synthesis window
    currAnaWinRan = ...                 % The range of the current analysis
     anaWinPos(i) + del: ...            % window, shifted by the offset 
     anaWinPos(i) + winLen-1 + del;     % 'del'
                                        
    yC(currSynWinRan) = ...             % Overlap and add
         yC(currSynWinRan) + ...
         xC(currAnaWinRan) .* w;
    ow(currSynWinRan) = ...             % Update the sum of overlapping 
         ow(currSynWinRan) + w;         % windows
    
     
    natProg = xC(currAnaWinRan + ...    % The 'natural progression' of the
         synHop);                       % last copied audio segment

    nextAnaWinRan = ...                 % The range where the next analysis 
     anaWinPos(i+1) - tol: ...          % window could be located
     anaWinPos(i+1) + winLen-1 + tol;   % (including the tolerance region)
    
    xNextAnaWinRan = xC(nextAnaWinRan); % The corresponding segment in x
    
    % cross correlation
    cc = ...                            % Compute the cross correlation
     crossCorr(xNextAnaWinRan,...
     natProg,winLen);
    
    [~,maxIndex] = max(cc);             % pick the optimizing index in the 
                                        % cross correlation
    
    del = tol - maxIndex + 1;           % Infer the new 'del'
    
end

% process last frame
yC(synWinPos(end):synWinPos(end)+winLen-1) = ...
    yC(synWinPos(end):synWinPos(end)+winLen-1) + ...
    xC(anaWinPos(i)+del:anaWinPos(i)+winLen-1+del) .* w;
ow(synWinPos(end):synWinPos(end)+winLen-1) = ...
    ow(synWinPos(end):synWinPos(end)+winLen-1) + w;

% renormalize the signal by dividing by the added windows
ow(ow<10^-3) = 1; % avoid potential division by zero
yC = yC ./ ow;

% remove zeropading at the beginning
yC = yC(winLenHalf+1:end);

% remove zeroPadding at the end
yC = yC(1:outputLength);

y(:,c) = yC;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% update sideinfo
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sideinfo.wsolaTSM.synHop =  parameter.synHop;
sideinfo.wsolaTSM.win = parameter.win;
sideinfo.wsolaTSM.tolerance = parameter.tolerance;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% cross correlation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function cc = crossCorr(x,y,winLen)
% cross correlation is essentially the same as convolution with the first
% signal being reverted. In principle we also need to take the complex
% conjugate of the reversed x, but since audio signals are real valued we
% can skip this operation.
cc = conv(x(length(x):-1:1),y);

% restrict the cross correlation result to just the relevant values.
% Values outside of this range are related to deltas bigger or smaller
% than our tolerance allows
cc = cc(winLen:end - winLen + 1);

end