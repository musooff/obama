x = sawtooth(2*pi*440*(1:8192)/44100);x = x';
w = win(2048,1);
X = zeros(2048,13);
for i = 1:13
    X(:,i) = fft(x(1+512*(i-1):2048+512*(i-1)).*w);
end

y = zeros(8192,1);
ow = zeros(8192,1);
for i = 1:13
    y(1+512*(i-1):2048+512*(i-1)) = y(1+512*(i-1):2048+512*(i-1)) + ifft(X(:,i)).*w;
    ow(1+512*(i-1):2048+512*(i-1)) = ow(1+512*(i-1):2048+512*(i-1)) + w.^2;
end

ow(ow<10^-3) = 1; % avoid potential division by zero
y = y ./ ow;