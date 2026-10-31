import pytest

from hello_app.__main__ import main


def test_main_default(capsys: pytest.CaptureFixture[str]) -> None:
    assert main([]) == 0
    assert capsys.readouterr().out.strip() == "Hello, World!"


def test_main_name(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--name", "CI"]) == 0
    assert capsys.readouterr().out.strip() == "Hello, CI!"
