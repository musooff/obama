function y = solaSampleBySample( x, alpha, beta )
%SOLASAMPLEBYSAMPLE Summary of this function goes here
%   Detailed explanation goes here
    x = x(:,1);
    y = [];

    winSize = 4096;
    halfWinSize = round(winSize/2);
    hopSize = round(halfWinSize/(alpha*beta));
    win = hann(winSize);
    
    i = 0;
    ptr = mod(i, halfWinSize) + 1;itp = 0;k=halfWinSize + ptr;
    winNum = floor(i/halfWinSize);
        
    j = hopSize*(winNum+1)-halfWinSize+ptr;
    while j+1 < length(x) && hopSize*winNum+ceil(ptr) < length(x)
        if j <= 0
            x2 = 0;
        else
            x2 = x(j)*(1-itp)+itp*x(j+1);
        end
        
        if k + 1 >= winSize
            k = winSize;
        end
        y = [y; (win(halfWinSize + ptr)*(1-itp)+itp*win(k))*(x(hopSize*winNum+ptr)*(1-itp)+itp*x(hopSize*winNum+ptr+1))+(win(ptr)*(1-itp)+itp*win(ptr+1))*x2];
        
        i = i + beta;
        ptr = mod(floor(i), halfWinSize) + 1;itp = i - floor(i);
        winNum = floor(i/halfWinSize);
        
        j = hopSize*(winNum+1)-halfWinSize+floor(ptr);
        k = halfWinSize + ptr;
    end

%     i = 0;
%     y = zeros(2*length(x),1);
%     while i*hopSize+winSize < length(x)
%         y(i*halfWinSize+1:i*halfWinSize+winSize) = y(i*halfWinSize+1:i*halfWinSize+winSize) + win.*x(i*hopSize+1:i*hopSize+winSize);
%         
%         i = i + 1;
%     end

end

