clear; close all; clc

addpath('ml-100k');

global alpha beta numUser numMovi poolSize M maxIters tolerence T

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
tolerence    = 1e-5; 
T            = 3;

%% Process the data and obtain rate matrices

trainRateMat  = zeros(numUser, numMovi);
testRateMat   = zeros(numUser, numMovi);

for i  = 1 : dataLen * 0.8
    trainRateMat(trainSet(i, 1), trainSet(i, 2)) = trainSet(i, 3);
end

for i  = 1 : size(testSet, 1)
    testRateMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 3);  
end

poolSize  = 70000;
pool      = trainSet(1:poolSize, :);

M         = 20;
userMat   = rand(M, numUser); % use the ALS algorithm to train, instead of
moviMat   = rand(M, numMovi); % using random vectors

%% The initial phase >> train two initial matrices
iniPred   = userMat' * moviMat;
[userMat, moviMat, MAE1] = getMAE(iniPred, testRateMat); disp(MAE1);
curPred   = userMat' * moviMat;

for i = (poolSize + 1) : dataLen * 0.8
    i
    userUpool1 = pool(find(pool(:, 1) == trainSet(i, 1)), :);
        
    if inORnot(trainSet(i, 4))
        
        timeArry  = pool(:, 4);
           
        [repIdx, threshArry2] = whichOut(timeArry, trainSet(i, 4));
                
        pool(repIdx, :) = trainSet(i, :); 
           
        userUpool2 = pool(find(pool(:, 1) == trainSet(i, 1)), :);
      
        SPuIdx = SamplePositiveInput(curPred, userUpool1, trainSet(i, :));

        SNuIdx = SampleNegativeInput(curPred, userUpool2, SPuIdx, trainSet(i, :));

        uID = trainSet(i, 1);

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

nowPred = userMat' * moviMat;
getMAE  = computeMAE(testRateMat, curPred)
    
    
    
    
    
    
    
    

