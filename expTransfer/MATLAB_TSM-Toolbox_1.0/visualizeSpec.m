function visualizeSpec(spec,parameter)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Name: visualizeSpec
% Date: 03-2014
% Programmer: Jonathan Driedger
% http://www.audiolabs-erlangen.de/resources/MIR/TSMtoolbox/
%
% Visualizes a waveform.
%
% Input:    spec             spectrogram.
%           parameter.
%               fAxis        frequency axis of the spectrogram.
%               tAxis        timeAxis of the spectrogram.
%               logComp      factor for logarithmic compression of the data
%                            for a clearer visualization.
%               visFreqRange frequency range that should be visualized.
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

if ~isfield(parameter,'fAxis')
    parameter.fAxis = 1:size(spec,1);
end
if ~isfield(parameter,'tAxis')
    parameter.tAxis = 1:size(spec,2);
end
if ~isfield(parameter,'logComp')
    parameter.logComp = 10;
end
if ~isfield(parameter,'visFreqRange')
    parameter.visFreqRange = [];
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% visualization
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
f = parameter.fAxis;
t = parameter.tAxis;
logComp = parameter.logComp;
visFreqRange = parameter.visFreqRange;

figure;
g = gray;
g = g(end:-1:1,:);

imagesc(t,f,log(1 + logComp*abs(spec)));
colormap(g);
axis xy;

if ~isempty(visFreqRange)
    ylim(visFreqRange)
end

xlabel('Time [sec]');
ylabel('Frequency [Hz]');

end