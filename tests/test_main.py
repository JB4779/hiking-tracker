from main import (
    main,
    hikes_menu,
    statistics_menu,
    gear_menu,
)


def test_hikes_menu_back(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    hikes_menu([])


def test_statistics_menu_back(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    statistics_menu([])


def test_gear_menu_back(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "0")

    gear_menu([])


def test_main_exit(monkeypatch, capsys):
    monkeypatch.setattr("main.load_hikes", lambda: [])
    monkeypatch.setattr("builtins.input", lambda _: "0")

    main()

    output = capsys.readouterr().out

    assert "Goodbye!" in output