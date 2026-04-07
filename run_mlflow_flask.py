import os
import subprocess
import sys


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "5000"
JOB_EXECUTION_ENV_VAR = "MLFLOW_SERVER_ENABLE_JOB_EXECUTION"
UNSAFE_REMOTE_HOSTS = {"0.0.0.0", "::"}


def build_waitress_command(host, port):
    return [
        "waitress-serve",
        f"--host={host}",
        f"--port={port}",
        "mlflow.server:app",
    ]


def should_enable_job_execution():
    return os.environ.get(JOB_EXECUTION_ENV_VAR, "").strip().lower() == "true"


def main(argv=None):
    argv = argv or sys.argv[1:]
    port = argv[0] if argv else DEFAULT_PORT
    host = os.environ.get("MLFLOW_HOST", DEFAULT_HOST)

    if host in UNSAFE_REMOTE_HOSTS and not should_enable_job_execution():
        print(
            "Refusing to expose MLflow on a network interface while job execution is disabled only by default. "
            "Keep the server bound to 127.0.0.1, or explicitly set both MLFLOW_HOST and "
            f"{JOB_EXECUTION_ENV_VAR}=true if you intend to manage that risk yourself.",
            file=sys.stderr,
        )
        return 1

    # Default to the safest available behavior until upstream ships a fix for the
    # unauthenticated jobs endpoint advisory. Operators can still opt in explicitly.
    os.environ.setdefault(JOB_EXECUTION_ENV_VAR, "false")

    subprocess.run(build_waitress_command(host, port), check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
