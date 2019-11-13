import pytest
import suctocude as su
import samples as sa


def test_checker():
    assert su.checker(sa.grid) == False
    assert su.checker(sa.gridSolved) == True
    assert su.checker(sa.gridShapeErr) == False
