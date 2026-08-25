# Changelog

## 1.1.0 - 2026-08-25

- separates the occurrence-indexed baseline from the repetition-sensitive type-collapsed refinement;
- adds explicit reference construction of windows, graphs, incidence data, and quiver arrows;
- implements and tests the asymptotic coefficient from Proposition 8;
- integrates Proposition 9 and the controlled Table 4 reproduction;
- adds special-token controls and manuscript regression checks for Tables 2–3;
- fixes normalized entropy for singleton sequences (`NaN` rather than zero);
- removes duplicate descriptor aliases and all `trust_remote_code=True` fallbacks;
- fixes corpus validation so an existing fixed file is checked against an independent deterministic regeneration;
- adds unit tests, randomized verification, pinned dependencies, CI, and repository metadata.
