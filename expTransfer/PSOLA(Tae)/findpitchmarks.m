function [m] = findpitchmarks(x,Fs,F0,hop,frameLen)
% The following code is borrowed from the original MATLAB code provided
% with the DAFX book (2nd Edition).
%
% findpitchmarks.m
% Author: A. von dem Knesebeck
% x         input signal
% Fs        sampling frequency
% F0        fundamental frequencies
% hop       hop size of F0 detection
% frameLen  length of frame
%
%--------------------------------------------------------------------------
% This source code is provided without any warranties as published in 
% DAFX book 2nd edition, copyright Wiley & Sons 2011, available at 
% http://www.dafx.de. It may be used for educational purposes and not 
% for commercial applications without further permission.
%--------------------------------------------------------------------------

% Initialization
m           = 0;    % vector of pitch mark positions
P0          = zeros (1,length(F0));
index       = 1;
local_m     = [];   % local pitch marker position

% processing frames i
for i = 1:length(F0)
    % set pitch periods of unvoiced frames
    if (i==1 && F0(i)==0)
        F0(i) = 120;     % 120Hz in case no preceding pitch
    elseif (F0(i)==0)
        F0(i) = F0(i-1);
    end
    P0(i) = round(Fs/F0(i));                % fundamental period of frame i
    frameRange  = (1:frameLen) + (i-1)*hop; % hopping window
    last_m = index;                         % last found pitch mark
    
    % beginning periods of 1st frame
    j = 1;  %period number
    if i==1
        % define limits of searchFrame
        searchUpLim = 1 * P0(i);
        searchRange = (1 : searchUpLim);
        [pk,loc]  = max(x(searchRange));
        local_m(j)  = round(loc);
        
        % beginning periods of 2nd - end frame
    else
        searchUpLim = searchUpLim + P0(i);
        local_m(j)  = last_m + P0(i);
    end % beginning periods of 1st - end frame
    
    % remaining periods of 1st - end frame
    index = local_m(1);
    j = 2;  % grain/period number
    while( searchUpLim + P0(i) <= frameRange(end))
        % define range in which a marker is to be found 
        searchUpLim = searchUpLim + P0(i);
        local_m(j)  = local_m(j-1) + P0(i);
        index = local_m(j);
        j = j+1;
    end %while frame end not reached
    m = [m local_m];
end % processing frames i

% finishing calculated pitch marks
m = sort(m);
m = unique(m);
m = m(2:end);