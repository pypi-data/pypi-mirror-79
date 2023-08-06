from tensorflow.keras.models import load_model

def getPrediction(input_test, output_test, modelPath):

    model = load_model(modelPath)

    test_loss, test_acc = model.evaluate(input_test, output_test, verbose=2)

    print('\nTest accuracy:', test_acc)

    predictions = model.predict(input_test)

    return predictions