#!/usr/bin/env python3
import sys
print(sys.executable)
print(sys.version)
for m in ("playwright", "numpy", "PIL", "requests"):
    try:
        __import__(m)
        print("OK", m)
    except Exception as e:
        print("FALTA", m, e)
