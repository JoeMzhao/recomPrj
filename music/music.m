clear; close all; clc

fid     = fopen('trimed.csv');
rawData = textscan(fid, '%d %d64 %s', 'delimiter',',');
fclose(fid);

k  = unique(rawData{1, 3});
kk = cell2mat(rawData{1, 3});

for i = 1:length(rawData{1, 3})
    i
    for j = 1:length(k)
        if kk(i) == k{j}
            idx(i) = j;
        end
    end
end
