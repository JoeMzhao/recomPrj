clear; close all; clc

addpath('ml-100k');

global alpha beta numUser numMovi poolSize M maxIters tolerence

rawData      = load('u.data');
sorted       = sortrows(rawData, 4);
sorted(:, 4) = sorted(: ,4) - sorted(1, 4); 
dataLen      = size(sorted, 1);

trainSet     = sorted(1:0.8 * dataLen, :);
testSet      = sorted(0.8 * dataLen + 1 : end, :);

numUser      = 943;
numMovi      = 1682;
maxIters     = 500; 
alpha        = 0.1;
beta         = 0.1;
tolerence    = 1e-5; 

%% Process the data and obtain rate matrices

trainRateMat  = zeros(numUser, numMovi);
trainTempMat  = zeros(numUser, numMovi);

for i  = 1 : dataLen * 0.8
    trainRateMat(trainSet(i, 1), trainSet(i, 2)) = trainSet(i, 3);
    trainTempMat(trainSet(i, 1), trainSet(i, 2)) = trainSet(i, 4);
end

testRateMat   = zeros(numUser, numMovi);
testTempMat   = zeros(numUser, numMovi);

for i  = 1 : size(testSet, 1)
    testRateMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 3);
    testTempMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 4);
end

poolSize  = 20000;
pool      = trainSet(1:poolSize, :);

M         = 20;
userMat   = rand(M, numUser);
moviMat   = rand(M, numMovi);

%% The initial phase >> train two initial matrices
iniPred   = userMat' * moviMat;
% [userMat, moviMat, MAE] = getMAE(iniPred, testRateMat); disp(MAE);


curPred   = userMat' * moviMat;

for i = (poolSize + 1) : dataLen * 0.8
       
%     userDataRaw1 = pool( find(pool(:, 1) == trainSet(i, 1)), :); 
    userDataRaw1 = pool;
    boo          = inORnot(trainSet(i, 4))
    if boo
           timeArry  = userDataRaw1(:, 4);
           
           [repIdx, threshArry2] = whichOut(timeArry, trainSet(i, 4));
           userDataRawBuff       = userDataRaw1;
           
           userDataRawBuff(repIdx, :) = trainSet(i, :); 
           fprintf('No. %d  data point is replaced\n', repIdx);
    end
       
end    
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

