
# python
import re
# aw11
import aw11.clean
import aw11.version
# pytest
import pytest


def test_help(capsys):
    with pytest.raises(SystemExit) as sys_exit:
        aw11.clean.main(['--help'])
    assert(sys_exit.value.code == 0)
    out, err = out, err = capsys.readouterr()
    assert(out != '')
    assert(err == '')


def test_version(capsys):
    aw11.clean.main(['--version'])
    out, err = capsys.readouterr()
    assert(re.match(
        rf'{re.escape(aw11.version.__version__)}(\[\+[a-zA-Z0-9]+\])?',
        out.strip(),
    ))
    assert(err == '')
