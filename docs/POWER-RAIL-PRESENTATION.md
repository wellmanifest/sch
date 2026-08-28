# Prezentacja wspólnych szyn

Identyczne etykiety globalne tworzą jedną poprawną sieć, ale nie zawsze tworzą
czytelny rysunek. W macierzy elementów kilkanaście napisów `GND` opisuje to, co
jedna linia wspólnej szyny mogłaby pokazać bez czytania.

## Kiedy rysować wspólny pień

Wspólny pień jest preferowany, gdy co najmniej trzy terminale tej samej szyny:

* należą do jednego funkcjonalnego skupiska, np. rzędu przycisków,
* leżą na tyle blisko, że krótka ortogonalna szyna nie przecina obcych symboli,
* mają tę samą rolę elektryczną i nie wymagają osobnego wskazania domeny zasilania.

Wtedy jedna szyna, krótkie odnogi i jeden symbol GND/zasilania pokazują zarówno
nazwę, jak i topologię.

## Kiedy nie scalać

Odległe bloki, różne domeny zasilania, bariery izolacyjne i osobne arkusze mogą
używać powtarzanych symboli zasilania. Reguła nie ogranicza liczby terminali
w całym projekcie i nie każe prowadzić długiego przewodu przez cały arkusz.

Globalna liczba etykiet jest złą miarą: sieć z dwudziestoma terminalami nadal ma
dwadzieścia połączeń. `RULE_SCH_SHARED_RAIL_PRESENTATION` mierzy wyłącznie grupy,
które są blisko siebie i nie mają żadnego widocznego wspólnego pnia.

## Bezpieczna naprawa

`draw_shared_rail` najpierw rysuje pień i odnogi do istniejących kotwic.
`collapse_redundant_labels` wykonuje drugi, osobny krok: rozcina pień w punktach
T, aby odnogi i pień miały wspólne końce, a następnie zostawia jedną etykietę
nazwy na każdy fizyczny komponent. Sama kropka `junction` jest oznaczeniem dla
czytelnika i nie może być jedynym dowodem elektrycznego połączenia.

Operacja nie scala na podstawie samego nakładania, nie łączy zwykłych skrzyżowań
i pomija komponent zawierający różne nazwy. Kandydat musi wykazać identyczną
netlistę przed i po zmianie; w przeciwnym razie poprawa prezentacji jest zmianą
układu i zostaje odrzucona.

## Etykieta bywa terminalem, nie powtórzeniem

Nie każda etykieta w komponencie jest nadmiarowa. Jeżeli koniec przewodu nie ma
ani pinu, ani drugiej gałęzi, to **etykieta jest jedynym, co go trzyma**. Po jej
usunięciu linia zwisa i `RULE_SCH_DANGLING_WIRE` odrzuca kandydata.

Dlatego grupa kotwic dzieli się na dwie role:

* **terminal** — punkt, który zwisałby, gdyby etykiet nie było wcale. Zostaje
  zawsze, niezależnie od tego, ile ich jest w komponencie;
* **odczep** — punkt trzymany przez pin albo przez dalszy przebieg. Z odczepów
  zostaje jeden, i to tylko wtedy, gdy w komponencie nie ma żadnego terminala.

Kryterium warto brać wprost od reguły zwisania, a nie definiować drugi raz.
Adopter, który zapyta „co zwisałoby bez etykiet", dostanie tę samą odpowiedź,
którą poda mu bramka — i nie rozjedzie się z nią przy następnej zmianie progu.

**Identyczna netlista nie jest dowodem poprawności tej operacji.** Usunięcie
terminala potrafi zostawić netlistę bez zmian, bo KiCad wiąże sieć nazwą, a nie
rysunkiem. Zmienia się to, co rysunek mówi czytelnikowi. Kandydat musi więc
przejść **obie** kontrole: porównanie netlisty i regresję stylu schematu.
Pierwsza pilnuje układu, druga pilnuje rysunku, i żadna nie zastępuje drugiej.
