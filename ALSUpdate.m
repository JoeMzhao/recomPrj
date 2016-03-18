function [ userMatOrig, moviMatOrig ] = ALSUpdate( trinRateMat, userMatOrig,...
    moviMatOrig, nonZeroRow, nonZeroCol )
global alpha beta numMovi M

% update user matrix
    for i = 1:size(trinRateMat, 1)

        Ii = cell2mat(nonZeroRow(i));

        if ~isempty(Ii)
            nui = size(Ii, 2);
            Mi  = moviMatOrig(:, Ii);
            Ri  = trinRateMat(i, Ii);
            userMatOrig(:, i) = (Mi*Mi' + alpha*nui*eye(M)) \ (Mi*Ri');
        end

    end

% update movie matrix
    for j = 1:numMovi

        Ij = cell2mat(nonZeroCol(j));

        if ~isempty(Ij)
            nmj = size(Ij, 1);
            Uj  = userMatOrig(:, Ij);
            Rj  = trinRateMat(Ij, j);
            moviMatOrig(:, j) = (Uj*Uj' + beta*nmj*eye(M)) \ (Uj*Rj);
        end

    end

end

