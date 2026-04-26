"""
Mock tools for the Hackathon Genius multi-agent demo.

These tools simulate external data sources (databases, APIs, libraries)
so the demo works without real external services. Each tool call is
visible as a separate step in the ADK web client, making the agent
flow clear and educational.
"""

import random


def browse_hackathon_themes(theme: str) -> dict:
    """
    Browse a database of past hackathon themes and winning project patterns
    to inspire idea generation.

    Args:
        theme: The hackathon or IT/MIT studnent theme or topic to search for (e.g. "sustainability", "AI", "health")

    Returns:
        A dict with inspiration data: popular categories, winning patterns, and example keywords.
    """
    theme_database = {
        "sustainability": {
            "popular_categories": ["Carbon tracking", "Food waste reduction", "Green energy", "Circular economy"],
            "winning_patterns": ["Gamification of eco-habits", "B2B marketplace for recycled materials", "AI-powered energy optimization"],
            "keywords": ["carbon footprint", "renewable", "zero-waste", "biodegradable", "upcycling"],
        },
        "health": {
            "popular_categories": ["Mental wellness", "Chronic disease management", "Telemedicine", "Preventive care"],
            "winning_patterns": ["Wearable data aggregation", "AI symptom checker", "Community support networks"],
            "keywords": ["well-being", "monitoring", "early detection", "remote care", "personalized medicine"],
        },
        "education": {
            "popular_categories": ["Personalized learning", "Skill verification", "Peer tutoring", "Accessibility"],
            "winning_patterns": ["Adaptive quiz engine", "Micro-credential platform", "AR/VR classroom"],
            "keywords": ["adaptive", "gamification", "peer-to-peer", "credentials", "accessibility"],
        },
        "fintech": {
            "popular_categories": ["Financial inclusion", "Fraud detection", "DeFi", "Personal budgeting"],
            "winning_patterns": ["AI spending advisor", "Micro-investment for students", "Cross-border payments"],
            "keywords": ["inclusion", "transparency", "automation", "blockchain", "savings"],
        },
    }

    # Case-insensitive search with fallback to a generic set
    key = theme.lower().strip()
    for db_key in theme_database:
        if db_key in key or key in db_key:
            return {"theme": theme, "inspiration": theme_database[db_key]}

    # Generic fallback for unknown themes
    return {
        "theme": theme,
        "inspiration": {
            "popular_categories": ["AI-powered assistant", "Community platform", "Data visualization", "Automation tool"],
            "winning_patterns": ["Solve a real daily pain point", "Use AI to reduce manual work", "Connect people who need help with people who can help"],
            "keywords": ["automation", "community", "AI", "efficiency", "impact"],
        },
    }


def get_tech_stack_library(project_type: str) -> dict:
    """
    Query a technology library to get recommended tech stacks for different
    types of projects.

    Args:
        project_type: Type of project (e.g. "mobile app", "web platform", "data analytics", "IoT")

    Returns:
        A dict with recommended frontend, backend, AI/ML, and database technologies.
    """
    library = {
        "web": {
            "frontend": ["React / Next.js", "Vue.js", "SvelteKit"],
            "backend": ["FastAPI (Python)", "Node.js + Express", "Django REST"],
            "ai_ml": ["Google Gemini API", "Vertex AI", "LangChain + OpenAI"],
            "database": ["PostgreSQL", "Firebase Firestore", "Supabase"],
            "hosting": ["Google Cloud Run", "Vercel + Railway", "Fly.io"],
        },
        "mobile": {
            "frontend": ["Flutter (cross-platform)", "React Native", "Swift / Kotlin (native)"],
            "backend": ["Firebase", "FastAPI (Python)", "Supabase"],
            "ai_ml": ["TensorFlow Lite", "Google ML Kit", "Gemini Nano (on-device)"],
            "database": ["Firebase Realtime DB", "SQLite (local)", "Realm"],
            "hosting": ["Google Play / App Store", "Firebase App Distribution"],
        },
        "data": {
            "frontend": ["Streamlit", "Grafana", "Plotly Dash"],
            "backend": ["Python + FastAPI", "Apache Spark", "dbt"],
            "ai_ml": ["scikit-learn", "PyTorch", "Google BigQuery ML"],
            "database": ["BigQuery", "ClickHouse", "DuckDB"],
            "hosting": ["Google Colab / Vertex AI Workbench", "Hugging Face Spaces"],
        },
        "iot": {
            "frontend": ["React Dashboard", "Grafana", "Flutter mobile"],
            "backend": ["MQTT + Node-RED", "FastAPI", "Google Cloud IoT Core"],
            "ai_ml": ["TensorFlow Lite", "Edge TPU", "ONNX Runtime"],
            "database": ["InfluxDB (time series)", "Firebase", "TimescaleDB"],
            "hosting": ["Google Cloud IoT", "AWS IoT Greengrass", "Azure IoT Hub"],
        },
    }

    key = project_type.lower()
    for lib_key, stack in library.items():
        if lib_key in key or key in lib_key:
            return {"project_type": project_type, "recommended_stack": stack}

    # Default web stack
    return {"project_type": project_type, "recommended_stack": library["web"]}


def get_sprint_templates(team_size: int, duration_days: int) -> dict:
    """
    Fetch sprint planning templates based on team size and hackathon duration.

    Args:
        team_size: Number of people in the team (1-6)
        duration_days: Length of the hackathon in days (1, 2, or 3)

    Returns:
        A sprint template with day-by-day milestones and task assignments.
    """
    templates = {
        1: {  # 1-day hackathon
            "phases": [
                {"name": "Setup & Planning", "hours": "0–2h", "tasks": ["Define scope", "Bootstrap project", "Set up version control"]},
                {"name": "Core Development", "hours": "2–7h", "tasks": ["Build MVP feature", "Integrate AI/API", "Basic UI"]},
                {"name": "Polish & Demo Prep", "hours": "7–9h", "tasks": ["Bug fixing", "Demo script", "Slide deck (3 slides)"]},
                {"name": "Presentation", "hours": "9–10h", "tasks": ["Live demo", "Q&A"]},
            ]
        },
        2: {  # 2-day hackathon
            "phases": [
                {"name": "Day 1 Morning – Discovery", "hours": "0–4h", "tasks": ["Problem validation", "Tech stack decision", "Repo setup", "Wireframes"]},
                {"name": "Day 1 Afternoon – Build", "hours": "4–8h", "tasks": ["Backend API skeleton", "Database schema", "Auth/login"]},
                {"name": "Day 2 Morning – Features", "hours": "8–14h", "tasks": ["Core feature complete", "AI integration", "Frontend connected to backend"]},
                {"name": "Day 2 Afternoon – Launch", "hours": "14–20h", "tasks": ["Testing", "Deploy to cloud", "Demo polish", "Pitch deck"]},
            ]
        },
        3: {  # 3-day hackathon
            "phases": [
                {"name": "Day 1 – Foundation", "hours": "0–8h", "tasks": ["Research & ideation", "Architecture design", "Environment setup", "Backend scaffolding"]},
                {"name": "Day 2 – Core Build", "hours": "8–20h", "tasks": ["All main features", "AI/ML pipeline", "Frontend UI", "API integration", "Unit tests"]},
                {"name": "Day 3 – Ship It", "hours": "20–30h", "tasks": ["Bug fixing", "User testing", "Cloud deployment", "Pitch deck (5–7 slides)", "Video demo (optional)", "Final presentation"]},
            ]
        },
    }

    duration_key = min(max(duration_days, 1), 3)
    template = templates[duration_key]
    return {
        "phases": template["phases"],
        "team_size": team_size,
        "duration_days": duration_days,
        "tip": f"For a team of {team_size}: split frontend/backend/AI roles. Daily standups every morning.",
    }


def get_pitch_frameworks(audience: str) -> dict:
    """
    Retrieve pitch frameworks tailored for different audiences.

    Args:
        audience: Target audience for the pitch (e.g. "judges", "investors", "students", "technical")

    Returns:
        A pitch framework with structure, key points to emphasize, and example phrases.
    """
    frameworks = {
        "judges": {
            "structure": ["Hook (problem story)", "Solution demo", "Tech innovation", "Impact / metrics", "Call to action"],
            "emphasize": ["Creativity", "Technical execution", "Potential real-world impact"],
            "time": "3–5 minutes",
            "opening_templates": [
                "What if you could [solve problem] in just [time]?",
                "Every day, [N] people struggle with [problem]. We changed that.",
                "We built [project] in 24 hours — here's what we learned.",
            ],
        },
        "investors": {
            "structure": ["Problem size (TAM)", "Our solution", "Business model", "Traction / MVP", "Team", "Ask"],
            "emphasize": ["Market opportunity", "Scalability", "Revenue model", "Competitive advantage"],
            "time": "5–7 minutes",
            "opening_templates": [
                "This is a $[X]B market that's still being done manually.",
                "[Customer type] spend [$ or hours] on [problem] every year.",
            ],
        },
        "students": {
            "structure": ["Relatable problem", "Cool demo", "How it works (simplified)", "What we learned", "Try it yourself"],
            "emphasize": ["Fun factor", "Learning journey", "Accessibility", "Open source"],
            "time": "2–3 minutes",
            "opening_templates": [
                "We've all experienced [frustration]. So we built something about it.",
                "This started as a crazy idea at 2am — and it actually worked.",
            ],
        },
        "technical": {
            "structure": ["Architecture overview", "Key technical challenges", "AI/ML components", "Performance metrics", "Future improvements"],
            "emphasize": ["Code quality", "System design", "Novel algorithms", "Scalability decisions"],
            "time": "5–10 minutes",
            "opening_templates": [
                "We built a [architecture type] system that handles [challenge].",
                "The interesting technical problem here is [challenge].",
            ],
        },
    }

    key = audience.lower()
    for fw_key, framework in frameworks.items():
        if fw_key in key or key in fw_key:
            return {"audience": audience, "framework": framework}

    return {"audience": audience, "framework": frameworks["judges"]}
