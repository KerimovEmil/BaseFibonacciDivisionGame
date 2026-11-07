"""Undo / redo via state snapshots (robust and exact for split/merge moves)."""


class History:
    def __init__(self, initial_state):
        self._undo = [(self._clone(initial_state), None)]
        self._redo = []

    @staticmethod
    def _clone(state):
        return [list(row) for row in state]

    def record(self, state, label=None):
        """Call after a successful move with the new state and optional move label."""
        self._undo.append((self._clone(state), label))
        self._redo.clear()

    def can_undo(self):
        return len(self._undo) > 1

    def can_redo(self):
        return bool(self._redo)

    def undo(self):
        if not self.can_undo():
            return None
        self._redo.append(self._undo.pop())
        return self._clone(self._undo[-1][0])

    def redo(self):
        if not self.can_redo():
            return None
        state, label = self._redo.pop()
        self._undo.append((self._clone(state), label))
        return self._clone(state)

    def reset_to_initial(self):
        first_state, _ = self._undo[0]
        self._undo = [(self._clone(first_state), None)]
        self._redo.clear()
        return self._clone(first_state)

    @property
    def labels(self):
        """Ordered list of active move descriptions (excluding undone moves)."""
        return [lbl for _, lbl in self._undo[1:] if lbl is not None]

    @property
    def move_count(self):
        return len(self._undo) - 1

