"""Mathematical core for tokenizer-induced Brauer descriptors.

This module implements both models used in the article:

* the occurrence-indexed baseline, whose descriptor vector is determined by
  sequence length N and local radius r;
* the token-type-collapsed refinement, which retains window multiplicities and
  becomes sensitive to repeated token strings.

The explicit constructors are deliberately simple reference implementations.
They are used to verify the closed formulas on small instances.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import combinations
import math
from typing import Iterable, Sequence


@dataclass(frozen=True)
class BrauerDescriptors:
    n_tokens: int
    n_vertices: int
    n_polygons: int
    CB: int
    nu: float
    HB: float
    H_norm: float
    dim_Lambda: int
    dim_Z: int
    connected_components: int
    graph_edges: int
    quiver_vertices: int
    quiver_arrows: int

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def _validate_radius(radius: int) -> None:
    if not isinstance(radius, int) or radius < 0:
        raise ValueError("radius must be a non-negative integer")


def _entropy(weights: Iterable[int]) -> tuple[float, float]:
    weights = list(weights)
    if not weights or any(w <= 0 for w in weights):
        raise ValueError("entropy weights must form a non-empty positive sequence")
    nu = float(sum(weights))
    h = -sum((w / nu) * math.log(w / nu) for w in weights)
    return float(h), nu


def _components(nodes: Iterable[object], edges: Iterable[tuple[object, object]]) -> int:
    nodes = list(nodes)
    if not nodes:
        return 0
    adjacency = {u: set() for u in nodes}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    seen: set[object] = set()
    count = 0
    for start in nodes:
        if start in seen:
            continue
        count += 1
        stack = [start]
        seen.add(start)
        while stack:
            u = stack.pop()
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
    return count


def occurrence_windows(n_tokens: int, radius: int) -> list[tuple[int, ...]]:
    """Materialize the radius-r windows on positions 0,...,N-1."""
    _validate_radius(radius)
    if n_tokens < 1:
        raise ValueError("n_tokens must be at least 1")
    return [
        tuple(range(max(0, i - radius), min(n_tokens, i + radius + 1)))
        for i in range(n_tokens)
    ]


def occurrence_valencies(n_tokens: int, radius: int) -> list[int]:
    """Return the occurrence valency profile from Eq. (7) of the article."""
    return [len(w) for w in occurrence_windows(n_tokens, radius)]


def local_multiplicities(valencies: Sequence[int]) -> list[int]:
    """Article convention: multiplicity two exactly at valency one."""
    return [2 if v == 1 else 1 for v in valencies]


def occurrence_reference_objects(n_tokens: int, radius: int) -> dict[str, object]:
    """Explicitly construct windows, graph/incidence edges, and quiver arrows."""
    windows = occurrence_windows(n_tokens, radius)
    graph: set[tuple[int, int]] = set()
    for window in windows:
        for a, b in combinations(window, 2):
            graph.add((min(a, b), max(a, b)))

    incident_windows: list[list[int]] = [[] for _ in range(n_tokens)]
    incidence_edges: list[tuple[object, object]] = []
    for p, window in enumerate(windows):
        for i in window:
            incident_windows[i].append(p)
            incidence_edges.append((("t", i), ("P", p)))

    quiver_arrows: list[tuple[int, int, int]] = []
    for i, polygons in enumerate(incident_windows):
        for k, src in enumerate(polygons):
            quiver_arrows.append((i, src, polygons[(k + 1) % len(polygons)]))

    incidence_nodes = [("t", i) for i in range(n_tokens)] + [
        ("P", p) for p in range(len(windows))
    ]
    return {
        "windows": windows,
        "graph_edges": graph,
        "incident_windows": incident_windows,
        "incidence_edges": incidence_edges,
        "connected_components": _components(incidence_nodes, incidence_edges),
        "quiver_arrows": quiver_arrows,
    }


def occurrence_descriptors(n_tokens: int, radius: int) -> BrauerDescriptors:
    """Compute the occurrence-indexed descriptor vector used in the article."""
    _validate_radius(radius)
    if n_tokens < 1:
        raise ValueError("n_tokens must be at least 1")

    valencies = occurrence_valencies(n_tokens, radius)
    multiplicities = local_multiplicities(valencies)
    weights = [v * mu for v, mu in zip(valencies, multiplicities)]
    entropy, nu = _entropy(weights)
    h_norm = entropy / math.log(n_tokens) if n_tokens > 1 else math.nan
    cb = int(sum(valencies))
    dim_lambda = int(
        2 * n_tokens
        + sum(v * (v * mu - 1) for v, mu in zip(valencies, multiplicities))
    )
    connected_components = n_tokens if radius == 0 else 1
    dim_z = int(connected_components + sum(multiplicities))
    max_distance = min(n_tokens - 1, 2 * radius)
    graph_edges = int(sum(n_tokens - d for d in range(1, max_distance + 1)))

    return BrauerDescriptors(
        n_tokens=n_tokens,
        n_vertices=n_tokens,
        n_polygons=n_tokens,
        CB=cb,
        nu=nu,
        HB=entropy,
        H_norm=h_norm,
        dim_Lambda=dim_lambda,
        dim_Z=dim_z,
        connected_components=connected_components,
        graph_edges=graph_edges,
        quiver_vertices=n_tokens,
        quiver_arrows=cb,
    )


def occurrence_closed_cost(n_tokens: int, radius: int) -> int:
    """Closed cost C_r=(2r+1)N-r(r+1), valid when N>=2r+1 and r>=1."""
    if radius < 1 or n_tokens < 2 * radius + 1:
        raise ValueError("closed cost requires r>=1 and N>=2r+1")
    return (2 * radius + 1) * n_tokens - radius * (radius + 1)


def entropy_asymptotic_coefficient(radius: int) -> float:
    """Return c_r from Eq. (18), valid for each fixed integer r>=1."""
    if radius < 1:
        raise ValueError("radius must be at least 1")
    r = radius
    a = 2 * r + 1
    boundary = sum(k * math.log(k) for k in range(r + 1, 2 * r + 1))
    return (
        r * (3 * r + 1) * math.log(a)
        - r * (r + 1)
        - 2 * boundary
    ) / a


def occurrence_entropy_closed(n_tokens: int, radius: int) -> float:
    """Exact H_B for r>=1 and N>=2r+1, as used in Proposition 8."""
    if radius < 1 or n_tokens < 2 * radius + 1:
        raise ValueError("closed entropy requires r>=1 and N>=2r+1")
    r = radius
    a = 2 * r + 1
    c = occurrence_closed_cost(n_tokens, radius)
    boundary = 2 * sum(k * math.log(k) for k in range(r + 1, 2 * r + 1))
    interior = (n_tokens - 2 * r) * a * math.log(a)
    return math.log(c) - (boundary + interior) / c


def verify_occurrence_closed_forms(max_n: int = 12, max_radius: int = 3) -> int:
    """Cross-check formula descriptors against explicit objects."""
    cases = 0
    for n_tokens in range(1, max_n + 1):
        for radius in range(max_radius + 1):
            explicit = occurrence_reference_objects(n_tokens, radius)
            formula = occurrence_descriptors(n_tokens, radius)
            vals = [len(x) for x in explicit["incident_windows"]]
            mus = local_multiplicities(vals)
            assert formula.CB == sum(vals)
            assert formula.graph_edges == len(explicit["graph_edges"])
            assert formula.connected_components == explicit["connected_components"]
            assert formula.quiver_arrows == len(explicit["quiver_arrows"])
            assert formula.dim_Lambda == 2 * n_tokens + sum(
                v * (v * mu - 1) for v, mu in zip(vals, mus)
            )
            assert formula.dim_Z == explicit["connected_components"] + sum(mus)
            cases += 1
    return cases


def type_collapsed_reference_objects(tokens: Sequence[str], radius: int) -> dict[str, object]:
    """Explicit token-type-collapsed configuration with multiset windows."""
    _validate_radius(radius)
    if not tokens:
        raise ValueError("tokens must be non-empty")
    n_tokens = len(tokens)
    windows_pos = occurrence_windows(n_tokens, radius)
    token_types = list(dict.fromkeys(tokens))
    windows_types = [tuple(tokens[i] for i in w) for w in windows_pos]

    incidence_copies: dict[str, list[tuple[int, int]]] = {u: [] for u in token_types}
    incidence_edges: set[tuple[object, object]] = set()
    for p, window in enumerate(windows_pos):
        for i in window:
            u = tokens[i]
            incidence_copies[u].append((i, p))
            incidence_edges.add((("t", u), ("P", p)))

    graph: set[tuple[str, str]] = set()
    for window in windows_types:
        distinct = list(dict.fromkeys(window))
        for a, b in combinations(distinct, 2):
            graph.add(tuple(sorted((a, b))))

    quiver_arrows: list[tuple[str, int, int]] = []
    for u in token_types:
        copies = sorted(incidence_copies[u], key=lambda z: (z[0], z[1]))
        cycle = [p for _, p in copies]
        for k, src in enumerate(cycle):
            quiver_arrows.append((u, src, cycle[(k + 1) % len(cycle)]))

    incidence_nodes = [("t", u) for u in token_types] + [
        ("P", p) for p in range(n_tokens)
    ]
    return {
        "token_types": token_types,
        "windows_positions": windows_pos,
        "windows_types": windows_types,
        "incidence_copies": incidence_copies,
        "incidence_edges": incidence_edges,
        "connected_components": _components(incidence_nodes, incidence_edges),
        "graph_edges": graph,
        "quiver_arrows": quiver_arrows,
    }


def type_collapsed_descriptors(tokens: Sequence[str], radius: int) -> BrauerDescriptors:
    """Compute the repetition-sensitive type-collapsed descriptors."""
    explicit = type_collapsed_reference_objects(tokens, radius)
    n_tokens = len(tokens)
    token_types = list(explicit["token_types"])
    copies = explicit["incidence_copies"]
    valencies = [len(copies[u]) for u in token_types]
    multiplicities = local_multiplicities(valencies)
    weights = [v * mu for v, mu in zip(valencies, multiplicities)]
    entropy, nu = _entropy(weights)
    n_vertices = len(token_types)
    h_norm = entropy / math.log(n_vertices) if n_vertices > 1 else math.nan
    cb = int(sum(valencies))
    dim_lambda = int(
        2 * n_tokens
        + sum(v * (v * mu - 1) for v, mu in zip(valencies, multiplicities))
    )
    dim_z = int(
        explicit["connected_components"] + n_tokens - n_vertices + sum(multiplicities)
    )
    return BrauerDescriptors(
        n_tokens=n_tokens,
        n_vertices=n_vertices,
        n_polygons=n_tokens,
        CB=cb,
        nu=nu,
        HB=entropy,
        H_norm=h_norm,
        dim_Lambda=dim_lambda,
        dim_Z=dim_z,
        connected_components=int(explicit["connected_components"]),
        graph_edges=len(explicit["graph_edges"]),
        quiver_vertices=n_tokens,
        quiver_arrows=len(explicit["quiver_arrows"]),
    )


def verify_type_refinement_identity(tokens: Sequence[str], radius: int) -> None:
    """Verify Proposition 9 for one sequence and r>=1."""
    if len(tokens) < 2 or radius < 1:
        raise ValueError("Proposition 9 assumes len(tokens)>=2 and radius>=1")
    occ = occurrence_descriptors(len(tokens), radius)
    typ = type_collapsed_descriptors(tokens, radius)
    repeated = len(set(tokens)) < len(tokens)
    assert typ.CB == occ.CB
    assert math.isclose(typ.nu, occ.nu, abs_tol=1e-12)
    assert typ.HB <= occ.HB + 1e-12
    assert typ.dim_Lambda >= occ.dim_Lambda
    assert typ.dim_Z == occ.dim_Z
    assert typ.quiver_arrows == occ.quiver_arrows
    if repeated:
        assert typ.HB < occ.HB - 1e-12
        assert typ.dim_Lambda > occ.dim_Lambda
    else:
        assert math.isclose(typ.HB, occ.HB, abs_tol=1e-12)
        assert typ.dim_Lambda == occ.dim_Lambda
