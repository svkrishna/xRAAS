# XReason Domain Pilots

XReason provides comprehensive domain-specific reasoning capabilities through specialized pilots. Each pilot is designed to handle industry-specific compliance, validation, and analysis requirements.

## Overview

The XReason platform includes the following domain pilots:

1. **Legal Compliance** - GDPR, HIPAA, CCPA, SOX, PCI DSS
2. **Scientific Validation** - Mathematical, Statistical, Physics, Chemistry, Biology, Computer Science, Engineering, Medicine, Psychology, Economics
3. **Healthcare Compliance** - HIPAA, FDA, Clinical Trials, Medical Devices, Quality Standards, Pharmacy, Laboratory, Emergency Medicine
4. **Finance Compliance** - Banking, Investment, AML/KYC, Basel, Financial Reporting, Insurance, Crypto, Fintech
5. **Manufacturing Compliance** - Quality Control, Safety Standards, Environmental, Supply Chain, ISO Standards, Lean Manufacturing, Automotive, Aerospace
6. **Cybersecurity Compliance** - Security Frameworks, Threat Detection, Incident Response, Data Protection

## Quick Start

### Using the SDK

```python
from xreason_sdk import XReasonClient

# Initialize client
client = XReasonClient(base_url="http://localhost:8000")

# Analyze legal compliance
legal_result = await client.analyze_gdpr_compliance(
    "Our company collects personal data for marketing purposes..."
)

# Analyze healthcare compliance
healthcare_result = await client.analyze_hipaa_compliance(
    "Our hospital stores patient medical records electronically..."
)

# Analyze finance compliance
finance_result = await client.analyze_banking_compliance(
    "Our bank maintains a capital adequacy ratio of 12%..."
)
```

### Using the API Directly

```bash
# Legal Compliance
curl -X POST "http://localhost:8000/api/v1/pilots/legal/gdpr" \
  -H "Content-Type: application/json" \
  -d '{"text": "Our company collects personal data...", "context": {}}'

# Healthcare Compliance
curl -X POST "http://localhost:8000/api/v1/pilots/healthcare/hipaa" \
  -H "Content-Type: application/json" \
  -d '{"text": "Our hospital stores patient records...", "context": {}}'

# Finance Compliance
curl -X POST "http://localhost:8000/api/v1/pilots/finance/banking" \
  -H "Content-Type: application/json" \
  -d '{"text": "Our bank maintains capital adequacy...", "context": {}}'
```

## Legal Compliance Pilot

### Supported Domains

- **GDPR** - General Data Protection Regulation
- **HIPAA** - Health Insurance Portability and Accountability Act
- **CCPA** - California Consumer Privacy Act
- **SOX** - Sarbanes-Oxley Act
- **PCI DSS** - Payment Card Industry Data Security Standard

### Example Usage

```python
# GDPR Analysis
gdpr_text = """
Our company collects personal data from users including names, email addresses, 
and browsing history. We use this data for marketing purposes and share it with 
third-party advertisers. Users can opt-out by clicking a link in our emails.
"""

result = await client.analyze_gdpr_compliance(gdpr_text)
print(f"Compliant: {result.is_compliant}")
print(f"Risk Score: {result.risk_score}")
print(f"Violations: {len(result.violations)}")

# HIPAA Analysis
hipaa_text = """
Our hospital stores patient medical records electronically. We have basic 
password protection and occasionally share patient information with insurance 
companies for billing purposes.
"""

result = await client.analyze_hipaa_compliance(hipaa_text)
print(f"Compliant: {result.is_compliant}")
print(f"Risk Score: {result.risk_score}")
```

### API Endpoints

- `POST /api/v1/pilots/legal/gdpr` - GDPR compliance analysis
- `POST /api/v1/pilots/legal/hipaa` - HIPAA compliance analysis
- `POST /api/v1/pilots/legal/ccpa` - CCPA compliance analysis
- `POST /api/v1/pilots/legal/sox` - SOX compliance analysis
- `POST /api/v1/pilots/legal/pci-dss` - PCI DSS compliance analysis
- `POST /api/v1/pilots/legal/comprehensive` - Comprehensive legal analysis

## Scientific Validation Pilot

### Supported Domains

- **Mathematics** - Mathematical consistency and formula validation
- **Statistics** - Statistical validity and methodology checks
- **Physics** - Physical laws and conservation principles
- **Chemistry** - Chemical reactions and molecular structures
- **Biology** - Biological processes and scientific methodology
- **Computer Science** - Algorithm analysis and computational complexity
- **Engineering** - Engineering principles and design validation
- **Medicine** - Medical research and clinical trial validation
- **Psychology** - Psychological research methodology
- **Economics** - Economic models and financial calculations

### Example Usage

```python
# Mathematical Analysis
math_text = """
In our study, we calculated the correlation coefficient between variables A and B.
We found r = 0.85, which indicates a strong positive correlation. The p-value was 
0.001, which is statistically significant at the 0.05 level.
"""

result = await client.analyze_mathematical_consistency(math_text)
print(f"Valid: {result.is_valid}")
print(f"Validity Score: {result.validity_score}")

# Statistical Analysis
stats_text = """
We conducted a study with 15 participants and used a t-test to compare means.
The sample size was adequate for our analysis. We found a significant difference
with p < 0.05, indicating strong evidence against the null hypothesis.
"""

result = await client.analyze_statistical_validity(stats_text)
print(f"Valid: {result.is_valid}")
print(f"Validity Score: {result.validity_score}")
```

### API Endpoints

- `POST /api/v1/pilots/scientific/mathematics` - Mathematical consistency analysis
- `POST /api/v1/pilots/scientific/statistics` - Statistical validity analysis
- `POST /api/v1/pilots/scientific/physics` - Physics validation analysis
- `POST /api/v1/pilots/scientific/chemistry` - Chemistry validation analysis
- `POST /api/v1/pilots/scientific/biology` - Biology validation analysis
- `POST /api/v1/pilots/scientific/computer-science` - Computer science validation analysis
- `POST /api/v1/pilots/scientific/engineering` - Engineering validation analysis
- `POST /api/v1/pilots/scientific/medicine` - Medicine validation analysis
- `POST /api/v1/pilots/scientific/psychology` - Psychology validation analysis
- `POST /api/v1/pilots/scientific/economics` - Economics validation analysis
- `POST /api/v1/pilots/scientific/comprehensive` - Comprehensive scientific analysis

## Healthcare Compliance Pilot

### Supported Domains

- **HIPAA** - Health Insurance Portability and Accountability Act
- **FDA** - Food and Drug Administration regulations
- **Clinical Trials** - Clinical trial compliance and methodology
- **Medical Devices** - Medical device regulations and safety
- **Quality Standards** - Healthcare quality and safety standards
- **Pharmacy** - Pharmaceutical regulations and dispensing
- **Laboratory** - Laboratory safety and quality standards
- **Emergency Medicine** - Emergency medical procedures and protocols

### Example Usage

```python
# HIPAA Analysis
hipaa_text = """
Our medical practice stores patient health information in electronic health records.
We have implemented basic security measures including passwords and regular backups.
Staff members have access to patient records for treatment purposes.
"""

result = await client.analyze_hipaa_compliance(hipaa_text)
print(f"Compliant: {result.is_compliant}")
print(f"Risk Score: {result.risk_score}")

# FDA Analysis
fda_text = """
Our pharmaceutical company is developing a new drug for diabetes treatment.
We have completed Phase I clinical trials and are preparing for Phase II.
The drug has shown promising results in animal studies.
"""

result = await client.analyze_fda_compliance(fda_text)
print(f"Compliant: {result.is_compliant}")
print(f"Risk Score: {result.risk_score}")
```

### API Endpoints

- `POST /api/v1/pilots/healthcare/hipaa` - HIPAA compliance analysis
- `POST /api/v1/pilots/healthcare/fda` - FDA compliance analysis
- `POST /api/v1/pilots/healthcare/clinical-trials` - Clinical trial compliance analysis
- `POST /api/v1/pilots/healthcare/medical-devices` - Medical device compliance analysis
- `POST /api/v1/pilots/healthcare/quality-standards` - Quality standards analysis
- `POST /api/v1/pilots/healthcare/pharmacy` - Pharmacy compliance analysis
- `POST /api/v1/pilots/healthcare/laboratory` - Laboratory compliance analysis
- `POST /api/v1/pilots/healthcare/emergency-medicine` - Emergency medicine compliance analysis
- `POST /api/v1/pilots/healthcare/comprehensive` - Comprehensive healthcare analysis

## Finance Compliance Pilot

### Supported Domains

- **Banking** - Banking regulations and capital requirements
- **Investment** - Investment regulations and portfolio management
- **AML/KYC** - Anti-Money Laundering and Know Your Customer
- **Basel** - Basel Committee on Banking Supervision standards
- **Financial Reporting** - Financial reporting and disclosure requirements
- **Insurance** - Insurance regulations and risk management
- **Crypto** - Cryptocurrency and blockchain regulations
- **Fintech** - Financial technology regulations and compliance

### Example Usage

```python
# Banking Analysis
banking_text = """
Our bank maintains a capital adequacy ratio of 12% and has implemented
basic risk management procedures. We monitor liquidity on a monthly basis
and have established lending standards for our customers.
"""

result = await client.analyze_banking_compliance(banking_text)
print(f"Compliant: {result.is_compliant}")
print(f"Risk Score: {result.risk_score}")

# AML/KYC Analysis
aml_text = """
Our financial institution has implemented customer identification procedures
and monitors transactions for suspicious activity. We file reports when
we detect unusual patterns in customer behavior.
"""

result = await client.analyze_aml_kyc_compliance(aml_text)
print(f"Compliant: {result.is_compliant}")
print(f"Risk Score: {result.risk_score}")
```

### API Endpoints

- `POST /api/v1/pilots/finance/banking` - Banking compliance analysis
- `POST /api/v1/pilots/finance/investment` - Investment compliance analysis
- `POST /api/v1/pilots/finance/aml-kyc` - AML/KYC compliance analysis
- `POST /api/v1/pilots/finance/basel` - Basel compliance analysis
- `POST /api/v1/pilots/finance/financial-reporting` - Financial reporting analysis
- `POST /api/v1/pilots/finance/insurance` - Insurance compliance analysis
- `POST /api/v1/pilots/finance/crypto` - Crypto compliance analysis
- `POST /api/v1/pilots/finance/fintech` - Fintech compliance analysis
- `POST /api/v1/pilots/finance/comprehensive` - Comprehensive finance analysis

## Manufacturing Compliance Pilot

### Supported Domains

- **Quality Control** - Quality management and control procedures
- **Safety Standards** - Workplace safety and occupational health
- **Environmental** - Environmental compliance and sustainability
- **Supply Chain** - Supply chain management and traceability
- **ISO Standards** - International Organization for Standardization
- **Lean Manufacturing** - Lean manufacturing principles and practices
- **Automotive** - Automotive industry standards and regulations
- **Aerospace** - Aerospace industry standards and safety

### Example Usage

```python
# Quality Control Analysis
quality_text = """
Our manufacturing facility has implemented basic quality control procedures
including inspection of finished products and documentation of processes.
We maintain records of our quality control activities.
"""

result = await client.analyze_quality_control(quality_text)
print(f"Compliant: {result.is_compliant}")
print(f"Risk Score: {result.risk_score}")

# Safety Standards Analysis
safety_text = """
Our factory has basic safety measures including safety signs and
personal protective equipment for workers. We conduct safety training
annually and have emergency procedures in place.
"""

result = await client.analyze_safety_standards(safety_text)
print(f"Compliant: {result.is_compliant}")
print(f"Risk Score: {result.risk_score}")
```

### API Endpoints

- `POST /api/v1/pilots/manufacturing/quality-control` - Quality control analysis
- `POST /api/v1/pilots/manufacturing/safety-standards` - Safety standards analysis
- `POST /api/v1/pilots/manufacturing/environmental` - Environmental compliance analysis
- `POST /api/v1/pilots/manufacturing/supply-chain` - Supply chain analysis
- `POST /api/v1/pilots/manufacturing/iso-standards` - ISO standards analysis
- `POST /api/v1/pilots/manufacturing/lean-manufacturing` - Lean manufacturing analysis
- `POST /api/v1/pilots/manufacturing/automotive` - Automotive standards analysis
- `POST /api/v1/pilots/manufacturing/aerospace` - Aerospace standards analysis
- `POST /api/v1/pilots/manufacturing/comprehensive` - Comprehensive manufacturing analysis

## Cybersecurity Compliance Pilot

### Supported Domains

- **Security Frameworks** - Security frameworks and best practices
- **Threat Detection** - Threat detection and monitoring systems
- **Incident Response** - Incident response and recovery procedures
- **Data Protection** - Data protection and privacy measures

### Example Usage

```python
# Security Frameworks Analysis
security_text = """
Our organization has implemented basic cybersecurity measures including
firewalls and antivirus software. We have a security policy in place
and conduct regular security assessments.
"""

result = await client.analyze_security_frameworks(security_text)
print(f"Compliant: {result.is_compliant}")
print(f"Risk Score: {result.risk_score}")
```

### API Endpoints

- `POST /api/v1/pilots/cybersecurity/security-frameworks` - Security frameworks analysis
- `POST /api/v1/pilots/cybersecurity/threat-detection` - Threat detection analysis
- `POST /api/v1/pilots/cybersecurity/incident-response` - Incident response analysis
- `POST /api/v1/pilots/cybersecurity/data-protection` - Data protection analysis
- `POST /api/v1/pilots/cybersecurity/comprehensive` - Comprehensive cybersecurity analysis

## Running the Comprehensive Demo

To run a comprehensive demo of all pilots:

```bash
# Run the comprehensive demo
./scripts/run-comprehensive-demo.sh

# Or run manually
python examples/comprehensive_pilot_demo.py
```

The demo will:
1. Test all domain pilots with realistic examples
2. Generate compliance/validity reports
3. Save detailed results to a JSON file
4. Provide a summary of all analyses

## Response Models

All pilot endpoints return structured responses with the following common fields:

### Compliance Analysis Response
```json
{
  "is_compliant": true,
  "confidence": 0.85,
  "risk_score": 0.15,
  "violations": [
    {
      "rule_id": "gdpr_consent",
      "rule_name": "Consent Requirement",
      "severity": "high",
      "description": "Missing explicit consent mechanism",
      "evidence": "No consent checkbox found",
      "recommendation": "Implement explicit consent mechanism",
      "article_reference": "GDPR Article 7",
      "penalty_info": "Up to €20 million or 4% of global revenue"
    }
  ],
  "recommendations": [
    "Implement explicit consent mechanism",
    "Add data minimization practices"
  ],
  "analysis_timestamp": "2024-01-15T10:30:00Z",
  "processing_time_ms": 1250
}
```

### Validation Analysis Response
```json
{
  "is_valid": true,
  "confidence": 0.92,
  "validity_score": 0.88,
  "issues": [
    {
      "issue_type": "statistical_power",
      "severity": "medium",
      "description": "Sample size may be insufficient",
      "evidence": "n=15 participants",
      "recommendation": "Increase sample size to at least 30 participants"
    }
  ],
  "recommendations": [
    "Increase sample size",
    "Use effect size calculations"
  ],
  "analysis_timestamp": "2024-01-15T10:30:00Z",
  "processing_time_ms": 980
}
```

## Error Handling

All pilot endpoints handle errors gracefully and return appropriate HTTP status codes:

- `200 OK` - Analysis completed successfully
- `400 Bad Request` - Invalid input data
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server-side errors

Error responses include detailed error messages:

```json
{
  "detail": "Analysis failed: Invalid text input",
  "error_code": "INVALID_INPUT",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Performance Considerations

- **Response Time**: Most analyses complete within 1-3 seconds
- **Concurrent Requests**: The system supports multiple concurrent requests
- **Caching**: Results are cached for identical inputs
- **Rate Limiting**: API endpoints include rate limiting for production use

## Monitoring and Observability

All pilot endpoints are monitored with:
- Request/response metrics
- Processing time tracking
- Error rate monitoring
- Domain-specific KPIs

View metrics at: http://localhost:3002 (Grafana)

## Extending Pilots

To add new rules or domains to existing pilots:

1. **Add Rules**: Update the rule loading methods in the pilot classes
2. **Add Domains**: Extend the domain enums and add corresponding analysis methods
3. **Update API**: Add new endpoints in `backend/app/api/pilots.py`
4. **Update SDK**: Add corresponding methods in the SDK client
5. **Test**: Run the comprehensive demo to verify functionality

## Support

For questions or issues with the pilots:
- Check the API documentation at http://localhost:8000/docs
- Review the comprehensive demo examples
- Check the logs: `docker-compose logs backend`
- Monitor metrics at http://localhost:3002
