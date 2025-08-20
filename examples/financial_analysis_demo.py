#!/usr/bin/env python3
"""
Financial Analysis Demo for XReason
Demonstrates specialized financial compliance and risk analysis capabilities.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, List
import httpx
from decimal import Decimal


class FinancialAnalysisDemo:
    """Demo class for financial analysis capabilities."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.results = []
    
    async def run_demo(self):
        """Run the complete financial analysis demo."""
        print("🏦 XReason Financial Analysis Demo")
        print("=" * 50)
        print("Demonstrating specialized financial compliance and risk analysis")
        print()
        
        try:
            # Check service health
            await self.check_health()
            
            # Demo individual company analysis
            await self.demo_single_company_analysis()
            
            # Demo batch analysis
            await self.demo_batch_analysis()
            
            # Demo financial insights
            await self.demo_financial_insights()
            
            # Demo regulatory frameworks
            await self.demo_regulatory_frameworks()
            
            # Demo financial rules
            await self.demo_financial_rules()
            
            # Generate summary report
            await self.generate_summary_report()
            
        except Exception as e:
            print(f"❌ Demo failed: {e}")
        finally:
            await self.client.aclose()
    
    async def check_health(self):
        """Check financial analysis service health."""
        print("🔍 Checking Financial Analysis Service Health...")
        
        try:
            response = await self.client.get(f"{self.base_url}/api/v1/financial/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Service Status: {health_data['status']}")
                print(f"   Components: {health_data['components']}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check error: {e}")
        
        print()
    
    async def demo_single_company_analysis(self):
        """Demo single company financial analysis."""
        print("📊 Single Company Financial Analysis")
        print("-" * 40)
        
        # Example 1: High-risk company
        high_risk_company = {
            "company_id": "TECH_CORP_001",
            "revenue": Decimal("1000000"),
            "costs": Decimal("950000"),
            "debt": Decimal("2000000"),
            "equity": Decimal("500000"),
            "assets": Decimal("3000000"),
            "liabilities": Decimal("2500000"),
            "cash_flow": Decimal("50000"),
            "industry": "technology",
            "market_cap": Decimal("5000000"),
            "pe_ratio": Decimal("25.0")
        }
        
        print("Analyzing High-Risk Technology Company...")
        result1 = await self.analyze_company(high_risk_company)
        self.results.append(("High-Risk Tech", result1))
        
        # Example 2: Stable company
        stable_company = {
            "company_id": "STABLE_CORP_002",
            "revenue": Decimal("5000000"),
            "costs": Decimal("3500000"),
            "debt": Decimal("1000000"),
            "equity": Decimal("4000000"),
            "assets": Decimal("6000000"),
            "liabilities": Decimal("2000000"),
            "cash_flow": Decimal("800000"),
            "industry": "manufacturing",
            "market_cap": Decimal("20000000"),
            "pe_ratio": Decimal("15.0")
        }
        
        print("Analyzing Stable Manufacturing Company...")
        result2 = await self.analyze_company(stable_company)
        self.results.append(("Stable Manufacturing", result2))
        
        # Example 3: Financial institution
        financial_company = {
            "company_id": "BANK_CORP_003",
            "revenue": Decimal("10000000"),
            "costs": Decimal("7000000"),
            "debt": Decimal("50000000"),
            "equity": Decimal("20000000"),
            "assets": Decimal("100000000"),
            "liabilities": Decimal("80000000"),
            "cash_flow": Decimal("1500000"),
            "industry": "banking",
            "market_cap": Decimal("50000000"),
            "pe_ratio": Decimal("12.0")
        }
        
        print("Analyzing Financial Institution...")
        result3 = await self.analyze_company(financial_company)
        self.results.append(("Financial Institution", result3))
        
        print()
    
    async def analyze_company(self, company_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single company."""
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/financial/analyze",
                json=company_data
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Analysis completed for {company_data['company_id']}")
                print(f"      Risk Level: {result['risk_assessment']['overall_risk']}")
                print(f"      Risk Score: {result['risk_assessment']['risk_score']:.2f}")
                print(f"      Compliance: {result['risk_assessment']['compliance_status']}")
                print(f"      Financial Health: {result['risk_assessment']['financial_health']}")
                print(f"      Confidence: {result['risk_assessment']['confidence']:.2f}")
                
                # Show key metrics
                metrics = result['metrics']
                print(f"      Key Metrics:")
                print(f"        Profit Margin: {metrics['profit_margin']:.2%}")
                print(f"        Debt/Equity: {metrics['debt_to_equity']:.2f}")
                print(f"        Current Ratio: {metrics['current_ratio']:.2f}")
                print(f"        ROE: {metrics['roe']:.2%}")
                
                return result
            else:
                print(f"   ❌ Analysis failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"   ❌ Analysis error: {e}")
            return None
    
    async def demo_batch_analysis(self):
        """Demo batch financial analysis."""
        print("📈 Batch Financial Analysis")
        print("-" * 40)
        
        # Create multiple companies for batch analysis
        companies = [
            {
                "company_id": "STARTUP_001",
                "revenue": Decimal("500000"),
                "costs": Decimal("600000"),
                "debt": Decimal("300000"),
                "equity": Decimal("200000"),
                "assets": Decimal("800000"),
                "liabilities": Decimal("600000"),
                "cash_flow": Decimal("-50000"),
                "industry": "startup"
            },
            {
                "company_id": "GROWTH_002",
                "revenue": Decimal("2000000"),
                "costs": Decimal("1200000"),
                "debt": Decimal("800000"),
                "equity": Decimal("1500000"),
                "assets": Decimal("3000000"),
                "liabilities": Decimal("1500000"),
                "cash_flow": Decimal("300000"),
                "industry": "growth"
            },
            {
                "company_id": "MATURE_003",
                "revenue": Decimal("8000000"),
                "costs": Decimal("5600000"),
                "debt": Decimal("2000000"),
                "equity": Decimal("6000000"),
                "assets": Decimal("10000000"),
                "liabilities": Decimal("4000000"),
                "cash_flow": Decimal("1200000"),
                "industry": "mature"
            }
        ]
        
        batch_request = {
            "companies": companies,
            "analysis_type": "comprehensive"
        }
        
        try:
            response = await self.client.post(
                f"{self.base_url}/api/v1/financial/batch-analyze",
                json=batch_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Batch analysis completed")
                print(f"   Total Companies: {result['total_companies']}")
                print(f"   Successful: {result['successful_analyses']}")
                print(f"   Failed: {result['failed_analyses']}")
                print(f"   Success Rate: {result['summary']['success_rate']:.1%}")
                print(f"   Average Risk Score: {result['summary']['average_risk_score']:.2f}")
                
                compliance_dist = result['summary']['compliance_distribution']
                print(f"   Compliance Distribution:")
                print(f"     Compliant: {compliance_dist['compliant']}")
                print(f"     At Risk: {compliance_dist['at_risk']}")
                print(f"     Non-Compliant: {compliance_dist['non_compliant']}")
                
                self.results.append(("Batch Analysis", result))
            else:
                print(f"❌ Batch analysis failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Batch analysis error: {e}")
        
        print()
    
    async def demo_financial_insights(self):
        """Demo financial insights retrieval."""
        print("💡 Financial Insights")
        print("-" * 40)
        
        company_ids = ["TECH_CORP_001", "STABLE_CORP_002", "BANK_CORP_003"]
        
        for company_id in company_ids:
            try:
                response = await self.client.get(
                    f"{self.base_url}/api/v1/financial/insights/{company_id}",
                    params={"timeframe": "1y"}
                )
                
                if response.status_code == 200:
                    insights = response.json()
                    print(f"📊 Insights for {company_id}:")
                    print(f"   Trends: {insights['trends']}")
                    print(f"   Risk Alerts: {len(insights['risk_alerts'])} alerts")
                    
                    if insights['risk_alerts']:
                        for alert in insights['risk_alerts']:
                            print(f"     ⚠️  {alert}")
                else:
                    print(f"❌ Failed to get insights for {company_id}")
                    
            except Exception as e:
                print(f"❌ Error getting insights for {company_id}: {e}")
        
        print()
    
    async def demo_regulatory_frameworks(self):
        """Demo regulatory frameworks information."""
        print("📋 Regulatory Frameworks")
        print("-" * 40)
        
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/financial/regulatory-frameworks"
            )
            
            if response.status_code == 200:
                frameworks = response.json()
                print(f"✅ Available Frameworks: {frameworks['total_frameworks']}")
                
                for name, details in frameworks['frameworks'].items():
                    print(f"   📄 {details['name']}")
                    print(f"      Requirements: {len(details['requirements'])} items")
                    print(f"      Penalties: {details['penalties']}")
            else:
                print(f"❌ Failed to get frameworks: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error getting frameworks: {e}")
        
        print()
    
    async def demo_financial_rules(self):
        """Demo financial analysis rules."""
        print("📐 Financial Analysis Rules")
        print("-" * 40)
        
        try:
            response = await self.client.get(
                f"{self.base_url}/api/v1/financial/financial-rules"
            )
            
            if response.status_code == 200:
                rules = response.json()
                print(f"✅ Available Rules: {rules['total_rules']}")
                
                for name, details in rules['rules'].items():
                    print(f"   📊 {name.upper()}")
                    print(f"      Formula: {details['formula']}")
                    print(f"      Description: {details['description']}")
                    print(f"      Thresholds: {details['thresholds']}")
            else:
                print(f"❌ Failed to get rules: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error getting rules: {e}")
        
        print()
    
    async def generate_summary_report(self):
        """Generate a summary report of the demo."""
        print("📋 Financial Analysis Demo Summary")
        print("=" * 50)
        
        print(f"📊 Total Analyses: {len(self.results)}")
        
        if self.results:
            print("\n📈 Analysis Results:")
            for name, result in self.results:
                if result and 'risk_assessment' in result:
                    risk_assessment = result['risk_assessment']
                    print(f"   🏢 {name}:")
                    print(f"      Risk Level: {risk_assessment['overall_risk']}")
                    print(f"      Risk Score: {risk_assessment['risk_score']:.2f}")
                    print(f"      Compliance: {risk_assessment['compliance_status']}")
                    print(f"      Financial Health: {risk_assessment['financial_health']}")
        
        print("\n🎯 Key Capabilities Demonstrated:")
        print("   ✅ Individual company financial analysis")
        print("   ✅ Batch analysis for multiple companies")
        print("   ✅ Risk assessment and scoring")
        print("   ✅ Regulatory compliance analysis")
        print("   ✅ Financial health evaluation")
        print("   ✅ AI-powered recommendations")
        print("   ✅ Regulatory framework integration")
        print("   ✅ Financial metrics calculation")
        
        print("\n🚀 Next Steps:")
        print("   • Integrate with real financial data sources")
        print("   • Add historical trend analysis")
        print("   • Implement real-time monitoring")
        print("   • Add custom regulatory frameworks")
        print("   • Deploy to production environment")
        
        print("\n📚 Documentation:")
        print("   • API Docs: http://localhost:8000/docs")
        print("   • Financial Analysis: /api/v1/financial/*")
        print("   • Health Check: /api/v1/financial/health")


async def main():
    """Main demo function."""
    demo = FinancialAnalysisDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())
