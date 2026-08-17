#Imports
from input_utils import (
    get_int,
    get_float,
    get_optional_int,
    get_optional_float,
    get_date,
    get_optional_date,
    is_valid_date_format,
    get_time,
    get_optional_time,
    format_time,
)


#Tests
def test_get_int(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda prompt: "500")

    result = get_int("Elevation: ")

    assert result == 500


def test_get_int_retries_after_invalid_input(monkeypatch, capsys):
    responses = iter(["abc", "500"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_int("Elevation: ")

    captured = capsys.readouterr()

    assert result == 500
    assert "Invalid input. Please enter an integer." in captured.out


def test_get_int_minimum(monkeypatch, capsys):
    responses = iter(["-100", "500"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_int("Elevation: ", minimum=0)

    captured = capsys.readouterr()

    assert result == 500
    assert "Value must be at least 0." in captured.out


def test_get_float(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "5.25"
    )

    result = get_float("Distance: ")

    assert result == 5.25


def test_get_float_minimum(monkeypatch, capsys):
    responses = iter(["-2.5", "5.25"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_float("Distance: ", minimum=0)

    captured = capsys.readouterr()

    assert result == 5.25
    assert "Value must be at least 0." in captured.out


def test_get_optional_int_keeps_current_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: ""
    )

    result = get_optional_int("Elevation: ", 500)

    assert result == 500


def test_get_optional_int_new_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "750"
    )

    result = get_optional_int("Elevation: ", 500)

    assert result == 750


def test_get_optional_int_minimum(monkeypatch, capsys):
    responses = iter(["-100", "750"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_optional_int(
        "Elevation: ",
        current_value=500,
        minimum=0,
    )

    captured = capsys.readouterr()

    assert result == 750
    assert "Value must be at least 0." in captured.out


#Float
def test_get_optional_float_keeps_current_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: ""
    )

    result = get_optional_float("Distance: ", 25.6)

    assert result == 25.6


def test_get_optional_float_new_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "75.4"
    )

    result = get_optional_float("Distance: ", 50.1)

    assert result == 75.4


def test_get_optional_float_minimum(monkeypatch, capsys):
    responses = iter(["-10.1", "75.1"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_optional_float(
        "Distance: ",
        current_value=50.1,
        minimum=0,
    )

    captured = capsys.readouterr()

    assert result == 75.1
    assert "Value must be at least 0." in captured.out


def test_valid_date_format():
    assert is_valid_date_format("2026-08-17") is True


def test_invalid_date_format():
    assert is_valid_date_format("08/17/2026") is False


def test_get_date(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "2026-08-17"
    )

    result = get_date("Date: ")

    assert result == "2026-08-17"


def test_get_date_retries_invalid_date(monkeypatch, capsys):
    responses = iter([
        "2026-02-30",
        "2026-02-28",
    ])

    # monkeypatch input here
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    # call get_date here
    result = get_date("Date: ")

    # capture printed output here
    captured = capsys.readouterr()

    # assert the returned date
    assert result == "2026-02-28"
    assert "Invalid date. Please enter a valid calendar date." in captured.out


def test_get_date_retries_invalid_format(monkeypatch, capsys):
    responses = iter([
        "08/17/2026",
        "2026-08-17",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_date("Date: ")

    captured = capsys.readouterr()

    assert result == "2026-08-17"
    assert "Invalid date format. Please use YYYY-MM-DD." in captured.out
 

def test_get_optional_date_keeps_current_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: ""
    )

    result = get_optional_date(
        "Date: ",
        current_value="2026-08-17",
    )

    assert result == "2026-08-17"


def test_get_optional_date_new_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "2026-09-01"
    )

    result = get_optional_date(
        "Date: ",
        current_value="2026-08-17",
    )

    assert result == "2026-09-01"


def test_get_optional_date_retries_invalid_date(monkeypatch, capsys):
    responses = iter([
        "2026-02-30",
        "2026-02-28",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_optional_date(
        "Date: ",
        current_value="2026-08-17",
    )

    captured = capsys.readouterr()

    assert result == "2026-02-28"
    assert "Invalid date. Please enter a valid calendar date." in captured.out


def test_get_optional_date_retries_invalid_format(monkeypatch, capsys):
    responses = iter([
        "08/17/2026",
        "2026-08-17",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_optional_date(
        "Date: ",
        current_value="2026-07-01",
    )

    captured = capsys.readouterr()

    assert result == "2026-08-17"
    assert "Invalid date format. Please use YYYY-MM-DD." in captured.out


def test_get_time(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "1:30"
    )

    result = get_time("Total time: ")

    assert result == 90


def test_get_time_retries_invalid_minutes(monkeypatch, capsys):
    responses = iter([
        "1:75",
        "1:30",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_time("Total time: ")

    captured = capsys.readouterr()

    assert result == 90
    assert "Invalid time format. Please use HH:MM." in captured.out


def test_format_time():
    assert format_time(90) == "01:30"


def test_get_optional_time_keeps_current_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: ""
    )

    result = get_optional_time(
        "Total time: ",
        current_value=90,
    )

    assert result == 90


def test_get_optional_time_new_value(monkeypatch):
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: "2:15"
    )

    result = get_optional_time(
        "Total time: ",
        current_value=90,
    )

    assert result == 135


def test_get_optional_time_retries_invalid_time(monkeypatch, capsys):
    responses = iter([
        "1:75",
        "2:15",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_optional_time(
        "Total time: ",
        current_value=90,
    )

    captured = capsys.readouterr()

    assert result == 135
    assert "Invalid time format. Please use HH:MM." in captured.out


def test_get_float_retries_after_invalid_input(monkeypatch, capsys):
    responses = iter(["abc", "5.25"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_float("Distance: ")

    captured = capsys.readouterr()

    assert result == 5.25
    assert "Invalid input. Please enter a number." in captured.out


def test_get_optional_float_retries_after_invalid_input(monkeypatch, capsys):
    responses = iter(["abc", "5.25"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_optional_float(
        "Distance: ",
        current_value=3.0,
    )

    captured = capsys.readouterr()

    assert result == 5.25
    assert "Invalid input. Please enter a number." in captured.out


def test_get_optional_int_retries_after_invalid_input(monkeypatch, capsys):
    responses = iter(["abc", "500"])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(responses)
    )

    result = get_optional_int(
        "Elevation: ",
        current_value=300,
    )

    captured = capsys.readouterr()

    assert result == 500
    assert "Invalid input. Please enter an integer." in captured.out
    