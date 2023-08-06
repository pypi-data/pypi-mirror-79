import os
import subprocess
import sys
import threading

import piquipe

VERSION = '0.0.0'


def run(args, *, env=None, shell=False, executable=None, timeout=None, check=False):
    with Popen(args, env=env, shell=shell, executable=executable) as process:
        try:
            stdout, stderr = process.communicate(timeout=timeout)

        except Exception:
            process.kill()
            raise

    completed_process = subprocess.CompletedProcess(
        process.args, process.returncode,
        stdout=stdout, stderr=stderr)

    if check:
        completed_process.check_returncode()

    return completed_process


def _forward_stream(in_stream, *out_streams):
    for line in iter(in_stream.readline, ''):
        for out_stream in out_streams:
            out_stream.write(line)

    in_stream.close()


def _new_forward_stream_thread(in_stream, *out_streams):
    thread = threading.Thread(target=_forward_stream, args=(in_stream, *out_streams), daemon=True)
    return thread


class Popen(subprocess.Popen):
    def __init__(self, args, *, env=None, shell=False, executable=None):
        super().__init__(
            args, env=env,
            shell=shell, executable=executable,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, text=True)

        self.__setup_stream_threads()

    def __setup_stream_threads(self):
        stdout_read_fd, stdout_write_fd = piquipe.pipe()
        stderr_read_fd, stderr_write_fd = piquipe.pipe()

        stdout_write_stream = os.fdopen(stdout_write_fd, mode='w', buffering=1)
        stderr_write_stream = os.fdopen(stderr_write_fd, mode='w', buffering=1)

        stdout_streams = [stdout_write_stream, sys.stdout]
        stderr_streams = [stderr_write_stream, sys.stderr]

        self.__stdout_thread = _new_forward_stream_thread(self.stdout, *stdout_streams)
        self.__stderr_thread = _new_forward_stream_thread(self.stderr, *stderr_streams)

        self.__stdout_thread.start()
        self.__stderr_thread.start()

        stdout_read_stream = os.fdopen(stdout_read_fd, mode='r', buffering=1)
        stderr_read_stream = os.fdopen(stderr_read_fd, mode='r', buffering=1)

        self.stdout = stdout_read_stream
        self.stderr = stderr_read_stream

    def __stop_stream_threads(self):
        self.__stdout_thread.join()
        self.__stderr_thread.join()

    def wait(self, timeout=None):
        returncode = super().wait(timeout)

        self.__stop_stream_threads()

        return returncode

    def __exit__(self, *args):
        self.wait()

        self.stdout.close()
        self.stderr.close()

    # pylint: disable=redefined-builtin
    def communicate(self, input=None, timeout=None):
        if input:
            raise ValueError("Interactive communication is not supported")

        self.wait(timeout)

        stdout = self.stdout.read()
        stderr = self.stderr.read()
        self.stdout.close()
        self.stderr.close()

        return (stdout, stderr)
