import pytest
import suctocude as su
import samples as sa


def test_checker():
    assert su.Suctocude.checker(su, sa.grid) == False
    assert su.Suctocude.checker(su, sa.gridSolved) == True
    assert su.Suctocude.checker(su, sa.gridShapeErr) == False
