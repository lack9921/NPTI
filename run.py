import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from backend.app import app

if __name__ == "__main__":
    print("=" * 54)
    print("  NPFJ — Network Personality Factor Indicator")
    print("  🖥  http://localhost:8080")
    print("=" * 54)
    app.run(host="0.0.0.0", port=8080, debug=True)
