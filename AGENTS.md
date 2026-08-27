# AGENTS.md

This repository is the **HOME** pack for schematic readability (`wellmanifest/sch`).

HOME vs ADOPT: `HOME wellmanifest`, `shape domain_pack`. Viewers, generators and CI
runners **ADOPT** this pack. They must not keep a second readability SSOT as
constants in their own source.

The rule vocabulary is closed. A profile naming an unknown rule must fail loudly,
never degrade into a rule that silently does nothing.

Boundary: this pack owns how the drawing reads. It does **not** own netlist truth
or board parity — those belong to `wellmanifest/pcb`. A change that improves
readability must never change connectivity; adopters are expected to verify that
independently.

This pack is **propose-only**: it describes the profile, the rule vocabulary and
the regression gate. It does not edit schematics and does not replace ERC.

Prefer `$id` host `https://wellmanifest.com/schemas/...` (no release tags in `$id`).
