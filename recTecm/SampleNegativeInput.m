function SNuIdx = SampleNegativeInput(curPred, userUpool2, SPuIdx, newCome)

    global numUser numMovi

    negaMoviIdx = [];

    uID = newCome(1);

    poolRateMat = zeros(numUser, numMovi);

    for i  = 1 : size(userUpool2, 1)
        poolRateMat(userUpool2(i, 1), userUpool2(i, 2)) = userUpool2(i, 3);
    end

    poolRateMat(uID, SPuIdx) = 0;

    for i = 1:numMovi
         if (((poolRateMat(uID, i) < 3.5) && (poolRateMat(uID, i)~=0)) && (curPred(uID, i) > 3.5))
                negaMoviIdx = [negaMoviIdx; i];
         elseif ((poolRateMat(uID, i) >= 3.5) && ((curPred(uID, i) <= 3.5) && (poolRateMat(uID, i)~=0)))
                negaMoviIdx = [negaMoviIdx; i];
         else
                continue;
         end
    end

    SNuIdx  = negaMoviIdx;
