clear; close all; clc

addpath('ml-100k');

global alpha beta numUser numMovi poolSize M maxIters tolerence T regular_u regular_v

rawData      = load('u.data');
sorted       = sortrows(rawData, 4);
sorted(:, 4) = 1:size(sorted, 1); 
dataLen      = size(sorted, 1);

trainSet     = sorted(1:0.8 * dataLen, :);
testSet      = sorted(0.8 * dataLen + 1 : end, :);

numUser      = 943;
numMovi      = 1682;
maxIters     = 100; 
alpha        = 1e-5;
beta         = 1e-5;
regular_u    = 0.1;
regular_v    = 0.1;
tolerence    = 1e-5; 
T            = 5;

%% Process the data and obtain rate matrices

poolSize  = 75000;
pool      = trainSet(1:poolSize, :);
M         = 20;


trainRateMat  = zeros(numUser, numMovi);
testRateMat   = zeros(numUser, numMovi);

for i  = 1 : poolSize
    trainRateMat(trainSet(i, 1), trainSet(i, 2)) = trainSet(i, 3);
end

for i  = 1 : size(testSet, 1)
    testRateMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 3);  
end


%% The initial phase >> train two initial matrices
[userMat, moviMat, MAE1] = getMAE(trainRateMat, testRateMat);
curPred   = userMat' * moviMat;

for i = (poolSize + 1) : dataLen * 0.8
    i
    curPred   = userMat' * moviMat;
    
    userUpool1 = pool(find(pool(:, 1) == trainSet(i, 1)), :);
        
    if inORnot(trainSet(i, 4))
        
        trainRateMat(trainSet(i, 1), trainSet(i, 2)) = trainSet(i, 3);
        
        uID = trainSet(i, 1);
        
        timeArry  = pool(:, 4);
           
        [repIdx, threshArry2] = whichOut(timeArry, trainSet(i, 4));
                
        pool(repIdx, :) = trainSet(i, :); 
           
        userUpool2 = pool(find(pool(:, 1) == trainSet(i, 1)), :);
      
        SPuIdxRaw = SamplePositiveInput(curPred, userUpool1, trainSet(i, :));

        SNuIdxRaw = SampleNegativeInput(curPred, userUpool2, SPuIdxRaw, trainSet(i, :));
        
        posiIdx = randperm(length(SPuIdxRaw));
       
        SPuIdx = SPuIdxRaw(posiIdx(1:ceil(length(posiIdx)/2)));
        
        SNuIdx = [];
        
        negaLen = length(SNuIdxRaw);
        
        for iii = 1:negaLen
            if curPred(uID, SNuIdxRaw(iii)) >= 3.8
                    SNuIdx = [SNuIdx; SNuIdxRaw(iii)];
            end
            if (trainRateMat(uID, SNuIdxRaw(iii)) == 0) && (mean(trainRateMat(:, SNuIdxRaw(iii))>3.8))
                    SNuIdx = [SNuIdx; SNuIdxRaw(iii)];
            end
        end
        
                      
        for round = 1:T
            for ii = 1:length(SPuIdx)
                rate_hat = curPred(uID, SPuIdx(ii));
                rate_avg = mean(curPred(uID, SNuIdx(:)));
                ita      = max(0, rate_hat - rate_avg);
                
                if isempty(SNuIdx) 
                    nega_avg = zeros(M, 1);
                else
                    nega_avg = sum(moviMat(:, SNuIdx(:)), 2) ./ length(SNuIdx);
                end

                userMat(:, uID) = userMat(:, uID) + ...
                                    alpha * ita .* (moviMat(:, ii) - nega_avg) - ...
                                    alpha * beta .* userMat(:, uID);

                moviMat(:, ii) = moviMat(:, ii) + alpha * ita .* userMat(:, uID) - ...
                                    alpha * beta .* moviMat(:, ii);
                  for j = 1:length(SNuIdx)
                      moviMat(:, j) = moviMat(:, j) - alpha * ita .* userMat(:, uID) ...
                                        - alpha * beta * moviMat(:, j);
                  end
            end
        end
    
    end          
end    

MAE1
nowPred = userMat' * moviMat;
getMAE  = computeMAE(testRateMat, nowPred)

    
    
    
    
    
    
    
    

