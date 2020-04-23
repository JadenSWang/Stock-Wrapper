import tensorflow as tf
import numpy as np

class LogisticRegression:
    def __init__(self, features, labels, options={}):
        if np.shape(features)[0] != np.shape(labels)[0]:
            raise ValueError("Features and Labels must have the same row shape; features: {}, labels: {}".format(np.shape(features), np.shape(labels)))
        self.mean = None
        self.variance = None
        self.cost_history = []

        self.features = self.process_features(features)
        self.labels = tf.cast(tf.Variable(labels), tf.dtypes.float32)
        self.weights = tf.cast(tf.zeros((np.shape(self.features)[1], np.shape(self.labels)[1])), tf.dtypes.float32)

        # options
        self.options = {'learning_rate': 0.1, 'iterations': 50, 'batchsize': 500}
        self.options.update(options)

    def train(self):
        num_batches = np.floor(np.shape(self.features)[0] / self.options['batchsize'])

        i = 0
        while i < self.options['batchsize']:
            batch_index = 0
            while batch_index < num_batches:
                start_index = batch_index * self.options['batchsize']

                features_slice = tf.slice(self.features, [start_index, 0], [self.options['batchsize'], -1])
                labels_slice = tf.slice(self.labels, [start_index, 0], [self.options['batchsize'], -1])

                self.weights = self.gradient_descent(features_slice, labels_slice)
                batch_index += 1

            self.record_cost();
            self.update_learning_rate()
            i += 1

    def gradient_descent(self, features, labels):
        current_guesses = tf.linalg.matmul(features, self.weights);
        current_guesses = tf.nn.softmax(current_guesses)

        differences = tf.math.subtract(current_guesses, labels)

        slopes = tf.transpose(features)
        slopes = tf.linalg.matmul(slopes, differences)
        slopes = tf.math.divide(slopes, tf.cast(tf.shape(features)[0], tf.dtypes.float32))

        return tf.math.subtract(self.weights, tf.math.multiply(slopes, self.options['learning_rate']))

    def record_cost(self):
        guesses = tf.linalg.matmul(self.features, self.weights)
        guesses = tf.nn.softmax(guesses)

        term_one = tf.transpose(self.labels)
        term_one = tf.linalg.matmul(term_one, tf.math.log(tf.math.add(guesses, 1e-7)))

        term_two = tf.math.multiply(self.labels, -1)
        term_two = tf.math.add(term_two, 1)
        term_two = tf.transpose(term_two)
        # multiply by -1, add 1, add 1e-7 (to avoid log(0)), then log
        guesses = tf.math.multiply(guesses, -1)
        guesses = tf.math.add(guesses, 1 + 1e-7)
        guesses = tf.math.log(guesses)
        term_two = tf.linalg.matmul(term_two, guesses)

        cross_entropy = tf.math.add(term_one, term_two)
        cross_entropy = tf.math.divide(cross_entropy, tf.cast(tf.shape(self.features)[0], tf.dtypes.float32))
        cross_entropy = tf.math.multiply(cross_entropy, -1)

        self.cost_history = [cross_entropy.numpy().item(0)] + self.cost_history

    def update_learning_rate(self):
        if(len(self.cost_history) < 2):
            return

        if(self.cost_history[0] > self.cost_history[1]):
            self.options['learning_rate'] /= 2
        else:
            self.options['learning_rate'] *= 1.05

    def process_features(self, features):
        features = tf.cast(tf.Variable(features), tf.dtypes.float32)

        if((not (self.mean == None)) and (not (self.variance == None))):
            features = tf.math.subtract(features, self.mean)
            features = tf.math.divide(features, tf.math.pow(self.variance, 0.5))
        else:
            features = self.standardize(features)

        to_return = tf.ones([tf.shape(features)[0], 1])
        to_return = tf.concat([to_return, features], 1)

        return to_return

    def standardize(self, features):
        mean, variance = tf.nn.moments(features, 0)
        mean = tf.cast(mean, tf.dtypes.float32)
        variance = tf.cast(variance, tf.dtypes.float32)

        filler = tf.cast(variance, tf.dtypes.bool)
        filler = tf.math.logical_not(filler)
        filler = tf.cast(filler, tf.dtypes.float32)

        self.mean = mean
        self.variance = tf.math.add(variance, filler)

        to_return = tf.math.subtract(features, mean)
        return tf.math.divide(to_return, tf.math.pow(self.variance, 0.5))

    # TESTING THE DATA SET
    def test(self, testFeatures, testLabels):
        testFeatures = tf.Variable(testFeatures)
        testLabels = tf.Variable(testLabels)

        testFeatures = self.standardize(testFeatures)
        predictions = self.predict(testFeatures);
        testLabels = tf.math.argmax(testLabels, 1)

        incorrect = tf.math.not_equal(predictions, testLabels)
        incorrect = tf.cast(incorrect, tf.dtypes.int32)
        incorrect = tf.math.reduce_sum(incorrect)

        return (tf.shape(predictions)[0] - incorrect.numpy().item(0)) / tf.shape(predictions)[0]

    def predict(self, features):
        to_return = self.process_features(features)
        to_return = tf.linalg.matmul(to_return, self.weights)
        to_return = tf.nn.softmax(to_return)

        return tf.math.argmax(to_return, 1)