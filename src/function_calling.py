"""
Function Calling System - Test automation function registry and execution
"""

import random
import time
from typing import Dict, Callable, Optional


class FunctionRegistry:
    """
    Registry for test automation functions
    Supports keyword-based intent detection and function execution
    """
    
    def __init__(self):
        """Initialize function registry with test automation functions"""
        self.functions: Dict[str, Callable] = {
            "run_test_suite": self._run_test_suite,
            "check_system_status": self._check_system_status,
            "generate_report": self._generate_report,
            "run_smoke_tests": self._run_smoke_tests,
            "check_api_health": self._check_api_health,
        }
        
        # Keyword mappings for intent detection
        self.keywords = {
            "run_test_suite": ["run tests", "execute tests", "start testing", "test suite"],
            "check_system_status": ["system status", "check status", "health check", "system health"],
            "generate_report": ["generate report", "create report", "test report", "generate_report"],
            "run_smoke_tests": ["smoke test", "quick test", "smoke check"],
            "check_api_health": ["api health", "check api", "api status", "api check"],
        }
    
    def get_function_names(self) -> list:
        """Get list of available function names"""
        return list(self.functions.keys())
    
    def try_execute_from_text(self, text: str) -> Optional[Dict]:
        """
        Try to detect and execute a function based on user text
        
        Args:
            text: User input text
            
        Returns:
            Dict with function result or None if no match
        """
        text_lower = text.lower()
        
        # Check each function's keywords
        for func_name, keywords in self.keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Execute the function
                    result = self.functions[func_name]()
                    return {
                        "function": func_name,
                        "args": {},
                        "result": result
                    }
        
        return None
    
    # Test automation functions
    
    def _run_test_suite(self) -> str:
        """Simulate running a full test suite"""
        time.sleep(0.5)  # Simulate execution time
        total = random.randint(50, 100)
        passed = random.randint(int(total * 0.85), total)
        failed = total - passed
        
        return f"✅ Test Suite Complete\nTotal: {total} | Passed: {passed} | Failed: {failed} | Success Rate: {(passed/total*100):.1f}%"
    
    def _check_system_status(self) -> str:
        """Check system health status"""
        time.sleep(0.3)
        services = ["API", "Database", "Cache", "Message Queue"]
        status = {service: "HEALTHY" if random.random() > 0.1 else "DEGRADED" for service in services}
        
        output = "🔍 System Status:\n"
        for service, state in status.items():
            emoji = "✅" if state == "HEALTHY" else "⚠️"
            output += f"{emoji} {service}: {state}\n"
        
        return output.strip()
    
    def _generate_report(self) -> str:
        """Generate a test execution report"""
        time.sleep(0.4)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"📊 Report Generated\nTimestamp: {timestamp}\nFormat: HTML\nLocation: /reports/test_report_{int(time.time())}.html"
    
    def _run_smoke_tests(self) -> str:
        """Run quick smoke tests"""
        time.sleep(0.2)
        tests = ["Login", "Homepage", "API Endpoints", "Database Connection"]
        results = [f"✅ {test}" for test in tests]
        
        return "🔥 Smoke Tests Complete:\n" + "\n".join(results)
    
    def _check_api_health(self) -> str:
        """Check API health"""
        time.sleep(0.3)
        latency = random.randint(50, 200)
        uptime = random.uniform(99.5, 99.99)
        
        return f"🌐 API Health:\nStatus: ONLINE\nLatency: {latency}ms\nUptime: {uptime:.2f}%\nLast Check: {time.strftime('%H:%M:%S')}"
