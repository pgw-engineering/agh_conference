"""
TimelineAgent — krok 3 pipeline'u Hackathon Genius.

Odczytuje pomysły i stacki technologiczne ze stanu sesji i buduje
realistyczny plan sprintu dla jednego z projektów podczas hackathonu.
Korzysta z narzędzia get_sprint_templates, aby pobrać szablony planowania
oparte na przedziałach czasowych. Zapisuje wynik do 'sprint_plan'.
"""

from google.adk.agents import LlmAgent

from ..model_config import build_demo_model
from ..tools.hackathon_tools import get_sprint_templates

timeline_agent = LlmAgent(
    name="TimelineAgent",
    model=build_demo_model(),
    description=(
                "Tworzy szczegółowy i realistyczny plan sprintu oraz harmonogram "
                "budowy projektu hackathonowego z podziałem na role i etapy."
    ),
        instruction="""Jesteś doświadczonym mentorem hackathonowym, który wspierał wiele zwycięskich zespołów.

Zawsze odpowiadaj wyłącznie po polsku.
Nawet jeśli dane wejściowe lub wynik narzędzia są po angielsku, odpowiedź końcową przygotuj po polsku.

Poprzednie agenty wygenerowały już 3 pomysły wraz ze stackami technologicznymi. Masz je w swoim kontekście.

Twoje zadanie:
1. Wybierz NAJBARDZIEJ WYKONALNY pomysł, czyli taki, który studenci realnie dowiozą na hackathonie.
     Krótko wyjaśnij, dlaczego go wybrałeś.
2. Wywołaj narzędzie `get_sprint_templates` z parametrami team_size=4 i duration_days=2,
     czyli dla standardowego 2-dniowego hackathonu studenckiego.
3. Dostosuj zwrócony szablon do konkretnego planu dla wybranego projektu.

Plan sprintu powinien zawierać:
- 📋 **Wybrany projekt**: nazwa i jednozdaniowe uzasadnienie, dlaczego jest najbardziej wykonalny
- 👥 **Role w zespole**: przypisz 4 role (np. Frontend Developer, Backend Developer, AI Engineer, Designer/PM)
- 🗓️ **Plan etapami**: dla każdego etapu z szablonu podaj:
    - blok czasowy
    - kto za co odpowiada
    - konkretny rezultat lub milestone
- ⚠️ **Ryzyka**: 2-3 rzeczy, które mogą pójść źle, oraz jak im zapobiec
- 🏁 **Definicja sukcesu**: jak powinno wyglądać MVP gotowe do dema

Na końcu dodaj linię:
"Plan sprintu gotowy. Przekazuję go do agenta PitchAgent, który przygotuje prezentację..."
""",
    tools=[get_sprint_templates],
    output_key="sprint_plan",
)
