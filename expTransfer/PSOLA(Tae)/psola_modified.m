function [out, prev_en] =psola_modified(in,m,alpha,beta)
% The following code is borrowed from the original MATLAB code provided
% with the DAFX book (2nd Edition).
%
% psola.m
% Authors: G. De Poli, U. Z?lzer, P. Dutilleux
%     in    input signal
%     m     pitch marks
%     alpha time stretching factor
%     beta  pitch shifting factor
%
%--------------------------------------------------------------------------
% This source code is provided without any warranties as published in
% DAFX book 2nd edition, copyright Wiley & Sons 2011, available at
% http://www.dafx.de. It may be used for educational purposes and not
% for commercial applications without further permission.
%--------------------------------------------------------------------------


P = diff(m);   %compute pitch periods

if m(1)<=P(1) %remove first pitch mark
    m=m(2:length(m));
    P=P(2:length(P));
end

if m(length(m))+P(length(P))>length(in) %remove last pitch mark
    m=m(1:length(m));
else
    P=[P P(length(P))];
end


Lout=ceil(length(in)*alpha);
out=zeros(1,Lout); %output signal

tk = P(1)+1;       %output pitch mark
k = 0;
while round(tk)<Lout
    k= k+1;
    [minimum, i] = min( abs(alpha*m - tk) ); %find analysis segment
    pit=P(i);
    
    
    % Starting & Last Window 
    ones_win = ones(2*pit+1,1);
    temp_win = hanning(2*pit+1);
    st_win = [ones_win(1: ceil(length(ones_win)/2)) ; temp_win(ceil(length(temp_win)/2)+1:length(temp_win))];
    en_win = [temp_win(1:ceil(length(temp_win)/2)) ; ones_win(ceil(length(ones_win)/2)+1: length(ones_win))];
    
    if m(i)+pit > length(in)
        in = [in; zeros(m(i)+pit - length(in),1)];
    end
    
    st=m(i)-pit;
    en=m(i)+pit;
    
    % CHANGING WINDOW FOR STARTING SEGMENT
    
    % Windowing for the rest of frame + selection of segment from input
    if(k > 1)
        gr = in(st:en) .* hanning(2*pit+1);
    end
    
    % Starting Windowing (first segment of the frame) 
    if( k == 1)
        gr = in(st:en) .* st_win;        
    end
    
    % Output segment indexing (iniGr: starting, endGr: ending)
    % Segment's length is 2 * pit + 1
    
    iniGr=round(tk)-pit;
    endGr=round(tk)+pit;
    

    % Loop ENDING 
    %   Giving window with half rectangular window at the end
    %   ???????? ?????? ???? ?????????? return??????...
    %
    if endGr>Lout
        
        gr = in(st:en) .* en_win;
        out(iniGr:Lout) = out(iniGr:Lout)+gr(1:Lout-iniGr+1)';

        if(prev_en > 2048)
            prev_en = 2048;
        end
        
        break;
    end
    
    % Input?? Last Segment Ending Index
    prev_en = en;
    
    % Output?? Last Previous Ending Index
    prev_endGr = endGr;

    out(iniGr:endGr) = out(iniGr:endGr)+gr'; %overlap new segment
    tk=tk+pit/beta;
        
end