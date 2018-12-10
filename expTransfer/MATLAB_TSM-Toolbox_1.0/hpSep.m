function [xHarm,xPerc,sideinfo] = hpSep(x,parameter,sideinfo)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name: hpSep
% Date: 03-2014
% Programmer: Jonathan Driedger
% http://www.audiolabs-erlangen.de/resources/MIR/TSMtoolbox/
%
% Seperates a given audio signal into a harmonic and a percussive component
% according to the paper "Harmonic/Percussive Separation using Median
% Filtering" by Fitzgerald.
%
% Input:  x                 input signal.
%         parameter.
%          anaHop           the stft hop size of the analysis window.
%          win              the stft analysis window used for windowing the
%                           input signal.
%          zeroPad          number of zeros that should be padded to the
%                           window to increase the fft size and therefore
%                           the frequency resolution.
%          filLenHarm       length of the median filter in time direction.
%          filLenPerc       length of the median filter in frequency
%                           direction.
%          maskingMode      either 'binary' or 'relative'. Specifies if a
%                           binary or a relative weighting mask should be
%                           applied to the spectrogram to perform the
%                           separation.
%
% Output: xHarm             the harmonic component of the input signal x.
%         xPerc             the percussive component of the input signal x.
%
%         sideinfo.
%            hpSep.stftAnaHop
%            hpSep.win
%            hpSep.zeroPad
%            hpSep.filLenHarm
%            hpSep.filLenPerc
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
if nargin < 3
    sideinfo = [];
end
if nargin < 2
    parameter = [];
end
if nargin<2
    error('Please specify input data x.');
end

if ~isfield(parameter,'anaHop')
    parameter.anaHop = 256;
end
if ~isfield(parameter,'win')
    parameter.win = win(1024,2); % hann window
end
if ~isfield(parameter,'zeroPad')
    parameter.zeroPad = 0;
end
if ~isfield(parameter,'filLenHarm')
    parameter.filLenHarm = 10;
end
if ~isfield(parameter,'filLenPerc')
    parameter.filLenPerc = 10;
end
if ~isfield(parameter,'maskingMode')
    parameter.maskingMode = 'binary';
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% some pre calculations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
anaHop = parameter.anaHop;
w = parameter.win;
zeroPad = parameter.zeroPad;
filLenHarm = parameter.filLenHarm;
filLenPerc = parameter.filLenPerc;
maskingMode = parameter.maskingMode;
numOfChan = size(x,2);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% harmonic-percussive separation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
xHarm = zeros(size(x,1),numOfChan);      % Initialize output
xPerc = zeros(size(x,1),numOfChan);      % Initialize output

for c = 1 : numOfChan                   % loop over channels
xC = x(:,c);

% stft
parStft.anaHop = anaHop;
parStft.win = w;
parStft.zeroPad = zeroPad;
spec = stft(xC,parStft);
magSpec = abs(spec);

% harmonic-percussive separation
magSpecHarm = medianFilter(magSpec,filLenHarm,2);
magSpecPerc = medianFilter(magSpec,filLenPerc,1);

switch maskingMode
    case 'binary'
        maskHarm = magSpecHarm >  magSpecPerc;
        maskPerc = magSpecHarm <= magSpecPerc;
        
    case 'relative'
        maskHarm = magSpecHarm ./ (magSpecHarm + magSpecPerc);
        maskPerc = magSpecPerc ./ (magSpecHarm + magSpecPerc);
        
    otherwise
        error('maskingMode must either be "binary" or "relative"');
end

specHarm = maskHarm .* spec;
specPerc = maskPerc .* spec;

% istft
parIstft.synHop = parameter.anaHop;
parIstft.win = parameter.win;
parIstft.zeroPad = parameter.zeroPad;
parIstft.numOfIter = 1;
parIstft.origSigLen= length(x);
xHarmC = istft(specHarm,parIstft);
xPercC = istft(specPerc,parIstft);

xHarm(:,c) = xHarmC;
xPerc(:,c) = xPercC;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% update sideinfo
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sideinfo.hpSep.stftAnaHop = parameter.anaHop;
sideinfo.hpSep.win = parameter.win;
sideinfo.hpSep.zeroPad = parameter.zeroPad;
sideinfo.hpSep.filLenHarm = parameter.filLenHarm;
sideinfo.hpSep.filLenPerc = parameter.filLenPerc;

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% median filter
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function Y = medianFilter(X,len,dim)

s = size(X);
Y = zeros(s);

switch dim
    case 1
        XPadded = [zeros(floor(len/2),s(2));X;zeros(ceil(len/2),s(2))];
        for i = 1 : s(1)
            Y(i,:) = median(XPadded(i:i+len-1,:),1);
        end
        
    case 2
        XPadded = [zeros(s(1),floor(len/2)) X zeros(s(1),ceil(len/2))];
        for i = 1 : s(2)
            Y(:,i) = median(XPadded(:,i:i+len-1),2);
        end
        
    otherwise
        error('unvalid dim.')
end 

end