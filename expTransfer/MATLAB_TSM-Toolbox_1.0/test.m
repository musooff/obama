fs = 44100;
a = sin(2*pi*440*(1:88200)/fs)';
rate = 1.5 - 0.5*cos(2*pi*(1:88200)/88200);

b = [];
pointer = 1;
p = pointer;
while pointer <= length(a)
    pf = floor(pointer);
    pc = ceil(pointer);
    pmid = pointer - pf;
    b = [b; (1-pmid)*a(pf) + pmid*a(pc)];
    
    pointer = pointer + (1-pmid)*rate(pf)+pmid*rate(pc);
    p = [p pointer];
end

%soundsc(b,fs);

%vq1 = interp1((1:88200),a,p);

rate2 = [22050 1.25; 44100 1.5; 66150 1.75; 88200 2];

c = [];
pointer = 1;
rateCounter = 1;
newPoint = [];
while pointer <= length(a)
    pf = floor(pointer);
    pc = ceil(pointer);
    pmid = pointer - pf;
    c = [c; (1-pmid)*a(pf) + pmid*a(pc)];
    if pointer > rate2(rateCounter,1)
        rateCounter = rateCounter + 1;
        newPoint = [newPoint; length(c)];
    end
    pointer = pointer + (1-pmid)*rate2(rateCounter,2)+pmid*rate2(rateCounter,2);
end

s = [1;newPoint;length(c)];
ss = s(2:end) - s(1:end-1);
ss = ss.*rate2(:,2);
ss = [1;ss];
for i = 2:length(ss)
    ss(i) = ss(i)+ss(i-1);
end
s = [s,ss];
d = hpTSM(c,s);








