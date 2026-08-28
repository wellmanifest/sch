# Changelog

## 1.3.1

- `reroute_wire` niesie teraz zmierzone ostrzeżenie: przy gęstym rozmieszczeniu
  symboli innego przebiegu przy zachowanych końcach zwykle **nie ma**. Na
  referencyjnym panel9 trasowanie pojedynczych przewodów routerem schodkowym
  pogorszyło wynik (38 → 41 naruszeń, blokujących 8 → 9) i zmieniło netlistę,
  mimo nietykalnych końców.
- Wniosek jest zgodny z tym, co mówi sama `RULE_SCH_CROSSING_BUDGET`: gdy budżet
  skrzyżowań jest przekroczony, źródłem bałaganu jest rozmieszczenie symboli,
  a nie trasy — i wtedy `reroute_wire` nie jest właściwym narzędziem. Opis
  operacji ma o tym mówić, zanim ktoś napisze drugie takie narzędzie.

## 1.3.0

- `RULE_SCH_NET_PRESENTATION` mierzy wielopunktowe sieci sygnałowe pokazane
  wyłącznie powtórzonymi etykietami globalnymi. Netlista może być poprawna,
  choć na rysunku nie widać przebiegu połączenia — standard nazywa teraz ten
  dług zamiast mylić go z brakiem łączności.
- `draw_net_wires` jawnie zamyka tę regułę. Profil określa minimalną liczbę
  kotwic, dopuszczalny budżet sieci label-only i wzorzec wyłączeń dla szyn.
- Ujednolicono wersję pakietu w `VERSION`, źródle kanonicznym, profilu i
  manifeście DSL; mapowanie do `wellmanifest/pcb` wskazuje 1.9.0.

## 1.2.0

- `drop_redundant_wire`: odcinek leżący **w całości** na innym odcinku tej samej
  sieci nie niesie żadnego połączenia, którego tamten już nie niesie — a dwie
  linie na sobie wyglądają jak jedna.
- Ma własną nazwę zamiast być przypadkiem `reroute_wire`, bo usunięcie
  i przetrasowanie różnią się tym, co trzeba udowodnić. Przetrasowanie zachowuje
  końce i zmienia przebieg; usunięcie musi wykazać, że przebiegu w ogóle nie było
  potrzeba. Obie drogi kończą się tym samym warunkiem `connectivity_preserved`,
  ale z innego powodu.
- Na referencyjnym panel9 zamyka jedyne blokujące naruszenie schematu: pionowy
  zjazd sieci `ENC_A` skręcał w lewo i biegł 0,8 mm po istniejącym przewodzie.

## 1.1.0

- **Zamknięty słownik operacji**: `draw_net_wires`, `snap_to_common_grid`,
  `reroute_wire`, `move_label`. Reguły mówiły, co czyni rysunek nieczytelnym,
  i nic nie mówiło, co wolno z tym zrobić.
- Każda operacja tego standardu musi żądać `connectivity_preserved` — i wymusza to
  walidator. Poprawa czytelności, która zmienia netlistę, nie jest poprawą
  czytelności, tylko przerysowaniem układu pod pozorem porządków.
- `reroute_wire` istnieje, bo scalanie nakładających się przewodów jest **złą**
  naprawą i zostało to zmierzone na panel9: współliniowe nakładanie w KiCadzie nie
  łączy, więc scalenie zwarło GP5 z GP7. Jedyną poprawną naprawą jest inny przebieg
  przy zachowanych końcach.
- `schemas/sch-operations.schema.v1.json`, `examples/operations.json` i przykład
  negatywny.

## 1.0.0

- Pierwsza wersja profilu `wellmanifest.sch/style/v1` z zamkniętym słownikiem
  ośmiu reguł czytelności rysunku dla `.kicad_sch`.
- Jawna granica wobec `wellmanifest/pcb`: czytelność tutaj, prawdziwość netlisty tam.
- Bramka regresji `SCH_STYLE_REGRESSION` / `SCH_STYLE_NOT_RUN`.
- Manifest zgodny z `wellmanifest.dsl/manifest/v1` z digestami artefaktów.
- Progi wyprowadzone z pomiaru na `panel9.kicad_sch`, nie z wyobraźni.
