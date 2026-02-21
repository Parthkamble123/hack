"""
simulation package

Handles:
- SUMO lifecycle management
- TraCI communication
- Traffic state extraction
- Emergency vehicle handling
- Signal coordination logic
- Metrics collection
"""

from .simulation_manager import SimulationManager
from .traci_controller import TraciController
from .state_extractor import StateExtractor
from .emergency_handler import EmergencyHandler
from .coordination_manager import CoordinationManager
from .metrics import MetricsCollector


__all__ = [
    "SimulationManager",
    "TraciController",
    "StateExtractor",
    "EmergencyHandler",
    "CoordinationManager",
    "MetricsCollector",
]