function y = max_filter(x, k)
% x: spectrogram 
% y: max_filtered spectrogram

y = zeros(size(x));

for i=1:size(x,2)
    for j=1:size(x,1)
        if j <= k
            y(j,i) = max(x(1:j+k,i));
        elseif j >= size(x,1) - k
            y(j,i) = max(x(j-k:j,i));
        else
            y(j,i) = max(x(j-k:j+k,i));
        end
    end
end


