# 05. Metody ewaluacji systemów AI

Ewaluacja systemów AI to nie jednorazowe sprawdzenie odpowiedzi. To proces, który pozwala porównywać wersje systemu, wykrywać regresje i świadomie poprawiać jakość.

## 1. Golden dataset

Golden dataset to zestaw przykładów testowych, które uznajemy za reprezentatywne dla naszego systemu.

Może zawierać:

- pytania użytkowników,
- oczekiwane odpowiedzi,
- dokumenty źródłowe,
- oczekiwane narzędzia,
- oczekiwane zachowanie przy błędach,
- przykłady, w których system powinien powiedzieć „nie wiem”.

### Po co?

Żeby po zmianie promptu, modelu, retrievera albo toola sprawdzić, czy system nadal działa dobrze.

### Przykład

```text
Pytanie:
„Czy student może oddać projekt po terminie?”

Źródło:
Regulamin mówi, że oddanie po terminie wymaga zgody prowadzącego.

Oczekiwane zachowanie:
System odpowiada, że jest to możliwe tylko za zgodą prowadzącego i wskazuje źródło.

Nieakceptowalne:
System mówi „tak, zawsze” albo „nie, nigdy”.
```

## 2. Regression testing

Regression testing sprawdza, czy nowa wersja systemu nie zepsuła tego, co wcześniej działało.

W aplikacjach AI regresja może pojawić się po zmianie:

- modelu,
- promptu,
- temperatury,
- chunkingu,
- retrievera,
- narzędzia,
- opisu toola,
- kolejności kroków w agencie.

### Prosty workflow

1. Uruchom testy na wersji A.
2. Zmień prompt/model/tool.
3. Uruchom te same testy na wersji B.
4. Porównaj wyniki.
5. Sprawdź, czy poprawa w jednym miejscu nie pogorszyła innego.

## 3. Component-level evaluation

Nie oceniaj tylko całego systemu end-to-end. Oceniaj też komponenty osobno.

### W RAG-u

- retrieval,
- reranking,
- generation,
- cytowanie źródeł,
- odmowa odpowiedzi przy braku danych.

### W agencie

- planowanie,
- wybór narzędzia,
- parametry tool calla,
- obsługa błędów,
- decyzja o handoffie,
- guardrails,
- finalna odpowiedź.

## 4. Trace-based evaluation

W agentach ważna jest ścieżka działania.

Nie wystarczy wiedzieć, że agent zwrócił finalną odpowiedź. Trzeba wiedzieć:

- jakie kroki wykonał,
- jakie narzędzia wybrał,
- jakie parametry przekazał,
- jakie odpowiedzi dostał z narzędzi,
- czy wystąpiły błędy,
- czy pojawiły się retry,
- czy aktywował guardrail,
- czy poprosił człowieka o decyzję.

### Przykład oceny trace’a

```text
Zadanie:
„Sprawdź status zgłoszenia #123 i przygotuj krótkie podsumowanie.”

Poprawny trace:
1. Agent rozpoznaje ID zgłoszenia.
2. Agent używa narzędzia get_ticket_status.
3. Agent podaje poprawne ID.
4. Tool zwraca status.
5. Agent generuje podsumowanie na podstawie wyniku toola.

Niepoprawny trace:
1. Agent nie używa narzędzia.
2. Agent zgaduje status.
3. Agent generuje odpowiedź bez danych.
```

## 5. Groundedness / faithfulness

Ta metoda sprawdza, czy odpowiedź jest oparta na źródłach.

Pytanie:

> Czy każde ważne twierdzenie w odpowiedzi da się podeprzeć pobranym kontekstem?

### Przykład

Jeśli dokument mówi:

```text
Termin oddania projektu to 15 maja.
```

To odpowiedź:

```text
Projekt należy oddać do 15 maja.
```

jest grounded.

Ale odpowiedź:

```text
Projekt należy oddać do 15 maja, a spóźnienie oznacza automatyczne 0 punktów.
```

nie jest w pełni grounded, jeśli druga część nie występuje w źródle.

## 6. LLM-as-a-judge

LLM-as-a-judge oznacza użycie modelu jako oceniającego.

Można poprosić drugi model, żeby ocenił:

- czy odpowiedź jest zgodna ze źródłami,
- czy odpowiedź jest kompletna,
- czy odpowiedź jest bezpieczna,
- czy agent użył właściwego narzędzia,
- czy output spełnia kryteria.

### Uwaga

LLM-as-a-judge też może się mylić.

Dlatego warto:

- kalibrować go na przykładach ocenionych przez człowieka,
- porównywać oceny różnych modeli,
- stosować jasne kryteria,
- nie używać go jako jedynego mechanizmu w krytycznych decyzjach.

## 7. Red teaming

Red teaming polega na celowym szukaniu słabości systemu.

Testujemy:

- prompt injection,
- jailbreaki,
- próby uzyskania danych spoza zakresu,
- błędne lub złośliwe dane wejściowe,
- manipulację dokumentem w RAG-u,
- wymuszanie użycia zakazanego narzędzia,
- akcje bez potwierdzenia.

## 8. Online monitoring

Po wdrożeniu testy nie kończą się.

Warto monitorować:

- najczęstsze pytania,
- odpowiedzi bez źródeł,
- odmowy,
- błędy narzędzi,
- retry,
- latency,
- koszt,
- przypadki human handoff,
- zgłoszenia użytkowników,
- spadek jakości po zmianach.

## 9. Prosta tabela metod

| Metoda | Kiedy używać? | Co daje? |
|---|---|---|
| Golden dataset | Od początku projektu | Powtarzalny zestaw testów |
| Regression testing | Po każdej zmianie | Wykrywanie regresji |
| Component-level eval | Przy debugowaniu | Wskazuje, gdzie system się psuje |
| Trace-based eval | Przy agentach | Pokazuje drogę działania |
| Groundedness | Przy RAG-ach | Ogranicza halucynacje |
| LLM-as-a-judge | Przy ocenie jakości | Automatyzuje część oceny |
| Red teaming | Przed pokazaniem szerszej grupie | Szuka podatności |
| Online monitoring | Po wdrożeniu | Wykrywa problemy w realnym użyciu |

## Final takeaway

Ewaluacja AI to nie jeden test.

To pętla:

```text
zbuduj → przetestuj → sprawdź trace → popraw → porównaj → monitoruj
```
