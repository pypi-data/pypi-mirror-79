import tensorflow as tf
from tensorflow import keras

def buildModel(input_train, output_train, modelPath):

    activation = "sigmoid"
    dropout = 0
    optimizer = "adam"
    loss = "mean_squared_error"
    epoch = 10

    initializer = tf.keras.initializers.RandomNormal(mean=0., stddev=1.)

    if len(input_train.shape)>1:
        input_size = input_train.shape[1]
    else:
        input_size = 1

    if len(output_train.shape)>1:
        output_size = output_train.shape[1]
    else:
        output_size = 1

    model = keras.Sequential([
        keras.layers.Dense(input_size, activation=activation, kernel_initializer=initializer),
        keras.layers.Dropout(dropout),
        keras.layers.Dense(250, activation=activation, kernel_initializer=initializer),
        keras.layers.Dropout(dropout),
        keras.layers.Dense(250, activation=activation, kernel_initializer=initializer),
        keras.layers.Dropout(dropout),
        keras.layers.Dense(output_size, activation=activation, kernel_initializer=initializer)
    ])

    if optimizer == 'sgd':
        optimizer = tf.keras.optimizers.SGD(learning_rate=0.01, momentum=0.0, nesterov=True)
    elif optimizer == 'adam':
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=True)
    elif optimizer == 'adadelta':
        optimizer = tf.keras.optimizers.Adadelta(learning_rate=0.001, rho=0.95, epsilon=1e-07)
    elif optimizer == 'adagrad':
        optimizer = tf.keras.optimizers.Adagrad(learning_rate=0.001, initial_accumulator_value=0.1, epsilon=1e-07)
    elif optimizer == 'adamax':
        optimizer = tf.keras.optimizers.Adamax(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07)
    elif optimizer == 'ftrl':
        optimizer = tf.keras.optimizers.Ftrl(learning_rate=0.001, learning_rate_power=-0.5,
                                             initial_accumulator_value=0.1, l1_regularization_strength=0.0,
                                             l2_regularization_strength=0.0, l2_shrinkage_regularization_strength=0.0)
    elif optimizer == 'nadam':
        optimizer = tf.keras.optimizers.Nadam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07)
    elif optimizer == 'rmsprop':
        optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.001, rho=0.9, momentum=0.0, epsilon=1e-07,
                                                centered=True)

    model.compile(optimizer=optimizer,
                  loss=loss,
                  metrics=['accuracy'])

    model.save(modelPath, model.fit(input_train, output_train, epochs=epoch))