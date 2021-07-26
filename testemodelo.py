from simpletransformers.classification import ClassificationModel
from scipy.special import softmax


lyrics = "I'm happy"

model = ClassificationModel("xlnet", "models", use_cuda=False)
predictions, raw_outputs = model.predict([lyrics])
probabilities = softmax(raw_outputs, axis=1)

print(predictions)

