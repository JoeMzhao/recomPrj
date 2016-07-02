clear; close all; clc
impMAE = load('performance.txt');
impMAE = impMAE(:, [5, 7]);
% terMAE = load('rndTTerecML.txt');
% terMAE = terMAE(:, [5, 7]);

% subplot(1, 2, 1)
% plot(terMAE(:, 1), terMAE(:, 2), '-^', 'MarkerSize', 8, 'lineWidth', 2, 'color', [0.1 0.2 0.7]);

plot(impMAE(:, 1), impMAE(:, 2), '-o', 'MarkerSize', 8, 'lineWidth', 2, 'color', [0.71 0.2 0.1]);
grid on; hold on;
xlabel('different value of round T')
ylabel('MAE')
set(gca, 'fontsize', 18)
title('MAE performance with different rounds T (ML-100k)')
legend('TeRec', 'DeMF')
hold off
set(gca, 'xtick', 1:2:15)

% subplot(1, 2, 2)
% load('terecTimeML');
% meanTimeTer = [];
% stdTimeTer = [];
% for i = 1:size(terecTime, 1)
%     meanTimeTer(i) = mean(terecTime{i, 1});
%     stdTimeTer(i) = std(terecTime{i, 1});
% end
% t = errorbar(impMAE(:, 1), meanTimeTer, stdTimeTer, '-o', 'color', [0.1 0.2 0.7]);
% hold on; grid on
% set(t,'MarkerSize', 8);
% set(t, 'lineWidth', 2);
% 
% load('impTimeML');
% meanTimeImp = [];
% stdTimeImp = [];
% for i = 1:size(terecTime, 1)
%     meanTimeImp(i) = mean(impTimeML{i, 1});
%     stdTimeImp(i) = std(impTimeML{i, 1});
% end
% i = errorbar(impMAE(:, 1), meanTimeImp, stdTimeImp, '-^', 'color', [0.71 0.2 0.1]);
% 
% set(gca, 'xtick', 1:2:15)
% legend('TeRec', 'DeMF')
% set(gca, 'fontsize', 18)
% set(i,'MarkerSize', 8);
% set(i, 'lineWidth', 2);
% axis([0 16 0 1])
% xlabel('different value of round T')
% ylabel('Time consumption (seconds)')
% title('Time consumpiton with different rounds T (ML-100k)')