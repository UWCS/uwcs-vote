import pytest

from votes.stv import Election, ElectionError


def test_fptp_equivalent():
    c = {1, 2}
    v = [(1, 2)] * 9 + [(2, 1)] * 8 + [(2,)] + [(1,)]
    e = Election(c, v, 1)
    e.full_election()
    assert e.winners() == [1]


def test_immediate_majority():
    c = {1, 2, 3, 4}
    v = [(1, 2, 3, 4)] * 9 + [(2, 3, 1, 4)] * 4 + [(3, 1, 4, 2)] * 3 + [(4, 1)] * 2
    e = Election(c, v, 1)
    e.full_election()
    assert e.winners() == [1]


def test_delayed_majority():
    c = {1, 2, 3, 4}
    v = [(4, 2, 1, 3)] * 4 + [(3, 2, 4, 1)] * 4 + [(2, 4, 1, 3)]
    e = Election(c, v, 1)
    e.full_election()
    assert e.winners() == [4]


def test_delayeder_majority():
    c = {1, 2, 3, 4}
    v = [(4, 2, 1, 3)] * 4 + [(3, 2, 4, 1)] * 5 + [(2, 1, 4, 3)] + [(1, 4, 2, 3)]
    e = Election(c, v, 1)
    e.full_election()
    assert e.winners() == [4]


def test_two_available_three():
    c = {1, 2, 3}
    v = [
        (1, 2, 3),
        (1, 3, 2),
        (2,),
        (3, 1),
        (3, 1),
        (1, 2, 3),
        (2,),
        (1, 3, 2),
        (1, 3, 2),
        (1, 3, 2),
        (1, 3, 2),
        (1, 3, 2),
    ]
    e = Election(c, v, 2)
    e.full_election()
    assert sorted(e.winners()) in [[1, 2], [1, 3]]


def test_corner_case():
    c = {1, 2, 3, 4, 5, 6, 7, 8}
    v = (
        [(1, 2, 3, 4, 5, 6, 7, 8)]
        + [(3, 4, 5, 6, 7, 8, 1, 2)] * 36
        + [(4, 5, 6, 7, 8, 1, 2, 3)] * 6
        + [(5, 6, 7, 8, 1, 2, 3, 4)] * 13
        + [(6, 7, 8, 1, 2, 3, 4, 5)] * 4
        + [(7, 8, 1, 2, 3, 4, 5, 6)] * 2
        + [(8, 1, 2, 3, 4, 5, 6, 7)] * 4
    )
    e = Election(c, v, 2)
    e.full_election()
    # Bug caused the second round to erroneously tiebreak between all people after electing 3.
    # Check this isn't reintroduced
    assert e.actlog[2]["type"] != "tiebreak"
    assert sorted(e.winners()) == [3, 5]


def test_two_available_four():
    c = {1, 2, 3, 4}
    v = (
        [(4, 2, 1, 3)] * 4
        + [(3, 2, 4, 1)] * 5
        + [(2, 1, 4, 3)] * 3
        + [(1, 4, 2, 3)] * 2
    )
    e = Election(c, v, 2)
    e.full_election()
    assert sorted(e.winners()) == [3, 4]


def test_tiebreaker():
    c = {1, 2, 3, 4}
    v = [(1,), (2,), (3,), (4,)]
    e = Election(c, v, 1)
    e.full_election()
    assert e.winners() in [[1], [2], [3], [4]]


def test_malformed():
    c = {1, 2}
    v = [(1, 2, 1)] * 10
    with pytest.raises(ElectionError):
        Election(c, v, 1)


def test_malformed2():
    c = {1, 2, 3}
    v = [(1, 2, 3, 4)] * 10
    with pytest.raises(ElectionError):
        Election(c, v, 1)
