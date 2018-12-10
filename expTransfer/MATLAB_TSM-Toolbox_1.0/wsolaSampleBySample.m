function [y, ps] = wsolaSampleBySample( x, alpha, beta )
%WSOLASAMPLEBYSAMPLE Summary of this function goes here
%   Detailed explanation goes here
alpha = alpha*beta;
winLen = 1024;
winLenHalf = round(winLen/2);
synHop = winLenHalf;
anaHop = round(synHop/(alpha))*beta;
w = win(winLen,2); %hann window
delta_max = 512;
%numOfChan = size(x,2);

bufferSize = 512;

y = [];ps = [];
p_xp = 1;
p_x = 1;p_w = 1;
Hp = 1 + anaHop;
while p_x < length(x) || p_xp < length(x)
    yb = [];
    for i = 1:bufferSize
        yb = [yb; read(x,p_xp)*read(w,p_w)+read(x,p_x)*read(w,p_w+winLenHalf)];
        p_xp = p_xp + beta;
        p_x = p_x + beta;
        p_w = p_w + 1;
        if p_w > winLenHalf
            p_x = p_xp;
            p_w = 1;
            Hp = Hp + anaHop;
            if p_xp == 229618
                break;
            end
            p_xp = maxSim3(x, p_xp, Hp, delta_max, winLen, beta);
            ps = [ps, p_xp];
        end
        if p_x >= length(x) || p_xp >= length(x)
            break;
        end
    end
    y = [y;yb];
end


end

function p_xp = maxSim(x, p_x_swing, p_x_plus, delta_max, winLen, beta)
    max = 0;p_xp = p_x_plus;
    for i = -delta_max:delta_max
        xcor = 0;
        for j = 0:winLen-1
            xcor = xcor + read(x,p_x_swing+j*beta)*read(x,p_x_plus+j*beta+i*beta);
        end
        if xcor > max
            max = xcor;
            p_xp = p_x_plus + i*beta;
        end
    end
end

function p_xp = maxSim2(x, p_x_swing, p_x_plus, delta_max, winLen, beta)
    C = xcorr(x(p_x_swing:p_x_swing+winLen),x(p_x_plus-delta_max:p_x_plus+delta_max));
    [~,maxIndex] = max(C);
    p_xp = p_x_plus + maxIndex;
end

function p_xp = maxSim3(x, p_x_swing, p_x_plus, delta_max, winLen, beta)
    x_swing = zeros(4096,1);
    x_plus = zeros(4096,1);
    for i = 1:1024
        x_swing(i) = read(x,p_x_swing+beta*(i-1));
    end
    for i = 1:2048
        x_plus(i) = read(x,p_x_plus+beta*(i-1)-delta_max*beta);
    end
    X_swing = fft(x_swing);
    X_plus = fft(x_plus);
    C = ifft(conj(X_swing).*X_plus);
    %c_len = floor(length(C)/2);
    %C = C([(c_len+1):end, 1:c_len]);
    [~,mx] = max(C(1:2048));
    p_xp = (mx-1)*beta+p_x_plus-delta_max*beta;
end

function y = read(x,i)
    if i < 1 || i > length(x)
        y = 0;
    elseif i + 1 > length(x)
        y = x(end)*(1+floor(i)-i);
    else
        y = x(floor(i))*(1+floor(i)-i)+(i-floor(i))*x(floor(i)+1);
        %y=x(i);
    end
end