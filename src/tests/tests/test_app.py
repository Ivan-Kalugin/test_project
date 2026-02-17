from src.app import run


def test_run(capsys):
    run()
    captured = capsys.readouterr()
    assert "Привет, Ив!" in captured.out
