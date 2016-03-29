clear; close all; clc

% u.data  The full u data set, 100000 ratings by 943 users on 1682 items.
%         Each user has rated at least 20 movies.  Users and items are
%         numbered consecutively from 1.  The data is randomly
%         ordered. This is a tab separated list of 
% 	      user id | item id | rating | timestamp. 
%         The time stamps are unix seconds since 1/1/1970 UTC  

addpath('ml-100k');
addpath('ml-1m');

global numUser numMovi M regular_u regular_v

DATA    = load('u.data');
% sorted  = sortrows(DATA, 4);

sorted  = DATA;
dataLen = size(sorted, 1);

% numUser = 943;
% numMovi = 1682;

numUser = 6040;
numMovi = 3952;

trinSet = sorted(1: 0.98 * dataLen, :);
testSet = sorted((1 + 0.98 * dataLen):dataLen, :);

trinRateMat  = zeros(numUser, numMovi);
trinTepoMat  = zeros(numUser, numMovi);

testRateMat  = zeros(numUser, numMovi);
testTepoMat  = zeros(numUser, numMovi);

for i = 1:size(DATA, 1)
    wholeRateMat(DATA(i, 1), DATA(i, 2)) = DATA(i, 3);
end


for i = 1:size(trinSet, 1)
    trinRateMat(trinSet(i, 1), trinSet(i, 2)) = trinSet(i, 3);
    trinTepoMat(trinSet(i, 1), trinSet(i, 2)) = trinSet(i, 4);
end

for i = 1:size(testSet, 1)
    testRateMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 3);
    testTepoMat(testSet(i, 1), testSet(i, 2)) = testSet(i, 4);
end

%% define parameters
maxIters  = 500;
M         = 20;
regular_u = 0.34;
regular_v = 0.1;

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

 if k == maxIters
     disp('Max number of interation reached.');
 end
    k
end

curPred = userMat' * moviMat;
MAE     = computeMAE(testRateMat, curPred)

%% calculating the recall rate
N       = 10;
counter = 0;

for i = 1:length(testSet)

    uID      = testSet(i, 1);
    moviID   = testSet(i, 2);
    
    oneKidx  = find(wholeRateMat(uID, :) == 0);    
    oneKidx  = oneKidx(randperm(length(oneKidx)));
    oneKidx  = oneKidx(1:50);
    
    corresp  = curPred(uID, moviID);  
    oneKrate = sort(curPred(uID, oneKidx));
    
    thre     = find(oneKrate > corresp);
    
    if length(thre) <= (N-1)
        counter = counter + 1;
    end
    
%     for j = length(oneKrate):-1:(length(oneKrate)-N+1)
%         reco{i, j} = find(curPred(uID, :) == oneKrate(j));
%     end
%     
%     recomm = cell2mat(reco(i, :));
%     
%     if intersect(recomm, moviID)
%         counter = counter + 1;
%     end
    
end
counter/size(testSet, 1)



