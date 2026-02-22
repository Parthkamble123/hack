# simulation/coordination_manager.py

from ai.model_loader import ModelLoader
from ai.feature_builder import FeatureBuilder
from ai.predictor import Predictor
from ai.decision_engine import DecisionEngine
from config.model_config import ModelConfig
from config.paths import Paths
from utils.logger import get_logger

logger = get_logger(__name__)


class CoordinationManager:
    def __init__(self):
        self.engines: dict = {}
        self._load_engines()

    def _load_engines(self):
        model_loader = ModelLoader(Paths.MODEL_FILE)
        try:
            model = model_loader.load()
        except FileNotFoundError:
            logger.warning("Model not found — AI disabled. SUMO fixed-time logic will run.")
            return

        predictor = Predictor(model)

        for tl_id in ModelConfig.INTERSECTION_IDS:
            feature_builder = FeatureBuilder(traffic_light_id=tl_id)
            engine = DecisionEngine(
                feature_builder=feature_builder,
                predictor=predictor,
                traffic_light_id=tl_id,
            )
            self.engines[tl_id] = engine
            logger.info("DecisionEngine ready: %s", tl_id)

    def step(self) -> dict:
        results = {}
        for tl_id, engine in self.engines.items():
            try:
                results[tl_id] = engine.step()
            except Exception as e:
                logger.error("Engine error [%s]: %s", tl_id, e)
        return results

    @property
    def is_ai_active(self) -> bool:
        return len(self.engines) > 0
