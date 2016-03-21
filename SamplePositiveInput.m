function SPuIdx = SamplePositiveInput(curPred, userUpool1, newCome)

    global numUser numMovi
    
    posiMoviIdx = [];
    
    uID = newCome(1);
    
    userUpool1 = [userUpool1; newCome];
    
    poolRateMat = zeros(numUser, numMovi);
    
    for i  = 1 : size(userUpool1, 1)
        poolRateMat(userUpool1(i, 1), userUpool1(i, 2)) = userUpool1(i, 3);
    end
    
    for i = 1:numMovi
         if ((poolRateMat(uID, i) > 3.5) && (curPred(uID, i) > 3.5))              
                posiMoviIdx = [posiMoviIdx; i];
         elseif ((poolRateMat(uID, i) <= 3.5) && (poolRateMat(uID, i)~=0) ...
                 && ((poolRateMat(uID, i)~=0) && (curPred(uID, i) <= 3.5)))
                posiMoviIdx = [posiMoviIdx; i];
         else
                continue;
         end
    end
    
    SPuIdx  = posiMoviIdx;
    
                
                
                
