clear; close all; clc
data = load('performance.txt');
data = data(:, [1, 2, 7]);
data = sortrows(data, 1);
data = double(data);

alpha = unique(data(:,1));
beta = unique(data(:,2));


for i = 1:size(data, 1)
    coorA = data(i, 1);
    coorB = data(i, 2);
    
    for j = 1:length(alpha)
        if coorA == alpha(j)
            localA = j;
        end
    end
   
    for k = 1:length(beta)
       if coorB == beta(k)
            localB = k;
       end
    end
    maeMAT(localA, localB) = data(i, 3);
end
[ALPHA, BETA] = meshgrid(alpha, beta);
surf(ALPHA, BETA, maeMAT')
shading interp
            

