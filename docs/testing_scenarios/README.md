# AI Agent Testing Starter Kit

Krótka, praktyczna pigułka edukacyjna o testowaniu prostych systemów AI: chatbotów, RAG-ów i agentów korzystających z narzędzi.

Materiał jest przygotowany z myślą o studentach i osobach, które chcą przejść od etapu: „zbudowałem demo i działa” do bardziej inżynierskiego pytania:

> Skąd wiem, że ten system jest wiarygodny, bezpieczny, kontrolowalny i możliwy do utrzymania?

## Dla kogo jest ten folder?

Dla osób, które:

- budują pierwsze chatboty lub RAG-i,
- eksperymentują z agentami AI,
- chcą lepiej rozumieć testowanie aplikacji LLM,
- chcą przygotować portfolio projektowe z bardziej profesjonalnym podejściem,
- chcą wiedzieć, czym różni się demo od rozwiązania gotowego do użycia przez prawdziwych użytkowników.

## Główna myśl

Nie testuj AI tylko po to, żeby potwierdzić, że działa.

Testuj tak, żeby zobaczyć:

- gdzie system zaczyna halucynować,
- gdzie traci kontakt ze źródłami,
- gdzie wykonuje złą akcję,
- gdzie ma zbyt szerokie uprawnienia,
- gdzie brakuje logów lub trace’ów,
- gdzie powinien powiedzieć „nie wiem”,
- gdzie powinien zatrzymać się i poprosić człowieka o decyzję.

## Co znajdziesz w tym folderze?

| Plik | Co zawiera |
|---|---|
| `01-mindset-testowania-ai.md` | Jak myśleć o testowaniu AI: demo vs produkcja, happy path vs edge cases |
| `02-checklista-rag.md` | Checklista testowania RAG-ów i chatbotów opartych o dokumenty |
| `03-checklista-agentow.md` | Checklista testowania agentów korzystających z narzędzi |
| `04-scenariusze-testowe.md` | Przykładowe scenariusze testowe do skopiowania |
| `05-metody-ewaluacji.md` | Evale, golden dataset, regression testing, trace-based evaluation, LLM-as-a-judge |
| `06-narzedzia-i-frameworki.md` | OpenAI Evals, LangSmith, Ragas, promptfoo, DeepEval, Phoenix, OWASP |
| `07-mini-projekty-dla-studentow.md` | Pomysły na małe projekty do nauki testowania AI |
| `08-red-teaming-i-bezpieczenstwo.md` | Prompt injection, excessive agency, uprawnienia, human approval |
| `09-zrodla-i-dalsza-lektura.md` | Linki do dokumentacji, artykułów i dalszej lektury |
| `10-co-robic-gdy-testy-failuja.md` | Praktyczny przewodnik: jak diagnozować i naprawiać problemy wykryte przez testy |

## Minimalny workflow testowania małego systemu AI

1. Zdefiniuj, co system ma robić.
2. Zdefiniuj, czego system NIE powinien robić.
3. Przygotuj zestaw przypadków testowych.
4. Uwzględnij happy path, edge cases i scenariusze awaryjne.
5. Sprawdź odpowiedź końcową.
6. Sprawdź drogę dojścia do odpowiedzi: źródła, narzędzia, logi, trace’y.
7. Po każdej większej zmianie promptu, modelu, retrievera albo toola uruchom testy ponownie.
8. Zapisuj wyniki, żeby widzieć regresje.

## Najważniejszy wniosek

Testowanie systemu AI to nie tylko sprawdzenie, czy odpowiedź dobrze brzmi.

To sprawdzenie:

- na jakich danych opiera się odpowiedź,
- jakich narzędzi użył system,
- jakie miał uprawnienia,
- co zrobił, gdy coś poszło nie tak,
- czy zostawił ślad działania,
- i czy wiedział, kiedy powinien się zatrzymać.

W systemach agentowych kontrola nie jest dodatkiem. Kontrola jest częścią produktu.
