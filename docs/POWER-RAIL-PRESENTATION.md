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

`draw_shared_rail` najpierw rysuje pień i odnogi do istniejących kotwic, następnie
usuwa zastąpione etykiety z tej jednej grupy. Nie scala przewodów na podstawie
samego nakładania. Kandydat musi wykazać identyczną netlistę przed i po zmianie;
w przeciwnym razie poprawa prezentacji jest zmianą układu i zostaje odrzucona.
