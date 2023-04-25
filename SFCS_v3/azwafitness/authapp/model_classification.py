import pickle
from Random_Forest.Random_Forest import Random_Forest

class Model_Classification(object):
    _instance = None

    model = None
    classes = ["Extremely Weak", "Weak", "Normal", "Overweight", "Obesity", "Extreme Obesity"]
    @staticmethod
    def get_instance():
        if Model_Classification._instance is None:
            Model_Classification._instance = Model_Classification()
        return Model_Classification._instance
    
    # tạo biến model, tải model
    def __init__(self):
        self.model = None
        self.model = self.load_model()

    def load_model(self):
        # load model
        with open('azwafitness\model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
        
    def predict(self, data):
        # predict
        result = self.model.predict(data)
        return result
    
    def get_classes(self):
        return self.classes
        