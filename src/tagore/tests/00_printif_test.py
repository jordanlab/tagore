#!/bin/env python3
import sys
from os import getcwd, pardir, path

import pytest

sys.path.append(path.abspath(path.join(getcwd())))
from tagore import printif


def test_printif_true():
    from io import StringIO

    output = StringIO()
    sys.stdout = output
    printif("Test passed", True)
    assert output.getvalue().strip() == "Test passed"


def test_printif_false():
    from io import StringIO

    output = StringIO()
    sys.stdout = output
    printif("Test false", False)
    assert output.getvalue().strip() == ""
