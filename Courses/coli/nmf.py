'''
NMF Implementation in Python
Richard Littauer
Computerlinguistics, Exercise 6
'''

'''
And now in Matlab, courtesty of Ehsan 
#=========#=========#=========#
function [ W,H ] = NMF( A,k)
    [n m] = size(A);

    W= random('norm',10,1,n,k);
    H= random('norm',10,1,k,m);

    epsilon=0.001;
    %0.5*norm(X-U*V','fro')> epsilon
    i=1;
    while i<2000 && 0.5*norm(A-W*H,2)> epsilon
        i=i+1;
        H= H .* (W'*A)./ (W'*W*H);
        W = W .* (A*H')./(W*H*H');
        H = my_norm_H(W,H);
        W = my_norm_W(W,H);
    end
    
   


end

function [H] = my_norm_H(W,H)
    V= H';
    for j=1:size(V,2)
        V(:,j) = V(:,j) .* sqrt(sum(W(:,j).^2));
    end
    H= V'; 
end

function [W] = my_norm_W(W,H)
    
    for j=1:size(W,2)
        W(:,j) = W(:,j) ./ sqrt(sum(W(:,j).^2));
    end
    
end
'''
