tfidf_precision = [12.42 , 10.67 , 9.29 , 8.30, 7.41];
tfidf_recall = [5.36 , 9.36 , 12.06, 14.31, 16.11];

bayes_precision = [3.45 ,5.06 ,5.52 ,5.46 ,5.31];
bayes_recall = [1.51 ,4.34 ,7.15, 9.41, 11.51];

x= 1:5;

figure;
plot(x, tfidf_precision);
hold on;
plot(x, tfidf_recall, 'r');
hold on;
plot(x, tfidf_precision, '*');
hold on;
plot(x, tfidf_recall, 'r*');
xlabel('No of tags choosen to be predicted');
ylabel('Metric (%)');
title('Performance of TF-IDF as the baseline Parameter');
legend('Precision', 'Recall', 'Location', 'northwest');

figure;
plot(x, bayes_precision);
hold on;
plot(x, bayes_recall, 'r');
hold on;
plot(x, bayes_precision, '*');
hold on;
plot(x, bayes_recall, 'r*');
xlabel('No of tags choosen to be predicted');
ylabel('Metric (%)');
title('Performance of Bayes Precision Classifier as the baseline Parameter');
legend('Precision', 'Recall', 'Location', 'northwest');