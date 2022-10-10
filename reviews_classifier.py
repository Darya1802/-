import numpy as np
import pandas as pd
from textblob.classifiers import NaiveBayesClassifier


# загрузка данных для обучения и теста
train_data = pd.read_csv('reviews.csv')
test_data = pd.read_csv('test_data_reviews.csv')

train_data = (np.array(train_data))
test_data = (np.array(test_data))

# инициализация классификатора
classifier = NaiveBayesClassifier(train_data)

# проверка работы классификатора
if (classifier.classify("Маникюр был сделан некачественно, все криво,больше не обращусь к этому мастеру за услугой")) == 'pos':
    print('Отзыв положительный')
else:
    print('Отзыв негативный')





