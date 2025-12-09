"""
Otto CLI - Command-line interface
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import List
import uuid

from .config import load_config
from .core.models import Task, TaskStatus
from .core.skill_base import SkillContext
from .core.runner import run_tasks
from .core.health import run_skill_health_checks
from .core.logging_utils import get_logger
from .skills import get_all_skills

logger = get_logger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Otto - Persistent AI Agent")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # run-sample command
    run_sample_parser = subparsers.add_parser("run-sample", help="Run a sample repo_list task")
    
    # health command
    health_parser = subparsers.add_parser("health", help="Run health checks on all skills")
    
    # audit command
    audit_parser = subparsers.add_parser("audit", help="Run repo audit on apps/otto")
    
    # server command
    server_parser = subparsers.add_parser("server", help="Start Otto API server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    server_parser.add_argument("--port", type=int, default=8001, help="Port to bind to")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Load config
    config = load_config()
    context = SkillContext(config=config, logger=logger)
    skills = get_all_skills()
    
    if args.command == "run-sample":
        # Create a sample task
        task = Task(
            id=str(uuid.uuid4()),
            type="repo_list",
            payload={
                "target_repo": config.storage.default_repo_root,
                "output_path": str(Path(config.storage.reports_dir) / "repo_tree_sample.md")
            },
            source="cli",
            status=TaskStatus.PENDING
        )
        
        results = run_tasks([task], skills, context)
        result = results[0]
        
        if result.success:
            print(f"✅ Success: {result.message}")
            if result.data:
                print(f"   Output: {result.data.get('output_path')}")
            sys.exit(0)
        else:
            print(f"❌ Failed: {result.message}")
            sys.exit(1)
    
    elif args.command == "health":
        # Run health checks
        report = run_skill_health_checks(skills, context)
        
        if not report.has_issues():
            print("✅ All skills are healthy!")
            sys.exit(0)
        else:
            print(f"⚠️  Found {report.total_issues()} issue(s) across skills:\n")
            for skill_name, issues in report.issues.items():
                print(f"**{skill_name}:**")
                for issue in issues:
                    print(f"  - [{issue.code}] {issue.message}")
                    if issue.suggestion:
                        print(f"    Suggestion: {issue.suggestion}")
                print()
            sys.exit(1)
    
    elif args.command == "audit":
        # Create audit task
        date_str = datetime.now().strftime("%Y-%m-%d")
        task = Task(
            id=str(uuid.uuid4()),
            type="repo_audit",
            payload={
                "target_repo": "apps/otto",
                "output_path": str(Path(config.storage.reports_dir) / "audits" / f"otto_audit_{date_str}.md")
            },
            source="cli",
            status=TaskStatus.PENDING
        )
        
        results = run_tasks([task], skills, context)
        result = results[0]
        
        if result.success:
            print(f"✅ Audit complete: {result.message}")
            if result.data:
                print(f"   Report: {result.data.get('output_path')}")
            sys.exit(0)
        else:
            print(f"❌ Audit failed: {result.message}")
            sys.exit(1)
    
    elif args.command == "server":
        # Start API server
        from .api import run_server
        run_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()

