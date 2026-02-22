# run_debug.py  ← create this new file
import sys, os
sys.path.insert(0, os.getcwd())

from simulation.simulation_manager import SimulationManager

try:
    mgr = SimulationManager()
    results = mgr.run()
    print("Done:", results["summary"])
except Exception as e:
    import traceback
    traceback.print_exc()
    input("\n\nPress ENTER to close...")  # keeps window open