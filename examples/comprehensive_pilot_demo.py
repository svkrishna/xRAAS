#!/usr/bin/env python3
"""
Comprehensive XReason Pilot Demo
Demonstrates all domain pilots with realistic examples.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Import the SDK
try:
    from xreason_sdk import XReasonClient
    from xreason_sdk.models import (
        LegalAnalysisRequest, ScientificAnalysisRequest,
        HealthcareAnalysisRequest, FinanceAnalysisRequest,
        ManufacturingAnalysisRequest, CybersecurityAnalysisRequest
    )
except ImportError:
    print("❌ XReason SDK not found. Please install it first:")
    print("   pip install -e ./sdk")
    exit(1)


class ComprehensivePilotDemo:
    """Comprehensive demo of all XReason pilots."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.client = XReasonClient(base_url=base_url)
        self.results = {}
    
    async def run_demo(self):
        """Run the comprehensive pilot demo."""
        print("🚀 XReason Comprehensive Pilot Demo")
        print("=" * 50)
        
        # Test health check first
        try:
            health = await self.client.health_check()
            print(f"✅ Health check passed: {health.get('status', 'unknown')}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            print("Make sure the XReason backend is running on http://localhost:8000")
            return
        
        print("\n" + "=" * 50)
        
        # Run all pilot demos
        await self.demo_legal_compliance()
        await self.demo_scientific_validation()
        await self.demo_healthcare_compliance()
        await self.demo_finance_compliance()
        await self.demo_manufacturing_compliance()
        await self.demo_cybersecurity_compliance()
        
        # Generate summary report
        self.generate_summary_report()
    
    async def demo_legal_compliance(self):
        """Demo legal compliance analysis."""
        print("\n⚖️  Legal Compliance Analysis")
        print("-" * 30)
        
        # GDPR Example
        gdpr_text = """
        Our company collects personal data from users including names, email addresses, 
        and browsing history. We use this data for marketing purposes and share it with 
        third-party advertisers. Users can opt-out by clicking a link in our emails.
        """
        
        print("📋 GDPR Compliance Analysis:")
        try:
            gdpr_analysis = await self.client.analyze_gdpr_compliance(gdpr_text)
            self.results['gdpr'] = gdpr_analysis
            print(f"   Compliance: {'✅' if gdpr_analysis.is_compliant else '❌'}")
            print(f"   Confidence: {gdpr_analysis.confidence:.2f}")
            print(f"   Risk Score: {gdpr_analysis.risk_score:.2f}")
            print(f"   Violations: {len(gdpr_analysis.violations)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # HIPAA Example
        hipaa_text = """
        Our hospital stores patient medical records electronically. We have basic 
        password protection and occasionally share patient information with insurance 
        companies for billing purposes.
        """
        
        print("\n📋 HIPAA Compliance Analysis:")
        try:
            hipaa_analysis = await self.client.analyze_hipaa_compliance(hipaa_text)
            self.results['hipaa'] = hipaa_analysis
            print(f"   Compliance: {'✅' if hipaa_analysis.is_compliant else '❌'}")
            print(f"   Confidence: {hipaa_analysis.confidence:.2f}")
            print(f"   Risk Score: {hipaa_analysis.risk_score:.2f}")
            print(f"   Violations: {len(hipaa_analysis.violations)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    async def demo_scientific_validation(self):
        """Demo scientific validation analysis."""
        print("\n🔬 Scientific Validation Analysis")
        print("-" * 30)
        
        # Mathematical Example
        math_text = """
        In our study, we calculated the correlation coefficient between variables A and B.
        We found r = 0.85, which indicates a strong positive correlation. The p-value was 
        0.001, which is statistically significant at the 0.05 level.
        """
        
        print("📊 Mathematical Analysis:")
        try:
            math_analysis = await self.client.analyze_mathematical_consistency(math_text)
            self.results['mathematics'] = math_analysis
            print(f"   Validity: {'✅' if math_analysis.is_valid else '❌'}")
            print(f"   Confidence: {math_analysis.confidence:.2f}")
            print(f"   Validity Score: {math_analysis.validity_score:.2f}")
            print(f"   Issues: {len(math_analysis.issues)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Statistical Example
        stats_text = """
        We conducted a study with 15 participants and used a t-test to compare means.
        The sample size was adequate for our analysis. We found a significant difference
        with p < 0.05, indicating strong evidence against the null hypothesis.
        """
        
        print("\n📊 Statistical Analysis:")
        try:
            stats_analysis = await self.client.analyze_statistical_validity(stats_text)
            self.results['statistics'] = stats_analysis
            print(f"   Validity: {'✅' if stats_analysis.is_valid else '❌'}")
            print(f"   Confidence: {stats_analysis.confidence:.2f}")
            print(f"   Validity Score: {stats_analysis.validity_score:.2f}")
            print(f"   Issues: {len(stats_analysis.issues)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    async def demo_healthcare_compliance(self):
        """Demo healthcare compliance analysis."""
        print("\n🏥 Healthcare Compliance Analysis")
        print("-" * 30)
        
        # HIPAA Example
        hipaa_text = """
        Our medical practice stores patient health information in electronic health records.
        We have implemented basic security measures including passwords and regular backups.
        Staff members have access to patient records for treatment purposes.
        """
        
        print("📋 HIPAA Compliance Analysis:")
        try:
            hipaa_analysis = await self.client.analyze_hipaa_compliance(hipaa_text)
            self.results['healthcare_hipaa'] = hipaa_analysis
            print(f"   Compliance: {'✅' if hipaa_analysis.is_compliant else '❌'}")
            print(f"   Confidence: {hipaa_analysis.confidence:.2f}")
            print(f"   Risk Score: {hipaa_analysis.risk_score:.2f}")
            print(f"   Violations: {len(hipaa_analysis.violations)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # FDA Example
        fda_text = """
        Our pharmaceutical company is developing a new drug for diabetes treatment.
        We have completed Phase I clinical trials and are preparing for Phase II.
        The drug has shown promising results in animal studies.
        """
        
        print("\n📋 FDA Compliance Analysis:")
        try:
            fda_analysis = await self.client.analyze_fda_compliance(fda_text)
            self.results['healthcare_fda'] = fda_analysis
            print(f"   Compliance: {'✅' if fda_analysis.is_compliant else '❌'}")
            print(f"   Confidence: {fda_analysis.confidence:.2f}")
            print(f"   Risk Score: {fda_analysis.risk_score:.2f}")
            print(f"   Violations: {len(fda_analysis.violations)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    async def demo_finance_compliance(self):
        """Demo finance compliance analysis."""
        print("\n💰 Finance Compliance Analysis")
        print("-" * 30)
        
        # Banking Example
        banking_text = """
        Our bank maintains a capital adequacy ratio of 12% and has implemented
        basic risk management procedures. We monitor liquidity on a monthly basis
        and have established lending standards for our customers.
        """
        
        print("📋 Banking Compliance Analysis:")
        try:
            banking_analysis = await self.client.analyze_banking_compliance(banking_text)
            self.results['finance_banking'] = banking_analysis
            print(f"   Compliance: {'✅' if banking_analysis.is_compliant else '❌'}")
            print(f"   Confidence: {banking_analysis.confidence:.2f}")
            print(f"   Risk Score: {banking_analysis.risk_score:.2f}")
            print(f"   Violations: {len(banking_analysis.violations)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # AML/KYC Example
        aml_text = """
        Our financial institution has implemented customer identification procedures
        and monitors transactions for suspicious activity. We file reports when
        we detect unusual patterns in customer behavior.
        """
        
        print("\n📋 AML/KYC Compliance Analysis:")
        try:
            aml_analysis = await self.client.analyze_aml_kyc_compliance(aml_text)
            self.results['finance_aml'] = aml_analysis
            print(f"   Compliance: {'✅' if aml_analysis.is_compliant else '❌'}")
            print(f"   Confidence: {aml_analysis.confidence:.2f}")
            print(f"   Risk Score: {aml_analysis.risk_score:.2f}")
            print(f"   Violations: {len(aml_analysis.violations)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    async def demo_manufacturing_compliance(self):
        """Demo manufacturing compliance analysis."""
        print("\n🏭 Manufacturing Compliance Analysis")
        print("-" * 30)
        
        # Quality Control Example
        quality_text = """
        Our manufacturing facility has implemented basic quality control procedures
        including inspection of finished products and documentation of processes.
        We maintain records of our quality control activities.
        """
        
        print("📋 Quality Control Analysis:")
        try:
            quality_analysis = await self.client.analyze_quality_control(quality_text)
            self.results['manufacturing_quality'] = quality_analysis
            print(f"   Compliance: {'✅' if quality_analysis.is_compliant else '❌'}")
            print(f"   Confidence: {quality_analysis.confidence:.2f}")
            print(f"   Risk Score: {quality_analysis.risk_score:.2f}")
            print(f"   Violations: {len(quality_analysis.violations)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        # Safety Standards Example
        safety_text = """
        Our factory has basic safety measures including safety signs and
        personal protective equipment for workers. We conduct safety training
        annually and have emergency procedures in place.
        """
        
        print("\n📋 Safety Standards Analysis:")
        try:
            safety_analysis = await self.client.analyze_safety_standards(safety_text)
            self.results['manufacturing_safety'] = safety_analysis
            print(f"   Compliance: {'✅' if safety_analysis.is_compliant else '❌'}")
            print(f"   Confidence: {safety_analysis.confidence:.2f}")
            print(f"   Risk Score: {safety_analysis.risk_score:.2f}")
            print(f"   Violations: {len(safety_analysis.violations)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    async def demo_cybersecurity_compliance(self):
        """Demo cybersecurity compliance analysis."""
        print("\n🔒 Cybersecurity Compliance Analysis")
        print("-" * 30)
        
        # Security Frameworks Example
        security_text = """
        Our organization has implemented basic cybersecurity measures including
        firewalls and antivirus software. We have a security policy in place
        and conduct regular security assessments.
        """
        
        print("📋 Security Frameworks Analysis:")
        try:
            security_analysis = await self.client.analyze_security_frameworks(security_text)
            self.results['cybersecurity_frameworks'] = security_analysis
            print(f"   Compliance: {'✅' if security_analysis.is_compliant else '❌'}")
            print(f"   Confidence: {security_analysis.confidence:.2f}")
            print(f"   Risk Score: {security_analysis.risk_score:.2f}")
            print(f"   Violations: {len(security_analysis.violations)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    def generate_summary_report(self):
        """Generate a summary report of all analyses."""
        print("\n" + "=" * 50)
        print("📊 COMPREHENSIVE ANALYSIS SUMMARY")
        print("=" * 50)
        
        total_analyses = len(self.results)
        compliant_analyses = sum(1 for r in self.results.values() if hasattr(r, 'is_compliant') and r.is_compliant)
        valid_analyses = sum(1 for r in self.results.values() if hasattr(r, 'is_valid') and r.is_valid)
        
        print(f"Total Analyses: {total_analyses}")
        print(f"Compliant: {compliant_analyses}")
        print(f"Valid: {valid_analyses}")
        print(f"Overall Success Rate: {((compliant_analyses + valid_analyses) / total_analyses * 100):.1f}%")
        
        print("\n📋 Detailed Results:")
        for name, result in self.results.items():
            if hasattr(result, 'is_compliant'):
                status = "✅ Compliant" if result.is_compliant else "❌ Non-Compliant"
                score = result.risk_score
            elif hasattr(result, 'is_valid'):
                status = "✅ Valid" if result.is_valid else "❌ Invalid"
                score = result.validity_score
            else:
                status = "❓ Unknown"
                score = 0.0
            
            print(f"   {name:25} | {status:15} | Score: {score:.2f}")
        
        # Save detailed results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_demo_results_{timestamp}.json"
        
        # Convert results to serializable format
        serializable_results = {}
        for name, result in self.results.items():
            if hasattr(result, 'dict'):
                serializable_results[name] = result.dict()
            else:
                serializable_results[name] = str(result)
        
        with open(filename, 'w') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        print(f"\n💾 Detailed results saved to: {filename}")
        print("\n🎉 Demo completed successfully!")


async def main():
    """Main demo function."""
    demo = ComprehensivePilotDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
