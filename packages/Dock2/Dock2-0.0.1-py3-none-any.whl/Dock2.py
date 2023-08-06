"""Dock2 - Simple Wrapper for h2csmuggle

"""

import os
import subprocess
import urllib.request


class CMD(list):
    def __init__(self, cmd):
        self.extend(cmd.split(' '))


def upgrade(url: str = 'https://www.example.com', h_path: str = 'driver.py'):
    cmd = CMD(f'python {h_path} -x {url} --test')
    out = b''
    pipe = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(pipe.stdout.readline, b''):
        out += line
    return out


def cmd(user_cmd: str = '-h', h_path: str = 'driver.py'):
    cmd = CMD(f'python driver.py {user_cmd}')
    out = b''
    pipe = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(pipe.stdout.readline, b''):
        out += line
    return out


def main():
    pass


if __name__ == '__main__':
    main()
