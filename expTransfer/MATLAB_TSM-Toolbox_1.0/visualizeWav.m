function visualizeWav(x,parameter)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name: visualizeWav
% Date: 03-2014
% Programmer: Jonathan Driedger
% http://www.audiolabs-erlangen.de/resources/MIR/TSMtoolbox/
%
% Visualizes a waveform.
%
% Input:    x               single-channel signal.
%           parameter.
%               fsAudio     the sampling rate of the audio signal x.
%               ampRange    maximal and minimal amplitude value.
%               timeRange   can be set to visualize just a specific time
%                           frame of the signal (given in seconds).
%               title       optional title of the figure.
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
if nargin<2
    parameter=[];
end
if nargin<1
    error('Please specify input data x.');
end

if ~isfield(parameter,'fsAudio')
    parameter.fsAudio = 22050;
end
if ~isfield(parameter,'ampRange')
    parameter.ampRange = [-0.8 0.8];
end
if ~isfield(parameter,'timeRange')
    parameter.timeRange = [0 length(x)/parameter.fsAudio];
end
if ~isfield(parameter,'title')
    parameter.title = '';
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% visualization
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
t = (1:length(x))/parameter.fsAudio; % time axis

f = figure;
plot(t,x,'b');
ylim(parameter.ampRange);
xlim(parameter.timeRange);
if~isempty(parameter.title)
    title(parameter.title);
end
set(f, 'Name',parameter.title);
xlabel('Time [sec]');
ylabel('Amplitude');

end