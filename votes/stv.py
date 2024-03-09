import secrets
from enum import Enum
from decimal import Decimal, Context, localcontext, ROUND_DOWN, ROUND_UP
from operator import attrgetter, itemgetter
from typing import Dict, List, Set, Tuple

"""
STV calculator

Based on procedure as defined in https://prfound.org/resources/reference/reference-meek-rule/
Uses exact ratio arithmetic to prevent need to use epsilon float comparisons.
Uses a secure random generator to split ties randomly. 
Unfortunately this is more likely to trigger than I'd prefer due to the small populations and single seats.
"""


class ElectionError(RuntimeError):
    pass


class States(Enum):
    HOPEFUL = 0
    WITHDRAWN = 1
    ELECTED = 2
    DEFEATED = 3

    def __repr__(self):
        return "<%s: %r>" % (self._name_, self._value_)

    def __str__(self):
        return "%s" % (self._name_)


class Candidate:
    def __init__(self, id_: int):
        self.id = id_
        self.status = States.HOPEFUL
        self.keep_factor: float = 1.0

    def __str__(self):
        return f"{self.id}: {self.status} ({str(self.keep_factor)})"

    def __repr__(self):
        return self.__str__()


class Vote:
    def __init__(self, candidates: Dict[int, Candidate], prefs: Tuple[int, ...]):
        self.prefs = tuple(map(candidates.get, prefs))

    def check(self, candidates: Set[Candidate]):
        if len(self.prefs) != len(set(self.prefs)):
            raise ElectionError(f"Double Vote [{self.prefs}]")
        for i in self.prefs:
            if i not in candidates:
                raise ElectionError(f"Unknown Candidate [{self.prefs}]")

    def __str__(self):
        return "(" + (", ".join(map(lambda x: str(x.id_), self.prefs))) + ")"

    def __repr__(self):
        return "Vote" + self.__str__()


class Election:
    def __init__(self, candidates: Set[int], votes: List[Tuple[int, ...]], seats: int):
        self.candidatedict = {i: Candidate(i) for i in candidates}
        self.candidates = set(self.candidatedict.values())
        self.votes = [Vote(self.candidatedict, i) for i in votes]
        self.seats = seats
        self.rounds = 0
        self.fulllog = []
        self.actlog = []
        print(candidates, votes, seats)
        self.omega = 0.000001
        for i in self.votes:
            i.check(self.candidates)

    def withdraw(self, candidates: Set[int]):
        candidates = [self.candidatedict[cand] for cand in candidates]
        for i in candidates:
            i.status = States.WITHDRAWN
            i.keep_factor = 0.0

    def round(self):
        self.rounds += 1
        # B1
        shortcircuit = False
        electable = []
        elected = []
        for candidate in self.candidates:
            if candidate.status == States.ELECTED or candidate.status == States.HOPEFUL:
                electable.append(candidate)
                if candidate.status == States.ELECTED:
                    elected.append(candidate)
        if len(electable) <= self.seats:
            for i in electable:
                i.status = States.ELECTED
            shortcircuit = True
        elif len(elected) == self.seats:
            for candidate in self.candidates:
                if candidate.status == States.HOPEFUL:
                    candidate.status = States.DEFEATED
            shortcircuit = True

        converged = False
        wastage = 0.0
        scores = {k: 0.0 for k in self.candidates}
        quota = None

        previous_surplus = float("+Infinity")
        while not converged:
            # B2a
            wastage = 0.0
            scores = {k: 0.0 for k in self.candidates}
            for vote in self.votes:
                weight: float = 1.0
                for candidate in vote.prefs:
                    delta: float = weight * candidate.keep_factor
                    scores[candidate] += delta
                    weight -= delta
                    if weight == 0:
                        continue
                wastage += weight

            # Check all votes accounted for
            assert len(self.votes) - self.omega <= wastage + sum(scores.values()) <= len(self.votes) + self.omega

            # B2b
            quota = sum(scores.values()) / (self.seats + 1) + 0.000000001

            if shortcircuit:
                # Defer shortcircuit until after scores calculated to log one extra line
                self._log(scores, wastage, quota)
                self._report()
                raise StopIteration("Election Finished")

            # B2c
            elected = False
            for candidate in self.candidates:
                if candidate.status == States.HOPEFUL and scores[candidate] > quota:
                    candidate.status = States.ELECTED
                    elected = True

            # B2d
            surplus = 0.0
            for candidate in self.candidates:
                if candidate.status == States.ELECTED:
                    surplus += scores[candidate] - quota

            # B2e
            if elected:
                self._log(scores, wastage, quota)
                return

            if surplus < self.omega or surplus >= previous_surplus:
                converged = True
            else:
                # B2f
                for candidate in self.candidates:
                    if candidate.status == States.ELECTED:
                        candidate.keep_factor = (candidate.keep_factor * quota) / scores[candidate]
            previous_surplus = surplus

        # B3
        sorted_results = sorted(
            filter(lambda x: x[0].status == States.HOPEFUL, scores.items()),
            key=itemgetter(1),
        )
        min_score = sorted_results[0][1]
        eliminated_candidate: Candidate = self._choose(
            list(filter(lambda x: x[1] <= min_score + self.omega, sorted_results))
        )
        eliminated_candidate.status = States.DEFEATED
        eliminated_candidate.keep_factor = 0.0

        self._log(scores, wastage, quota)

    def _choose(self, candidates):
        if len(candidates) > 1:
            a = secrets.choice(candidates)[0]
            self._addlog("-Tiebreak-")
            self._addlog(a)
            self._addlog()
            self._addaction(
                "tiebreak",
                {
                    "round": self.rounds,
                    "candidates": [str(candidate[0].id) for candidate in candidates],
                    "choice": str(a.id),
                },
            )
        else:
            a = candidates[0][0]
        return a

    def _addaction(self, type, details):
        self.actlog.append({"type": type, "details": details})

    def _addlog(self, *args):
        string = " ".join(map(str, args))
        self.fulllog.append(string)
        print(string)

    def _log(self, scores, wastage, quota):
        self._addlog(self.rounds)
        self._addlog("======")
        candstates = {}
        for i in sorted(self.candidates, key=attrgetter('id')):
            assert isinstance(i, Candidate)
            self._addlog("Candidate:", i.id, i.keep_factor)
            self._addlog("Status:", str(i.status))
            self._addlog("Votes:", str(scores[i]))
            self._addlog()
            candstates[str(i.id)] = {
                "keep_factor": float(i.keep_factor),
                "status": str(i.status),
                "votes": float(scores[i]),
            }
        self._addlog("Wastage:", str(wastage))
        self._addlog("Threshold:", str(quota))
        self._addlog()

        self._addaction(
            "round",
            {
                "round": self.rounds,
                "candidates": candstates,
                "wastage": float(wastage),
                "threshold": float(quota),
            },
        )

    def _report(self):
        self._addlog("**Election Results**")
        self._addlog()
        candstates = {"ELECTED": [], "DEFEATED": [], "WITHDRAWN": []}
        self._addlog("ELECTED")
        for i in filter(lambda x: x.status == States.ELECTED, self.candidates):
            self._addlog(" Candidate", i.id)
            candstates["ELECTED"].append(str(i.id))
        self._addlog("DEFEATED")
        for i in filter(lambda x: x.status == States.DEFEATED, self.candidates):
            self._addlog(" Candidate", i.id)
            candstates["DEFEATED"].append(str(i.id))
        self._addlog("WITHDRAWN")
        for i in filter(lambda x: x.status == States.WITHDRAWN, self.candidates):
            self._addlog(" Candidate", i.id)
            candstates["WITHDRAWN"].append(str(i.id))
        self._addlog()
        self._addaction("report", candstates)

    def full_election(self):
        # Log initial state
        scores = {k: Decimal(0) for k in self.candidates}
        wastage = Decimal(0)
        for vote in self.votes:
            if len(vote.prefs) > 0:
                scores[vote.prefs[0]] += 1
            else:
                wastage += 1
        quota = Decimal(sum(scores.values())) / Decimal(self.seats + 1)
        self._log(scores, wastage, quota)

        try:
            while True:
                self.round()
        except StopIteration:
            pass

    def winners(self):
        return list(
            map(
                attrgetter("id"),
                filter(lambda x: x.status == States.ELECTED, self.candidates),
            )
        )


class DeterministicElection(Election):
    def __init__(self, *args, random_picks=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.random_picks = random_picks

    def _choose(self, candidates):
        if len(candidates) > 1:
            # Fix random choice to known behaviour. Only useful for tests
            i = self.random_picks[self.rounds]
            a = [candidate[0] for candidate in candidates if candidate[0].id == i][0]
            self._addlog("-Tiebreak-")
            self._addlog("! DETERMINISTIC PICK ! DEBUG ONLY ! DETERMINISTIC PICK !")
            self._addlog(a)
            self._addlog()
            self._addaction(
                "tiebreak",
                {
                    "round": self.rounds,
                    "candidates": [str(candidate[0].id) for candidate in candidates],
                    "choice": str(a.id),
                },
            )
        else:
            a = candidates[0][0]
        return a
