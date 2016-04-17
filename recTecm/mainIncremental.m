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
alpha        = 1e-6;
beta         = 1e-6;
regular_u    = 1e-6;
regular_v    = 1e-6;

tolerence    = 1e-5; 
T            = 5;

%% Process the data and obtain rate matrices

poolSize  = 50000;
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

% userMat = rand(M, numUser);
% moviMat = rand(M, numMovi);
% MAE1    = computeMAE(testRateMat, userMat'*moviMat);

curPred    = userMat' * moviMat;

countIn  = [];
countOut = [];
itCount  = [];
negaMat  = zeros(20, 1);

for i = (poolSize + 1) : dataLen * 0.8
    i
    
    uID = trainSet(i, 1);
    
    userUpool1 = pool(find(pool(:, 1) == uID), :);
        
    if inORnot(trainSet(i, 4))
           
            countIn = [countIn; i];
        
            trainRateMat(trainSet(i, 1), trainSet(i, 2)) = trainSet(i, 3);

            timeArry  = pool(:, 4);

            [repIdx, threshArry2] = whichOut(timeArry, trainSet(i, 4));
            
            countOut = [countOut; repIdx];

            pool(repIdx, :) = trainSet(i, :); 

            userUpool2 = pool(find(pool(:, 1) == uID), :);

            SPuIdx = SamplePositiveInput(curPred, userUpool1, trainSet(i, :));

            SNuIdx = SampleNegativeInput(curPred, userUpool2, SPuIdx, trainSet(i, :));

%             posiIdx = randperm(length(SPuIdxRaw));
% 
%             SPuIdx = SPuIdxRaw(posiIdx(1:ceil(length(posiIdx)/2)));
% 
%             SNuIdx = [];
% 
%             negaLen = length(SNuIdxRaw);
% 
%             for iii = 1:negaLen
%                 flag = 0;
%                 if trainRateMat(uID, SNuIdxRaw(iii)) >= 3.5
%                         SNuIdx = [SNuIdx; SNuIdxRaw(iii)];
%                         flag = 1;
%                 end
%                 
%                 vec      = trainRateMat(:, SNuIdxRaw(iii));
%                 meanRate = sum(vec)/sum(vec~=0, 1);
%                 
%                 if ~flag && (trainRateMat(uID, SNuIdxRaw(iii)) == 0) && (meanRate > 3.5)
%                         SNuIdx = [SNuIdx; SNuIdxRaw(iii)];
%                 end
%             end

            for round = 1:T
                for ii = 1:length(SPuIdx)
                    rate_hat = trainRateMat(uID, SPuIdx(ii));
                    rate_avg = mean(trainRateMat(uID, SNuIdx(:)));
                    ita      = max(0, rate_hat - rate_avg);


                    if isempty(SNuIdx) 
                        nega_avg = zeros(M, 1);
                        %nega_avg = moviMat(:, SPuIdx(ii));
                    else
                        nega_avg = sum(moviMat(:, SNuIdx(:)), 2) ./ length(SNuIdx);
                    end

                    userMat(:, uID) = userMat(:, uID) + ...
                                        alpha * ita .* (moviMat(:, SPuIdx(ii)) - nega_avg) - ...
                                        alpha * beta .* userMat(:, uID);

                    moviMat(:, SPuIdx(ii)) = moviMat(:, SPuIdx(ii)) + alpha * ita .* userMat(:, uID) - ...
                                        alpha * beta .* moviMat(:, SPuIdx(ii));
                                    
                      for j = 1:length(SNuIdx)
                          moviMat(:, SNuIdx(j)) = moviMat(:, SNuIdx(j)) - alpha * ita .* userMat(:, uID) ...
                                            - alpha * beta * moviMat(:, SNuIdx(j));
                      end
                end
            end
            
            curPred   = userMat' * moviMat;
    
    end          
end    

MAE1
nowPred = userMat' * moviMat;
getMAE  = computeMAE(testRateMat, nowPred)

    
    
    
    
    
    
    
    

