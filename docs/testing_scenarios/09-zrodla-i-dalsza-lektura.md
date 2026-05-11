# 09. Źródła i dalsza lektura

Poniżej znajduje się lista źródeł do dalszej nauki. Najlepiej zacząć od oficjalnych dokumentacji narzędzi i materiałów organizacji zajmujących się bezpieczeństwem AI.

## 1. Evals i testowanie aplikacji LLM

### OpenAI

- OpenAI — Working with evals  
  https://developers.openai.com/api/docs/guides/evals

- OpenAI — Evaluation best practices  
  https://developers.openai.com/api/docs/guides/evaluation-best-practices

- OpenAI — Evaluate agent workflows  
  https://developers.openai.com/api/docs/guides/agent-evals

- OpenAI Evals — GitHub  
  https://github.com/openai/evals

Dlaczego warto?

OpenAI pokazuje podejście oparte o datasety, gradery, evaluation runs i testowanie workflow agentowych z użyciem trace’ów.

## 2. Tracing i agent workflows

### OpenAI Agents SDK

- Tracing  
  https://openai.github.io/openai-agents-python/tracing/

- Guardrails  
  https://openai.github.io/openai-agents-python/guardrails/

Dlaczego warto?

Dobre źródło do zrozumienia, że w agentach ważny jest nie tylko output, ale też ścieżka działania: tool calls, handoffs, guardrails i custom events.

## 3. RAG evaluation

### LangSmith

- LangSmith — Evaluation  
  https://docs.langchain.com/langsmith/evaluation

- LangSmith — Evaluate a RAG application  
  https://docs.langchain.com/langsmith/evaluate-rag-tutorial

- LangSmith product page — Evaluation  
  https://www.langchain.com/langsmith/evaluation

Dlaczego warto?

LangSmith pokazuje praktyczny workflow: dataset, uruchomienie aplikacji na danych testowych, evaluatory, eksperymenty i porównywanie wyników.

### Ragas

- Ragas documentation  
  https://docs.ragas.io/en/stable/

- Ragas — Available metrics  
  https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/

- Ragas — Faithfulness  
  https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/

- Ragas — Context Precision  
  https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/

Dlaczego warto?

Ragas jest bardzo przydatny do RAG-ów, bo pomaga mierzyć m.in. faithfulness, answer relevancy, context precision i context recall.

## 4. Prompt testing, red teaming i CI/CD

### promptfoo

- promptfoo  
  https://www.promptfoo.dev/

- promptfoo — LLM red teaming guide  
  https://www.promptfoo.dev/docs/red-team/

- promptfoo — How to red team LLM applications  
  https://www.promptfoo.dev/docs/guides/llm-redteaming/

- promptfoo — How to red team RAG applications  
  https://www.promptfoo.dev/docs/red-team/rag/

- promptfoo — GitHub  
  https://github.com/promptfoo/promptfoo

Dlaczego warto?

promptfoo jest praktycznym narzędziem do testowania promptów, porównywania modeli, red teamingu, prompt injection testing i automatyzacji testów w CI/CD.

## 5. Test cases i metryki dla aplikacji LLM

### DeepEval

- DeepEval  
  https://deepeval.com/

- DeepEval — Test cases  
  https://deepeval.com/docs/evaluation-test-cases

- DeepEval — Metrics  
  https://deepeval.com/docs/metrics-introduction

- DeepEval — GitHub  
  https://github.com/confident-ai/deepeval

Dlaczego warto?

DeepEval pozwala myśleć o testowaniu aplikacji LLM w stylu podobnym do testów jednostkowych: test cases, metryki, eval datasets i uruchamianie ewaluacji.

## 6. Observability i tracing

### Phoenix / Arize

- Phoenix  
  https://phoenix.arize.com/

- Phoenix docs  
  https://arize.com/docs/phoenix

- Phoenix — LLM traces  
  https://arize.com/docs/phoenix/tracing/llm-traces

- Phoenix — GitHub  
  https://github.com/arize-ai/phoenix

Dlaczego warto?

Phoenix pomaga obserwować aplikacje LLM przez trace’y, debugowanie, ewaluacje, eksperymenty i wykrywanie regresji.

## 7. Security i AI red teaming

### OWASP

- OWASP GenAI Security Project  
  https://genai.owasp.org/

- OWASP Top 10 for LLM Applications  
  https://genai.owasp.org/llm-top-10/

- OWASP AI Agent Security Cheat Sheet  
  https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html

- OWASP Top 10 for Large Language Model Applications  
  https://owasp.org/www-project-top-10-for-large-language-model-applications/

Dlaczego warto?

OWASP porządkuje najważniejsze ryzyka bezpieczeństwa aplikacji LLM i agentów, m.in. prompt injection, sensitive information disclosure, excessive agency i insecure tool/plugin design.

### Microsoft AI Red Team

- Microsoft AI Red Team  
  https://learn.microsoft.com/en-us/security/ai-red-team/

- Microsoft AI Red Team training  
  https://learn.microsoft.com/en-us/security/ai-red-team/training

- Microsoft AI Red Team Playground Labs  
  https://github.com/microsoft/AI-Red-Teaming-Playground-Labs

Dlaczego warto?

Microsoft pokazuje AI red teaming jako praktykę zabezpieczania systemów generatywnej AI i dostarcza materiały szkoleniowe oraz laboratoria.

## 8. Governance i risk management

### NIST

- NIST AI Risk Management Framework  
  https://www.nist.gov/itl/ai-risk-management-framework

- NIST AI RMF: Generative AI Profile  
  https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence

Dlaczego warto?

NIST daje perspektywę organizacyjną: zarządzanie ryzykiem, trustworthiness, governance i ocenę ryzyk generatywnej AI.

## 9. Projektowanie agentów

### Anthropic

- Anthropic — Building Effective AI Agents  
  https://www.anthropic.com/research/building-effective-agents

- Anthropic — Writing effective tools for AI agents  
  https://www.anthropic.com/engineering/writing-tools-for-agents

- Anthropic — Effective context engineering for AI agents  
  https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

Dlaczego warto?

Anthropic mocno podkreśla prostotę, kompozycyjne workflow, dobre projektowanie narzędzi i unikanie nadmiarowej złożoności.

## 10. Hasła do dalszego researchu

Warto szukać fraz:

- `LLM evals production`
- `RAG faithfulness`
- `RAG context precision`
- `agent trajectory evaluation`
- `tool use evaluation agents`
- `LLM-as-a-judge pitfalls`
- `prompt regression testing`
- `prompt injection testing`
- `AI red teaming`
- `agent observability`
- `human-in-the-loop AI agents`
- `least privilege AI agents`
- `AI guardrails testing`


## 11. Debugowanie i poprawianie wyników evali

Przy poprawianiu wyników testów warto łączyć kilka perspektyw:

- dokumentacje evali, np. OpenAI Evals i LangSmith,
- metryki RAG, np. Ragas,
- tracing i observability, np. LangSmith, Phoenix albo OpenAI Agents SDK,
- red teaming i security checklisty, np. OWASP i promptfoo,
- projektowanie prostszych workflow i narzędzi, np. materiały Anthropic.

W praktyce słaby wynik testu może oznaczać problem z promptem, ale równie dobrze może oznaczać problem z danymi, retrievalem, narzędziem, uprawnieniami, trace’em albo architekturą.

## Proponowana ścieżka czytania

Jeśli masz mało czasu, zacznij tak:

1. OpenAI — Evaluation best practices
2. LangSmith — Evaluate a RAG application
3. Ragas — Faithfulness i Context Precision
4. promptfoo — LLM red teaming guide
5. OWASP AI Agent Security Cheat Sheet
6. Anthropic — Building Effective AI Agents

## Final takeaway

Nie musisz znać wszystkich narzędzi.

Ważniejsze jest, żeby rozumieć podstawowe pytania:

- czy odpowiedź wynika ze źródeł?
- czy agent użył właściwego narzędzia?
- czy system zostawił trace?
- czy ma ograniczone uprawnienia?
- czy testujemy nie tylko happy path?
- czy system wie, kiedy powinien się zatrzymać?
