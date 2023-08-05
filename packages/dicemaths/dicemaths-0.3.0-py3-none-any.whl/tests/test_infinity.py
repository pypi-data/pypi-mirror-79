from dicemaths.infinity import (contested_roll_hit_avg, uncontested_hit_avg)
import pytest

def test_contested_basic():
    (hits, crits) = contested_roll_hit_avg(1, 10, 1, 0)
    assert (round(hits, 5), round(crits, 5)) == (0.4275, 0.0475)

def test_uncontested_basic():
    (hits, crits) = uncontested_hit_avg(1, 10)
    assert (round(hits, 4), round(crits, 4)) == (0.45, 0.05)

def test_uncontested_bonus():
    (hits, crits) = uncontested_hit_avg(1, 25)
    assert (round(hits, 4), round(crits, 4)) == (0.7, 0.3)

def test_uncontested_one():
    (hits, crits) = uncontested_hit_avg(1, 1)
    assert (round(hits, 4), round(crits, 4)) == (0.0, 0.05)