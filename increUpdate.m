function [Wu, moviMat] = increUpdate (pool, userMat, moviMat, Wu)

    global alpha beta
    
    snIdx = find(pool(:, 3) <= 3);
    spIdx = find(pool(:, 3) >  3);
    
    numNega = length(snIdx);
    numPosi = length(spIdx);
    
    avgSN = mean(pool(snIdx, 3));
    avgNH = sum(moviMat(:, snIdx), 2) ./ numNega ;
    
for i = 1:numPosi
        
   ratePosi = pool(spIdx(i), 3);
   ita      = max(0, ratePosi - avgSN);
    

   Wu = Wu + alpha * ita * (moviMat(:, spIdx(i)) - avgNH)- alpha * beta * Wu;
    
   moviMat(:, spIdx(i)) = moviMat(:, spIdx(i)) + alpha * ita .* Wu - ...
                                    alpha * beta .* moviMat(:, spIdx(i));
   
   for j = 1:numNega
       moviMat(:, snIdx(j)) = moviMat(:, snIdx(j)) - alpha * ita * Wu - ...
                                alpha * beta * moviMat(:, snIdx(j));
   end
   
end

                
    
    
  
    
    
    