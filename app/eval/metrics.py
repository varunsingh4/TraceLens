def recall_at_k(relevant: set[str], retrieved: list[str], k: int) -> float:
    """Share of labeled-relevant documents that appear in the top k retrieved docs.

    Recall@k = |relevant ∩ retrieved[:k]| / |relevant|

    Retrieved is ordered. Duplicates in the top k still count as one document.
    If there are no gold labels, the score is undefined and we return 0.0.
    """
    if not relevant or k <= 0:
        return 0.0
    top_k = set(retrieved[:k])
    return len(relevant & top_k) / len(relevant)
