# 01. Mindset testowania AI

## Demo to nie produkcja

Demo pokazuje potencjał. Produkcja sprawdza, czy systemowi można zaufać.

W przypadku aplikacji AI samo „odpowiedział dobrze” nie wystarcza, bo system może:

- odpowiedzieć poprawnie na jednym przykładzie, ale źle na innym,
- wygenerować przekonującą odpowiedź bez źródeł,
- użyć złego narzędzia,
- wykonać akcję bez wystarczających uprawnień,
- nie zostawić śladu działania,
- zachować się inaczej po zmianie promptu, modelu albo bazy wiedzy.

## Klasyczne testowanie vs testowanie AI

W klasycznym programowaniu często mamy jasny expected result:

```text
input: 2 + 2
expected output: 4
```

W systemach AI wynik bywa mniej deterministyczny. Dlatego oprócz samego outputu trzeba oceniać także:

- zgodność odpowiedzi ze źródłami,
- kompletność odpowiedzi,
- bezpieczeństwo odpowiedzi,
- sposób użycia narzędzi,
- zachowanie przy niepełnych danych,
- zachowanie przy błędach,
- zachowanie przy próbach manipulacji.

## Trzy poziomy testowania

### 1. Output

Czy odpowiedź końcowa jest poprawna, użyteczna i zgodna z wymaganiami?

Przykład:

- Czy odpowiedź odpowiada na pytanie użytkownika?
- Czy nie zawiera informacji spoza źródeł?
- Czy nie udaje pewności tam, gdzie dane są niepełne?

### 2. Process / trace

Czy wiemy, jak system doszedł do odpowiedzi?

Przykład:

- Jakie dokumenty zostały pobrane?
- Jakie narzędzia zostały użyte?
- Jakie parametry zostały przekazane do narzędzia?
- Czy pojawiły się błędy?
- Czy system wykonał retry?
- Czy nastąpił handoff do człowieka?

### 3. Safety / control

Czy system działa w granicach, które mu wyznaczyliśmy?

Przykład:

- Czy agent nie wykonuje akcji bez potwierdzenia?
- Czy nie próbuje obejść uprawnień?
- Czy nie ujawnia danych spoza zakresu?
- Czy ignoruje złośliwe instrukcje użytkownika?
- Czy zatrzymuje się przy decyzjach wysokiego ryzyka?

## Najczęstszy błąd początkujących

Najczęstszy błąd to testowanie tylko jednego idealnego scenariusza.

```text
Pytanie: Co to jest RAG?
Odpowiedź: Retrieval-Augmented Generation...
Wniosek: Działa.
```

To za mało.

Lepsze pytania testowe:

- Co jeśli dokumenty są niepełne?
- Co jeśli dokumenty sobie przeczą?
- Co jeśli odpowiedzi nie ma w źródłach?
- Co jeśli użytkownik próbuje wymusić złą akcję?
- Co jeśli narzędzie zwróci błąd?
- Co jeśli model brzmi pewnie, ale nie ma podstaw?

## Zasada praktyczna

Nie testuj tylko, czy AI potrafi pomóc.

Testuj także, czy AI potrafi:

- odmówić,
- dopytać,
- zatrzymać się,
- wskazać brak danych,
- pokazać źródła,
- obsłużyć błąd,
- nie wykonać akcji bez zgody.

## Prosta formuła dobrego testu AI

Dobry test powinien opisywać:

1. Cel testu.
2. Wejście użytkownika.
3. Dostępne dane lub narzędzia.
4. Oczekiwane zachowanie.
5. Zachowanie nieakceptowalne.
6. Sposób oceny wyniku.

Przykład:

```text
Cel: sprawdzić, czy RAG nie halucynuje przy braku danych.

Input:
„Jaki jest termin egzaminu z przedmiotu X?”

Dane:
W bazie wiedzy nie ma informacji o terminie egzaminu.

Oczekiwane zachowanie:
System mówi, że nie ma tej informacji w dostępnych źródłach.

Nieakceptowalne zachowanie:
System wymyśla datę albo odpowiada z dużą pewnością bez podstaw.
```

## Final takeaway

W AI engineeringu pytanie nie brzmi tylko:

> Czy system odpowiedział?

Pytanie brzmi:

> Czy odpowiedział na podstawie właściwych danych, w granicach swoich uprawnień, w sposób możliwy do sprawdzenia i bezpieczny dla użytkownika?
