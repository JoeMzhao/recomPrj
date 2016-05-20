clear; close all; clc

addpath('ml-100k');

global alpha beta numUser numMovi poolSize M maxIters 
global tolerence T regular_u regular_v 

rawData      = load('u.data');
sorted       = sortrows(rawData, 4);
%sorted       = rawData;
sorted(:, 4) = 1:size(sorted, 1); 
dataLen      = size(sorted, 1);

prop         = 0.95;
mftrainEND   = (prop - 0.00) * dataLen;
increSTART   = mftrainEND + 1;
increEND     = prop * dataLen;
testSTART    = prop * dataLen + 1;

trainSet     = sorted(1:mftrainEND, :);
testSet      = sorted(testSTART : end, :);
increSet     = sorted(increSTART:increEND, :);

numUser      = 943;
numMovi      = 1682;
maxIters     = 400; 
regular_u    = 0.1;
regular_v    = 0.34;
tolerence    = 1e-5; 
T            = 15;
alpha        = 1e-1;
beta         = 1e-1;

poolSize  = mftrainEND;
pool      = trainSet(1:poolSize, :);
M         = 20;
tobecheck1 = [];
tobecheck2 = [];

%% Process the data and obtain rate matrices
trainRateMat  = zeros(numUser, numMovi);
testRateMat   = zeros(numUser, numMovi);

for i  = 1 : poolSize
    trainRateMat(trainSet(i, 1), trainSet(i, 2)) = trainSet(i, 3);
end
for i  = 1 : size(testSet, 1)
    testRateMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 3);  
end


%% The initial phase >> train two initial matrices and keeps learning
[userMat, moviMat, MAE1] = getMAE(trainRateMat, testRateMat);
MAE1
userMat = rand(20, 943);
moviMat = rand(20, 1682);
curPred  = userMat' * moviMat;
N        = 10;
P10K     = 200;

num5test = 0;
numHits  = 0;

counter1 = 0;
counter2 = 0;

for i = 1:size(testSet, 1)
    if testSet(i, 3) == 5
        counter2 = counter2 + 1;
    else
        continue;
    end
    
    uID      = testSet(i, 1);
    moviID   = testSet(i, 2);
        
    oneKidx  = find(trainRateMat(uID, :) == 0);    
    oneKidx  = oneKidx(randperm(length(oneKidx)));
    oneKidx  = oneKidx(1:P10K);
    
    corresp  = curPred(uID, moviID);  
    oneKrate = curPred(uID, oneKidx);
    
    thre     = find(oneKrate > corresp);
    
    if length(thre) <= (N-1) 
        counter1 = counter1 + 1;
    end 
end
counter1/counter2

numIn = 0;

for i = 1:length(testSet)         
           uID    = testSet(i, 1);
           moviID = testSet(i, 2);
           
           userUpool1 = pool(find(pool(:, 1) == uID), :);
        
      if inORnot(testSet(i, 4))
               numIn  = numIn + 1;
               trainRateMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 3);          
               timeArry              = pool(:, 4);          
               [repIdx, threshArry2] = whichOut(timeArry, testSet(i, 4)); 
               pool(repIdx, :)       = testSet(i, :);

               userUpool2 = pool(find(pool(:, 1) == uID), :);

               SPuIdx = SamplePositiveInput(curPred, userUpool1, testSet(i, :));          
               SNuIdx = SampleNegativeInput(curPred, userUpool2, SPuIdx, testSet(i, :));
               
               disp('Length of SPuIdx is')
               length(SPuIdx)
               
               disp('Length of SNuIdx is')
               length(SNuIdx)

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
                       
%                        tobecheck1 = [tobecheck1 userMat(:, uID)];
%                        tobecheck2 = [tobecheck2 alpha * ita .* (moviMat(:, SPuIdx(ii)) - nega_avg) - ...
%                            alpha * beta .* userMat(:, uID)];
                       
%                        mean(alpha * ita .* (moviMat(:, SPuIdx(ii)) - nega_avg) - ...
%                            alpha * beta .* userMat(:, uID))


                       moviMat(:, SPuIdx(ii)) = moviMat(:, SPuIdx(ii)) + alpha * ita .* userMat(:, uID) - ...
                           alpha * beta .* moviMat(:, SPuIdx(ii));

                       for j = 1:length(SNuIdx)
                           moviMat(:, SNuIdx(j)) = moviMat(:, SNuIdx(j)) - alpha * ita .* userMat(:, uID) ...
                               - alpha * beta * moviMat(:, SNuIdx(j));
                       end
                   end
               end
       end 
       
           curPred   = userMat' * moviMat;
           
           if testSet(i, 3) == 5 
               num5test = num5test + 1;       
               oneKidx  = find(trainRateMat(uID, :) == 0);
               oneKidx  = oneKidx(randperm(length(oneKidx)));
               oneKidx  = oneKidx(1:P10K);
               corresp  = curPred(uID, moviID);
               oneKrate = curPred(uID, oneKidx);

               thre     = find(oneKrate > corresp);

               if length(thre) <= (N-1)
                   numHits = numHits + 1;
               end
           end
               
end

recall = numHits/num5test