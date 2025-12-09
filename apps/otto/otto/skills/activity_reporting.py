"""
ActivityReportingSkill - Tracks and reports on OTTO activity and changes
Generates activity reports for specified time periods and automatic daily reports
"""

from typing import List, Dict, Any, Optional
import os
import httpx
from datetime import datetime, timedelta, date

from ..core.models import Task, TaskResult, TaskStatus
from ..core.skill_base import Skill, SkillHealthIssue, SkillContext
from ..core.logging_utils import get_logger

logger = get_logger(__name__)


class ActivityReportingSkill:
    """Skill for tracking and reporting on OTTO activity"""
    
    name = "activity_reporting"
    description = "Tracks and reports on all OTTO activity and changes within specified time periods"
    
    def __init__(self):
        # Life OS backend API URL
        self.life_os_api_url = os.getenv("LIFE_OS_API_URL", "http://localhost:8000")
    
    def can_handle(self, task: Task) -> bool:
        """Check if this skill can handle the task"""
        return task.type in [
            "activity.report",
            "activity.daily_report",
            "activity.compare_periods",
            "activity.list_reports",
            "activity.get_report",
        ]
    
    def run(self, task: Task, context: SkillContext) -> TaskResult:
        """Execute the activity reporting operation"""
        try:
            if task.type == "activity.report":
                return self._handle_report(task, context)
            elif task.type == "activity.daily_report":
                return self._handle_daily_report(task, context)
            elif task.type == "activity.compare_periods":
                return self._handle_compare_periods(task, context)
            elif task.type == "activity.list_reports":
                return self._handle_list_reports(task, context)
            elif task.type == "activity.get_report":
                return self._handle_get_report(task, context)
            else:
                return TaskResult(
                    task_id=task.id,
                    success=False,
                    message=f"Unknown activity reporting operation: {task.type}"
                )
        except Exception as e:
            logger.error(f"Error in ActivityReportingSkill: {str(e)}", exc_info=True)
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error in activity reporting: {str(e)}"
            )
    
    def _handle_report(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle activity.report - Generate report for custom time period"""
        payload = task.payload or {}
        
        start_time = payload.get("start_time")
        end_time = payload.get("end_time")
        include_timeline = payload.get("include_timeline", True)
        include_comparison = payload.get("include_comparison", False)
        
        if not start_time or not end_time:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required fields: 'start_time', 'end_time'"
            )
        
        try:
            with httpx.Client(timeout=30.0) as client:
                params = {
                    "start": start_time,
                    "end": end_time,
                    "include_timeline": str(include_timeline).lower(),
                    "include_comparison": str(include_comparison).lower()
                }
                response = client.get(f"{self.life_os_api_url}/otto/activity/report", params=params)
                
                if response.status_code == 200:
                    report = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Generated activity report for period {start_time} to {end_time}",
                        data=report,
                        reasoning={
                            "steps": [{
                                "id": "step1",
                                "type": "report_generation",
                                "summary": f"Generated activity report covering {report.get('period', {}).get('duration_hours', 0)} hours",
                                "evidence": [{"kind": "activity_report", "period_start": start_time, "period_end": end_time}]
                            }]
                        }
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to generate report: {response.status_code} - {response.text}"
                    )
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error generating report: {str(e)}"
            )
    
    def _handle_daily_report(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle activity.daily_report - Generate or retrieve daily report"""
        payload = task.payload or {}
        
        target_date = payload.get("target_date")  # Optional, defaults to yesterday
        store = payload.get("store", True)
        compare_previous = payload.get("compare_previous", True)
        
        try:
            with httpx.Client(timeout=30.0) as client:
                params = {}
                if target_date:
                    params["target_date"] = target_date
                if not store:
                    params["store"] = "false"
                if not compare_previous:
                    params["compare_previous"] = "false"
                
                response = client.get(f"{self.life_os_api_url}/otto/activity/daily", params=params)
                
                if response.status_code == 200:
                    report = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Generated daily activity report for {target_date or 'yesterday'}",
                        data=report,
                        reasoning={
                            "steps": [{
                                "id": "step1",
                                "type": "daily_report_generation",
                                "summary": f"Generated daily activity report with {report.get('summary', {}).get('total_changes', 0)} total changes",
                                "evidence": [{"kind": "daily_activity_report", "target_date": target_date}]
                            }]
                        }
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to generate daily report: {response.status_code} - {response.text}"
                    )
        except Exception as e:
            logger.error(f"Error generating daily report: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error generating daily report: {str(e)}"
            )
    
    def _handle_compare_periods(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle activity.compare_periods - Compare two reports"""
        payload = task.payload or {}
        
        report1_id = payload.get("report1_id")
        report2_id = payload.get("report2_id")
        
        if not report1_id or not report2_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required fields: 'report1_id', 'report2_id'"
            )
        
        try:
            with httpx.Client(timeout=30.0) as client:
                params = {
                    "report1_id": report1_id,
                    "report2_id": report2_id
                }
                response = client.get(f"{self.life_os_api_url}/otto/activity/compare", params=params)
                
                if response.status_code == 200:
                    comparison = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Compared reports {report1_id} and {report2_id}",
                        data=comparison
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to compare reports: {response.status_code} - {response.text}"
                    )
        except Exception as e:
            logger.error(f"Error comparing reports: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error comparing reports: {str(e)}"
            )
    
    def _handle_list_reports(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle activity.list_reports - List available reports"""
        payload = task.payload or {}
        
        report_type = payload.get("report_type")  # Optional filter
        limit = payload.get("limit", 30)
        
        try:
            with httpx.Client(timeout=10.0) as client:
                params = {"limit": limit}
                if report_type:
                    params["report_type"] = report_type
                
                response = client.get(f"{self.life_os_api_url}/otto/activity/reports", params=params)
                
                if response.status_code == 200:
                    reports = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Retrieved {len(reports.get('reports', []))} reports",
                        data=reports
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to list reports: {response.status_code} - {response.text}"
                    )
        except Exception as e:
            logger.error(f"Error listing reports: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error listing reports: {str(e)}"
            )
    
    def _handle_get_report(self, task: Task, context: SkillContext) -> TaskResult:
        """Handle activity.get_report - Get specific report by ID"""
        payload = task.payload or {}
        
        report_id = payload.get("report_id")
        
        if not report_id:
            return TaskResult(
                task_id=task.id,
                success=False,
                message="Missing required field: 'report_id'"
            )
        
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(f"{self.life_os_api_url}/otto/activity/reports/{report_id}")
                
                if response.status_code == 200:
                    report = response.json()
                    return TaskResult(
                        task_id=task.id,
                        success=True,
                        message=f"Retrieved report {report_id}",
                        data=report
                    )
                elif response.status_code == 404:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Report {report_id} not found"
                    )
                else:
                    return TaskResult(
                        task_id=task.id,
                        success=False,
                        message=f"Failed to get report: {response.status_code} - {response.text}"
                    )
        except Exception as e:
            logger.error(f"Error getting report: {str(e)}")
            return TaskResult(
                task_id=task.id,
                success=False,
                message=f"Error getting report: {str(e)}"
            )
    
    def self_test(self, context: SkillContext) -> List[SkillHealthIssue]:
        """Run health checks on this skill"""
        issues = []
        
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.get(f"{self.life_os_api_url}/health")
                if response.status_code != 200:
                    issues.append(SkillHealthIssue(
                        code="life_os_unavailable",
                        message=f"Life OS backend not available: {response.status_code}",
                        suggestion="Check if Life OS backend is running"
                    ))
        except Exception as e:
            issues.append(SkillHealthIssue(
                code="life_os_connection_failed",
                message=f"Cannot connect to Life OS backend: {str(e)}",
                suggestion="Check LIFE_OS_API_URL environment variable and ensure backend is running"
            ))
        
        return issues
