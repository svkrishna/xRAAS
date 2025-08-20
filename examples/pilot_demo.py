#!/usr/bin/env python3
"""
XReason Pilot Demo Script
Demonstrates the legal compliance and scientific validation pilots.
"""

import asyncio
import json
from typing import Dict, Any

# Example texts for demonstration
LEGAL_TEXTS = {
    "gdpr_compliant": """
    Our privacy policy clearly states that we collect user data only with explicit consent.
    Users have the right to access their data, request deletion, and withdraw consent at any time.
    We implement data minimization principles and only collect necessary information for our services.
    In case of a data breach, we will notify affected users within 72 hours as required by GDPR.
    """,
    
    "gdpr_non_compliant": """
    We collect user data for marketing and analytics purposes.
    User information is stored indefinitely and may be shared with third parties.
    We use cookies to track user behavior across our website.
    """,
    
    "hipaa_compliant": """
    Our healthcare system implements comprehensive privacy and security safeguards.
    Protected Health Information (PHI) is encrypted and access is strictly controlled.
    We have established breach notification procedures and business associate agreements.
    All workforce members receive HIPAA training and sign confidentiality agreements.
    """,
    
    "hipaa_non_compliant": """
    Patient data is stored in our database for medical records.
    Healthcare providers can access patient information through our system.
    We maintain patient records for billing and treatment purposes.
    """,
    
    "contract_comprehensive": """
    This agreement may be terminated by either party with 30 days written notice.
    The parties agree to hold each other harmless and indemnify against any damages.
    All confidential information shared under this agreement shall remain proprietary.
    This agreement is governed by the laws of the State of California.
    """,
    
    "contract_basic": """
    This agreement covers the provision of services between the parties.
    Payment terms are net 30 days from invoice date.
    Services will be provided according to the specifications.
    """
}

SCIENTIFIC_TEXTS = {
    "math_correct": """
    The force is calculated using Newton's second law: F = m * a = 5 kg * 2 m/s² = 10 N.
    The kinetic energy is E = ½mv² = ½ * 2 kg * (3 m/s)² = 9 J.
    The pressure is P = F/A = 100 N / 0.01 m² = 10,000 Pa.
    """,
    
    "math_incorrect": """
    The force is calculated as F = m * a = 5 * 2 = 8 N.
    The kinetic energy is E = mv² = 2 * 3² = 18 J.
    The pressure is P = F * A = 100 * 0.01 = 1 Pa.
    """,
    
    "stats_valid": """
    We conducted a study with n=50 participants and found a correlation of r=0.65, p<0.01.
    The 95% confidence interval was [0.45, 0.85].
    Effect size was calculated using Cohen's d = 0.8, indicating a large effect.
    """,
    
    "stats_questionable": """
    With n=15 participants, we found r=0.9, p<0.05.
    The correlation was very strong and highly significant.
    Our results show a perfect relationship between variables.
    """,
    
    "methodology_sound": """
    We conducted a randomized controlled trial with 100 participants.
    Participants were randomly assigned to treatment and control groups.
    The study was double-blind with proper blinding of participants and researchers.
    We controlled for confounding variables and assessed internal validity.
    """,
    
    "methodology_weak": """
    We studied the effects of our treatment on participants.
    Participants were divided into groups based on availability.
    We observed the outcomes and recorded the results.
    The study showed positive effects of our treatment.
    """
}


async def demo_legal_compliance(client):
    """Demonstrate legal compliance analysis."""
    print("\n" + "="*60)
    print("LEGAL COMPLIANCE ANALYSIS DEMO")
    print("="*60)
    
    # GDPR Analysis
    print("\n📋 GDPR Compliance Analysis")
    print("-" * 40)
    
    gdpr_compliant = await client.analyze_gdpr_compliance(LEGAL_TEXTS["gdpr_compliant"])
    print(f"✅ Compliant Text: {'✓' if gdpr_compliant.is_compliant else '✗'}")
    print(f"   Confidence: {gdpr_compliant.confidence:.2f}")
    print(f"   Risk Score: {gdpr_compliant.risk_score:.2f}")
    print(f"   Violations: {len(gdpr_compliant.violations)}")
    
    gdpr_non_compliant = await client.analyze_gdpr_compliance(LEGAL_TEXTS["gdpr_non_compliant"])
    print(f"❌ Non-Compliant Text: {'✓' if gdpr_non_compliant.is_compliant else '✗'}")
    print(f"   Confidence: {gdpr_non_compliant.confidence:.2f}")
    print(f"   Risk Score: {gdpr_non_compliant.risk_score:.2f}")
    print(f"   Violations: {len(gdpr_non_compliant.violations)}")
    
    for violation in gdpr_non_compliant.violations:
        print(f"   - {violation.rule_name}: {violation.description}")
    
    # HIPAA Analysis
    print("\n🏥 HIPAA Compliance Analysis")
    print("-" * 40)
    
    hipaa_compliant = await client.analyze_hipaa_compliance(LEGAL_TEXTS["hipaa_compliant"])
    print(f"✅ Compliant Text: {'✓' if hipaa_compliant.is_compliant else '✗'}")
    print(f"   Confidence: {hipaa_compliant.confidence:.2f}")
    print(f"   Risk Score: {hipaa_compliant.risk_score:.2f}")
    
    hipaa_non_compliant = await client.analyze_hipaa_compliance(LEGAL_TEXTS["hipaa_non_compliant"])
    print(f"❌ Non-Compliant Text: {'✓' if hipaa_non_compliant.is_compliant else '✗'}")
    print(f"   Confidence: {hipaa_non_compliant.confidence:.2f}")
    print(f"   Risk Score: {hipaa_non_compliant.risk_score:.2f}")
    
    # Contract Analysis
    print("\n📄 Contract Analysis")
    print("-" * 40)
    
    contract_comprehensive = await client.analyze_contract(LEGAL_TEXTS["contract_comprehensive"])
    print(f"✅ Comprehensive Contract: {'✓' if contract_comprehensive.is_compliant else '✗'}")
    print(f"   Confidence: {contract_comprehensive.confidence:.2f}")
    print(f"   Risk Score: {contract_comprehensive.risk_score:.2f}")
    
    contract_basic = await client.analyze_contract(LEGAL_TEXTS["contract_basic"])
    print(f"⚠️ Basic Contract: {'✓' if contract_basic.is_compliant else '✗'}")
    print(f"   Confidence: {contract_basic.confidence:.2f}")
    print(f"   Risk Score: {contract_basic.risk_score:.2f}")
    
    for violation in contract_basic.violations:
        print(f"   - {violation.rule_name}: {violation.description}")


async def demo_scientific_validation(client):
    """Demonstrate scientific validation analysis."""
    print("\n" + "="*60)
    print("SCIENTIFIC VALIDATION ANALYSIS DEMO")
    print("="*60)
    
    # Mathematical Analysis
    print("\n🔢 Mathematical Consistency Analysis")
    print("-" * 40)
    
    math_correct = await client.analyze_mathematical_consistency(SCIENTIFIC_TEXTS["math_correct"])
    print(f"✅ Correct Math: {'✓' if math_correct.is_valid else '✗'}")
    print(f"   Confidence: {math_correct.confidence:.2f}")
    print(f"   Validity Score: {math_correct.validity_score:.2f}")
    
    math_incorrect = await client.analyze_mathematical_consistency(SCIENTIFIC_TEXTS["math_incorrect"])
    print(f"❌ Incorrect Math: {'✓' if math_incorrect.is_valid else '✗'}")
    print(f"   Confidence: {math_incorrect.confidence:.2f}")
    print(f"   Validity Score: {math_incorrect.validity_score:.2f}")
    
    for issue in math_incorrect.issues:
        print(f"   - {issue.issue_type}: {issue.description}")
    
    # Statistical Analysis
    print("\n📊 Statistical Validity Analysis")
    print("-" * 40)
    
    stats_valid = await client.analyze_statistical_validity(SCIENTIFIC_TEXTS["stats_valid"])
    print(f"✅ Valid Statistics: {'✓' if stats_valid.is_valid else '✗'}")
    print(f"   Confidence: {stats_valid.confidence:.2f}")
    print(f"   Validity Score: {stats_valid.validity_score:.2f}")
    
    stats_questionable = await client.analyze_statistical_validity(SCIENTIFIC_TEXTS["stats_questionable"])
    print(f"⚠️ Questionable Statistics: {'✓' if stats_questionable.is_valid else '✗'}")
    print(f"   Confidence: {stats_questionable.confidence:.2f}")
    print(f"   Validity Score: {stats_questionable.validity_score:.2f}")
    
    for issue in stats_questionable.issues:
        print(f"   - {issue.issue_type}: {issue.description}")
    
    # Methodology Analysis
    print("\n🔬 Research Methodology Analysis")
    print("-" * 40)
    
    methodology_sound = await client.analyze_research_methodology(SCIENTIFIC_TEXTS["methodology_sound"])
    print(f"✅ Sound Methodology: {'✓' if methodology_sound.is_valid else '✗'}")
    print(f"   Confidence: {methodology_sound.confidence:.2f}")
    print(f"   Validity Score: {methodology_sound.validity_score:.2f}")
    
    methodology_weak = await client.analyze_research_methodology(SCIENTIFIC_TEXTS["methodology_weak"])
    print(f"❌ Weak Methodology: {'✓' if methodology_weak.is_valid else '✗'}")
    print(f"   Confidence: {methodology_weak.confidence:.2f}")
    print(f"   Validity Score: {methodology_weak.validity_score:.2f}")
    
    for issue in methodology_weak.issues:
        print(f"   - {issue.issue_type}: {issue.description}")


async def demo_comprehensive_analysis(client):
    """Demonstrate comprehensive analysis."""
    print("\n" + "="*60)
    print("COMPREHENSIVE ANALYSIS DEMO")
    print("="*60)
    
    # Combined legal and scientific analysis
    legal_text = LEGAL_TEXTS["gdpr_non_compliant"]
    scientific_text = SCIENTIFIC_TEXTS["stats_questionable"]
    
    print(f"\n📋 Legal Text: {legal_text[:100]}...")
    print(f"🔬 Scientific Text: {scientific_text[:100]}...")
    
    # Legal analysis
    legal_analyses = await client.analyze_legal_compliance(
        text=legal_text,
        domains=["gdpr", "hipaa", "contract"]
    )
    
    print("\n📊 Legal Analysis Results:")
    for domain, analysis in legal_analyses.items():
        status = "✓" if analysis.is_compliant else "✗"
        print(f"   {domain.upper()}: {status} (Risk: {analysis.risk_score:.2f})")
    
    # Scientific analysis
    scientific_analyses = await client.analyze_scientific_validity(
        text=scientific_text,
        domains=["mathematics", "statistics", "methodology"]
    )
    
    print("\n📊 Scientific Analysis Results:")
    for domain, analysis in scientific_analyses.items():
        status = "✓" if analysis.is_valid else "✗"
        print(f"   {domain.upper()}: {status} (Validity: {analysis.validity_score:.2f})")


async def demo_api_info(client):
    """Demonstrate API information endpoints."""
    print("\n" + "="*60)
    print("API INFORMATION DEMO")
    print("="*60)
    
    # Get available domains
    legal_domains = await client.get_legal_domains()
    scientific_domains = await client.get_scientific_domains()
    
    print("\n📋 Available Legal Domains:")
    for domain in legal_domains["domains"]:
        print(f"   - {domain['name']}: {domain['value']}")
    
    print("\n🔬 Available Scientific Domains:")
    for domain in scientific_domains["domains"]:
        print(f"   - {domain['name']}: {domain['value']}")
    
    # Get rules information
    legal_rules = await client.get_legal_rules()
    scientific_rules = await client.get_scientific_rules()
    
    print(f"\n📋 Legal Rules Available:")
    print(f"   - GDPR Rules: {len(legal_rules['gdpr_rules'])}")
    print(f"   - HIPAA Rules: {len(legal_rules['hipaa_rules'])}")
    print(f"   - Contract Rules: {len(legal_rules['contract_rules'])}")
    
    print(f"\n🔬 Scientific Rules Available:")
    print(f"   - Math Rules: {len(scientific_rules['math_rules'])}")
    print(f"   - Statistical Rules: {len(scientific_rules['statistical_rules'])}")
    print(f"   - Research Rules: {len(scientific_rules['research_rules'])}")


async def main():
    """Main demo function."""
    print("🚀 XReason Pilot Demo")
    print("="*60)
    
    # Import here to avoid circular imports
    from xreason_sdk import XReasonClient
    
    async with XReasonClient("http://localhost:8000") as client:
        # Check health
        try:
            health = await client.health_check()
            print(f"✅ API Health: {health.get('status', 'unknown')}")
        except Exception as e:
            print(f"❌ API Health Check Failed: {e}")
            return
        
        # Run demos
        await demo_legal_compliance(client)
        await demo_scientific_validation(client)
        await demo_comprehensive_analysis(client)
        await demo_api_info(client)
        
        print("\n" + "="*60)
        print("🎉 Demo Complete!")
        print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
