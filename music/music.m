clear; close all; clc

fid     = fopen('parsed');
rawData = textscan(fid, '%d64 %d64 %d64', 'delimiter',',');
fclose(fid);

rawMat       = cell2mat(rawData);
rawMat(:, 2) = rawMat(:, 2)./1000;
rawMat(:, 2) = rawMat(:, 2) - min(rawMat(:, 2));
rawMat(:, 3) = rawMat(:, 3) + 1;
sorted       = sortrows(rawMat, 2);
dataLen      = size(sorted, 1);

poption       = 0.8;
trainSection1 = sorted((1:round(poption/2*dataLen)), :);
trainSection2 = sorted((round(poption/2*dataLen)+1) : poption*dataLen, :);
testSection   = sorted((round(poption*dataLen)+1) : end, :);

numUser  = 1000;
numTrack = 298837;
alpha    = 40;
f        = 20;
countMat = zeros(numUser, numTrack);

% initial count matrix
for i = 1:size(trainSection1, 1)
    countMat(trainSection1(i, 1), trainSection1(i, 3)) = ...
                    countMat(trainSection1(i, 1), trainSection1(i, 3)) + 1;
end
% initial confidence matrix
confiMat = 1 + alpha .* countMat;
% initial preference matrix
prefeMat = countMat | zeros(numUser, numTrack);


% start looping
Y  = zeros(numTrack, f);
X  = zeros(numUser, f);

YTY = Y' * Y; 
for i = 1:numUser
    C_up_u_user  = diag(confiMat(i, :));
    YT_C_Y  = YTY + Y'* (C_up_u_user - eye(numTrack)) * Y;
    X(i, :) = (YT_C_Y) \ Y' * C_up_u_user * prefeMat(i, :);
end

XTX = X' * X;
for j = 1:numTrack
    C_up_i_track = diag(confiMat(:, j));
    XT_C_X  = XTX + X' * (C_up_i_track - eye(numUser)) * X;
    Y(j, :) = (XT_C_X) \ X' * C_up_i_track * prefeMat(:, j);
end

    










