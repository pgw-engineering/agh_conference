# Mechanizmy kontroli w kontekście demo Hackathon Genius

## Co oznacza ten slajd

Ten slajd pokazuje, że w naszym demo agent nie działa bez ograniczeń. Działa autonomicznie, ale tylko w ramach jasno zdefiniowanych reguł bezpieczeństwa i jakości.

To podejście można streścić tak:

**Autonomia tak, ale pod kontrolą.**

---

## Jak to mapuje się na nasze demo

### 1. Tools i function calling

**Na slajdzie:** Agent powinien wykonywać tylko dozwolone akcje.

**W demo:**
- `IdeaAgent` ma allowlistę narzędzi.
- Callback `tool_argument_guard()` blokuje wywołania poza zakresem.
- Ograniczamy ryzyko nieautoryzowanych działań i nadużyć.

### 2. Zakotwiczenie odpowiedzi w danych

**Na slajdzie:** Odpowiedzi mają wynikać z kontekstu i danych, nie z przypadkowej improwizacji.

**W demo:**
- Pipeline: `IdeaAgent -> TechStackAgent -> TimelineAgent -> PitchAgent`.
- Agenci wymieniają kontekst przez `session.state`.
- Każdy etap dokłada konkretny, przewidywalny element do wyniku.

### 3. Walidacja i reguły kontrolne

**Na slajdzie:** Każde wejście powinno przejść przez reguły bezpieczeństwa.

**W demo:**
- `prompt_injection_guard()` wykrywa wzorce prompt injection.
- Limit długości wejścia użytkownika chroni przed nadużyciami.
- Walidacja argumentów blokuje path traversal i niebezpieczne znaki.

### 4. Fallbacki i nadzór człowieka

**Na slajdzie:** System powinien umieć bezpiecznie odmówić zamiast działać na siłę.

**W demo:**
- Rate limiting (token bucket) ogranicza flood i DoS.
- Przy przekroczeniu limitu użytkownik dostaje komunikat blokujący.
- Przy wejściu ryzykownym callback zwraca bezpieczną odmowę.

### 5. Ścieżka dojścia do wyniku

**Na slajdzie:** Wynik ma być osiągany przez kontrolowany proces.

**W demo:**
- Orkiestrator sekwencyjny pilnuje kolejności kroków.
- Role agentów są jawne i rozdzielone.
- Decyzje są audytowalne na poziomie etapów pipeline.

---

## Co oznacza prawa część slajdu: "Kiedy NIE używać agenta"

W naszym kontekście:

- Nie używamy agenta do zadań prostych i deterministycznych.
- Jeśli wystarczy klasyczny workflow, reguły biznesowe lub RAG, to autonomia agenta może tylko podnieść koszt i niepewność.
- Agenta warto użyć tam, gdzie potrzebna jest synteza, iteracyjne rozumowanie i łączenie wielu perspektyw.

Właśnie dlatego ten case (od tematu do pitchu) jest dobrym kandydatem na multi-agent, ale z warstwami kontroli.

---

## Krótka wersja do powiedzenia na slajdzie (20-30 sekund)

"Ten slajd pokazuje, że w naszym demo autonomia agentów jest celowo ograniczona. IdeaAgent działa przez bramki bezpieczeństwa: walidację promptu, walidację narzędzi i rate limiting. Dalej mamy kontrolowany pipeline ról i wspólny stan sesji. Dzięki temu agent pomaga tworzyć wartość, ale nie działa poza polityką systemu."

---

## One-liner do zapamiętania

**Nie chodzi o to, żeby agent był wszędzie. Chodzi o to, żeby miał dokładnie tyle autonomii, ile problem naprawdę wymaga.**
