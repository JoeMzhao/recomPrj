clear; close all; clc

% u.data  The full u data set, 100000 ratings by 943 users on 1682 items.
%         Each user has rated at least 20 movies.  Users and items are
%         numbered consecutively from 1.  The data is randomly
%         ordered. This is a tab separated list of 
% 	      user id | item id | rating | timestamp. 
%         The time stamps are unix seconds since 1/1/1970 UTC  

addpath('ml-100k');

global regular_u regular_m numUser numMovi M

DATA    = load('u.data');
sorted  = sortrows(DATA, 4);
sorted  = DATA;
dataLen = size(sorted, 1);

numUser = 943;
numMovi = 1682;

trinSet = sorted(1: 0.8 * dataLen, :);
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
maxIters  = 500;
M         = 5;
regular_u = 0.1;
regular_m = 0.1;
tolerence = 1e-8;

%% obtain index of non-zero entries in trinSetMat
for i = 1:numUser
    nonZeroRow(i) = {find(trinRateMat(i, :))};
    zeroRow(i)    = {find(trinRateMat(i, :) == 0)};
end

for i = 1:numMovi
    nonZeroCol(i) = {find(trinRateMat(:, i))};
end

%% normalisation
% rateMean = zeros(1, numUser);
% rateStd  = zeros(1, numUser);
% backup   = trinRateMat;
% 
% for i = 1:numUser                
%         idx         = cell2mat(nonZeroRow(i));
%         rateMean(i) = mean(trinRateMat(i,idx));
%         rateStd(i)  = std(trinRateMat(i,idx));
%         
%    if ~isempty(idx)
%       if rateStd(i) == 0
%             trinRateMat(i,idx) = 0;
%        else
%          trinRateMat(i,idx) = (trinRateMat(i,idx) - ...
%                                 rateMean(i))./rateStd(i);
%        end
%    end   
% end


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

pred = userMat' * moviMat;
MAE  = computeMAE( testRateMat, pred)


    
        
    
    


