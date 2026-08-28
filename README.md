# wellmanifest/sch — Schematic Readability Contract Standard

Mierzalny kontrakt na to, że schemat **da się przeczytać**. Netlista może być
poprawna, a rysunek i tak nieczytelny: linie jedna na drugiej, pasma równoległych
przewodów zlewające się w jedną kreskę, kilkadziesiąt skrzyżowań. To są rzeczy
mierzalne, więc przestają być kwestią gustu.

## Granica wobec `wellmanifest/pcb`

Rozdział jest celowy i zapisany w `sch-standard.json`:

- **`wellmanifest/sch` ma czytelność rysunku** — ortogonalność, odstępy, nakładanie,
  skrzyżowania, siatka, rozmieszczenie etykiet.
- **`wellmanifest/pcb` ma prawdziwość netlisty i zgodność z płytką** —
  `RULE_PIN_WIRE_GAP`, `RULE_RAIL_LABEL_CANONICAL`, `RULE_SIGNAL_LABEL_NAMING`,
  `RULE_SCH_PCB_NET_PARITY`.

Powód: rysunek bywa nieczytelny przy poprawnej netliście i odwrotnie. Jedno mierzy
się geometrią, drugie połączeniami. Trzymanie tego w jednym słowniku zmuszałoby
adoptera do przyjęcia obu naraz.

## Słownik reguł

| Reguła | Domyślnie | Mierzy |
|---|---|---|
| `RULE_SCH_WIRE_ORTHOGONAL` | blocking | przewody inne niż poziome i pionowe |
| `RULE_SCH_WIRE_OVERLAP` | blocking | odcinki leżące współliniowo jeden na drugim |
| `RULE_SCH_WIRE_OVER_SYMBOL` | blocking | przewód przechodzący przez korpus symbolu |
| `RULE_SCH_WIRE_OVER_PIN` | blocking | przewód przechodzący przez pin obcej sieci |
| `RULE_SCH_WIRE_SPACING` | advisory | równoległe przewody bliżej niż krok siatki |
| `RULE_SCH_LABEL_SPACING` | advisory | nachodzące na siebie etykiety |
| `RULE_SCH_NET_PRESENTATION` | advisory | wielopunktowe sieci sygnałowe pokazane wyłącznie etykietami |
| `RULE_SCH_SHARED_RAIL_PRESENTATION` | advisory | skupiska wspólnej szyny pokazane powtórzonym tekstem zamiast widocznym pniem |
| `RULE_SCH_CROSSING_BUDGET` | advisory | skrzyżowania ponad budżet na sieć |
| `RULE_SCH_COMMON_GRID` | advisory | piny i końce przewodów na kilku różnych siatkach |

Nowa reguła prezentacji odróżnia poprawność elektryczną od czytelności: globalne
etykiety nadal tworzą jedną sieć w netliście, ale projekt może wymagać pokazania
przynajmniej fragmentu sieci sygnałowej przewodem. Szyny zasilania można wyłączyć
przez `exclude_pattern`, a próg ustawia `max_label_only_nets`.

`RULE_SCH_SHARED_RAIL_PRESENTATION` osobno obejmuje szyny wyłączone z powyższej
reguły. Dla regularnego skupiska, np. rzędu mikroswitchy, preferuje jeden wspólny
pień GND z krótkimi odnogami i jednym symbolem szyny. Nie ogranicza globalnej
liczby terminali ani nie każe scalać odległych bloków. Szczegóły:
[`docs/POWER-RAIL-PRESENTATION.md`](docs/POWER-RAIL-PRESENTATION.md).

Po narysowaniu wspólnego przebiegu `collapse_redundant_labels` może zostawić po
jednej etykiecie nazwy na fizyczny komponent. Najpierw rozcina pień w punktach T;
sama widoczna kropka nie jest dowodem łączności. Komponenty z różnymi nazwami są
pomijane, a identyczność netlisty jest obowiązkową bramką kandydata.

Cztery reguły blokujące opisują rzeczy **niejednoznaczne**: dwie linie jedna na
drugiej wyglądają jak jedna, przewód przez pin wygląda na połączony. Reguły
doradcze opisują rzeczy **męczące**: da się przeczytać, tylko trudniej.

## Skąd te progi

Z pomiaru, nie z wyobraźni. Referencyjny `panel9.kicad_sch` po dorysowaniu połączeń:

```
przewodów: 184        skrzyżowań: 80
nakładanie współliniowe: 20 par     równoległe bliżej niż 2,54 mm: 41 par
przewody przez korpus symbolu: 0    przez obcy pin: 0    skośne: 0
piny na jednej siatce 1,27 mm: 23 z 81
```

Reguły blokujące trafiają dokładnie w to, co ten rysunek psuje, a doradcze opisują
dług, który zostaje po automatycznym trasowaniu.

## Kształt profilu

```json
{
  "schema_id": "wellmanifest.sch/style/v1",
  "profile": "panel9",
  "rules": {
    "RULE_SCH_WIRE_SPACING": {"min_mm": 2.54},
    "RULE_SCH_NET_PRESENTATION": {"max_label_only_nets": 0},
    "RULE_SCH_SHARED_RAIL_PRESENTATION": {"min_anchors": 3},
    "RULE_SCH_CROSSING_BUDGET": {"severity": "advisory", "max_per_net": 8}
  }
}
```

Rozszerzenie lokalne zmienia pojedyncze pola i dziedziczy resztę. Reguła spoza
zamkniętego słownika kończy się błędem wczytania — nigdy regułą po cichu nieaktywną.

Kolejność wyszukiwania: `$WELLMANIFEST_SCH_PROFILE`,
`<artefakty>/.wellmanifest/sch.json`, profil domyślny adoptera.

## Bramka

Jak w `wellmanifest/pcb`: **regresja**, nie stan bezwzględny. Kandydat nie może
zwiększyć liczby naruszeń reguły blokującej; naruszenie obecne po obu stronach to
dług rysunku, nie powód blokady. Brak możliwości policzenia kontroli to
`SCH_STYLE_NOT_RUN` — blokada, nie zaliczenie.

Czytelność liczy się **przed** ERC i DRC, nigdy zamiast nich.

## Walidacja pakietu

```bash
./project.sh check      # słownik, schemat, przykłady, przykład negatywny, manifest DSL
./project.sh digests    # przelicz digesty po zmianie artefaktu
```

## Placement & Governance

- `HOME`: `wellmanifest`
- `SHAPE`: `domain_pack`
- `ADOPT`: `wellmanifest/sch`
