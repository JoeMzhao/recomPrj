function [Wu, Hp] = increUpdate (pool, Wu, Hp)

    global alpha beta
    
    newRate = pool(1, 3);
    
    snIdx = find(pool(:, 3) <= 3);
    spIdx = find(pool(:, 3) >  3);
    
    avgSN = mean(pool(snIdx, 3));  
    ita   = max(0, newRate - avgSN);
    
%     sigRa = sum(Hp(snIdx)) / (length(snIdx));
    sigRa = 0;
    
    Wu = Wu + alpha * ita * (Hp - sigRa) - alpha * beta * Wu;
    Hp = Hp + alpha * ita * Wu - alpha * beta * Hp;
    
  
    
    
    