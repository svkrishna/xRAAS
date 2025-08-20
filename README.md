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
                       │ • AI Agents     │
                       └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │  AI Agents      │
                       │                 │
                       │ • Reasoning     │
                       │ • Knowledge     │
                       │ • Validation    │
                       │ • Memory        │
                       │ • Learning      │
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
│   │   ├── schemas/        # Pydantic schemas
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
├── examples/               # Demo and example scripts
├── scripts/                # Utility scripts
└── sdk/                    # Python SDK
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
   - **AI Agents:**
     - Agent Health: http://localhost:8000/api/v1/agents/health
     - Agent Status: http://localhost:8000/api/v1/agents/status

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

## 📊 Use Cases & Pilots

XReason provides comprehensive domain-specific reasoning capabilities through specialized pilots. Each pilot is designed to handle industry-specific compliance, validation, and analysis requirements.

### 🏛️ Legal Compliance Pilot
- **GDPR Compliance**: Analyze privacy policies and data handling practices
- **HIPAA Compliance**: Validate healthcare data protection measures  
- **CCPA Compliance**: California Consumer Privacy Act analysis
- **SOX Compliance**: Sarbanes-Oxley Act financial reporting
- **PCI DSS Compliance**: Payment card industry security standards
- **Example**: "Is this privacy policy compliant with GDPR Article 7?"

### 🔬 Scientific Validation Pilot
- **Mathematical Consistency**: Validate calculations and formulas
- **Statistical Validity**: Check statistical analysis and interpretations
- **Physics Validation**: Physical laws and conservation principles
- **Chemistry Validation**: Chemical reactions and molecular structures
- **Biology Validation**: Biological processes and scientific methodology
- **Computer Science**: Algorithm analysis and computational complexity
- **Engineering**: Engineering principles and design validation
- **Medicine**: Medical research and clinical trial validation
- **Psychology**: Psychological research methodology
- **Economics**: Economic models and financial calculations
- **Example**: "Is this statistical analysis methodologically sound?"

### 🏥 Healthcare Compliance Pilot
- **HIPAA Compliance**: Health Insurance Portability and Accountability Act
- **FDA Compliance**: Food and Drug Administration regulations
- **Clinical Trials**: Clinical trial compliance and methodology
- **Medical Devices**: Medical device regulations and safety
- **Quality Standards**: Healthcare quality and safety standards
- **Pharmacy**: Pharmaceutical regulations and dispensing
- **Laboratory**: Laboratory safety and quality standards
- **Emergency Medicine**: Emergency medical procedures and protocols
- **Example**: "Is this access request compliant with HIPAA 164.312(a)(1)?"

### 💰 Finance Compliance Pilot
- **Banking**: Banking regulations and capital requirements
- **Investment**: Investment regulations and portfolio management
- **AML/KYC**: Anti-Money Laundering and Know Your Customer
- **Basel**: Basel Committee on Banking Supervision standards
- **Financial Reporting**: Financial reporting and disclosure requirements
- **Insurance**: Insurance regulations and risk management
- **Crypto**: Cryptocurrency and blockchain regulations
- **Fintech**: Financial technology regulations and compliance
- **Example**: "If debt=100, equity=50, what is Debt-to-Equity ratio?"

### 🏭 Manufacturing Compliance Pilot
- **Quality Control**: Quality management and control procedures
- **Safety Standards**: Workplace safety and occupational health
- **Environmental**: Environmental compliance and sustainability
- **Supply Chain**: Supply chain management and traceability
- **ISO Standards**: International Organization for Standardization
- **Lean Manufacturing**: Lean manufacturing principles and practices
- **Automotive**: Automotive industry standards and regulations
- **Aerospace**: Aerospace industry standards and safety
- **Example**: "Does this manufacturing process meet ISO 9001 standards?"

### 🔒 Cybersecurity Compliance Pilot
- **Security Frameworks**: Security frameworks and best practices
- **Threat Detection**: Threat detection and monitoring systems
- **Incident Response**: Incident response and recovery procedures
- **Data Protection**: Data protection and privacy measures
- **Example**: "Is our security posture compliant with NIST Cybersecurity Framework?"

### 🚀 Comprehensive Demo

Run the comprehensive pilot demo to see all domains in action:

```bash
# Run comprehensive demo
./scripts/run-comprehensive-demo.sh

# Or run manually
python examples/comprehensive_pilot_demo.py
```

For detailed pilot documentation, see [docs/PILOTS.md](docs/PILOTS.md).

## 🤖 AI Agents

XReason includes advanced AI agents with intelligent reasoning, knowledge integration, and learning capabilities.

### Agent Types

- **🧠 Reasoning Agent**: Advanced logical reasoning and hypothesis generation
- **📚 Knowledge Agent**: Knowledge integration and discovery
- **✅ Validation Agent**: Fact checking and consistency validation
- **🧠 Memory System**: Short-term and long-term memory with pattern recognition
- **🎓 Learning System**: Adaptive learning and pattern recognition

### Quick Start

```bash
# Run AI agent demo
./scripts/run-ai-agent-demo.sh

# Or run manually
python examples/ai_agent_demo.py
```

### Example Usage

```python
import httpx
import asyncio

async def ai_agent_example():
    async with httpx.AsyncClient() as client:
        # Create session
        session_response = await client.post(
            "http://localhost:8000/api/v1/agents/sessions",
            json={"user_id": "user_001", "domain": "general"}
        )
        session_id = session_response.json()["session_id"]
        
        # Process with reasoning agent
        reasoning_response = await client.post(
            "http://localhost:8000/api/v1/agents/reasoning",
            json={
                "session_id": session_id,
                "input_data": {
                    "question": "What is the profit margin if revenue is $1M and costs are $600K?",
                    "context": "Financial analysis"
                }
            }
        )
        
        result = reasoning_response.json()
        print(f"Success: {result['success']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Reasoning: {result['reasoning']}")

asyncio.run(ai_agent_example())
```

For detailed AI agent documentation, see [docs/AI_AGENTS.md](docs/AI_AGENTS.md).

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
- ✅ Legal and scientific pilots demonstrate domain expertise
- ✅ SDK enables developer integration in <30 minutes

## 📝 API Documentation

The API documentation is available at `/docs` when the backend is running.

### Key Endpoints

- `POST /reason` - Main reasoning endpoint
- `GET /health` - Health check
- `GET /rules` - Available rule sets

### Pilot Endpoints

#### Legal Compliance
- `POST /api/v1/pilots/legal/gdpr` - GDPR compliance analysis
- `POST /api/v1/pilots/legal/hipaa` - HIPAA compliance analysis
- `POST /api/v1/pilots/legal/ccpa` - CCPA compliance analysis
- `POST /api/v1/pilots/legal/sox` - SOX compliance analysis
- `POST /api/v1/pilots/legal/pci-dss` - PCI DSS compliance analysis
- `POST /api/v1/pilots/legal/comprehensive` - Comprehensive legal analysis

#### Scientific Validation
- `POST /api/v1/pilots/scientific/mathematics` - Mathematical consistency
- `POST /api/v1/pilots/scientific/statistics` - Statistical validity
- `POST /api/v1/pilots/scientific/physics` - Physics validation
- `POST /api/v1/pilots/scientific/chemistry` - Chemistry validation
- `POST /api/v1/pilots/scientific/biology` - Biology validation
- `POST /api/v1/pilots/scientific/computer-science` - Computer science validation
- `POST /api/v1/pilots/scientific/engineering` - Engineering validation
- `POST /api/v1/pilots/scientific/medicine` - Medicine validation
- `POST /api/v1/pilots/scientific/psychology` - Psychology validation
- `POST /api/v1/pilots/scientific/economics` - Economics validation
- `POST /api/v1/pilots/scientific/comprehensive` - Comprehensive scientific analysis

#### Healthcare Compliance
- `POST /api/v1/pilots/healthcare/hipaa` - HIPAA compliance analysis
- `POST /api/v1/pilots/healthcare/fda` - FDA compliance analysis
- `POST /api/v1/pilots/healthcare/clinical-trials` - Clinical trial compliance
- `POST /api/v1/pilots/healthcare/medical-devices` - Medical device compliance
- `POST /api/v1/pilots/healthcare/quality-standards` - Quality standards analysis
- `POST /api/v1/pilots/healthcare/pharmacy` - Pharmacy compliance
- `POST /api/v1/pilots/healthcare/laboratory` - Laboratory compliance
- `POST /api/v1/pilots/healthcare/emergency-medicine` - Emergency medicine compliance
- `POST /api/v1/pilots/healthcare/comprehensive` - Comprehensive healthcare analysis

#### Finance Compliance
- `POST /api/v1/pilots/finance/banking` - Banking compliance analysis
- `POST /api/v1/pilots/finance/investment` - Investment compliance analysis
- `POST /api/v1/pilots/finance/aml-kyc` - AML/KYC compliance analysis
- `POST /api/v1/pilots/finance/basel` - Basel compliance analysis
- `POST /api/v1/pilots/finance/financial-reporting` - Financial reporting analysis
- `POST /api/v1/pilots/finance/insurance` - Insurance compliance analysis
- `POST /api/v1/pilots/finance/crypto` - Crypto compliance analysis
- `POST /api/v1/pilots/finance/fintech` - Fintech compliance analysis
- `POST /api/v1/pilots/finance/comprehensive` - Comprehensive finance analysis

#### Manufacturing Compliance
- `POST /api/v1/pilots/manufacturing/quality-control` - Quality control analysis
- `POST /api/v1/pilots/manufacturing/safety-standards` - Safety standards analysis
- `POST /api/v1/pilots/manufacturing/environmental` - Environmental compliance
- `POST /api/v1/pilots/manufacturing/supply-chain` - Supply chain analysis
- `POST /api/v1/pilots/manufacturing/iso-standards` - ISO standards analysis
- `POST /api/v1/pilots/manufacturing/lean-manufacturing` - Lean manufacturing analysis
- `POST /api/v1/pilots/manufacturing/automotive` - Automotive standards analysis
- `POST /api/v1/pilots/manufacturing/aerospace` - Aerospace standards analysis
- `POST /api/v1/pilots/manufacturing/comprehensive` - Comprehensive manufacturing analysis

#### Cybersecurity Compliance
- `POST /api/v1/pilots/cybersecurity/security-frameworks` - Security frameworks analysis
- `POST /api/v1/pilots/cybersecurity/threat-detection` - Threat detection analysis
- `POST /api/v1/pilots/cybersecurity/incident-response` - Incident response analysis
- `POST /api/v1/pilots/cybersecurity/data-protection` - Data protection analysis
- `POST /api/v1/pilots/cybersecurity/comprehensive` - Comprehensive cybersecurity analysis

### AI Agent Endpoints

#### Session Management
- `POST /api/v1/agents/sessions` - Create agent session
- `GET /api/v1/agents/sessions/{session_id}` - Get session info

#### Agent Processing
- `POST /api/v1/agents/process` - General agent processing
- `POST /api/v1/agents/reasoning` - Reasoning agent processing
- `POST /api/v1/agents/knowledge-integration` - Knowledge agent processing
- `POST /api/v1/agents/validation` - Validation agent processing

#### Memory & Learning
- `POST /api/v1/agents/memory` - Memory operations
- `POST /api/v1/agents/learning` - Learning operations
- `POST /api/v1/agents/knowledge` - Knowledge integration

#### System Monitoring
- `GET /api/v1/agents/status` - System status
- `GET /api/v1/agents/agents` - Agent statuses
- `GET /api/v1/agents/health` - Health check

## 🛠️ SDK & Development

### Python SDK

XReason provides a comprehensive Python SDK for easy integration:

```bash
pip install xreason-sdk
```

```python
import asyncio
from xreason_sdk import XReasonClient

async def main():
    async with XReasonClient("http://localhost:8000") as client:
        # Legal compliance analysis
        gdpr_analysis = await client.analyze_gdpr_compliance(
            text="We collect user data for marketing purposes..."
        )
        print(f"GDPR Compliant: {gdpr_analysis.is_compliant}")
        
        # Healthcare compliance analysis
        hipaa_analysis = await client.analyze_hipaa_compliance(
            text="Our hospital stores patient medical records electronically..."
        )
        print(f"HIPAA Compliant: {hipaa_analysis.is_compliant}")
        
        # Finance compliance analysis
        banking_analysis = await client.analyze_banking_compliance(
            text="Our bank maintains a capital adequacy ratio of 12%..."
        )
        print(f"Banking Compliant: {banking_analysis.is_compliant}")
        
        # Manufacturing compliance analysis
        quality_analysis = await client.analyze_quality_control(
            text="Our manufacturing facility has implemented quality control procedures..."
        )
        print(f"Quality Control Compliant: {quality_analysis.is_compliant}")
        
        # Cybersecurity compliance analysis
        security_analysis = await client.analyze_security_frameworks(
            text="Our organization has implemented cybersecurity measures..."
        )
        print(f"Security Compliant: {security_analysis.is_compliant}")
        
        # Scientific validation
        math_analysis = await client.analyze_mathematical_consistency(
            text="F = m * a = 5 * 2 = 10 N"
        )
        print(f"Mathematically Valid: {math_analysis.is_valid}")

asyncio.run(main())
```

### Demo Scripts

Run the demos to see the system in action:

```bash
# Setup development environment (first time only)
./scripts/setup-dev.sh

# Run the basic pilot demo
./scripts/run-demo.sh

# Run the comprehensive pilot demo (all pilots)
./scripts/run-comprehensive-demo.sh

# Run the AI agent demo
./scripts/run-ai-agent-demo.sh

# Or run directly with virtual environment
.venv/bin/python examples/pilot_demo.py
.venv/bin/python examples/comprehensive_pilot_demo.py
.venv/bin/python examples/ai_agent_demo.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
