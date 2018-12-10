function [spec,f,t,sideinfo] = stft(x,parameter,sideinfo)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name: stft
% Date: 12-2013
% Programmer: Jonathan Driedger
% http://www.audiolabs-erlangen.de/resources/MIR/TSMtoolbox/
%
% Computes the short-time Fourier transform (stft) of the input audio 
% signal.
%
% Input:    x               single-channel signal.
%           parameter.
%               anaHop      either the constant hop size of the analysis 
%                           window or a vector of analysis positions in the 
%                           input signal.
%               win         the analysis window used for windowing the
%                           input signal.
%               zeroPad     number of zeros that should be padded to the
%                           window to increase the fft size and therefore
%                           the frequency resolution.
%               fsAudio     the sampling rate of the input audio signal x.
%               numOfFrames can be set to fix the number of spectra that 
%                           should be computed.
%               fftShift    can be set to 1 to apply a circular shift of 
%                           samples to each frame by half its length prior 
%                           to the application of the fft. 
%
% Output:   spec            complex spectrogram
%           f               vector of the center frequencies of all Fourier
%                           bins given in Hertz.
%           t               vector specifying the time instances in seconds
%                           where the respective Fourier spectra were
%                           computed.
%           sideinfo.
%               stft.anaHop
%               stft.win
%               stft.zeroPad
%               stft.featureRate
%               stft.originalLength
%               stft.fsAudio
%               stft.fftShift
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
if nargin<3
    sideinfo=[];
end
if nargin<2
    parameter=[];
end
if nargin<1
    error('Please specify input data x.');
end

if ~isfield(parameter,'anaHop')
    parameter.anaHop = 2048;
end
if ~isfield(parameter,'win')
    parameter.win = win(4096,2); % hann window
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
if ~isfield(parameter,'fftShift')
    parameter.fftShift = 0;
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% some pre calculations
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% zeropad the window
w = parameter.win;
w = w(:);
zp = parameter.zeroPad;
w = [zeros(floor(zp/2),1);w;zeros(floor(zp/2),1)];
winLen = length(w);
winLenHalf = round(winLen/2);

fsAudio = parameter.fsAudio;
signalLength = length(x);
anaHop = parameter.anaHop;

% Pad the audio to center the windows and to avoid problems at the end
maxAnaHop = max(anaHop);
xPadded = [zeros(winLenHalf,1);x;zeros(winLen+maxAnaHop,1)];

% in case anaHop is a scalar, sample the window positions evenly in the
% input signal
if isscalar(anaHop)
    if parameter.numOfFrames >= 0
        numOfFrames = parameter.numOfFrames;
    else
        numOfFrames = floor((length(xPadded) - winLen)/anaHop + 1);
    end
    winPos = (0:numOfFrames-1) * anaHop + 1;
else
    if parameter.numOfFrames >= 0
        numOfFrames = parameter.numOfFrames;
    else
        numOfFrames = length(anaHop);
    end
    winPos = anaHop(1:numOfFrames);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% spectrogram calculation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
spec = zeros(winLenHalf+1,numOfFrames);
for i = 1 : numOfFrames
    xi = xPadded(winPos(i):winPos(i) + winLen - 1) .* w;
    if parameter.fftShift == 1
        xi = fftshift(xi);
    end
    Xi = fft(xi);
    spec(:,i) = Xi(1:winLenHalf+1);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% axis calculation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
t = (winPos - 1) ./ fsAudio;
f = (0 : winLenHalf) * fsAudio / winLen;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% update sideinfo
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sideinfo.stft.anaHop = parameter.anaHop;
sideinfo.stft.win = parameter.win;
sideinfo.stft.zeroPad = parameter.zeroPad;
if isscalar(anaHop)
    sideinfo.stft.featureRate = fsAudio/anaHop;
else
    sideinfo.stft.featureRate = 'variable';
end
sideinfo.stft.originalLength = signalLength;
sideinfo.stft.fsAudio = parameter.fsAudio;
sideinfo.stft.fftShift = parameter.fftShift;

end
