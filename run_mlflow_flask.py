import subprocess
import sys

# Allow optional port override: e.g., `python run_mlflow_flask.py 5001`
port = sys.argv[1] if len(sys.argv) > 1 else "5000"

subprocess.run([
    "waitress-serve",
    "--host=0.0.0.0",
    f"--port={port}",
    "mlflow.server:app"
])