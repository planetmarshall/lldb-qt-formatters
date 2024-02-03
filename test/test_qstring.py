import re

import pytest


@pytest.mark.lldb_script("frame variable hello")
def test_qstring_summary(lldb):
    match = re.search(r"\(QString\) hello = (?P<summary>.+)", lldb, re.MULTILINE)
    assert match.group('summary') == '"Hello World"'


@pytest.mark.lldb_script("frame variable demosthenes")
def test_qstring_utf8(lldb):
    demosthenes = "Οὐχὶ ταὐτὰ παρίσταταί μοι γιγνώσκειν, ὦ ἄνδρες ᾿Αθηναῖοι"
    match = re.search(r"\(QString\) demosthenes = (?P<summary>.+)", lldb, re.MULTILINE)
    assert match.group('summary') == f'"{demosthenes}"'
