%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name: demoNonlinearTSM
% Date: 03-2014
% Programmer: Jonathan Driedger
% http://www.audiolabs-erlangen.de/resources/MIR/TSMtoolbox/
%
% This is a demo script which shows how non-linear TSM can be performed
% using the TSM algorithms in the 'TSM toolbox'.
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
filenameWav1 = 'BeethovenPiano.wav';
filenameWav2 = 'BeethovenOrchestra.wav';
filenameAP = 'BeethovenAnchorpoints.mat';

warning('OFF','MATLAB:audiovideo:audiowrite:dataClipped');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% load the data and the anchorpoints
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[x1,~      ] = audioread([pathData filenameWav1]);
[x2,fsAudio] = audioread([pathData filenameWav2]);
mat = load([pathData filenameAP]);
anchorpoints = mat.anchorpoints;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% visualize the anchorpoints
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
paramVis.fsAudio = fsAudio;
visualizeAP(anchorpoints);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% synchronization using TSM based on HPSS
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% here we fit the time axis of the orchestra version to the time axis of 
% the piano version
y = hpTSM(x2,anchorpoints);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% write results
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% unsynchronized recordings
% write stereo file: left channel: original piano version, right channel:
% unstretched orchestra version
x2_padded = [x2;zeros(size(x1,1)-size(x2,1),size(x2,2))];
audiowrite(...
    [pathOutput 'BeethovenPianoOrchestra_unsync.wav'],[x1 x2_padded],fsAudio);

% synchronized recordings
% write stereo file: left channel: original piano version, right channel:
% stretched orchestra version
audiowrite(...
    [pathOutput 'BeethovenPianoOrchestra_sync.wav'],[x1 y],fsAudio);
