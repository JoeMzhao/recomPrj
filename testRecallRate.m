clear; close all; clc

% u.data  The full u data set, 100000 ratings by 943 users on 1682 items.
%         Each user has rated at least 20 movies.  Users and items are
%         numbered consecutively from 1.  The data is randomly
%         ordered. This is a tab separated list of 
% 	      user id | item id | rating | timestamp. 
%         The time stamps are unix seconds since 1/1/1970 UTC  

addpath('ml-100k');

global alpha beta numUser numMovi M regular_u regular_v

DATA    = load('u.data');
sorted  = sortrows(DATA, 4);
% sorted  = DATA;
dataLen = size(sorted, 1);

numUser = 943;
numMovi = 1682;

trinSet = sorted(1: 0.2 * dataLen, :);
testSet = sorted((1 + 0.8 * dataLen):dataLen, :);

trinRateMat  = zeros(numUser, numMovi);
trinTepoMat  = zeros(numUser, numMovi);

testRateMat  = zeros(numUser, numMovi);
testTepoMat  = zeros(numUser, numMovi);

for i = 1:size(trinSet, 1)
    trinRateMat(trinSet(i, 1), trinSet(i, 2)) = trinSet(i, 3);
    trinTepoMat(trinSet(i, 1), trinSet(i, 2)) = trinSet(i, 4);
end

for i = 1:size(testSet, 1)
    testRateMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 3);
    testTepoMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 4);
end

%% define parameters
maxIters  = 1000;
M         = 20;
alpha     = 1e-5;
beta      = 1e-5;

tolerence = 1e-5;

%% obtain index of non-zero entries in trinSetMat
for i = 1:numUser
    nonZeroRow(i) = {find(trinRateMat(i, :))};
    zeroRow(i)    = {find(trinRateMat(i, :) == 0)};
end

for i = 1:numMovi
    nonZeroCol(i) = {find(trinRateMat(:, i))};
end


%% ALS algorithm

userMatOrig = rand(M, numUser);
moviMatOrig = rand(M, numMovi);

for i = 1:numMovi
    idx = cell2mat(nonZeroCol(i));
    if ~isempty(idx)
        moviMatOrig(1,i) = mean(trinRateMat(idx,i));
    end
end

tolerBuffer = zeros(1,maxIters);
noZeroEntri = length(find(trinRateMat));

for k = 1:maxIters
    
    [userMat, moviMat] = ALSUpdate(trinRateMat, userMatOrig, moviMatOrig,...
                                    nonZeroRow, nonZeroCol);
    
    tolerBuffer(k) = computeRMSE(trinRateMat , userMat, moviMat, ...
                                            nonZeroRow, noZeroEntri);
    
    if k>1 && abs(tolerBuffer(k) - tolerBuffer(k-1)) < tolerence
        break;
    end
    
    userMatOrig = userMat;
    moviMatOrig = moviMat;
    k
 if k == maxIters
     disp('Max number of interation reached..');
 end
    
end

curPred = userMat' * moviMat;
MAE  = computeMAE( testRateMat, pred)



releventSet = unique(testSet(:, 1));
numUserInTest = length(releventSet);

for j = 1:size(testSet, 1)
        idx = find(releventSet(:, 1) == testSet(j, 1));
        len = length(find(releventSet(idx, :)~=0));
        releventSet(idx, len + 1) = testSet(j, 2);
end
uniOn   = cell(numUserInTest, 2);

for i = 1:size(testSet, 1)
    uniOn{i, 1} = releventSet(i, 1);
end

N       = 10;

for i = 1:size(testSet, 1)
    testUid   = testSet(i, 1);
    buff1     = curPred(testUid, :);
    buff      = sort(buff1, 2);
    buff      = buff(end-N+1:end);
    recom     = zeros(1, N);

    for jjjj = 1:N

        k  = buff(jjjj);
        idxBuff = find(curPred(testUid, :) == k);

        if length(idxBuff) > 1
            idxBuff = idxBuff(1);
        end

        recom(jjjj) = idxBuff;
    end

    uniIdx = find(testUid == releventSet(:, 1));
    uniOn{uniIdx, 2} = union(uniOn{uniIdx, 2}, recom);
end

releSet = cell(numUserInTest,1);
for i = 1:numUserInTest   
    releSet{i,1} = releventSet(i, 2:end);
end

intSectionSize = zeros(numUserInTest, 1);
intSection = cell(numUserInTest,1);

for i = 1:numUserInTest
    intSection{i,1}   = intersect(releSet{i, 1}, uniOn{i, 2});
    intSectionSize(i) = length(intersect(releSet{i, 1}, uniOn{i, 2}));
end

releventSet  = releventSet(:, 2:end);
releventSize = zeros(numUserInTest, 1);
for i = 1:size(releventSet, 1)
    for j = 1:size(releventSet,2)
        if releventSet(i,j)~=0
            releventSize(i) = releventSize(i) + 1;
        end
    end
end

mean(intSectionSize./releventSize)

























    
        
    
    


