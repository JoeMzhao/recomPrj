clear; close all; clc

addpath('ml-100k');

global alpha beta numUser numMovi poolSize M maxIters tolerence T  

rawData      = load('u.data');
sorted       = sortrows(rawData, 4);
sorted(:, 4) = 1:size(sorted, 1); 
dataLen      = size(sorted, 1);

trainSet     = sorted(1:0.95 * dataLen, :);
testSet      = sorted(0.95 * dataLen + 1 : end, :);

numUser      = 943;
numMovi      = 1682;
maxIters     = 100; 
alpha        = 1e-6;
beta         = 1e-6;
tolerence    = 1e-5; 
T            = 5;

%% Process the data and obtain rate matrices

poolSize  = 90000;
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
%[userMat, moviMat, MAE1] = getMAE(trainRateMat, testRateMat);

userMat = rand(M, numUser);
moviMat = rand(M, numMovi);

releventSet = unique(testSet(:, 1));
for j = 1:size(testSet, 1)
        idx = find(releventSet(:, 1) == testSet(j, 1));
        len = length(find(releventSet(idx, :)~=0));
        releventSet(idx, len + 1) = testSet(j, 2);
end

uniOn   = cell(301, 2);

for i = 1:301
    uniOn{i, 1} = releventSet(i, 1);
end

curPred = userMat' * moviMat;


N       = 10;
num5test = 0;
numHits  = 0;

for i = 1:length(testSet)
            i
            
           uID    = testSet(i, 1);
           moviID = testSet(i, 2);
           
           if testSet(i, 3) >= 4
               num5test = num5test + 1;
           end
           % if inORnot(trainSet(i, 4))

           trainRateMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 3);
           
          % timeArry  = pool(:, 4);
           
          % [repIdx, threshArry2] = whichOut(timeArry, trainSet(i, 4));
           
          % pool(repIdx, :) = trainSet(i, :);
           
          % userUpool2 = pool(find(pool(:, 1) == uID), :);
           
           SPuIdx = SamplePositiveInput(curPred, userUpool1, trainSet(i, :));          
           SNuIdx = SampleNegativeInput(curPred, userUpool2, SPuIdx, trainSet(i, :));
           
           
           for round = 1:T
               for ii = 1:length(SPuIdx)
                   rate_hat = trainRateMat(uID, SPuIdx(ii));
                   rate_avg = mean(trainRateMat(uID, SNuIdx(:)));
                   ita      = max(0, rate_hat - rate_avg);
                   
                   
                   if isempty(SNuIdx)
                       nega_avg = zeros(M, 1);
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
           
           oneKidx  = find(trinRateMat(uID, :) == 0);
           oneKidx  = oneKidx(randperm(length(oneKidx)));
           oneKidx  = oneKidx(1:1000);
           
           corresp  = curPred(uID, moviID);
           oneKrate = sort(curPred(uID, oneKidx));
           
           thre     = find(oneKrate > corresp);
           
           if length(thre) <= (N-1)
               numHits = numHits + 1;
           end
               
end

recall = numHits/num5test
 

    

