clear; close all; clc

imp = load('performance.txt');
imp = imp(:, [3, 7]);
% trc = load('trc_ml_100k.txt');
% trc = trc(:, [3, 7]);

% subplot(1, 2, 1)
% plot(trc(1:9, 1), trc(1:9, 2), 'r^-', 'MarkerSize', 5, 'LineWidth', 2, 'color', [0.1, 0.1, 0.8]);
plot(imp(1:9, 1), imp(1:9, 2), 'r^-', 'MarkerSize', 5, 'LineWidth', 2, 'color', [0.8, 0.1, 0.1]);
grid on; hold on;
xlabel('Size of the reservior')
ylabel('MAE')

title('Effects of different size of reserviors (ML-100k)')
set(gca, 'fontsize', 18)
set(gca, 'xtick', [10, 30, 40 50:10:90])

% plot(50, imp(5, 2), 'go', 'MarkerSize', 10, 'LineWidth', 3)
% plot(40, trc(4, 2), 'co', 'MarkerSize', 10, 'LineWidth', 3)
legend('TeRec', 'DeMF')


% clear
% 
% imp = load('ciao_imp.txt');
% imp = imp(1:10, [3, 7]);
% trc = load('ciao_ter.txt');
% trc = trc(1:10, [3, 7]);
% 
% subplot(1, 2, 2)
% plot(trc(:, 1), trc(:, 2), 'r^-', 'MarkerSize', 5, 'LineWidth', 2, 'color', [0.1, 0.1, 0.8]);
% grid on; hold on;
% plot(imp(:, 1), imp(:, 2), 'r^-', 'MarkerSize', 5, 'LineWidth', 2, 'color', [0.8, 0.1, 0.1]);
% xlabel('Size of the reservior')
% ylabel('MAE')
% 
% title('Effects of different size of reserviors (Ciao)')
% set(gca, 'fontsize', 18)
% set(gca, 'xtick', [10, 30, 40 50:10:90])
% plot(50, imp(5, 2), 'go', 'MarkerSize', 10, 'LineWidth', 3)
% plot(60, trc(6, 2), 'co', 'MarkerSize', 10, 'LineWidth', 3)
% legend('TeRec', 'DeMF')