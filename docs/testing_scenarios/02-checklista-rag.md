# 02. Checklista testowania RAG

RAG, czyli Retrieval-Augmented Generation, łączy model językowy z zewnętrzną bazą wiedzy. Model nie powinien odpowiadać tylko „z pamięci”, ale korzystać z pobranych dokumentów, fragmentów lub danych.

Dlatego RAG testujemy na dwóch poziomach:

1. **Retrieval** — czy system znalazł właściwy kontekst?
2. **Generation** — czy odpowiedź faktycznie wynika z tego kontekstu?

## 1. Testowanie retrievalu

Retrieval odpowiada za wyszukanie właściwych fragmentów wiedzy.

### Pytania kontrolne

- Czy system znajduje właściwe dokumenty?
- Czy najważniejsze fragmenty są wysoko w wynikach?
- Czy system nie zwraca przypadkowych lub słabo powiązanych fragmentów?
- Czy chunking nie rozcina ważnego kontekstu?
- Czy system radzi sobie z synonimami i innym sposobem zadania pytania?
- Czy system odróżnia aktualne dokumenty od starych?
- Czy system umie znaleźć informacje rozproszone w kilku miejscach?

### Przykładowe testy

- Pytanie zadane dokładnie tak, jak w dokumencie.
- Pytanie zadane innymi słowami.
- Pytanie wymagające połączenia dwóch fragmentów.
- Pytanie o informację ze starego dokumentu.
- Pytanie o informację, której nie ma w bazie wiedzy.
- Pytanie z literówką lub niepełną nazwą.

## 2. Testowanie generowania odpowiedzi

Generation odpowiada za stworzenie odpowiedzi na podstawie kontekstu.

### Pytania kontrolne

- Czy odpowiedź wynika ze źródeł?
- Czy system nie dodaje informacji spoza kontekstu?
- Czy odpowiedź wskazuje źródła lub cytaty?
- Czy system potrafi powiedzieć „nie wiem”?
- Czy odpowiedź jest zgodna z ograniczeniami domeny?
- Czy system rozróżnia fakty od przypuszczeń?
- Czy odpowiedź nie ukrywa sprzeczności między źródłami?

## 3. Minimalna checklista RAG

Przed pokazaniem RAG-a innym osobom sprawdź:

- [ ] Czy masz zestaw pytań testowych?
- [ ] Czy testy obejmują pytania łatwe i trudne?
- [ ] Czy testujesz pytania bez odpowiedzi w źródłach?
- [ ] Czy testujesz sprzeczne źródła?
- [ ] Czy testujesz niepełne dokumenty?
- [ ] Czy testujesz stare lub nieaktualne dokumenty?
- [ ] Czy sprawdzasz, jakie fragmenty zostały pobrane?
- [ ] Czy odpowiedź jest zgodna z pobranym kontekstem?
- [ ] Czy system wskazuje źródła?
- [ ] Czy system umie powiedzieć „nie mam tej informacji”?
- [ ] Czy po zmianie promptu lub retrievera możesz uruchomić te same testy ponownie?

## 4. Scenariusze, które warto mieć w datasetcie

| Typ scenariusza | Po co go testować? |
|---|---|
| Happy path | Czy system działa na prostym, typowym pytaniu |
| Missing answer | Czy system nie halucynuje, gdy nie ma danych |
| Conflicting sources | Czy system pokazuje konflikt zamiast wybierać losowo |
| Outdated source | Czy system rozpoznaje ryzyko nieaktualnych danych |
| Partial context | Czy system nie dopowiada brakujących faktów |
| Irrelevant retrieval | Czy system nie odpowiada pewnie na słabym kontekście |
| Multi-hop question | Czy system umie połączyć kilka fragmentów |
| Domain boundary | Czy system nie odpowiada poza zakresem aplikacji |

## 5. Przykład testu RAG

```text
Nazwa testu:
Sprzeczne źródła w dokumentach

Dane:
Dokument A: „Zwrot produktu możliwy jest w ciągu 14 dni.”
Dokument B: „Zwrot produktu możliwy jest w ciągu 30 dni.”

Pytanie użytkownika:
„Ile dni mam na zwrot produktu?”

Oczekiwane zachowanie:
System powinien wskazać, że źródła są sprzeczne, albo zaznaczyć niepewność.

Nieakceptowalne zachowanie:
System wybiera jedną odpowiedź bez ostrzeżenia i podaje ją jako pewny fakt.
```

## 6. Przykładowe metryki RAG

| Metryka | Co mierzy? | Prosty sens |
|---|---|---|
| Faithfulness | Czy odpowiedź wynika z kontekstu | „Czy model nie zmyśla?” |
| Answer relevancy | Czy odpowiedź odpowiada na pytanie | „Czy odpowiedź jest na temat?” |
| Context precision | Czy właściwe fragmenty są wysoko w wynikach | „Czy retrieval dobrze rankinguje?” |
| Context recall | Czy znaleziono wystarczająco dużo potrzebnego kontekstu | „Czy nie pominięto ważnych źródeł?” |

## Final takeaway

Dobry RAG nie tylko odpowiada.

Dobry RAG pokazuje, na czym opiera odpowiedź, i potrafi przyznać, że nie ma wystarczających danych.
