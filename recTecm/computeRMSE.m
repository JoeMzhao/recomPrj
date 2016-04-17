function  RMSE  = computeRMSE( R, U, A, IdxR, N )

E = 0;

for i = 1:size(R,1)
    Ii = cell2mat(IdxR(i));
    E = E + sum((R(i,Ii)-U(:,i)'*A(:,Ii)).^2);
end

RMSE = sqrt(2*E/N);

end

