__all__ = ["grow"]


def grow(axiom: str, rules: dict[str, str], n: int) -> str:
    """Grow an L-system from an axiom by iteratively applying rules.

    More info:
    https://en.wikipedia.org/wiki/L-system

    Growing the original Algea:
    >>> grow("A", {"A": "AB", "B": "A"}, 5)
    'ABAABABAABAAB'
    >>> grow("A", {"A": "AB", "B": "A"}, 6)
    'ABAABABAABAABABAABABA'

    Parameters
    ----------
    axiom : str
        The starting string
    rules : :obj:`dict` of :obj:`str`:
        Dictionary of reqrite rules, i.e. key becomes value
    n : int
        Amount of iterations

    Returns
    -------
    str
        The grown string
    """
    s = axiom
    for _ in range(n):
        s = "".join(rules.get(s_n, s_n) for s_n in s)
    return s
