"""Undo / redo via state snapshots (robust and exact for split/merge moves)."""


class History:
    def __init__(self, initial_state):
        self._undo = [self._clone(initial_state)]
        self._redo = []

    @staticmethod
    def _clone(state):
        return [list(row) for row in state]

    def record(self, state):
        """Call after a successful move with the new state."""
        self._undo.append(self._clone(state))
        self._redo.clear()

    def can_undo(self):
        return len(self._undo) > 1

    def can_redo(self):
        return bool(self._redo)

    def undo(self):
        if not self.can_undo():
            return None
        self._redo.append(self._undo.pop())
        return self._clone(self._undo[-1])

    def redo(self):
        if not self.can_redo():
            return None
        state = self._redo.pop()
        self._undo.append(self._clone(state))
        return self._clone(state)

    def reset_to_initial(self):
        first = self._undo[0]
        self._undo = [self._clone(first)]
        self._redo.clear()
        return self._clone(first)

    @property
    def move_count(self):
        return len(self._undo) - 1
