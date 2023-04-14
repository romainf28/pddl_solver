
from typing import FrozenSet, Set, Tuple


Fact = Tuple[str, str]
State = FrozenSet[Fact]
Ordering = Tuple[Fact, Fact]

class Fact:
    def __init__(self, fact: Tuple[str, str], negative: bool) -> None:
        self.variable, self.value = fact
        self.negative = negative

class Landmark:
    def __init__(self, facts: Set[Fact], negative_facts: Set[Fact]) -> None:
        self.facts = facts
        self.nfacts = negative_facts

    @property
    def is_fact(self) -> bool:
        return len(self.facts) == 1 and len(self.nfacts) == 0
    
    @property
    def is_nfact(self) -> bool:
        return len(self.nfacts) == 1 and len(self.facts) == 0

    @property
    def fact(self) -> Fact:
        if self.is_fact:
            return next(iter(self.facts))
        raise Exception("This landmark is not a fact landmark")
    
    @property
    def nfact(self) -> Fact:
        if self.is_nfact:
            return next(iter(self.nfacts))
        raise Exception("This landmark is not a negative fact landmark")
    
    @property
    def variables(self) -> Set[str]:
        return {fact[0] for fact in self.facts | self.nfacts}

    def contains(self, fact: Fact) -> bool:
        return not self.is_fact and fact in self.facts
    
    def containsn(self, nfact: Fact) -> bool:
        return not self.is_nfact and nfact in self.nfacts
    
    def is_satisfied_in_state(self, state: State):
        return self.facts.intersection(state) == self.facts and not self.nfacts.intersection(state)