from Classes.LogisticRegression import LogisticRegression
from Classes.JSONReader import JSONReader
from Classes.Stocks import Stocks
import tensorflow as tf

data = JSONReader.read_file('Classes/weights.json')
weights = data['weights']

credentials = JSONReader.read_file("Credentials.json")
stocks = Stocks(credentials['email'], credentials['password'])

data = stocks.get_data(['UAL'], 'day')
features, labels = stocks.get_training_data(['UAL'], '3month')

regression = LogisticRegression(features, labels, options={'learning_rate': 1, 'iterations': 80, 'batchsize': 10})
regression.weights = tf.cast(tf.Variable(weights), tf.dtypes.float32)

accuracy = regression.test(features, labels).numpy().tolist()
print(accuracy)
