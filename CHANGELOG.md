# Changelog

## 1.9.0

- `move_symbol` nazywa brakującą operację placementu: przesuwa symbol przed
  routingiem i odbudowuje wyłącznie przewody dochodzące do jego pinów.
- Operacja zamyka dług spacingu, clearance przy złączach, skrzyżowań i siatki,
  ale obowiązkowo zachowuje netlistę i nie może pogorszyć żadnej reguły stylu.
- To bezpośrednia konsekwencja pomiaru `reroute_wire` 38 → 41: gdy końce nie
  dostają nowego korytarza, routing nie naprawia błędnego placementu.

## 1.8.0

- `RULE_SCH_NET_PRESENTATION.require_all_anchors_for` pozwala wskazać sieci,
  których wszystkie kotwice muszą należeć do jednego widocznego komponentu
  przewodów. Powtórzone globalne etykiety nadal zachowują netlistę, ale nie
  zaliczają jawnego wymagania czytelnego połączenia punkt-punkt.

## 1.7.1

- Wskazówka do `collapse_redundant_labels`: etykieta trzymająca wolny koniec
  przewodu jest terminalem, nie powtórzeniem, i nie wolno jej usunąć. Kryterium
  bierzemy od `RULE_SCH_DANGLING_WIRE`, zamiast definiować je drugi raz.
- Zapisane wprost, bo pomiar na panel9 pokazał, że identyczna netlista **nie
  jest** dowodem poprawności tej operacji: usunięcie dwóch terminali przy
  enkoderze zostawiło netlistę bez zmian i dwa zwisające przewody. Kandydat musi
  przejść porównanie netlisty **i** regresję stylu schematu.
- Bez zmian w słowniku reguł.

## 1.7.0

- `RULE_SCH_DANGLING_WIRE` wykrywa puste ogonki i gałęzie przewodów, które nie
  kończą się na pinie, etykiecie ani dalszym przebiegu. Takie linie pozostały
  na panel9 po przeniesieniu czterech sygnałów z GP9–GP12 na boczne GPIO.
- Reguła jest blokująca: pusta kreska udaje połączenie, choć nie ma terminala.
  `reroute_wire` może ją usunąć tylko z obowiązkowym `connectivity_preserved`.

## 1.6.0

- `RULE_SCH_CONNECTOR_ESCAPE_CLEARANCE` rozdziela margines czytelności przy
  złączach od elektrycznej `RULE_PIN_WIRE_GAP`. Krótki odcinek kończący się na
  własnym pinie pozostaje dozwolony, ale nieincydentny pień nie może przeciskać
  się pomiędzy punktami gęstego złącza.
- Profil domyślny wymaga 2,54 mm, czyli jednego kroku siatki, i wybiera złącza
  przez konfigurowalny `connector_pattern`. Granica progu jest dozwolona.
- `reroute_wire` może zamknąć nową regułę wyłącznie przy zachowanej netliście i
  bez regresji stylu; samo zwiększenie globalnego clearance nie jest dowodem.

## 1.5.0

- `collapse_redundant_labels` zostawia po jednej etykiecie nazwy na fizyczny
  komponent przewodów. Nie usuwa powtórzeń globalnie i odmawia działania, gdy
  widoczny komponent zawiera różne nazwy.
- Odnoga dochodząca do środka pnia jest wspólną topologią dla oka, ale sama
  kropka `junction` nie wystarcza do zachowania netlisty KiCada. Przed usunięciem
  etykiety operacja rozcina pień, aby odcinki miały wspólne końce; identyczna
  netlista pozostaje obowiązkowym dowodem, nie założeniem.
- Manifest DSL deklaruje tę samą wersję co źródło kanoniczne i profil.

## 1.4.0

- `RULE_SCH_SHARED_RAIL_PRESENTATION` mierzy skupiska terminali tej samej szyny,
  które są pokazane wyłącznie powtórzonymi etykietami globalnymi. W regularnej
  macierzy elementów wspólny pień z krótkimi odnogami pokazuje topologię lepiej
  niż kilkanaście napisów `GND`.
- `draw_shared_rail` zastępuje etykiety w jednym skupisku wspólną szyną bez
  zmiany łączności. Operacja obowiązkowo przechodzi `connectivity_preserved` i
  bramkę braku regresji czytelności.
- Reguła nie narzuca jednego symbolu zasilania dla całego arkusza. Odległe,
  niezależne bloki mogą używać osobnych symboli; wadą jest tekstowa prezentacja
  gęstego, funkcjonalnie wspólnego skupiska.

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
