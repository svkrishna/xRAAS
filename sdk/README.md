# XReason SDK

Python SDK for XReason Reasoning as a Service (RaaS) - a modular reasoning pipeline combining LLM intuition with symbolic/rule-based checks.

## Features

- **Core Reasoning API**: Perform reasoning on questions with explainable traces
- **Legal Compliance Analysis**: GDPR, HIPAA, and contract analysis
- **Scientific Validation**: Mathematical consistency, statistical validity, and research methodology
- **Async Support**: Full async/await support for high-performance applications
- **Type Safety**: Full type hints and Pydantic models
- **Error Handling**: Comprehensive error handling with custom exceptions

## Installation

```bash
pip install xreason-sdk
```

## Quick Start

### Basic Reasoning

```python
import asyncio
from xreason_sdk import XReasonClient

async def main():
    async with XReasonClient("http://localhost:8000") as client:
        # Perform reasoning
        response = await client.reason(
            question="What is the debt-to-equity ratio if debt=100 and equity=50?",
            domain="finance"
        )
        
        print(f"Answer: {response.answer}")
        print(f"Confidence: {response.confidence}")
        
        # Print reasoning trace
        for trace in response.reasoning_trace:
            print(f"{trace.stage}: {trace.output}")

asyncio.run(main())
```

### Legal Compliance Analysis

```python
import asyncio
from xreason_sdk import XReasonClient

async def main():
    async with XReasonClient("http://localhost:8000") as client:
        # Analyze GDPR compliance
        gdpr_analysis = await client.analyze_gdpr_compliance(
            text="We collect user data for marketing purposes..."
        )
        
        print(f"GDPR Compliant: {gdpr_analysis.is_compliant}")
        print(f"Risk Score: {gdpr_analysis.risk_score}")
        
        for violation in gdpr_analysis.violations:
            print(f"Violation: {violation.rule_name} - {violation.description}")
        
        # Analyze HIPAA compliance
        hipaa_analysis = await client.analyze_hipaa_compliance(
            text="Patient health information is stored securely..."
        )
        
        print(f"HIPAA Compliant: {hipaa_analysis.is_compliant}")

asyncio.run(main())
```

### Scientific Validation

```python
import asyncio
from xreason_sdk import XReasonClient

async def main():
    async with XReasonClient("http://localhost:8000") as client:
        # Analyze mathematical consistency
        math_analysis = await client.analyze_mathematical_consistency(
            text="The force is calculated as F = m * a = 5 * 2 = 10 N"
        )
        
        print(f"Mathematically Valid: {math_analysis.is_valid}")
        
        # Analyze statistical validity
        stats_analysis = await client.analyze_statistical_validity(
            text="With n=25 participants, we found r=0.8, p<0.05"
        )
        
        print(f"Statistically Valid: {stats_analysis.is_valid}")
        
        # Analyze research methodology
        methodology_analysis = await client.analyze_research_methodology(
            text="We conducted a randomized controlled trial with proper blinding..."
        )
        
        print(f"Methodologically Sound: {methodology_analysis.is_valid}")

asyncio.run(main())
```

### Comprehensive Analysis

```python
import asyncio
from xreason_sdk import XReasonClient

async def main():
    async with XReasonClient("http://localhost:8000") as client:
        # Comprehensive legal analysis
        legal_analyses = await client.analyze_legal_compliance(
            text="Our privacy policy states that we collect user data...",
            domains=["gdpr", "hipaa", "contract"]
        )
        
        for domain, analysis in legal_analyses.items():
            print(f"{domain.upper()}: {'✓' if analysis.is_compliant else '✗'}")
        
        # Comprehensive scientific analysis
        scientific_analyses = await client.analyze_scientific_validity(
            text="Our study used a sample of 30 participants...",
            domains=["mathematics", "statistics", "methodology"]
        )
        
        for domain, analysis in scientific_analyses.items():
            print(f"{domain.upper()}: {'✓' if analysis.is_valid else '✗'}")

asyncio.run(main())
```

## API Reference

### XReasonClient

The main client class for interacting with XReason API.

#### Constructor

```python
XReasonClient(
    base_url: str = "http://localhost:8000",
    api_key: Optional[str] = None,
    timeout: int = 30,
    max_retries: int = 3
)
```

#### Methods

##### Core Reasoning

- `reason(question, context=None, domain=None, ruleset_id=None)` - Perform reasoning
- `health_check()` - Check API health status

##### Legal Analysis

- `analyze_gdpr_compliance(text, context=None)` - Analyze GDPR compliance
- `analyze_hipaa_compliance(text, context=None)` - Analyze HIPAA compliance
- `analyze_contract(text, context=None)` - Analyze contract provisions
- `analyze_legal_compliance(text, domains=None, context=None)` - Comprehensive legal analysis

##### Scientific Analysis

- `analyze_mathematical_consistency(text, context=None)` - Analyze mathematical consistency
- `analyze_statistical_validity(text, context=None)` - Analyze statistical validity
- `analyze_research_methodology(text, context=None)` - Analyze research methodology
- `analyze_scientific_validity(text, domains=None, context=None)` - Comprehensive scientific analysis

##### Information

- `get_legal_domains()` - Get available legal domains
- `get_scientific_domains()` - Get available scientific domains
- `get_legal_rules()` - Get legal compliance rules
- `get_scientific_rules()` - Get scientific validation rules

## Error Handling

The SDK provides custom exceptions for different error types:

```python
from xreason_sdk import XReasonAPIError, XReasonValidationError

try:
    response = await client.reason(question="What is 2+2?")
except XReasonAPIError as e:
    print(f"API Error: {e.message} (Status: {e.status_code})")
except XReasonValidationError as e:
    print(f"Validation Error: {e}")
```

## Configuration

### Environment Variables

```bash
XREASON_API_URL=http://localhost:8000
XREASON_API_KEY=your_api_key_here
```

### Authentication

```python
# Using API key
client = XReasonClient(
    base_url="http://localhost:8000",
    api_key="your_api_key_here"
)
```

## Development

### Installation

```bash
git clone https://github.com/xreason/xreason-sdk.git
cd xreason-sdk
pip install -e .
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black xreason_sdk/
isort xreason_sdk/
```

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: https://xreason-sdk.readthedocs.io/
- Issues: https://github.com/xreason/xreason-sdk/issues
- Email: support@xreason.ai
