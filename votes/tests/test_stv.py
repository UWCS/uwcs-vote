from pathlib import Path

import pytest

from votes.stv import Election, ElectionError, DeterministicElection


def read_blt(file_path: Path, det_picks: dict[int,int]):
    """
    A blt file looks a bit like this
    4 2
    -2
    3 1 3 4 0
    4 1 3 2 0
    2 4 1 3 0
    1 2 0
    2 2 4 3 1 0
    1 3 4 2 0
    0
    "Adam"
    "Basil"
    "Charlotte"
    "Donald"
    "Title"
    """

    def split_vote(line) -> list[tuple[int, ...]] | None:
        vals = [int(x) for x in line.split(" ")]
        c = vals.pop(0)
        if c == 0:
            return None
        assert vals.pop() == 0
        return [tuple(vals)] * c

    with file_path.open() as fp:
        count, seats = map(int, fp.readline().strip().split(" "))
        maybe_withdrawn = fp.readline().strip()
        votes = []
        if "-" in maybe_withdrawn:
            withdrawn = [-int(x) for x in maybe_withdrawn.split(" ")]
            line = fp.readline().strip()
        else:
            withdrawn = []
            line = maybe_withdrawn
        while True:
            v = split_vote(line)
            if v is None:
                break
            votes.extend(v)
            line = fp.readline().strip()
        e = DeterministicElection(set(range(1, count + 1)), votes, seats, random_picks=det_picks)
        if withdrawn:
            e.withdraw(set(withdrawn))
        return e


@pytest.mark.parametrize("file,picks,winners,tiebreak", [
    ("42.blt", {2:3}, [1, 2], {2: [2, 3]}),
    ("513.blt", {2:3}, [1, 2], {2: [2, 3]}),
    ("M135.blt", {12:13}, [1, 2, 3, 4, 6, 9, 10], {12: [13, 16]}),
    ("SC.blt", {2:6, 3:10, 4:11}, [4, 7, 8, 13], {2: [6, 10, 11, 12], 3: [10, 11, 12], 4:[11,12]}),
    ("SCw.blt", {2:6, 3:10, 4:11}, [1, 7, 8, 13], {2: [6, 10, 11, 12], 3: [10, 11, 12], 4:[11,12]}),
    ("SC-Vm-12.blt", {2: 3}, [1, 2, 4], {2: [3, 4, 5]}),
])
def test_blts(data, file, winners, tiebreak, picks):
    e = read_blt(data / file, picks)
    e.full_election()
    assert sorted(e.winners()) == winners
    count = 0
    for i in e.actlog:
        if i['type'] == "tiebreak":
            count += 1
            d = i['details']
            assert d['round'] in tiebreak.keys()
            assert sorted([int(c) for c in d['candidates']]) == sorted(tiebreak[d['round']])
    assert count == len(tiebreak)


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
    assert sorted(e.winners()) == [3, 4]


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
