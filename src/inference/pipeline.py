from src.preprocessing.pipeline import run_preprocessing_pipeline
from src.inference.predictor import predictor
from src.inference.response import build_response
from src.models.registry import registry

class InferencePipeline:

    def run(self, data):

        processed = run_preprocessing_pipeline(
            data=data,
            scaler=registry.scaler_X
        )

        prediction = predictor.predict(processed)

        return build_response(prediction)


pipeline = InferencePipeline()