close all;
figure;

% read in the data
data = load('iris.txt.pmass');
X = data(:, 1:2);
y = data(:, 3);

% Find ids of positive and negative examples
pos = find(y==1); 
neg = find(y==0);

% Plot examples
plot(X(pos, 1), X(pos, 2), 'cr', 'MarkerSize', 5);
hold on;
plot(X(neg, 1), X(neg, 2), 'cb', 'MarkerSize', 5);
hold on;

legend('virginica:', 'versicolor:');
axis([3, 8, -5, 110])
hold off
