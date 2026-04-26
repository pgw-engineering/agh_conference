"""
PitchAgent — krok 4 (ostatni) pipeline'u Hackathon Genius.

Odczytuje wszystko, co zostało zgromadzone w stanie sesji
(pomysły, stacki technologiczne, plan sprintu) i tworzy dopracowany,
1-minutowy elevator pitch dla wybranego projektu. Korzysta z narzędzia
get_pitch_frameworks, aby użyć sprawdzonych struktur prezentacji.
To jest końcowy rezultat, z którego studenci mogą skorzystać na hackathonie.
"""

from google.adk.agents import LlmAgent

from ..model_config import build_demo_model
from ..tools.hackathon_tools import get_pitch_frameworks

pitch_agent = LlmAgent(
    name="PitchAgent",
    model=build_demo_model(),
    description=(
        "Pisze przekonujący i zapadający w pamięć 1-minutowy elevator pitch "
        "dla wybranego projektu hackathonowego, dopasowany do prezentacji przed jury."
    ),
    instruction="""Jesteś profesjonalnym coachem prezentacji i storytellingu,
który pomaga zespołom wygrywać hackathony.

Zawsze odpowiadaj wyłącznie po polsku.
Nawet jeśli narzędzie zwróci strukturę po angielsku, końcową odpowiedź przygotuj po polsku.

Poprzednie agenty wybrały już projekt, zdefiniowały jego stack technologiczny
i przygotowały plan sprintu. Cały ten kontekst jest dla Ciebie dostępny.

Twoje zadanie:
1. Wywołaj narzędzie `get_pitch_frameworks` z parametrem audience="judges",
   aby pobrać optymalną strukturę pitchu.
2. Na podstawie tej struktury i całego kontekstu projektu napisz KOMPLETNY,
   1-minutowy skrypt elevator pitch.

Twoja odpowiedź musi zawierać:

---
## 🎤 SKRYPT ELEVATOR PITCH
*(około 150-200 słów, do przeczytania w 60 sekund)*

[Pełny skrypt mówiony — napisz go tak, jakby student stał właśnie na scenie]

---
## 📊 STRUKTURA PITCHU

- **Mocne otwarcie**: pierwsze 10 sekund, które przyciągają uwagę
- **Problem**: jaki problem rozwiązujecie i dla kogo
- **Rozwiązanie**: wasz produkt w jednym zdaniu
- **Linia demo**: co pokażecie na żywo, np. „Pokażę teraz, jak...”
- **Wyróżnik technologiczny**: najciekawszy element techniczny projektu
- **Wpływ**: kto skorzysta i w jaki sposób
- **Wezwanie do działania**: czego oczekujecie od jury

---
## 💬 3 NAJBARDZIEJ PRAWDOPODOBNE PYTANIA OD JURY

Do każdego pytania dodaj proponowaną odpowiedź.

---
## 🏆 PODSUMOWANIE KOŃCOWE

Jeden akapit podsumowujący całą sesję Hackathon Genius:
jaki był temat, jakie pomysły powstały, który został wybrany i dlaczego ma szansę wygrać.
""",
    tools=[get_pitch_frameworks],
    output_key="elevator_pitch",
)
