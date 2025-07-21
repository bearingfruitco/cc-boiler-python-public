#!/usr/bin/env python3
"""
PRP Runner for Python Projects
Executes PRPs with Claude Code in various modes
"""

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterator, Optional

# Project root
ROOT = Path(__file__).resolve().parent.parent

# PRP metadata
META_HEADER = """You are a Python AI development agent executing a PRP (Product Requirement Prompt).

# WORKFLOW GUIDANCE:

## Planning Phase
- Review the PRP thoroughly before starting
- Check all referenced files and documentation
- Create a comprehensive implementation plan
- Identify potential issues early

## Implementation Phase
- Follow existing patterns in the codebase
- Use type hints and proper documentation
- Implement comprehensive error handling
- Write tests alongside implementation

## Validation Phase
- Run all validation loops in sequence
- Fix any issues before proceeding
- Ensure all success criteria are met
- Document any deviations or improvements

## Python-Specific Guidelines
- Use async/await for I/O operations
- Follow PEP 8 and project conventions
- Ensure Python 3.11+ compatibility
- Use Poetry for dependency management

---

"""

class PRPRunner:
    def __init__(self, prp_name: str, interactive: bool = False, 
                 output_format: str = "text"):
        self.prp_name = prp_name
        self.interactive = interactive
        self.output_format = output_format
        self.start_time = datetime.now()
        self.prp_path = self._locate_prp()
        
    def _locate_prp(self) -> Path:
        """Find PRP file in active or templates directory"""
        locations = [
            ROOT / f"PRPs/active/{self.prp_name}.md",
            ROOT / f"PRPs/active/{self.prp_name}",
            ROOT / f"PRPs/{self.prp_name}.md",
            ROOT / f"PRPs/{self.prp_name}",
        ]
        
        for path in locations:
            if path.exists():
                return path
                
        raise FileNotFoundError(f"PRP not found: {self.prp_name}")
    
    def build_prompt(self) -> str:
        """Build complete prompt with metadata and PRP content"""
        prp_content = self.prp_path.read_text()
        
        # Extract confidence score if present
        confidence = "Unknown"
        if "Confidence Score:" in prp_content:
            try:
                line = [l for l in prp_content.split('\n') 
                       if "Confidence Score:" in l][0]
                confidence = line.split(':')[1].strip()
            except:
                pass
        
        metadata = f"""
PRP: {self.prp_name}
Path: {self.prp_path}
Started: {self.start_time.isoformat()}
Confidence: {confidence}
Mode: {"Interactive" if self.interactive else "Automated"}

---

"""
        
        return META_HEADER + metadata + prp_content
    
    def pre_execution_checks(self) -> bool:
        """Run safety checks before execution"""
        print("Running pre-execution checks...")
        
        # Check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        if result.stdout.strip():
            if not self.interactive:
                raise RuntimeError("Uncommitted changes detected. Commit or stash first.")
            else:
                print("⚠️  Warning: Uncommitted changes detected")
                response = input("Continue anyway? (y/n): ")
                if response.lower() != 'y':
                    return False
        
        # Check dependencies
        if (ROOT / "pyproject.toml").exists():
            print("Checking Python dependencies...")
            dep_result = subprocess.run(
                ["poetry", "check"],
                capture_output=True,
                text=True
            )
            if dep_result.returncode != 0:
                print(f"⚠️  Dependency issues: {dep_result.stderr}")
        
        # Check for conflicting PRPs
        active_prps = list((ROOT / "PRPs/active").glob("*.md"))
        other_prps = [p for p in active_prps if p.stem != self.prp_name]
        
        if other_prps:
            print(f"⚠️  Other active PRPs found: {[p.stem for p in other_prps]}")
            if not self.interactive:
                response = input("Continue with multiple active PRPs? (y/n): ")
                if response.lower() != 'y':
                    return False
        
        print("✅ Pre-execution checks passed")
        return True
    
    def run(self) -> Dict[str, Any]:
        """Execute the PRP with Claude Code"""
        if not self.pre_execution_checks():
            return {"completed": False, "aborted": True}
        
        prompt = self.build_prompt()
        
        # Base command
        cmd = ["claude"]
        
        # Add allowed tools for Python development
        tools = [
            "Edit", "Write", "Read", "MultiEdit",
            "Bash", "Python", "Search", "Replace",
            "WebSearch", "WebFetch", "TodoWrite",
            "GitOps", "TestRunner"
        ]
        cmd.extend(["--allowedTools", ",".join(tools)])
        
        if self.interactive:
            # Interactive mode - feed prompt via stdin
            result = subprocess.run(
                cmd,
                input=prompt.encode(),
                capture_output=True,
                text=True
            )
            return {
                "mode": "interactive",
                "completed": result.returncode == 0
            }
        else:
            # Automated mode
            cmd.extend(["-p", prompt])
            cmd.extend(["--output-format", self.output_format])
            
            if self.output_format == "json":
                return self._run_json_mode(cmd)
            elif self.output_format == "stream-json":
                return self._run_stream_mode(cmd)
            else:
                return self._run_text_mode(cmd)
    
    def _run_json_mode(self, cmd: list) -> Dict[str, Any]:
        """Run in JSON output mode"""
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return {
                "error": True,
                "message": result.stderr,
                "returncode": result.returncode
            }
        
        try:
            data = json.loads(result.stdout)
            # Add execution metadata
            data["prp_metadata"] = {
                "name": self.prp_name,
                "duration": (datetime.now() - self.start_time).total_seconds(),
                "path": str(self.prp_path)
            }
            return data
        except json.JSONDecodeError as e:
            return {
                "error": True,
                "message": f"Failed to parse JSON: {e}",
                "raw_output": result.stdout
            }
    
    def _run_stream_mode(self, cmd: list) -> Dict[str, Any]:
        """Run in streaming JSON mode"""
        metrics = {
            "messages": 0,
            "tool_calls": 0,
            "errors": 0,
            "cost_usd": 0.0
        }
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        try:
            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    msg = json.loads(line)
                    
                    # Track metrics
                    if msg.get("type") == "assistant":
                        metrics["messages"] += 1
                    elif msg.get("type") == "tool_call":
                        metrics["tool_calls"] += 1
                    elif msg.get("type") == "error":
                        metrics["errors"] += 1
                    elif msg.get("type") == "result":
                        metrics["cost_usd"] = msg.get("cost_usd", 0)
                    
                    # Output for downstream processing
                    print(json.dumps(msg))
                    
                except json.JSONDecodeError:
                    print(f"Warning: Invalid JSON: {line}", file=sys.stderr)
            
            process.wait()
            
            return {
                "completed": process.returncode == 0,
                "metrics": metrics,
                "duration": (datetime.now() - self.start_time).total_seconds()
            }
            
        except KeyboardInterrupt:
            process.terminate()
            return {
                "completed": False,
                "interrupted": True,
                "metrics": metrics
            }
    
    def _run_text_mode(self, cmd: list) -> Dict[str, Any]:
        """Run in text output mode"""
        result = subprocess.run(cmd, text=True)
        
        return {
            "completed": result.returncode == 0,
            "returncode": result.returncode,
            "duration": (datetime.now() - self.start_time).total_seconds()
        }
    
    def save_execution_record(self, result: Dict[str, Any]):
        """Save execution details for tracking"""
        record_dir = ROOT / "PRPs" / "execution_logs"
        record_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        record_file = record_dir / f"{self.prp_name}_{timestamp}.json"
        
        record = {
            "prp": self.prp_name,
            "started": self.start_time.isoformat(),
            "completed": datetime.now().isoformat(),
            "result": result
        }
        
        record_file.write_text(json.dumps(record, indent=2))
        print(f"\nExecution record saved: {record_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Run a Python PRP with Claude Code"
    )
    parser.add_argument(
        "--prp",
        required=True,
        help="PRP name (without .md extension)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--output-format",
        choices=["text", "json", "stream-json"],
        default="text",
        help="Output format for automated mode"
    )
    parser.add_argument(
        "--save-record",
        action="store_true",
        default=True,
        help="Save execution record"
    )
    
    args = parser.parse_args()
    
    try:
        runner = PRPRunner(
            args.prp,
            args.interactive,
            args.output_format
        )
        
        print(f"Executing PRP: {args.prp}")
        print(f"Mode: {'Interactive' if args.interactive else 'Automated'}")
        print("-" * 50)
        
        result = runner.run()
        
        if args.save_record:
            runner.save_execution_record(result)
        
        # Exit with appropriate code
        if result.get("completed"):
            print("\n✅ PRP execution completed successfully")
            sys.exit(0)
        else:
            print("\n❌ PRP execution failed")
            sys.exit(1)
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
