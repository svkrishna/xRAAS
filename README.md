# XReason - Reasoning as a Service (RaaS)

A modular reasoning pipeline combining LLM intuition (System 1) with symbolic/rule-based checks (System 2).

## 🎯 Project Overview

XReason is a reasoning-as-a-service platform that orchestrates multiple reasoning systems to provide explainable, validated answers. The system combines:

- **System 1 (LLM Layer)**: Fast, intuitive reasoning using OpenAI GPT-4o
- **System 2 (Symbolic Logic)**: Rule-based verification and validation
- **Knowledge Graph**: Fact storage and relationship verification
- **Orchestration Layer**: Pipeline coordination and trace generation

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Infrastructure │
│   (React/TS)    │◄──►│   (FastAPI)     │◄──►│   (Docker)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  Reasoning      │
                       │  Pipeline       │
                       │                 │
                       │ • LLM Layer     │
                       │ • Symbolic      │
                       │ • Knowledge     │
                       │ • Orchestration │
                       └─────────────────┘
```

## 📁 Project Structure

```
xreason/
├── backend/                 # FastAPI backend service
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Data models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── tests/              # Backend tests
│   └── Dockerfile          # Backend container
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Frontend utilities
│   ├── public/             # Static assets
│   └── Dockerfile          # Frontend container
├── infrastructure/         # Infrastructure configs
│   ├── docker-compose.yml  # Local development
│   └── kubernetes/         # K8s manifests
├── docs/                   # Documentation
└── scripts/                # Utility scripts
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.9+ (3.9 recommended for Prolog compatibility)
- Node.js 18+
- OpenAI API key
- SWI-Prolog (for local development; automatically installed in Docker)

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd xreason
   ```

2. **Environment setup**:
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your OpenAI API key
   ```

3. **Start services**:
   ```bash
   ./scripts/start-xreason.sh
   # Or: docker-compose up -d
   ```

4. **Access services**:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs
   - **Observability:**
     - Prometheus: http://localhost:9090
     - Grafana: http://localhost:3002 (admin/xreason123)
     - Alertmanager: http://localhost:9093

## 🔧 Development

### Backend Development

```bash
cd backend

# Install SWI-Prolog (required for Prolog reasoning)
# macOS: brew install swi-prolog
# Ubuntu: sudo apt-get install swi-prolog
# Windows: Download from https://www.swi-prolog.org/Download.html

python3.9 -m venv venv  # Use Python 3.9 for Prolog compatibility
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

## 📊 Use Cases

### Healthcare (HIPAA Compliance)
- Policy engine for HIPAA compliance checks
- Example: "Is this access request compliant with HIPAA 164.312(a)(1)?"

### Finance (Mathematical Validation)
- Sanity checks for financial calculations
- Example: "If debt=100, equity=50, what is Debt-to-Equity ratio?"

## 📊 Observability & Monitoring

XReason includes a comprehensive observability stack with Prometheus, Grafana, and Alertmanager.

### Metrics Collected

- **Reasoning Metrics**: Request rates, response times, confidence scores
- **LLM Metrics**: API calls, token usage, model performance
- **Prolog Metrics**: Query execution times, success rates
- **Ruleset Metrics**: Execution times, validation results
- **System Metrics**: CPU, memory, active sessions
- **Business KPIs**: Success rates, error rates by domain

### Alerts Configured

- **Critical**: Service down, high error rates, LLM failures
- **Warning**: Slow response times, low confidence, high resource usage
- **Business**: Low success rates, no requests, high token usage

### Dashboard Features

- Real-time reasoning performance metrics
- Confidence score distributions
- Token usage tracking
- Error rate monitoring
- System health indicators

### Quick Start Observability

```bash
# Start all services including observability
./scripts/start-xreason.sh

# Or manually:
docker-compose up -d

# Access Grafana dashboard
# URL: http://localhost:3002
# Login: admin/xreason123
```

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📈 Success Metrics

- ✅ API responds in < 2s
- ✅ End-to-end reasoning trace is interpretable
- ✅ Domain pilot shows LLM errors caught by symbolic layer
- ✅ Positive feedback from vertical pilots

## 📝 API Documentation

The API documentation is available at `/docs` when the backend is running.

### Key Endpoints

- `POST /reason` - Main reasoning endpoint
- `GET /health` - Health check
- `GET /rules` - Available rule sets

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
