import Dock2

url = 'https://www.example.com'


def test_upgrade_url():
    assert Dock2.upgrade(
        url) == b'[INFO] Failed to upgrade: https://www.example.com\r\n'


def test_upgrade_cmd():
    assert Dock2.cmd(
        f'-x {url} --test') == b'[INFO] Failed to upgrade: https://www.example.com\r\n'
