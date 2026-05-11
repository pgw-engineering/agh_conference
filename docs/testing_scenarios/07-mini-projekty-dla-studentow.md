# 07. Mini-projekty dla studentów

Najlepiej uczyć się testowania AI przez małe, kontrolowane projekty.

Nie zaczynaj od wielkiego autonomicznego agenta. Zacznij od prostego systemu, który ma jasny cel i da się świadomie „psuć” testami.

## Poziom 1: RAG na notatkach z zajęć

### Cel

Zbudować prostego chatbota, który odpowiada na pytania na podstawie notatek, PDF-ów albo materiałów z zajęć.

### Czego się nauczysz?

- chunking,
- retrieval,
- źródła,
- groundedness,
- pytania bez odpowiedzi,
- sprzeczne informacje,
- podstawy evali RAG.

### Co testować?

- pytania z odpowiedzią w notatkach,
- pytania bez odpowiedzi,
- pytania ze sprzecznymi fragmentami,
- pytania zadane innymi słowami,
- pytania z literówkami,
- odpowiedzi bez wskazania źródła.

### Rozszerzenie

Dodaj prosty mechanizm cytowania źródeł.

## Poziom 2: Asystent do analizy Pull Requestów

### Cel

Zbudować asystenta, który analizuje opis PR-a i sugeruje, na co reviewer powinien zwrócić uwagę.

### Ważne

To nie ma zastąpić code review. To ma pomóc znaleźć potencjalne punkty uwagi.

### Czego się nauczysz?

- praca z kodem,
- ograniczenia modeli,
- hallucination risk,
- tworzenie kryteriów oceny,
- testowanie jakości odpowiedzi.

### Co testować?

- PR z małą zmianą,
- PR z brakującym testem,
- PR z potencjalnym problemem bezpieczeństwa,
- PR z refactorem,
- PR z niepełnym opisem,
- PR, gdzie asystent powinien powiedzieć „brakuje kontekstu”.

### Oczekiwane zachowanie

Asystent powinien sugerować obszary do sprawdzenia, ale nie udawać, że ma pełną pewność.

## Poziom 3: Agent z jednym narzędziem

### Cel

Zbudować prostego agenta, który ma dostęp do jednego narzędzia, np. `get_weather`, `get_ticket_status`, `search_notes`.

### Czego się nauczysz?

- tool calling,
- parametry narzędzi,
- błędy narzędzi,
- walidacja inputu,
- trace działania.

### Co testować?

- poprawne użycie narzędzia,
- brak wymaganego parametru,
- błędny parametr,
- timeout,
- odpowiedź narzędzia bez danych,
- sytuację, w której agent nie powinien użyć toola.

### Oczekiwane zachowanie

Agent powinien używać narzędzia tylko wtedy, gdy ma to sens, i nie powinien zgadywać wyniku.

## Poziom 4: Agent z human approval

### Cel

Zbudować agenta, który może przygotować akcję, ale nie może jej wykonać bez potwierdzenia człowieka.

Przykłady:

- przygotowanie maila,
- przygotowanie status update’u,
- przygotowanie listy plików do usunięcia,
- przygotowanie komentarza do PR-a.

### Czego się nauczysz?

- human-in-the-loop,
- akcje wysokiego ryzyka,
- approval flow,
- logowanie decyzji,
- ograniczanie autonomii.

### Co testować?

- czy agent zatrzymuje się przed akcją,
- czy pokazuje plan działania,
- czy człowiek może zatwierdzić lub odrzucić,
- czy agent nie wykonuje akcji po prompt injection,
- czy decyzja jest logowana.

## Poziom 5: Red teaming małego RAG-a

### Cel

Sprawdzić, czy RAG jest odporny na złośliwe lub podchwytliwe wejścia.

### Czego się nauczysz?

- prompt injection,
- data exfiltration risk,
- niezaufane dokumenty,
- separacja instrukcji systemowych od treści użytkownika,
- bezpieczeństwo RAG.

### Co testować?

- dokument zawierający instrukcję „zignoruj system prompt”,
- pytanie wymuszające odpowiedź bez źródeł,
- próba ujawnienia danych z dokumentów,
- próba wymuszenia odpowiedzi poza zakresem,
- próba ukrycia braku źródeł.

## Poziom 6: Mini dashboard ewaluacyjny

### Cel

Zrobić prostą tabelę wyników testów AI.

### Co można mierzyć?

- pass/fail,
- źródło odpowiedzi,
- czy odpowiedź była grounded,
- czy użyto właściwego toola,
- czy pojawił się trace,
- czy był human approval,
- czas odpowiedzi,
- koszt,
- komentarz reviewera.

### Przykładowe kolumny

```text
test_id
category
input
expected_behavior
actual_output
pass_fail
source_used
tool_used
trace_available
human_approval_required
notes
```

## Jak opisać taki projekt w CV lub portfolio?

Przykład:

```text
Built a small RAG-based knowledge assistant and created an evaluation checklist covering missing answers, conflicting sources, groundedness, prompt injection and regression testing.
```

Albo po polsku:

```text
Zbudowałam/zbudowałem prostego asystenta RAG i przygotowałam/przygotowałem zestaw testów obejmujący brakujące odpowiedzi, sprzeczne źródła, zgodność odpowiedzi ze źródłami, prompt injection i testy regresyjne.
```

## Final takeaway

Mały projekt AI z dobrymi testami może być bardziej wartościowy niż duże demo bez kontroli.

Portfolio nie musi pokazywać tylko, że potrafisz użyć modelu.

Może pokazywać, że rozumiesz jakość, bezpieczeństwo i utrzymanie systemu.
