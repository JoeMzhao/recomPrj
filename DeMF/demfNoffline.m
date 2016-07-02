clear; close all; clc

memoList1 = load('memoValueImpML.txt');
timeList = load('resultTimeImpML.txt');
j = 1;
for i = 1:size(memoList1, 1)
    if memoList1(i, 2) == 0
        continue
    else
        memoList(j, :) = memoList1(i, :);
        j = j + 1;
    end
end

meanTime  = mean(timeList);
varianceT = std(timeList);
 
meanMemo  = mean(memoList);
varianceM = std(memoList);


offLineTime = 175.173198;
offLineMemo = 13109344;

% offLineTime = 97.242441;
% offLineMemo = 323842240;

meanArray1 = [offLineTime, meanTime]; 
meanArray2 = [offLineMemo, meanMemo]; 


figure
t1 = subplot(1, 2, 1);
hold on
bar(1:2, log(meanArray2), 0.4, 'FaceColor',[0.3 .6 .3])
errorbar(1:2, log(meanArray2), log([0  varianceM]), '-r', 'linewidth',1.2)
grid on
set(gca,'YScale','log')
set(gca,'Xtick',1:2,'XTickLabel',{'pureMF', 'DeMF'})
set(gca, 'fontsize', 15)
ylabel('Memory consumption (Bytes)')
title('Memory comparision (ML-100k)')

subplot(1, 2, 2)
hold on
bar(1:2, log(1000*meanArray1), 0.4, 'FaceColor',[0.0 .6 .7])
errorbar(1:2, log(1000*meanArray1), log([0  1000*varianceT]), 'r-', 'linewidth',1.2)
grid on
set(gca,'YScale','log')
set(gca,'Xtick',1:2,'XTickLabel',{'pureMF', 'DeMF'})
set(gca, 'fontsize', 15)
ylabel('Time consumption (ms)')
title('Time comparision (ML-100k)')











