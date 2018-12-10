function r=yin(x,p)
% YIN - Fundamental frequency (F0) of file or vector
%
% YIN('FILE') estimates and plots the F0 of signal in FILE.	 
%   F0 is plotted in octaves re: 440 Hz, together with residual 
%   (aperiodicity) and power measures.  A 'best' estimate is printed.
% YIN(X,SR) estimates and plots the F0 of array X assuming sampling rate SR (Hz).
%
% R=YIN(X) produces no plot but returns result in structure R:
%   R.f0: fundamental frequency in octaves re: 440 Hz
%   R.ap: aperiodicity measure (ratio of aperiodic to total power)
%   R.pwr: period-smoothed instantaneous power
%   (R also lists the parameters used by YIN)
%
% YIN(NAME,P) uses parameters stored in P:
%   P.minf0:    Hz - minimum expected F0 (default: 30 Hz)
%   P.maxf0:    Hz - maximum expected F0 (default: SR/(4*dsratio))
%   P.thresh:   threshold (default: 0.1)
%   P.relfag:   if ~0, thresh is relative to min of difference function (default: 1)
%   P.hop:      s - interval between estimates (default: 32/SR)
%   P.range:    samples - range of samples ([start stop]) to process
%   P.bufsize:  samples - size of computation buffer (default: 10000)
%	P.sr:		Hz - sampling rate (usually taken from file header)
%	P.wsize:	samples - integration window size (defaut: SR/minf0)
%	P.lpf:		Hz - intial low-pass filtering (default: SR/4)
%	P.shift		0: shift symmetric, 1: shift right, -1: shift left (default: 0)
%
% See 'yin.html' for more info.
% Version 28 July 2003.

% Alain de Cheveign? CNRS/Ircam, 2002.
% Copyright (c) 2002 Centre National de la Recherche Scientifique.
%
% Permission to use, copy, modify, and distribute this software without 
% fee is hereby granted FOR RESEARCH PURPOSES only, provided that this
% copyright notice appears in all copies and in all supporting 
% documentation, and that the software is not redistributed for any 
% fee (except for a nominal shipping charge). 
%
% For any other uses of this software, in original or modified form, 
% including but not limited to consulting, production or distribution
% in whole or in part, specific prior permission must be obtained from CNRS.
% Algorithms implemented by this software may be claimed by patents owned 
% by CNRS, France Telecom, Ircam or others.
%
% The CNRS makes no representations about the suitability of this 
% software for any purpose.  It is provided "as is" without express
% or implied warranty.


% Hidden parameters are integration window size (set equal to sr/minf0), search
% range for 'best neighboring estimate' (set equal to +/- sr/(2*minf0)), maximum
% expected width of period dip (stop/start ratio == 1.85), margin for "beam search"
% of final estimate (+1.8/-0.6 times the initial estimate).


% default parameter values ([]: to be determined)
minf0 = 30;			% Hz - minimum frequency
maxf0 = [];			% Hz - maximum frequency
wsize = []; 		% s - integration window size
lpf = [];			% Hz - lowpass prefiltering cutoff
thresh = 0.1;		% difference function threshold
relflag = 1;		% if true threshold is relative to global min of difference function
bufsize=10000;		% computation buffer size
hop = 32;			% samples - interval between estimates
range=[];			% range of file samples to process
sr=[];				% sampling rate
shift=0;			% flag to control the temporal shift of analysis windows (left/sym/right)
plotthreshold=0.2;	% aperiodicity above which plot is green or yellow

% if 2~=exist('allread')
% 	error('sf routines missing: put them in your path & try again');
% end

% handle parameters
if nargin<1; help yin; return; end
if nargin<2; p=[]; end
fileinfo=sf_info(x); if ~isempty(fileinfo.sr) p.sr=fileinfo.sr;	end % get sr from file
if fileinfo.nchans > 1
	disp(['warning: using column 1 of ', num2str(fileinfo.nchans), '-column data']); 
end
if isa(p, 'double') 
    temp = p;
    p = struct;
    p.sr=temp; 
end
if ~isfield(p, 'sr'); p.sr=sr; end
if isempty(p.sr); error('YIN2: must specify SR'); end
if ~isfield(p, 'range') | isempty(p.range); p.range=[1 fileinfo.nsamples]; end
if ~isfield(p, 'minf0'); p.minf0=minf0; end
if ~isfield(p, 'thresh'); p.thresh=thresh; end
if ~isfield(p, 'relflag'); p.relflag=relflag; end
if ~isfield(p, 'bufsize'); p.bufsize=bufsize; end
if ~isfield(p, 'hop'); p.hop=hop; end
if ~isfield(p, 'maxf0'); p.maxf0=floor(p.sr/4); end % default
if ~isfield(p, 'wsize'); p.wsize=ceil(p.sr/p.minf0); end % default
if ~isfield(p, 'lpf'); p.lpf=p.sr/4; end % default
if mod(p.hop,1); error('hop should be integer'); end
if ~isfield(p, 'shift'); p.shift=shift; end % default
if ~isfield(p, 'plotthreshold'); p.plotthreshold=plotthreshold; end % default

% estimate period
r=yink(p,fileinfo);
prd=r.r1; % period in samples
ap0=r.r2; % gross aperiodicity measure
ap= r.r3; % fine aperiodicity measure
pwr=r.r4; % period-smoothed instantaneous power
f0 = log2(p.sr ./ prd) - log2(440); 	% convert to octaves re: 440 Hz

best = f0;
best(find(ap0>p.plotthreshold)) = nan;
%best(isnan(best)) = 0;
% load estimates and major parameters in result structure
clear r;
r.f0 = f0;
r.ap0 = ap0;
r.ap = ap;
r.pwr = pwr;
r.sr = p.sr;
r.range=p.range;
r.minf0 = p.minf0;
r.maxf0 = p.maxf0;
r.thresh=p.thresh;
r.relflag=p.relflag;
r.hop = p.hop;
r.bufsize = p.bufsize;
r.wsize = p.wsize;
r.lpf = p.lpf;
r.shift = p.shift;
r.plotthreshold=p.plotthreshold;
r.best = best;

% plot estimates (if nargout == 0)
if nargout<1
	if isnan(f0)
		display('no estimates: signal too short or buffersize too small');
		return;
	end
	% choose sample to report as "the" f0 of the entire signal
	[mn, idx] = min(ap0);
	best=f0(idx);
	disp(['best: ', num2str(2^best*440), 'Hz (', note(best),...
		') at ', num2str(idx/(p.sr/p.hop)), 's (aperiodic/total power: ', num2str(mn), ')']);
	% plot f0 in 3 colors according to periodicity
	good = f0;
	good(find(ap0>p.plotthreshold*2)) = nan;
	best = f0;
	best(find(ap0>p.plotthreshold)) = nan;
	subplot(211);
	fsr=p.sr/p.hop;
	nframes=size(prd,2);
	if nframes <2; error('F0 track is too short to plot'); end
	plot((1:nframes)/fsr, f0, 'y', (1:nframes)/fsr, good, 'g', (1:nframes)/fsr, best, 'b');
	lo = max(min(f0),min(good)); hi=min(max(f0),max(good));
	set(gca, 'ylim', [lo-0.5; hi+0.5]); 
	set(gca, 'xlim', [1,nframes]/fsr);
	set(get(gca,'ylabel'), 'string', 'Oct. re: 440 Hz');
	set(get(gca,'xlabel'), 'string', 's');
	% plot periodicity
	ap0=max(0,ap0); ap=max(0,ap);
	ap1=ap;
	ap(find(ap0>plotthreshold)) = nan;
	subplot(413); plot((1:nframes), ap0.^0.5, 'b'); 
	%subplot(413); plot((1:nframes), ap0.^0.5, 'c', (1:nframes), ap1.^0.5, 'y',  (1:nframes), ap.^0.5, 'b'); 
	set(gca, 'ylim', [0 1]); 
	set(gca, 'xlim', [1, nframes]);
	set(get(gca,'ylabel'), 'string', 'sqrt(apty)');
	% plot power
	subplot(414); plot((1:nframes), sqrt(pwr), 'b');	
	set(gca, 'xlim', [1, nframes]);
	set(get(gca,'ylabel'), 'string', 'sqrt(power)');
	set(get(gca,'xlabel'), 'string', 'frames');
    if isa(x, 'double')
        set(gcf, 'Name', 'workspace matrix');
    else
        set (gcf, 'Name', x);
    end
end


% convert octave re 440 to note:
function s=note(o)
n=round(12*o);
cents = 100*(12*o-n);
oct=floor((n-3)/12)+5;
chroma=mod(n,12);
chromalist = {'A'; 'A#'; 'B'; 'C'; 'C#'; 'D'; 'D#'; 'E'; 'F'; 'F#';...
	'G'; 'G#'};
cents = sprintf('%+.0f',cents);
s=[char(chromalist(chroma+1)),num2str(oct),' ',num2str(cents), ' cents'];
