import src.evaluate as evaluate_module
from src.evaluate import evaluate_model
from src.preprocess import split_features_target
from src.train import train_model


def test_evaluate_model_creates_confusion_matrix(titanic_df, tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(evaluate_module, "REPORTS_DIR", tmp_path)

    X, y = split_features_target(titanic_df)
    model, X_test, y_test = train_model(X, y)

    evaluate_model(model, X_test, y_test)

    assert (tmp_path / "confusion_matrix.png").exists()
    captured = capsys.readouterr()
    assert "Accuracy" in captured.out
