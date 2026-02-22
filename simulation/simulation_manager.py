# simulation/simulation_manager.py

import time
from config.simulation_config import SimulationConfig
from config.paths import Paths
from simulation.traci_controller import TraCIController
from simulation.coordination_manager import CoordinationManager
from simulation.metrics import Metrics
from utils.metrics_store import metrics_store
from utils.logger import get_logger

logger = get_logger(__name__)


class SimulationManager:
    def __init__(self):
        Paths.validate()
        self.traci        = TraCIController()
        self.coordinator  = CoordinationManager()
        self.metrics      = Metrics()

    def run(self) -> dict:
        metrics_store.reset()
        metrics_store.set_running(True)

        self.traci.start()
        logger.info("Simulation started | AI: %s | Steps: %d",
                    self.coordinator.is_ai_active, SimulationConfig.MAX_STEPS)

        step = 0
        try:
            for step in range(SimulationConfig.MAX_STEPS):
                self.traci.step()
                phase_decisions = self.coordinator.step()
                self.metrics.update(phase_decisions)

                if step > 0 and step % 100 == 0:
                    logger.info("Step %d/%d | Sim time: %.1fs | Arrived: %d",
                                step, SimulationConfig.MAX_STEPS,
                                self.traci.get_simulation_time(),
                                self.metrics._arrived_total)

                if SimulationConfig.REAL_TIME_DELAY > 0:
                    time.sleep(SimulationConfig.REAL_TIME_DELAY)

        except KeyboardInterrupt:
            logger.warning("Simulation interrupted at step %d.", step)
        except Exception as e:
            logger.error("Simulation error at step %d: %s", step, e, exc_info=True)
            metrics_store.set_error(str(e))
            raise
        finally:
            self.traci.close()
            csv_path = self.metrics.export_csv()
            summary  = self.metrics.get_results()
            metrics_store.set_summary(summary)
            metrics_store.set_running(False)
            logger.info("Done. Summary: %s", summary)

        return {"summary": self.metrics.get_results(), "history": self.metrics.history}
