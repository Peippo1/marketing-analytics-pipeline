import run_mlflow_flask


def test_build_waitress_command_uses_host_and_port():
    assert run_mlflow_flask.build_waitress_command("127.0.0.1", "5001") == [
        "waitress-serve",
        "--host=127.0.0.1",
        "--port=5001",
        "mlflow.server:app",
    ]


def test_main_defaults_to_loopback_and_disables_job_execution(monkeypatch):
    recorded = {}

    def fake_run(cmd, check):
        recorded["cmd"] = cmd
        recorded["check"] = check

    monkeypatch.delenv("MLFLOW_HOST", raising=False)
    monkeypatch.delenv(run_mlflow_flask.JOB_EXECUTION_ENV_VAR, raising=False)
    monkeypatch.setattr(run_mlflow_flask.subprocess, "run", fake_run)

    exit_code = run_mlflow_flask.main(["5001"])

    assert exit_code == 0
    assert recorded["check"] is True
    assert recorded["cmd"] == [
        "waitress-serve",
        "--host=127.0.0.1",
        "--port=5001",
        "mlflow.server:app",
    ]
    assert run_mlflow_flask.os.environ[run_mlflow_flask.JOB_EXECUTION_ENV_VAR] == "false"


def test_main_rejects_remote_bind_without_explicit_job_execution_opt_in(monkeypatch, capsys):
    monkeypatch.setenv("MLFLOW_HOST", "0.0.0.0")
    monkeypatch.delenv(run_mlflow_flask.JOB_EXECUTION_ENV_VAR, raising=False)

    exit_code = run_mlflow_flask.main(["5001"])

    assert exit_code == 1
    assert "Refusing to expose MLflow" in capsys.readouterr().err


def test_main_allows_remote_bind_only_with_explicit_opt_in(monkeypatch):
    recorded = {}

    def fake_run(cmd, check):
        recorded["cmd"] = cmd
        recorded["check"] = check

    monkeypatch.setenv("MLFLOW_HOST", "0.0.0.0")
    monkeypatch.setenv(run_mlflow_flask.JOB_EXECUTION_ENV_VAR, "true")
    monkeypatch.setattr(run_mlflow_flask.subprocess, "run", fake_run)

    exit_code = run_mlflow_flask.main(["5001"])

    assert exit_code == 0
    assert recorded["check"] is True
    assert recorded["cmd"][1] == "--host=0.0.0.0"
