clear; close all; clc

% u.data  The full u data set, 100000 ratings by 943 users on 1682 items.
%         Each user has rated at least 20 movies.  Users and items are
%         numbered consecutively from 1.  The data is randomly
%         ordered. This is a tab separated list of 
% 	      user id | item id | rating | timestamp. 
%         The time stamps are unix seconds since 1/1/1970 UTC  

addpath('ml-100k');

global regular_u regular_m numUser numMovi M poolSize maxIters tolerence

DATA         = load('u.data');
sorted       = sortrows(DATA, 4);
sorted(:, 4) = sorted(: ,4) - sorted(1, 4); 
dataLen      = size(sorted, 1);

%% define parameters

numUser  = 943;
numMovi  = 1682;

maxIters  = 500;
M         = 20;
regular_u = 1.1;
regular_m = 0.34;
tolerence = 1e-6;

testSet      = sorted((1 + 0.8 * dataLen):dataLen, :);
testRateMat  = zeros(numUser, numMovi);
testTepoMat  = zeros(numUser, numMovi);

for i   = 1:size(testSet, 1)
    testRateMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 3);
end

%% define storages
% for each user, we need to define a pool
freq     = tabulate(sorted(:, 1));
sizeVec  = floor(0.6 * freq(:, 2));
order    = sizeVec + 5;

% using the first part of data to train the initial two matrices
oriTrinSet = sorted(1 : 0.05 * dataLen, :);
comingSet  = sorted(0.05 * dataLen + 1 : 0.8 * dataLen, :);

existVec = zeros(numUser, 1);
buff     = tabulate(oriTrinSet(:, 1));
existVec(1:size(buff, 1))   = buff(:, 2);

trinRateMat = zeros(numUser, numMovi);
for i = 1:size(oriTrinSet, 1)
    trinRateMat(oriTrinSet(i, 1), oriTrinSet(i, 2)) = oriTrinSet(i, 3);
end

dstctIdx = unique(oriTrinSet(:,1));
poolAry  = cell(numUser, 1);

for i = 1:length(dstctIdx)   
    poolAry{dstctIdx(i)} = oriTrinSet(find((oriTrinSet(:, 1)) ==...
                                                         dstctIdx(i)), :);
end

[userMat, moviMat, MAE] = getMAE(trinRateMat, testRateMat);
kkk = userMat;
jjj = moviMat;
MAE

% eliminate oldest data if number of existing rates exceed pool size
% the original data is used in training the original 2 matrices
% is it ok to delete them?

for i = 1:numUser
    if existVec(i) > sizeVec(i)
        amout = existVec(i) - sizeVec(i);
        poolAry{i}(1:amout, :) = [];
        existVec(i) = sizeVec(i);
    end
end

%% when a new data comes...
%comingSet
global alpha beta T

alpha  = 1e-6;
beta   = 1e-6;
T      = 3;


for i = 1:size(comingSet, 1)
  i
    diceIn  = rand(1);
    uidx    = comingSet(i, 1);
    midx    = comingSet(i, 2);
    addIdx  = 1;
      
      if diceIn <= ( 1 - sizeVec(uidx) / order(uidx) )
            order(uidx) = order(uidx) + 1;
%             diceOut = 
            poolAry{uidx}(addIdx, :) = comingSet(i, :);
            addIdx  = addIdx + 1;
%             disp('updated!')
            
      end
       
    if ~isempty(poolAry{uidx})
      for iter = 1: T
         [Wu, Hp] = increUpdate(poolAry{uidx}, userMat, moviMat, userMat(:, uidx));
         
         userMat(:, uidx) = Wu;
         moviMat = Hp;
%          disp('ALGO used!')
      end
    else
        continue;
    end
end

pred = userMat' * moviMat;

MAE2 = computeMAE(userMat' * moviMat, testRateMat)   
MAE
 

    


