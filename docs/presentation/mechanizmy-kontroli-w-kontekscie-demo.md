# Mechanizmy kontroli w kontekście demo Hackathon Genius

## Autonomia z ograniczeniami – jądro podejścia

Budując multi-agent system, musimy odpowiedzieć na pytanie: **Jak dać agentowi autonomię, jednocześnie zachowując kontrolę?**

Odpowiedź: przez warstwowe bramki bezpieczeństwa, które działają na trzech poziomach:
1. **Wejście** — validacja promptu, detekcja ataku
2. **Działanie** — allowlista narzędzi, walidacja argumentów
3. **Przepustowość** — rate limiting, zatrzymanie zamiast siłą

To podejście można streścić tak:

**Autonomia tak, ale pod kontrolą.**

---

## Mechanizm 1: Bramka promptu – ochrona na wejściu

**Zasada:** Zanim agent zobaczy prompt użytkownika, musi przejść przez walidację. Chronimy przed prompt injection, nadużyciem API i spam-floodem.

**Implementacja w demo:**
- Callback `prompt_injection_guard()` sprawdza każde wejście przed wysłaniem do LLM.
- Wykrywa 22 wspólne wzorce ataku (prompt injection, jailbreak, token manipulation).
- Ogranicza długość wejścia do 500 znaków.
- Sprawdza rate limit — jeśli użytkownik przekroczył limit 2 req/min, zwraca odmowę bezpieczną zamiast paniki.

**Wizualizacja na slajdzie:** Bramka wejścia z symbolem blokowania.

---

## Mechanizm 2: Allowlista narzędzi – kontrola działań

**Zasada:** Agent ma dostęp tylko do wybranych narzędzi. Każde wywołanie narzędzia przechodzi walidację.

**Implementacja w demo:**
- `IdeaAgent` ma zdefiniowaną allowlistę funkcji, które może wywoływać.
- Callback `tool_argument_guard()` sprawdza argumenty każdego wywołania:
  - Blokuje path traversal (`../`, `//` itp.)
  - Waliduje typy argumentów
  - Zapobiega niebezpiecznym znakom specjalnym.
- Role mają jasne granice: IdeaAgent tworzy ideę, TechStackAgent nie tworzy pomysłów.

**Wizualizacja na slajdzie:** Rząd narzędzi z zaznaczonymi dostępnymi + zablokowanymi.

---

## Mechanizm 3: Pipeline z wspólnym stanem – zakotwiczenie w danych

**Zasada:** Zamiast każdemu agentowi działać samemu, tworzą łańcuch, gdzie każdy etap:
- Bierze wyjście poprzednika
- Dodaje swój element
- Przekazuje dalej

**Implementacja w demo:**
- Sekwencja: `IdeaAgent -> TechStackAgent -> TimelineAgent -> PitchAgent`
- Agenci wymieniają kontekst przez `session.state` (obiekt dzielony)
- Każdy agent zna pełny kontekst dotychczasowych decyzji
- Wynik na końcu to syntetyczna odpowiedź, nie pojedyncze zgadnięcie.

**Wizualizacja na slajdzie:** Cztery boxy połączone strzałkami, w środku zielone checkmarki.

---

## Mechanizm 4: Rate limiting – zatrzymanie zamiast przeciążenia

**Zasada:** Żaden użytkownik nie powinien móc floodować systemu żądaniami. Lepiej odmówić niż pracować w paniką.

**Implementacja w demo:**
- Token bucket: każdy użytkownik dostaje 2 tokeny na minutę (regularne uzupełnienie).
- Możliwość chwilowego burst do 3 tokeni (elastyczność).
- Gdy limit wyczerpany: callback zwraca komunikat „Zbyt wiele żądań. Spróbuj za chwilę."
- Logowanie: każda próba przekroczenia limitu jest rejestrowana.

**Wizualizacja na slajdzie:** Timer z przeszklonym segmentem (tokeny) i wskaźnikiem refreshu.

---

## Mechanizm 5: Jawne role i audytowalność

**Zasada:** Każdy agent zna swoją rolę i pracuje przejrzyście. Decyzje można śledzić od strony biznesowej.

**Implementacja w demo:**
- `IdeaAgent` = tworzenie idei (inspiracja, brainstorm, powiązania)
- `TechStackAgent` = jak technologia wspiera ideę
- `TimelineAgent` = kiedy i w jakich fazach
- `PitchAgent` = jak to sprzedać słowami

Każdy ma pełny kontekst: kto przede mną pracował, co zrobił, czego oczekuję.

**Wizualizacja na slajdzie:** Cztery koła z ikonami ról wewnątrz pipeline.

---

## Mechanizm 6: Sandboxowanie – izolacja na poziomie infrastruktury

**Zasada:** Nawet jeśli wszystko inne zawiedzie, aplikacja nie może wyjść poza swoją piaskownicę. System operacyjny i containeryzacja stanowią ostatnią linię obrony.

**Implementacja w demo:**
- Kontener Docker z **read-only filesystem** — pliki systemowe nie mogą być zmieniane
- Writable tmpfs dla wybranych katalogów (`/tmp`, `/app/data`) — kontrolowany dostęp
- **Unprivileged user** (UID 1001, `appuser`) — żadne uprawnienia administracyjne
- **Capabilities dropped** (`cap_drop: ALL`) — żadne specjalne uprawnienia na poziomie kernela
- **Security option** `no-new-privileges` — procesy potomne nie mogą uzyskać wyższych uprawnień
- Resource limits: 1 CPU, 512MB RAM — ochrona przed wyczerpaniem zasobów
- Bridge network isolation — aplikacja nie może komunikować się bezpośrednio z hostem

**Wizualizacja na slajdzie:** Pudełko (kontener) otoczone pancerzem bezpieczeństwa.

---

## Kiedy używać takiego podejścia – a kiedy nie

W naszym kontekście:

**✅ Użyj agenta z kontrolą, gdy:**
- Potrzebujesz syntezy wieloperspektywicznej (ideacja, planowanie, strategy)
- Problem wymaga iteracyjnego rozumowania
- Chcesz oparty na danych, ale nie całkowicie deterministyczny wynik

**❌ Nie używaj agenta, gdy:**
- Wystarczy klasyczny workflow (np. wysłanie emaila) reguły biznesowe lub RAG, to autonomia agenta może tylko podnieść koszt i niepewność.
- Problem ma jednoznaczną regułę biznesową
- Potrzebujesz gwarancji, że dokładnie A → dokładnie B
- Nie używamy agenta do zadań prostych i deterministycznych.
- Agenta warto użyć tam, gdzie potrzebna jest synteza, iteracyjne rozumowanie i łączenie wielu perspektyw.

Hackathon Genius to przypadek z pierwszej kategorii: od tematu do pitchu wymaga kombinowania danych, kreatywności i logicznych skoków. **Ale musimy mieć kontrolę na każdym poziomie.**



## Summary: Sześć mechanizmów kontroli

Ten projekt opiera się na sześciu mechanizmach kontroli (3 warstwy na poziomie kodu, 1 warstwa infrastruktury):

**Warstwy na poziomie kodu:**
1. **Bramka promptu** — walidacja każdego wejścia przed LLM, detekcja prompt injection
2. **Allowlista narzędzi** — agent ma dostęp tylko do wybranych funkcji, każde wywołanie sprawdzane
3. **Pipeline z wspólnym stanem** — agenci pracują w łańcuchu, każdy zna pełny kontekst

**Warstwy na poziomie operacyjnym:**
4. **Rate limiting** — ochrona przed floodem poprzez token bucket (2 req/min)
5. **Jawne role** — każdy agent zna swoją robotę i działa przejrzyście, decyzje są audytowalne
6. **Sandboxowanie** — izolacja infrastrukturalny (read-only fs, unprivileged user, cap_drop, resource limits)

Razem dają **autonomię z kontrolą** — dokładnie tyle niezależności, ile problem wymaga.

---

## One-liner do zapamiętania

**Nie chodzi o to, żeby agent był wszędzie. Chodzi o to, żeby miał dokładnie tyle autonomii, ile problem naprawdę wymaga.**

