function [idx, threArry2] = whichOut (timeArry, timestamp)
    threArry1 = exp(1./(timestamp - timeArry));
    buff      = - exp (- threArry1);
    threArry2 = 1 - exp(buff); % the out threshold. 
    probArry  = rand(size(timeArry, 1), 1);
    
    idx = find((threArry2-probArry) == max(threArry2 - probArry));
    
    
    
end
