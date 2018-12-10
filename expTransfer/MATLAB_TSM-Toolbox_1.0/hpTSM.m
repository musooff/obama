function [y,sideinfo] = hpTSM(x,s,parameter,sideinfo)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name: hpTSM
% Date: 12-2013
% Programmer: Jonathan Driedger
% http://www.audiolabs-erlangen.de/resources/MIR/TSMtoolbox/
%
% hpTsm is a time-scale modification algorithm. It rescales the time-axis
% of the input signal x according to the time-stretch function s without
% altering the pitch of x. To achieve good quality results, x is first
% separated in a harmonic and a percussive component. Afterwards the two
% components are stretched using different algorithms (phase vocoder with
% identity phase locking for the harmonic component, OLA for the percussive 
% component). Finally the two TSM results are superimposed to form the 
% output. See also the paper "Improving Time-Scale Modification of Music
% Signals using Harmonic-Percussive Separation" by Driedger and Mueller.
%
% Input:  x                 input signal.
%         s                 time-stretch function. Either a constant
%                           scaling factor or a n x 2 matrix representing a
%                           set of n anchorpoints relating sample positions
%                           in the input signal with sample positions in
%                           the output signal.
%         parameter.
%          hpsAnaHop        hop size of the stft analysis window for
%                           computing the spectrogram that is used in the
%                           harmonic-percussive separation process.
%          hpsWin           the analysis and synthesis window for the stft
%                           used in the harmonic-percussive separation
%                           process.
%          hpsZeroPad       number of zeros that should be padded to the
%                           window to increase the fft size and therefore
%                           the frequency resolution.
%          hpsFilLenHarm    length of the median filter in time direction.
%          hpsFilLenPerc    length of the median filter in frequency 
%                           direction.
%          pvSynHop         hop size of the stft synthesis window for the
%                           phase vocoder
%          pvWin            the stft analysis and synthesis window of the
%                           phase vocoder.
%          pvZeroPad        number of zeros that should be padded to the
%                           window to increase the fft size and therefore
%                           the frequency resolution.
%          pvRestoreEnergy  set to 1 in case the istft in the phase vocoder
%                           should account for a potential energy loss of  
%                           the output signal.
%          pvFftShift       set to 1 in case the stft and istft in the
%                           phase vocoder should apply a circular shift by
%                           half the frame length to each frame prior to
%                           their application.
%          olaSynHop        hop size of the synthesis window used in OLA.
%          olaWin           the window used in OLA.
%
% Output: y                 the time-scale modified output signal.
%         sideinfo.
%           hpTSM.xHarm
%           hpTSM.xPerc
%           hpTSM.yHarm
%           hpTSM.yPerc
%           hpSep
%           pvTSM
%           wsolaTSM
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

% parameters: harmonic-percussive separation
if ~isfield(parameter,'hpsAnaHop')
    parameter.hpsAnaHop = 256;
end
if ~isfield(parameter,'hpsWin')
    parameter.hpsWin = win(1024,2); % hann window
end
if ~isfield(parameter,'hpsZeroPad')
    parameter.hpsZeroPad = 0;
end
if ~isfield(parameter,'hpsFilLenHarm')
    parameter.hpsFilLenHarm = 10;
end
if ~isfield(parameter,'hpsFilLenPerc')
    parameter.hpsFilLenPerc = 10;
end
% parameters: phase vocoder
if ~isfield(parameter,'pvSynHop')
    parameter.pvSynHop = 512;
end
if ~isfield(parameter,'pvWin')
    parameter.pvWin = win(2048,2); % hann window
end
if ~isfield(parameter,'pvZeroPad')
    parameter.pvZeroPad = 0;
end
if ~isfield(parameter,'pvRestoreEnergy')
    parameter.pvRestoreEnergy = 0;
end
if ~isfield(parameter,'pvFftShift')
    parameter.pvFftShift = 0;
end
% parameters: ola
if ~isfield(parameter,'olaSynHop')
    parameter.olaSynHop = 128;
end
if ~isfield(parameter,'olaWin')
    parameter.olaWin = win(256,2); % hann window
end
        
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% harmonic-percussive separation
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
parHps.anaHop = parameter.hpsAnaHop;
parHps.win = parameter.hpsWin;
parHps.zeroPad = parameter.hpsZeroPad;
parHps.filLenHarm = parameter.hpsFilLenHarm;
parHps.filLenPerc = parameter.hpsFilLenPerc;
parHps.maskingMode = 'binary';
[xHarm,xPerc,sideinfo] = hpSep(x,parHps,sideinfo);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% phase vocoder
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
parPv.synHop = parameter.pvSynHop;
parPv.win = parameter.pvWin;
parPv.zeroPad = parameter.pvZeroPad;
parPv.restoreEnergy = parameter.pvRestoreEnergy;
parPv.fftShift = parameter.pvFftShift;
parPv.phaseLocking = 1;
[yHarm,sideinfo] = pvTSM(xHarm,s,parPv,sideinfo);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% ola
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
parOla.synHop = parameter.olaSynHop;
parOla.win = parameter.olaWin;
parOla.tolerance = 0;
[yPerc,sideinfo] = wsolaTSM(xPerc,s,parOla,sideinfo);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% synthesis
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
y = yHarm + yPerc;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% update sideinfo
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
sideinfo.hpTSM.xHarm = xHarm;
sideinfo.hpTSM.xPerc = xPerc;
sideinfo.hpTSM.yHarm = yHarm;
sideinfo.hpTSM.yPerc = yPerc;

end