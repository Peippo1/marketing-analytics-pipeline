from pathlib import Path

from models import evaluate_model


def test_resolve_latest_model_path_picks_newest_file(tmp_path: Path):
    older = tmp_path / "trained_model_20240101_010101.pkl"
    newer = tmp_path / "trained_model_20240102_010101.pkl"
    older.write_text("old")
    newer.write_text("new")

    resolved = evaluate_model.resolve_latest_model_path(tmp_path)

    assert resolved == newer


def test_write_metrics_uses_model_stem(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(evaluate_model, "METRICS_OUTPUT_DIR", tmp_path)

    output_path = evaluate_model.write_metrics(
        {"accuracy": 0.9},
        Path("trained_model_20240102_010101.pkl"),
    )

    assert output_path == tmp_path / "trained_model_20240102_010101_evaluation.json"
    assert output_path.exists()
