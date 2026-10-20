from app.eval.metrics import recall_at_k


def test_perfect_recall() -> None:
    relevant = {"release_notes.txt", "stack_trace.log"}
    retrieved = ["release_notes.txt", "stack_trace.log", "inventory.md"]
    assert recall_at_k(relevant, retrieved, k=5) == 1.0


def test_partial_recall_at_k() -> None:
    relevant = {"a", "b", "c"}
    retrieved = ["a", "noise", "b"]
    assert recall_at_k(relevant, retrieved, k=3) == 2 / 3


def test_miss_outside_k_does_not_count() -> None:
    relevant = {"needed"}
    retrieved = ["noise", "noise2", "needed"]
    assert recall_at_k(relevant, retrieved, k=2) == 0.0
