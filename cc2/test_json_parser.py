import os
import subprocess
import pytest
import json

cwd = 'cc2'

if os.path.basename(os.getcwd()) == "cc2":
    os.chdir(os.path.dirname(os.getcwd()))

def test_step_1_valid():
    result = subprocess.run(
        ["python", os.path.join(cwd, "json_parser_cli.py"), "-f", os.path.join("tests", "step1", "valid.json")],
        capture_output=True,
        text=True,
    )
    
    try:
        with open(os.path.join("cc2","tests", "step1", "valid.json"), "r") as valid_json:
            data = valid_json.read()
    except FileNotFoundError:
        assert False

    assert json.loads(result.stdout) == json.loads(data)
    assert result.returncode == 0

def test_step_1_invalid():
    result = subprocess.run(
        ["python", os.path.join(cwd, "json_parser_cli.py"), "-f", os.path.join("tests", "step1", "invalid.json")],
        capture_output=True,
        text=True,
    )

    assert result.returncode !=0
    assert len(result.stdout) == 0
    assert len(result.stderr) != 0

def test_step_2_valid():
    result = subprocess.run(
        ["python", os.path.join(cwd, "json_parser_cli.py"), "-f", os.path.join("tests", "step2", "valid.json")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert len(result.stderr) == 0
    assert len(result.stdout) != 0

def test_step_4_valid():
    result = subprocess.run(
        ["python", os.path.join(cwd, "json_parser_cli.py"), "-f", os.path.join("tests", "step4", "valid.json")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert len(result.stderr) == 0
    assert len(result.stdout) != 0

if __name__ == "__main__":
    pytest.main()