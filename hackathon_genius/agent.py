"""
Hackathon Genius — orkiestrator (root_agent)

To jest punkt wejścia dla frameworka ADK. `root_agent` jest agentem
        idea_agent,        # Krok 1: wygeneruj 3 pomysły na projekt

  Wejście użytkownika
      │
      ▼
  [IdeaAgent]          ← przegląda bazę motywów i generuje 3 pomysły
      │  (output_key: "hackathon_ideas")
      ▼
  [TechStackAgent]     ← dobiera stack technologiczny do każdego pomysłu
      │  (output_key: "tech_stacks")
      ▼
  [TimelineAgent]      ← wybiera najbardziej wykonalny pomysł i tworzy plan sprintu
      │  (output_key: "sprint_plan")
      ▼
  [PitchAgent]         ← pisze 1-minutowy pitch i przygotowuje pytania od jury
         (output_key: "elevator_pitch")

Wszystkie agenty komunikują się przez współdzielony stan sesji
(session.state). Każdy agent odczytuje poprzednie output_key i zapisuje
własny wynik. Dzięki temu cały przepływ jest widoczny jako osobne zdarzenia
w kliencie webowym ADK.

Aby uruchomić:
    adk web
    (z katalogu nadrzędnego: c:/swdtools/github/agh_conference)

Następnie otwórz http://localhost:8000 i wybierz "hackathon_genius".
Wpisz temat hackathonu, np. "zrównoważony rozwój" albo "AI w ochronie zdrowia".
"""

from google.adk.agents import SequentialAgent

from .sub_agents.idea_agent import idea_agent
from .sub_agents.tech_stack_agent import tech_stack_agent
from .sub_agents.timeline_agent import timeline_agent
from .sub_agents.pitch_agent import pitch_agent

# ---------------------------------------------------------------------------
# Root agent — to ten obiekt ADK wykrywa i uruchamia w `adk web`
# ---------------------------------------------------------------------------
root_agent = SequentialAgent(
    name="HackathonGenius",
    description=(
        "Wieloagentowy pipeline, który zamienia temat hackathonu w kompletny "
        "plan działania: 3 pomysły na projekt -> stack technologiczny -> plan sprintu -> pitch."
    ),
    sub_agents=[
        idea_agent,        # Krok 1: wygeneruj 3 pomysły na projekt
        tech_stack_agent,  # Krok 2: dobierz stack dla każdego pomysłu
        timeline_agent,    # Krok 3: zbuduj plan sprintu dla najlepszego pomysłu
        pitch_agent,       # Krok 4: napisz końcowy pitch
    ],
)
