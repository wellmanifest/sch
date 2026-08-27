#!/usr/bin/env python3
"""Walidacja pakietu wellmanifest/sch.

Sprawdzamy cztery rzeczy, bo tylko razem znaczą, że standard jest jeden:
schemat i manifest wymieniają ten sam zamknięty słownik reguł, przykładowe
profile są zgodne ze schematem, przykład negatywny zostaje odrzucony, a manifest
DSL zgadza się z plikami i z `wellmanifest.dsl/manifest/v1`.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "sch-style.schema.v1.json"
MANIFEST = ROOT / "dsl-manifest.json"
STANDARD = ROOT / "sch-standard.json"
DEFAULT = ROOT / "examples" / "default.json"
ADOPTER_DEFAULT = "app/profiles/wellmanifest-sch.v1.json"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _fail(message: str) -> None:
    print(f"✗ {message}", file=sys.stderr)
    raise SystemExit(1)


def refresh_digests() -> int:
    manifest = _load(MANIFEST)
    for artifact in manifest["artifacts"]:
        artifact["digest"] = "sha256:" + hashlib.sha256((ROOT / artifact["path"]).read_bytes()).hexdigest()
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✔ odświeżono digesty {len(manifest['artifacts'])} artefaktów")
    return 0


def _check_dsl_manifest() -> None:
    manifest = _load(MANIFEST)
    for artifact in manifest["artifacts"]:
        path = ROOT / artifact["path"]
        if not path.is_file():
            _fail(f"manifest DSL wskazuje nieistniejący artefakt {artifact['path']}")
        actual = "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != artifact["digest"]:
            _fail(f"digest {artifact['path']} nieaktualny — uruchom ./project.sh digests")
    print(f"✔ digesty {len(manifest['artifacts'])} artefaktów zgodne z plikami")

    schema_path = Path.home() / "github" / "wellmanifest" / "dsl" / "schemas" / "dsl-manifest.schema.json"
    if not schema_path.is_file():
        print("… wellmanifest/dsl niedostępny lokalnie — pominięto walidację manifestu DSL")
        return
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        print("… brak jsonschema — pominięto walidację manifestu DSL")
        return
    errors = list(Draft202012Validator(_load(schema_path)).iter_errors(manifest))
    if errors:
        where = "/".join(str(part) for part in errors[0].path) or "(root)"
        _fail(f"manifest DSL {where}: {errors[0].message}")
    print("✔ dsl-manifest.json zgodny z wellmanifest.dsl/manifest/v1")


def main() -> int:
    if "--refresh-digests" in sys.argv:
        return refresh_digests()

    schema = _load(SCHEMA)
    standard = _load(STANDARD)
    schema_rules = set(schema["properties"]["rules"]["properties"])
    standard_rules = {item["id"] for item in standard["rules"]}
    if schema_rules != standard_rules:
        _fail(f"słownik reguł rozjechany: {sorted(schema_rules ^ standard_rules)}")
    print(f"✔ zamknięty słownik reguł zgodny ({len(schema_rules)} reguł)")

    if schema["properties"]["rules"].get("additionalProperties") is not False:
        _fail("schemat musi zamykać listę reguł (additionalProperties: false)")
    print("✔ nieznana reguła jest błędem profilu, nie regułą nieaktywną")

    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        validator = None
        print("… jsonschema niedostępny — sprawdzam profile strukturalnie")
    else:
        validator = Draft202012Validator(schema)

    severities = set(standard["severities"])
    for path in sorted((ROOT / "examples").glob("*.json")):
        if path.name.startswith("invalid"):
            continue
        document = _load(path)
        if validator is not None:
            errors = sorted(validator.iter_errors(document), key=lambda item: list(item.path))
            if errors:
                _fail(f"{path.name}: {errors[0].message}")
        for name, rule in (document.get("rules") or {}).items():
            if name not in schema_rules:
                _fail(f"{path.name}: nieznana reguła {name}")
            if "severity" in rule and rule["severity"] not in severities:
                _fail(f"{path.name}: severity {rule['severity']!r} spoza słownika")
        print(f"✔ {path.name} zgodny z {schema['title']}")

    invalid = ROOT / "examples" / "invalid-unknown-rule.json"
    if invalid.is_file():
        document = _load(invalid)
        unknown = [name for name in document.get("rules") or {} if name not in schema_rules]
        if not unknown:
            _fail("examples/invalid-unknown-rule.json przestał być przykładem negatywnym")
        if validator is not None and not list(validator.iter_errors(document)):
            _fail("examples/invalid-unknown-rule.json przechodzi walidację, a nie powinien")
        print(f"✔ przykład negatywny odrzucony ({unknown[0]})")

    _check_dsl_manifest()

    directory = os.environ.get("ADOPTER_DIR")
    if directory:
        candidate = Path(directory) / ADOPTER_DEFAULT
        if candidate.is_file():
            if _load(candidate) != _load(DEFAULT):
                _fail(f"profil adoptera {candidate} różni się od examples/default.json")
            print("✔ adopter używa profilu domyślnego bez lokalnej mutacji")
        else:
            print(f"… adopter nie ma jeszcze {ADOPTER_DEFAULT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
