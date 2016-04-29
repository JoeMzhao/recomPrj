clear; close all; clc

fid     = fopen('parsed');
rawData = textscan(fid, '%d64 %d64 %d64', 'delimiter',',');
fclose(fid);

rawMat       = cell2mat(rawData);
rawMat(:, 2) = rawMat(:, 2)./1000;
rawMat(:, 2) = rawMat(:, 2) - min(rawMat(:, 2));
rawMat(:, 3) = rawMat(:, 3) + 1;
sorted       = sortrows(rawMat, 2);
sorted       = sorted(1:end-1, :);

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
    i
    countMat(trainSection1(i, 1), trainSection1(i, 3)) = ...
                    countMat(trainSection1(i, 1), trainSection1(i, 3)) + 1;
end


for i = 1:numUser
    i
    none_zeroIdx = find(countMat(i, :) > 0);
    le = length(none_zeroIdx);   
        for j = 1:le
            storePair{i, j} = [i, none_zeroIdx(j), countMat(i, none_zeroIdx(j))];
        end
end

storePair = storePair';
id = 1;
for i = 1:size(storePair, 1) * size(storePair, 2)
    if storePair{i}
        outPut{id, 1} = storePair{i};
        id = id + 1;
    end   
end

OUT = cell2mat(outPut);

dlmwrite('forPY.csv',OUT, 'precision', '%6d') 
p = 0;
for i = 1:1000
    if ~sum(countMat(i, :))
        p = p + 1;
    end
end
k = 0;
for j = 1:size(countMat,2)
    j
    if ~sum(countMat(:, j))
        k = k + 1;
    end
end
k


