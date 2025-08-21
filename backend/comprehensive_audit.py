#!/usr/bin/env python3
"""
Comprehensive XReason Application Audit
Tests all components and identifies any issues or missing features.
"""

import os
import sys
import asyncio
import importlib
from typing import Dict, List, Any, Optional
from datetime import datetime

# Set required environment variables
os.environ["OPENAI_API_KEY"] = "sk-demo-key-for-testing"
os.environ["SECRET_KEY"] = "dev-secret-key-for-testing-only"

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class AuditResult:
    def __init__(self, component: str, status: str, details: str = "", errors: List[str] = None):
        self.component = component
        self.status = status  # "PASS", "FAIL", "WARNING", "SKIP"
        self.details = details
        self.errors = errors or []
        self.timestamp = datetime.utcnow()

class XReasonAuditor:
    def __init__(self):
        self.results: List[AuditResult] = []
        self.issues_found = 0
        self.warnings_found = 0
        
    def add_result(self, result: AuditResult):
        self.results.append(result)
        if result.status == "FAIL":
            self.issues_found += 1
        elif result.status == "WARNING":
            self.warnings_found += 1
    
    def test_core_imports(self) -> None:
        """Test core module imports."""
        print("🔍 Testing core imports...")
        
        core_modules = [
            "app.core.config",
            "app.models.base",
            "app.models.auth",
            "app.models.reasoning",
            "app.models.reasoning_graph",
            "app.models.rulesets",
            "app.models.agent"
        ]
        
        for module_name in core_modules:
            try:
                importlib.import_module(module_name)
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="PASS",
                    details="Module imported successfully"
                ))
            except Exception as e:
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="FAIL",
                    details=f"Failed to import module",
                    errors=[str(e)]
                ))
    
    def test_service_imports(self) -> None:
        """Test service module imports."""
        print("🔍 Testing service imports...")
        
        service_modules = [
            "app.services.llm_service",
            "app.services.symbolic_service",
            "app.services.knowledge_service",
            "app.services.orchestration_service",
            "app.services.reasoning_graph_service",
            "app.services.ruleset_service",
            "app.services.metrics_service",
            "app.services.ai_agent_service",
            "app.services.auth_service",
            "app.services.rbac_service",
            "app.services.financial_analysis_service",
            "app.services.ruleset_registry"
        ]
        
        for module_name in service_modules:
            try:
                importlib.import_module(module_name)
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="PASS",
                    details="Service imported successfully"
                ))
            except Exception as e:
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="FAIL",
                    details=f"Failed to import service",
                    errors=[str(e)]
                ))
    
    def test_api_imports(self) -> None:
        """Test API module imports."""
        print("🔍 Testing API imports...")
        
        api_modules = [
            "app.api.health",
            "app.api.metrics",
            "app.api.reasoning",
            "app.api.rulesets",
            "app.api.reasoning_graphs",
            "app.api.pilots",
            "app.api.agents",
            "app.api.financial_analysis",
            "app.api.auth",
            "app.api.commercial"
        ]
        
        for module_name in api_modules:
            try:
                importlib.import_module(module_name)
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="PASS",
                    details="API module imported successfully"
                ))
            except Exception as e:
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="FAIL",
                    details=f"Failed to import API module",
                    errors=[str(e)]
                ))
    
    def test_pilot_imports(self) -> None:
        """Test pilot module imports."""
        print("🔍 Testing pilot imports...")
        
        pilot_modules = [
            "app.pilots.cybersecurity_compliance",
            "app.pilots.finance_compliance",
            "app.pilots.healthcare_compliance",
            "app.pilots.legal_compliance",
            "app.pilots.manufacturing_compliance",
            "app.pilots.scientific_validation"
        ]
        
        for module_name in pilot_modules:
            try:
                importlib.import_module(module_name)
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="PASS",
                    details="Pilot imported successfully"
                ))
            except Exception as e:
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="FAIL",
                    details=f"Failed to import pilot",
                    errors=[str(e)]
                ))
    
    def test_security_imports(self) -> None:
        """Test security module imports."""
        print("🔍 Testing security imports...")
        
        security_modules = [
            "app.security.audit_logger",
            "app.security.encryption_service",
            "app.security.access_control",
            "app.security.data_classification"
        ]
        
        for module_name in security_modules:
            try:
                importlib.import_module(module_name)
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="PASS",
                    details="Security module imported successfully"
                ))
            except Exception as e:
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="FAIL",
                    details=f"Failed to import security module",
                    errors=[str(e)]
                ))
    
    def test_reliability_imports(self) -> None:
        """Test reliability module imports."""
        print("🔍 Testing reliability imports...")
        
        reliability_modules = [
            "app.reliability.disaster_recovery",
            "app.reliability.health_monitor",
            "app.reliability.circuit_breaker",
            "app.reliability.sla_manager"
        ]
        
        for module_name in reliability_modules:
            try:
                importlib.import_module(module_name)
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="PASS",
                    details="Reliability module imported successfully"
                ))
            except Exception as e:
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="FAIL",
                    details=f"Failed to import reliability module",
                    errors=[str(e)]
                ))
    
    def test_commercial_imports(self) -> None:
        """Test commercial module imports."""
        print("🔍 Testing commercial imports...")
        
        commercial_modules = [
            "app.billing.usage_meter",
            "app.billing.billing_service",
            "app.billing.quota_manager",
            "app.marketplace.partner_registry",
            "app.marketplace.certification_manager",
            "app.marketplace.marketplace_api"
        ]
        
        for module_name in commercial_modules:
            try:
                importlib.import_module(module_name)
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="PASS",
                    details="Commercial module imported successfully"
                ))
            except Exception as e:
                self.add_result(AuditResult(
                    component=f"Import: {module_name}",
                    status="FAIL",
                    details=f"Failed to import commercial module",
                    errors=[str(e)]
                ))
    
    def test_schema_imports(self) -> None:
        """Test schema module imports."""
        print("🔍 Testing schema imports...")
        
        try:
            from app.schemas import reasoning, auth, agent, financial
            self.add_result(AuditResult(
                component="Import: app.schemas",
                status="PASS",
                details="Schema modules imported successfully"
            ))
        except Exception as e:
            self.add_result(AuditResult(
                component="Import: app.schemas",
                status="FAIL",
                details="Failed to import schema modules",
                errors=[str(e)]
            ))
    
    def test_ruleset_imports(self) -> None:
        """Test ruleset imports."""
        print("🔍 Testing ruleset imports...")
        
        try:
            from app.rulesets import legal_gdpr, scientific_validation
            self.add_result(AuditResult(
                component="Import: app.rulesets",
                status="PASS",
                details="Ruleset modules imported successfully"
            ))
        except Exception as e:
            self.add_result(AuditResult(
                component="Import: app.rulesets",
                status="FAIL",
                details="Failed to import ruleset modules",
                errors=[str(e)]
            ))
    
    def test_main_app_import(self) -> None:
        """Test main application import."""
        print("🔍 Testing main app import...")
        
        try:
            from app.main import app
            self.add_result(AuditResult(
                component="Import: app.main",
                status="PASS",
                details="Main application imported successfully"
            ))
        except Exception as e:
            self.add_result(AuditResult(
                component="Import: app.main",
                status="FAIL",
                details="Failed to import main application",
                errors=[str(e)]
            ))
    
    def test_dependencies(self) -> None:
        """Test critical dependencies."""
        print("🔍 Testing dependencies...")
        
        critical_deps = [
            "fastapi",
            "uvicorn",
            "sqlmodel",
            "pydantic",
            "openai",
            "networkx",
            "matplotlib",
            "plotly",
            "prometheus_client",
            "cryptography",
            "passlib",
            "python-jose",
            "PyJWT",
            "psutil",
            "requests"
        ]
        
        for dep in critical_deps:
            try:
                importlib.import_module(dep.replace("-", "_"))
                self.add_result(AuditResult(
                    component=f"Dependency: {dep}",
                    status="PASS",
                    details="Dependency available"
                ))
            except ImportError:
                self.add_result(AuditResult(
                    component=f"Dependency: {dep}",
                    status="FAIL",
                    details="Dependency not available",
                    errors=[f"Module {dep} not found"]
                ))
    
    def test_optional_dependencies(self) -> None:
        """Test optional dependencies."""
        print("🔍 Testing optional dependencies...")
        
        optional_deps = [
            "pyswip",  # Prolog integration
            "z3",      # Z3 solver
            "graphviz" # Graph visualization
        ]
        
        for dep in optional_deps:
            try:
                importlib.import_module(dep)
                self.add_result(AuditResult(
                    component=f"Optional: {dep}",
                    status="PASS",
                    details="Optional dependency available"
                ))
            except ImportError:
                self.add_result(AuditResult(
                    component=f"Optional: {dep}",
                    status="WARNING",
                    details="Optional dependency not available",
                    errors=[f"Module {dep} not found - some features may be limited"]
                ))
    
    def check_file_structure(self) -> None:
        """Check if all expected files exist."""
        print("🔍 Checking file structure...")
        
        expected_files = [
            "app/main.py",
            "app/__init__.py",
            "app/core/config.py",
            "app/models/__init__.py",
            "app/services/__init__.py",
            "app/api/__init__.py",
            "app/pilots/__init__.py",
            "app/security/__init__.py",
            "app/reliability/__init__.py",
            "app/billing/__init__.py",
            "app/marketplace/__init__.py",
            "app/schemas/__init__.py",
            "app/rulesets/__init__.py",
            "requirements.txt",
            "Dockerfile"
        ]
        
        for file_path in expected_files:
            if os.path.exists(file_path):
                self.add_result(AuditResult(
                    component=f"File: {file_path}",
                    status="PASS",
                    details="File exists"
                ))
            else:
                self.add_result(AuditResult(
                    component=f"File: {file_path}",
                    status="FAIL",
                    details="File missing",
                    errors=[f"Expected file {file_path} not found"]
                ))
    
    def check_configuration(self) -> None:
        """Check configuration settings."""
        print("🔍 Checking configuration...")
        
        try:
            from app.core.config import settings
            
            required_settings = [
                "openai_api_key",
                "secret_key",
                "algorithm",
                "access_token_expire_minutes"
            ]
            
            for setting in required_settings:
                if hasattr(settings, setting):
                    self.add_result(AuditResult(
                        component=f"Config: {setting}",
                        status="PASS",
                        details="Configuration setting available"
                    ))
                else:
                    self.add_result(AuditResult(
                        component=f"Config: {setting}",
                        status="FAIL",
                        details="Configuration setting missing",
                        errors=[f"Setting {setting} not found in config"]
                    ))
                    
        except Exception as e:
            self.add_result(AuditResult(
                component="Configuration",
                status="FAIL",
                details="Failed to load configuration",
                errors=[str(e)]
            ))
    
    def run_comprehensive_audit(self) -> Dict[str, Any]:
        """Run the complete audit."""
        print("🚀 Starting XReason Comprehensive Audit...")
        print("=" * 60)
        
        # Run all audit tests
        self.test_core_imports()
        self.test_service_imports()
        self.test_api_imports()
        self.test_pilot_imports()
        self.test_security_imports()
        self.test_reliability_imports()
        self.test_commercial_imports()
        self.test_schema_imports()
        self.test_ruleset_imports()
        self.test_main_app_import()
        self.test_dependencies()
        self.test_optional_dependencies()
        self.check_file_structure()
        self.check_configuration()
        
        # Generate summary
        summary = {
            "total_tests": len(self.results),
            "passed": len([r for r in self.results if r.status == "PASS"]),
            "failed": len([r for r in self.results if r.status == "FAIL"]),
            "warnings": len([r for r in self.results if r.status == "WARNING"]),
            "skipped": len([r for r in self.results if r.status == "SKIP"]),
            "results": self.results,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return summary
    
    def print_report(self, summary: Dict[str, Any]) -> None:
        """Print the audit report."""
        print("\n" + "=" * 60)
        print("📊 XREASON COMPREHENSIVE AUDIT REPORT")
        print("=" * 60)
        
        print(f"\n📈 Summary:")
        print(f"   Total Tests: {summary['total_tests']}")
        print(f"   ✅ Passed: {summary['passed']}")
        print(f"   ❌ Failed: {summary['failed']}")
        print(f"   ⚠️  Warnings: {summary['warnings']}")
        print(f"   ⏭️  Skipped: {summary['skipped']}")
        
        success_rate = (summary['passed'] / summary['total_tests'] * 100) if summary['total_tests'] > 0 else 0
        print(f"   📊 Success Rate: {success_rate:.1f}%")
        
        print(f"\n🔍 Detailed Results:")
        print("-" * 60)
        
        # Group results by status
        failed_results = [r for r in self.results if r.status == "FAIL"]
        warning_results = [r for r in self.results if r.status == "WARNING"]
        passed_results = [r for r in self.results if r.status == "PASS"]
        
        if failed_results:
            print(f"\n❌ FAILED TESTS ({len(failed_results)}):")
            for result in failed_results:
                print(f"   • {result.component}")
                print(f"     {result.details}")
                for error in result.errors:
                    print(f"     Error: {error}")
                print()
        
        if warning_results:
            print(f"\n⚠️  WARNINGS ({len(warning_results)}):")
            for result in warning_results:
                print(f"   • {result.component}: {result.details}")
                for error in result.errors:
                    print(f"     Note: {error}")
                print()
        
        if passed_results:
            print(f"\n✅ PASSED TESTS ({len(passed_results)}):")
            for result in passed_results:
                print(f"   • {result.component}: {result.details}")
        
        print("\n" + "=" * 60)
        
        if summary['failed'] == 0:
            print("🎉 All critical tests passed! XReason is ready for deployment.")
        else:
            print(f"⚠️  {summary['failed']} critical issues found. Please address before deployment.")
        
        if summary['warnings'] > 0:
            print(f"📝 {summary['warnings']} warnings found. Consider addressing for optimal functionality.")
        
        print("=" * 60)


def main():
    """Main audit function."""
    auditor = XReasonAuditor()
    
    try:
        summary = auditor.run_comprehensive_audit()
        auditor.print_report(summary)
        
        # Exit with appropriate code
        if summary['failed'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        print(f"❌ Audit failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
