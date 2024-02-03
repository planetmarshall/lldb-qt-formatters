import re

import pytest


@pytest.mark.lldb_script("frame variable map")
def test_qmap_of_qstring_uint_summary(lldb):
    match = re.search(r"\(QMap<.+>\) map = (?P<summary>.+) {", lldb, re.MULTILINE)
    assert match.group('summary') == 'Size: 3'


@pytest.mark.lldb_script("frame variable map")
def test_qmap_of_qstring_uint_children(lldb):
    match = re.search(r"\[0] = (?P<summary>\{.+})", lldb, re.MULTILINE)
    assert match.group('summary') == '{"forty-two": 42}'
