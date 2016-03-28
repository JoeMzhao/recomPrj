function [userMat, moviMat, MAE] = getMAE(trinRateMat, testRateMat)


global numUser numMovi M maxIters tolerence

for i = 1:numUser
    nonZeroRow(i) = {find(trinRateMat(i, :))};
    zeroRow(i)    = {find(trinRateMat(i, :) == 0)};
end

for i = 1:numMovi
    nonZeroCol(i) = {find(trinRateMat(:, i))};
end

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
    k
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
     disp('Max number of interation reached..');
 end
    
end

pred = userMat' * moviMat;
MAE  = computeMAE( testRateMat, pred);