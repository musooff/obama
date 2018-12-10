%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name: demoTSMtoolbox
% Date: 12-2013
% Programmer: Jonathan Driedger
% http://www.audiolabs-erlangen.de/resources/MIR/TSMtoolbox/
%
% This is the demo script which illustrates the main functionalities of the
% 'TSM toolbox'. For a detailed description we refer to  [DM14] (see 
% References below).
%
% The script proceeds in the following steps:
%   1. It loads a wav file.
%   2. It applies different TSM algorithms to the loaded signal with a
%      fixed constant stretching factor.
%   3. It visualizes the TSM results.
%   4. It writes the computed TSM results as wav files to the hard drive.
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
% initialization
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
pathData = 'data/';
pathOutput = 'output/';

filename = 'CastanetsViolin.wav';
% filename = 'Bongo.wav';
% filename = 'DrumSolo.wav';
% filename = 'Glockenspiel.wav';
% filename = 'Jazz.wav';
% filename = 'Pop.wav';
% filename = 'SingingVoice.wav';
% filename = 'Stepdad.wav';
% filename = 'SynthMono.wav';
% filename = 'SynthPoly.wav';

alpha = 1.8; % constant stretching factor

warning('OFF','MATLAB:audiovideo:audiowrite:dataClipped');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1. load the audio signal
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[x,fsAudio] = audioread([pathData filename]);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 2. compute TSM results
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% OLA
paramOLA.tolerance = 0;
paramOLA.synHop = 128;
paramOLA.win = win(256,2); % hann window
yOLA = wsolaTSM(x,alpha,paramOLA);

% WSOLA
yWSOLA = wsolaTSM(x,alpha);

% Phase Vocoder
yPV = pvTSM(x,alpha);

% Phase Vocoder with identity phase locking
paramPVpl.phaseLocking = 1;
yPVpl = pvTSM(x,alpha,paramPVpl);

% TSM based on HPSS
yHP = hpTSM(x,alpha);

% elastique
% To execute elastique, you will need an access id from 
% http://www.sonicapi.com. Furthermore, you need to download 'curl'
% from http://curl.haxx.se/download.html. For further information, see the
% function header of the file elastiqueTSM.m.

% paramElast.fsAudio = fsAudio;
% yELAST = elastiqueTSM(x,alpha,paramElast);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 3. visualize TSM results
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Original
timeRange =  [5.1 5.3];
paramVis.timeRange = timeRange;
paramVis.title = 'Original';
visualizeWav(x,paramVis);

timeRange = timeRange * alpha;
paramVis.timeRange = timeRange;

% OLA
paramVis.title = 'OLA';
visualizeWav(yOLA,paramVis);

% WSOLA
paramVis.title = 'WSOLA';
visualizeWav(yWSOLA,paramVis);

% Phase Vocoder
paramVis.title = 'Phase Vocoder';
visualizeWav(yPV,paramVis);

% Phase Vocoder with identity phase locking
paramVis.title = 'Phase Vocoder with identity phase locking';
visualizeWav(yPVpl,paramVis);

% TSM based on HPSS
paramVis.title = 'HP-TSM';
visualizeWav(yHP,paramVis);

% elastique
% paramVis.title = 'elastique';
% visualizeWav(yELAST,paramVis);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 4. write TSM results
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% OLA
audiowrite([pathOutput filename(1:end-4)...
    '_' sprintf('%0.2f',alpha) '_OLA.wav'],yOLA,fsAudio);

% WSOLA
audiowrite([pathOutput filename(1:end-4)...
    '_' sprintf('%0.2f',alpha) '_WSOLA.wav'],yWSOLA,fsAudio);

% Phase Vocoder
audiowrite([pathOutput filename(1:end-4)...
    '_' sprintf('%0.2f',alpha) '_PV.wav'],yPV,fsAudio);

% Phase Vocoder with identity phase locking
audiowrite([pathOutput filename(1:end-4)...
    '_' sprintf('%0.2f',alpha) '_PVpl.wav'],yPVpl,fsAudio);

% TSM based on HPSS
audiowrite([pathOutput filename(1:end-4)...
    '_' sprintf('%0.2f',alpha) '_HP.wav'],yHP,fsAudio);

% elastique
% wavwrite(yELAST,fsAudio,[pathOutput filename(1:end-4)...
%     '_' sprintf('%0.2f',alpha) '_ELAST.wav']);
