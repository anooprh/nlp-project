tfidf_precision = [12.42 , 10.67 , 9.29 , 8.30, 7.41];
bayes_precision = [3.45 ,5.06 ,5.52 ,5.46 ,5.31];
lextree_precision = [1,1,1,1,1];
rnn_precision = [12.7008, 17.8189, 18.9756, 18.5902, 18.0796];
rnn_word2vec_precision = [13.9702, 18.7833, 19.3309, 18.7114, 18.1035 ];

tfidf_recall = [5.36 , 9.36 , 12.06, 14.31, 16.11];
bayes_recall = [1.51 ,4.34 ,7.15, 9.41, 11.51];
lextree_recall = [1,1,1,1,1];
rnn_recall = [12.7012, 19.8857, 23.8042, 25.9919, 27.3508];
rnn_word2vec_recall = [13.9706, 20.9619, 24.2499, 26.1613, 27.387];

x= 1:5;

figure;
plot(x, tfidf_precision);
hold on;
plot(x, bayes_precision, 'r--');
hold on;
plot(x, lextree_precision, 'g:');
hold on;
plot(x, rnn_precision, 'k-.');
hold on;
plot(x, rnn_word2vec_precision, 'm', 'LineWidth' ,2.5);
hold on;

plot(x, tfidf_precision, 'b*');
hold on;
plot(x, bayes_precision, 'r*');
hold on;
plot(x, lextree_precision, 'g*');
hold on;
plot(x, rnn_precision, 'k*');
hold on;
plot(x, rnn_word2vec_precision, 'm*', 'LineWidth' ,2.5);
hold on;

xlabel('No of tags choosen to be predicted');
ylabel('Precision (%)');
title('Precison For varios algorithms');
legend('TFIDF', 'TFIDF-Bayesian Classifier', 'Lexical Tree', 'RNN', 'RNN-word2vect', 'Location', 'northeastoutside');

figure;
plot(x, tfidf_recall);
hold on;
plot(x, bayes_recall, 'r--');
hold on;
plot(x, lextree_recall, 'g:');
hold on;
plot(x, rnn_recall, 'k-.');
hold on;
plot(x, rnn_word2vec_recall, 'm', 'LineWidth', 2.5);
hold on;

plot(x, tfidf_recall, 'b*');
hold on;
plot(x, bayes_recall, 'r*');
hold on;
plot(x, lextree_recall, 'g*');
hold on;
plot(x, rnn_recall, 'k*');
hold on;
plot(x, rnn_word2vec_recall, 'm*', 'LineWidth', 2.5);
hold on;

xlabel('No of tags choosen to be predicted');
ylabel('Recall (%)');
title('Recall For varios algorithms');
legend('TFIDF', 'TFIDF-Bayesian Classifier', 'Lexical Tree', 'RNN', 'RNN-word2vect', 'Location', 'northeastoutside');
