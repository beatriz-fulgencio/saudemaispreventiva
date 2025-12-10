# Changelog - Saúde+ Preventiva

## [1.1.0] - 2025-12-10

### 🤖 Added - AI Agent Integration

#### Major Features
- **HealthAIAgent**: Complete AI agent for intelligent health analysis
  - Multi-dimensional scoring with Machine Learning algorithms
  - Gaussian curves for sleep analysis (optimal: 7-9h)
  - Adaptive scoring based on scientific evidence
  - Automated prioritization of health areas

- **Personalized Goal Generation**
  - AI generates 2-3 weekly goals based on user's lowest scores
  - Context-specific goals (e.g., "Sleep 7h/night (currently 5.5h)")
  - Gradual progression recommendations
  - Category-based goals (sleep, activity, nutrition, mental)

- **Contextual Insights System**
  - Specific insights per health area
  - Pattern recognition (e.g., "1.5h below recommended sleep")
  - Status classification (Excellent, Good, Regular, Needs Attention)
  - Detailed analysis per dimension

- **OpenAI Integration (Optional)**
  - GPT-3.5 powered message enrichment
  - Empathetic and motivational tone
  - Natural language personalization
  - Requires OPENAI_API_KEY environment variable

#### Files Added
- `backend/ai_agent.py` - Complete AI agent implementation (800+ lines)
- `backend/AI_AGENT_README.md` - Comprehensive documentation
- `CHANGELOG.md` - This file

#### Files Modified
- `backend/main.py` - Integration with HealthAIAgent
- `backend/requirements.txt` - Added openai==1.6.1
- `frontend/src/components/LandingPage.jsx` - AI feature highlights
- `frontend/src/components/Results.jsx` - AI-generated goals indicator
- `README.md` - Updated architecture and features

#### API Changes
- Added endpoint: `GET /api/analise-detalhada/{usuario_id}`
  - Returns detailed AI analysis per health area
  - Includes scores, status, and insights

#### Algorithm Improvements
- **Sleep Score**: Gaussian curve centered on 7-9h range
  - Progressive penalty for sleep deficit/excess
  - Quality score integration (50% of total)

- **Activity Score**: Level + frequency combination
  - Optimal: 3-5 exercises per week
  - Progressive scoring based on intensity

- **Nutrition Score**: Quality (70%) + hydration (30%)
  - Ideal water intake: 2-3L/day
  - Food quality on 1-10 scale

- **Mental Health Score**: Stress (40%) + social support (35%) + screen time (25%)
  - Inverted metrics (lower stress is better)
  - Screen time ideal: ≤4h/day

#### Health Patterns (Evidence-Based)
```python
ideal_patterns = {
    "horas_sono": {"min": 7.0, "max": 9.0, "optimal": 8.0},
    "frequencia_exercicio": {"min": 3, "optimal": 5},
    "consumo_agua": {"min": 2.0, "max": 3.0, "optimal": 2.5},
    "nivel_stress": {"max": 4, "optimal": 2},
    # ... more patterns
}
```

#### Importance Weights (Scientific)
- Sleep: 30% (fundamental for overall health)
- Physical Activity: 25% (crucial for well-being)
- Nutrition: 25% (essential for energy)
- Mental Health: 20% (affects all areas)

### Testing
- ✅ Scenario 1: Poor health habits → Score 43, 3 targeted goals
- ✅ Scenario 2: Healthy habits → Score 87, maintenance goals
- ✅ Scenario 3: Mixed habits → Score 62, balanced recommendations
- ✅ All scenarios generate appropriate insights and tips

### Documentation
- Complete AI agent documentation in `AI_AGENT_README.md`
- Updated main README with AI features
- API documentation unchanged (backward compatible)

### Security
- ✅ CodeQL scan: 0 vulnerabilities
- ✅ Dependency check: All packages secure
- ✅ OpenAI API key properly handled (environment variable)

---

## [1.0.0] - 2025-12-10

### Initial Release

#### Features
- Complete full-stack MVP implementation
- Backend: FastAPI with RESTful API
- Frontend: React 19 + Vite
- Portuguese language interface
- Primary color: #528aae
- 4 main pages: Landing, Questionnaire, Results, Dashboard
- Rule-based health scoring system
- 6 API endpoints
- In-memory data storage
- Mobile-responsive design

#### Security Fixes
- Updated fastapi: 0.104.1 → 0.109.1 (ReDoS vulnerability)
- Updated python-multipart: 0.0.6 → 0.0.18 (DoS vulnerability)

#### Documentation
- Complete README with installation instructions
- API_DOCUMENTATION.md with all endpoints
- Startup script (start.sh)
