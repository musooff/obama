function y = pvSampleBySample( x, alpha, beta )
%WSOLASAMPLEBYSAMPLE Summary of this function goes here
%   Detailed explanation goes here
winLen = 2048;
winLenHalf = round(winLen/2);
synHop = 512;
anaHop = round(synHop/(alpha*beta));
%w = [zeros(winLenHalf/2,1);win(winLenHalf,2);zeros(winLenHalf/2,1)]; %hann window
w = win(winLen,2);

bufferSize = 512;

X = zeros(winLen,2);
XMod = zeros(winLen,4);
xMod = zeros(winLen,4);

y = [];
p_xp = 1;

count = -3;
for i = 1:4
    xm = [];
    p_x = count*anaHop*beta;count = count + 1;
    for j = 1:winLen
        xm = [xm; read(x,p_x)];
        p_x = p_x + beta;
    end
    X(:,1) = X(:,2);
    X(:,2) = fft(xm.*w);
    
    if i == 1
        XMod(:,i) = X(:,2);
    else
        XMod(:,i) = phaseMod(XMod(:,i-1),X(:,1),X(:,2),winLen,anaHop,synHop);
    end
    xMod(:,i) = real(ifft(XMod(:,i))).*w;
end

% for i = 2:4
%     XMod(:,i) = phaseMod(XMod(:,i-1),X(:,i-1),X(:,i),winLen,anaHop,synHop);
%     xMod(:,i) = ifft(XMod(:,i)).*w;
% end

while p_x < length(x)+winLen*beta
    yb = [];
    for i = 1:bufferSize
        if p_xp <= winLen / 4
            yb = [yb; xMod(p_xp+synHop*3,1) + xMod(p_xp+synHop*2,2) + xMod(p_xp+synHop,3) + xMod(p_xp,4)];
            p_xp = p_xp + 1;
        else
            XMod(:,1) = XMod(:,2);XMod(:,2) = XMod(:,3);XMod(:,3) = XMod(:,4);
            xMod(:,1) = xMod(:,2);xMod(:,2) = xMod(:,3);xMod(:,3) = xMod(:,4);
            X(:,1) = X(:,2);
            xm = [];
            p_x = count*anaHop*beta;count = count + 1;
            for j = 1:winLen
                xm = [xm; read(x,p_x)];
                p_x = p_x + beta;
            end
            X(:,2) = fft(xm.*w);
            XMod(:,4) = phaseMod(XMod(:,3),X(:,1),X(:,2),winLen,anaHop,synHop);
            xMod(:,4) = real(ifft(XMod(:,4))).*w;
            p_xp = 1;
        end
    end
    y = [y;yb/1.5];
end


end

function XMod = phaseMod(XMod_1,Xm_1,Xm,winLen,anaHop,synHop)
    XMod_1 = XMod_1(1:1+winLen/2);
    Xm_1 = Xm_1(1:1+winLen/2);
    Xm = Xm(1:1+winLen/2);

    k = (0:winLen/2)';
    omega = 2*pi*k/winLen;
    omegaT = omega*anaHop;
    phiPred = angle(Xm_1) + omegaT;
    phiDiff = angle(Xm) - phiPred;
    phiErr = phiDiff - 2*pi*round(phiDiff/(2*pi));
    
    ipa_sample = (omega+phiErr/anaHop);
    ipa_hop = ipa_sample * synHop;
    
    theta = angle(XMod_1) + ...             % Phases of the last output frame
            ipa_hop - ...               % Instantaneous phase advance
            angle(Xm);                     % Phases of the current input frame
    phasor = exp(1i*theta);
    
    XMod = phasor .* Xm;
    XMod = [XMod ; conj(flip(XMod(2:end-1)))];
end

function y = read(x,i)
    if i < 1 || i > length(x)
        y = 0;
    elseif i + 1 > length(x)
        y = x(end)*(1+floor(i)-i);
    else
        y = x(floor(i))*(1+floor(i)-i)+(i-floor(i))*x(floor(i)+1);
    end
end