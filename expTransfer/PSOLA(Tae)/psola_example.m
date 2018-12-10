% Time stretching by PSOLA
%
% Version 0.1, May-10-2015 
%
% By Juhan Nam, KAIST
% 

addpath(genpath('yin'));

file_name = 'yeah(C-C-C)';
[x,fs]=audioread('yeah(C-C-C).wav');

x = x(:,1);

%x2 = x((length(x)/gamma):length(x),:);

% time stretching ratio
alpha = 1.0;

% pitch shifting ratio
beta = 1.2;

P.hop = 64;
P.wsize = 256;
P.sr = fs;

% pitch detection by YIN
warning off;
R = yin(x,P);
warning on;

% convert to Hertz 
f0 = 440.0 * 2.^ R.f0;
f0(isnan(f0)) = 0;
%%
%f1=f0(:,(length(f0)/gamma)-1:length(f0));

% find pitch mark
marks = findpitchmarks(x, fs, f0, R.hop, R.wsize);

% PSOLA
y = psola(x, marks, alpha, beta);

% 
% x1 = x(1:((length(x)/gamma)-1),:);
% 
% x1 = x1';
% 
% y = [x1 y2];

soundsc(y,fs);
%soundsc(y, fs);

