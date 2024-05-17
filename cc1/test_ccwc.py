import os
import subprocess
import pytest

cwd = "cc1"

if os.path.basename(os.getcwd()) == "cc1":
    os.chdir(os.path.dirname(os.getcwd()))


def test_step_1():
    result = subprocess.run(
        ["python", os.path.join(cwd, "ccwc.py"), "-c", os.path.join(cwd, "text.txt")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert int(result.stdout.split()[0]) == 342190

def test_step_2():
    result = subprocess.run(
        ["python", os.path.join(cwd, "ccwc.py"), "-l", os.path.join(cwd, "text.txt")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert int(result.stdout.split()[0]) == 7145

def test_step_3():
    result = subprocess.run(
        ["python", os.path.join(cwd, "ccwc.py"), "-w", os.path.join(cwd, "text.txt")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert int(result.stdout.split()[0]) == 58164

def test_step_4():
    result = subprocess.run(
        ["python", os.path.join(cwd, "ccwc.py"), "-m", os.path.join(cwd, "text.txt")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert int(result.stdout.split()[0]) == 339292

def test_step_5():
    result = subprocess.run(
        ["python", os.path.join(cwd, "ccwc.py"), os.path.join(cwd, "text.txt")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert int(result.stdout.split()[0]) == 7145
    assert int(result.stdout.split()[1]) == 58164
    assert int(result.stdout.split()[2]) == 342190

def test_step_6():
    p1 = subprocess.Popen(['cat', os.path.join(cwd, 'text.txt')], stdout=subprocess.PIPE, text=True)
    p2 = subprocess.Popen(['python', os.path.join(cwd, 'ccwc.py'), '-c', os.path.join(cwd, 'text.txt')], stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
    if p1.stdout is not None:
        p1.stdout.close() 
    result = p2.communicate()[0]

    assert p2.returncode == 0
    assert int(result.split()[0]) == 342190

    


if __name__ == "__main__":
    pytest.main()
