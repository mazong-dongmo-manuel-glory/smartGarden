import sys
import os
print("CWD:", os.getcwd())
print("sys.path:", sys.path)
try:
    import sensors
    print("sensors imported:", sensors)
    from sensors import temperature
    print("sensors.temperature imported:", temperature)
except ImportError as e:
    print("Import failed:", e)
