function  MAE = computeMAE( test, pred )

E   = zeros(1, size(test,1));
len = zeros(1, size(test,1));
N   = length(find(test));

for i = 1:size(test, 1)
    Ii     = find(test(i,:));
    len(i) = length(Ii);
    E(i)   = sum(abs(test(i, Ii)-pred(i, Ii)));
end

MAE = sum(E)/N;

end

