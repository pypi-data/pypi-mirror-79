import subprocess

import pytest

import dualitee


def test_popen_wait(capsys):
    with dualitee.Popen(['env', '--version']) as process:
        returncode = process.wait()

        process.stdout.read()
        process.stderr.read()

    stdout_sys, stderr_sys = capsys.readouterr()

    assert returncode == 0

    assert 'env' in stdout_sys
    assert stderr_sys == ''


def test_popen_wait_timeout():
    with pytest.raises(subprocess.TimeoutExpired):
        process = dualitee.Popen(['sleep', '9999'])
        process.wait(timeout=0.001)

    # pylint: disable=protected-access
    process.terminate()
    process.wait()

    process.stdout.read()
    process.stderr.read()
    process.stdout.close()
    process.stderr.close()


def test_popen_communicate(capsys):
    with dualitee.Popen(['env', '--version']) as process:
        stdout_buffer, stderr_buffer = process.communicate()

    returncode = process.returncode
    stdout_sys, stderr_sys = capsys.readouterr()

    assert 'env' in stdout_buffer
    assert stderr_buffer == ''

    assert returncode == 0

    assert 'env' in stdout_sys
    assert stderr_sys == ''


def test_popen_communicate_input():
    with pytest.raises(ValueError):
        process = dualitee.Popen(['env', '--version'])
        process.communicate(input=True)

    # pylint: disable=protected-access
    process.terminate()
    process.wait()

    process.stdout.read()
    process.stderr.read()
    process.stdout.close()
    process.stderr.close()


def test_popen_communicate_timeout(capsys):
    process = dualitee.Popen(['env', '--version'])

    stdout_buffer, stderr_buffer = process.communicate(timeout=3)
    returncode = process.wait()
    stdout_sys, stderr_sys = capsys.readouterr()

    assert 'env' in stdout_buffer
    assert stderr_buffer == ''

    assert returncode == 0

    assert 'env' in stdout_sys
    assert stderr_sys == ''


def test_popen_communicate_timeout_error():
    with pytest.raises(subprocess.TimeoutExpired):
        process = dualitee.Popen(['sleep', '9999'])
        process.communicate(timeout=0.001)

    # pylint: disable=protected-access
    process.terminate()
    process.wait()

    process.stdout.read()
    process.stderr.read()
    process.stdout.close()
    process.stderr.close()


def test_popen_shell(capsys):
    with dualitee.Popen('env --version', shell=True) as process:
        stdout_buffer, stderr_buffer = process.communicate()

    returncode = process.returncode
    stdout_sys, stderr_sys = capsys.readouterr()

    assert 'env' in stdout_buffer
    assert stderr_buffer == ''

    assert returncode == 0

    assert 'env' in stdout_sys
    assert stderr_sys == ''


def test_popen_bash(capsys):
    with dualitee.Popen('echo $SHELL', shell=True, executable='bash') as process:
        stdout_buffer, stderr_buffer = process.communicate()

    returncode = process.returncode
    stdout_sys, stderr_sys = capsys.readouterr()

    assert 'bash' in stdout_buffer
    assert stderr_buffer == ''

    assert returncode == 0

    assert 'bash' in stdout_sys
    assert stderr_sys == ''


def test_popen_env(capsys):
    with dualitee.Popen('echo $VAR', env={'VAR': 'variable'}, shell=True) as process:
        stdout_buffer, stderr_buffer = process.communicate()

    returncode = process.returncode
    stdout_sys, stderr_sys = capsys.readouterr()

    assert stdout_buffer.rstrip() == 'variable'
    assert stderr_buffer == ''

    assert returncode == 0

    assert stdout_sys.rstrip() == 'variable'
    assert stderr_sys == ''


def test_popen_stderr(capsys):
    with dualitee.Popen('echo error >&2', shell=True) as process:
        stdout_buffer, stderr_buffer = process.communicate()

    returncode = process.returncode
    stdout_sys, stderr_sys = capsys.readouterr()

    assert stdout_buffer == ''
    assert stderr_buffer.rstrip() == 'error'

    assert returncode == 0

    assert stdout_sys == ''
    assert stderr_sys.rstrip() == 'error'
