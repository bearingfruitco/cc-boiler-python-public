#!/usr/bin/env python3
"""
Orchestrates the 4-level validation for PRPs
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

class ValidationLevel:
    def __init__(self, name: str, commands: List[str], 
                 required: bool = True):
        self.name = name
        self.commands = commands
        self.required = required
        self.results = []
    
    def run(self) -> Tuple[bool, List[str]]:
        """Run validation commands and return success status"""
        print(f"\n🔍 Running {self.name}...")
        print("-" * 50)
        
        all_passed = True
        
        for cmd in self.commands:
            print(f"$ {cmd}")
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✅ Passed")
            else:
                print("❌ Failed")
                if result.stderr:
                    print(f"Error: {result.stderr}")
                all_passed = False
                
            self.results.append({
                "command": cmd,
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr
            })
        
        return all_passed, self.results


def run_validation(feature: str) -> bool:
    """Run all 4 levels of validation"""
    
    levels = [
        ValidationLevel(
            "Level 1: Syntax & Style",
            [
                "ruff check src/ --fix",
                "ruff format src/",
                "mypy src/ --strict"
            ]
        ),
        ValidationLevel(
            "Level 2: Unit Tests",
            [
                f"pytest tests/test_{feature}_*.py -v",
                f"pytest tests/ --cov=src/{feature} --cov-report=term-missing"
            ]
        ),
        ValidationLevel(
            "Level 3: Integration Tests",
            [
                "docker-compose -f docker-compose.test.yml up -d",
                f"pytest tests/test_{feature}_integration.py -v -m integration",
                "docker-compose -f docker-compose.test.yml down"
            ]
        ),
        ValidationLevel(
            "Level 4: Security & Performance",
            [
                f"bandit -r src/{feature}/",
                "safety check",
                f"python -m pytest tests/test_{feature}_load.py"
            ],
            required=False  # Optional but recommended
        )
    ]
    
    all_passed = True
    
    for level in levels:
        passed, results = level.run()
        
        if not passed and level.required:
            all_passed = False
            print(f"\n⚠️  {level.name} failed!")
            if not level.required:
                print("This is optional but recommended.")
    
    return all_passed


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: prp_validator.py <feature_name>")
        sys.exit(1)
    
    feature = sys.argv[1]
    print(f"🚀 Validating PRP implementation for: {feature}")
    
    if run_validation(feature):
        print("\n✅ All validation levels passed!")
        sys.exit(0)
    else:
        print("\n❌ Validation failed. Fix issues and retry.")
        sys.exit(1)
