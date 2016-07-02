clear; close all; clc
rawData = load('mae_distribution.txt');
rawData = sortrows(rawData', 2)';
bd1 = find(rawData(2, :) > 0);
rawData = rawData(:, bd1(1):end);
%rawData = rawData(5:end, :);

rawData = sortrows(rawData', 2)';
bd2 = find(rawData(1, :) > 0);
rawData = rawData(:, bd2(1):end);
rawData(5, :) = 1 * ( rawData(4, :) - rawData(3, :))/2000;
% rawData(:, find(rawData(5, :)<=0)) = [];

rawData = sortrows(rawData',1)';
[x, y] = find(rawData(1, :) > 150);    
rawData = rawData(:, y(1):end); %26
rawData = sortrows(rawData', 2)';

xzuobiao = 1:size(rawData, 2);

[ax, h1, h2] = plotyy(xzuobiao, rawData(5, :), xzuobiao, rawData(2, :), 'bar', 'plot');
grid on
set(h1, 'FaceColor', [0.7, 0.2, 0.2])
set(h2, 'marker', 'o', 'LineWidth', 2, 'MarkerSize', 5)%, 'MarkerEdgeColor', 'b', 'MarkerFaceColor', 'b')
set(gca, 'fontsize', 18, 'fontweight', 'bold')
xlabel('Different users')
set(gca, 'xtick', 1:1:25, 'ytick', 0:0.01:0.04)
set(get(ax(1), 'Ylabel'), 'String', 'MAE improvements')
set(get(ax(2), 'Ylabel'), 'String', 'Appeared times in testing dataset')
set(ax(2), 'fontsize', 18, 'fontweight', 'bold')
set(ax(1), 'YColor', [0.7, 0.2, 0.2])
title('MAE improvements and usage')

% plot(rawData(1, :), 'b.-')

