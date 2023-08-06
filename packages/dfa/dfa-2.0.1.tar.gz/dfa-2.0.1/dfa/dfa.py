from typing import Hashable, FrozenSet, Callable, Optional

import attr
import funcy as fn


State = Hashable
Letter = Hashable
Alphabet = FrozenSet[Letter]


@attr.s(frozen=True, auto_attribs=True)
class DFA:
    start: State
    _label: Callable[[State], Letter] = attr.ib(
        converter=fn.memoize
    )
    _transition: Callable[[State, Letter], State] = attr.ib(
        converter=fn.memoize
    )
    inputs: Optional[Alphabet] = attr.ib(
        converter=lambda x: x if x is None else frozenset(x), default=None
    )
    outputs: Alphabet = attr.ib(converter=frozenset, default={True, False})

    def trace(self, word, *, start=None):
        state = self.start if start is None else start
        yield state

        for char in word:
            assert (self.inputs is None) or (char in self.inputs)
            state = self._transition(state, char)
            yield state

    def transition(self, word, *, start=None):
        return fn.last(self.trace(word, start=start))

    def label(self, word, *, start=None):
        output = self._label(self.transition(word, start=start))
        assert (self.outputs is None) or (output in self.outputs)
        return output

    def transduce(self, word, *, start=None):
        return tuple(map(self._label, self.trace(word, start=start)))[:-1]

    @fn.memoize()
    def states(self):
        assert self.inputs is not None, "Need to specify inputs field for DFA!"

        visited = set()
        stack = [self.start]
        while stack:
            curr = stack.pop()
            if curr in visited:
                continue
            else:
                visited.add(curr)

            successors = [self._transition(curr, a) for a in self.inputs]
            stack.extend(successors)

        return visited
