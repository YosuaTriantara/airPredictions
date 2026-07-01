from src.models.loader import ModelLoader

class ModelRegistry:
    def __init__(self):
        self.lstm = None
        self.xgboost = None
        self.scaler_X = None
        self.scaler_y = None
        self.category_mapping = None
        

    def initialize(self):
        self.lstm = ModelLoader.load_lstm()
        self.xgboost = ModelLoader.load_xgboost()
        self.scaler_X = ModelLoader.load_scaler_X()
        self.scaler_y = ModelLoader.load_scaler_y()
        self.category_mapping = ModelLoader.load_category_mapping()

registry = ModelRegistry()
