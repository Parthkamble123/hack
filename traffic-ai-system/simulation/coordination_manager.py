# simulation/coordination_manager.py

from ai.model_loader import ModelLoader
from ai.feature_builder import FeatureBuilder
from ai.predictor import Predictor
from ai.decision_engine import DecisionEngine
from config.model_config import ModelConfig
from config.paths import Paths


class CoordinationManager:
    """
    Manages multiple intersections.
    """

    def __init__(self):
        self.engines = {}
        self._initialize_engines()

    def _initialize_engines(self):
        model_loader = ModelLoader(Paths.MODEL_FILE)
        model = model_loader.load()
        predictor = Predictor(model)

        for tl_id in ModelConfig.INTERSECTION_IDS:
            feature_builder = FeatureBuilder()
            engine = DecisionEngine(
                model_loader,
                feature_builder,
                predictor,
                traffic_light_id=tl_id
            )
            self.engines[tl_id] = engine

    def step(self):
        for engine in self.engines.values():
            engine.step()