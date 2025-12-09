"""
Activity Reporting API - Tracks and reports on OTTO activity and changes
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime, timedelta, date
import json

from database import get_db
from models import (
    ActivityReport, OttoTask, OttoRun, LifeOSTask, Bill, CalendarEvent,
    Income, Transaction, OttoMemory
)
from otto.context import get_default_context

router = APIRouter(prefix="/otto/activity", tags=["activity_reporting"])


def generate_period_report(
    db: Session,
    start_time: datetime,
    end_time: datetime,
    include_timeline: bool = True,
    household_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Generate a comprehensive activity report for a time period.
    
    Queries all relevant tables and aggregates activity data.
    """
    # Base filter for time period
    time_filter = lambda col: and_(col >= start_time, col <= end_time)
    
    # If household_id is provided, filter by it
    household_filter = lambda col: col == household_id if household_id else True
    
    # Initialize report structure
    report = {
        "period": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
            "duration_hours": (end_time - start_time).total_seconds() / 3600
        },
        "summary": {
            "total_changes": 0,
            "tasks_created": 0,
            "tasks_completed": 0,
            "actions_executed": 0,
            "entities_created": 0,
            "entities_updated": 0
        },
        "by_category": {
            "tasks": {
                "created": 0,
                "completed": 0,
                "failed": 0,
                "pending": 0
            },
            "actions": {},
            "entities": {}
        },
        "timeline": []
    }
    
    # Query Otto Tasks
    otto_tasks_query = db.query(OttoTask).filter(time_filter(OttoTask.created_at))
    if household_id:
        otto_tasks_query = otto_tasks_query.filter(OttoTask.household_id == household_id)
    
    otto_tasks = otto_tasks_query.all()
    for task in otto_tasks:
        report["summary"]["tasks_created"] += 1
        report["summary"]["total_changes"] += 1
        report["by_category"]["tasks"]["created"] += 1
        
        if task.status == "success":
            report["by_category"]["tasks"]["completed"] += 1
        elif task.status == "error" or task.status == "failed":
            report["by_category"]["tasks"]["failed"] += 1
        elif task.status == "pending":
            report["by_category"]["tasks"]["pending"] += 1
        
        if include_timeline:
            report["timeline"].append({
                "timestamp": task.created_at.isoformat(),
                "type": "otto_task_created",
                "entity": "otto_tasks",
                "id": task.id,
                "description": task.description,
                "status": task.status
            })
    
    # Query Otto Runs
    otto_runs_query = db.query(OttoRun).filter(time_filter(OttoRun.created_at))
    if household_id:
        otto_runs_query = otto_runs_query.filter(OttoRun.household_id == household_id)
    
    otto_runs = otto_runs_query.all()
    for run in otto_runs:
        report["summary"]["actions_executed"] += 1
        report["summary"]["total_changes"] += 1
        
        # Try to extract action types from output_payload
        if run.output_payload and isinstance(run.output_payload, dict):
            actions = run.output_payload.get("actions", [])
            for action in actions:
                action_type = action.get("type", "unknown")
                report["by_category"]["actions"][action_type] = report["by_category"]["actions"].get(action_type, 0) + 1
        
        if include_timeline:
            report["timeline"].append({
                "timestamp": run.created_at.isoformat(),
                "type": "otto_run",
                "entity": "otto_runs",
                "id": run.id,
                "status": run.status,
                "source": run.source
            })
    
    # Query Life OS Tasks
    life_os_tasks_query = db.query(LifeOSTask).filter(
        or_(
            time_filter(LifeOSTask.created_at),
            time_filter(LifeOSTask.updated_at),
            and_(LifeOSTask.completed_at.isnot(None), time_filter(LifeOSTask.completed_at))
        )
    )
    if household_id:
        life_os_tasks_query = life_os_tasks_query.filter(LifeOSTask.household_id == household_id)
    
    life_os_tasks = life_os_tasks_query.all()
    for task in life_os_tasks:
        if start_time <= task.created_at <= end_time:
            report["summary"]["entities_created"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("life_os_tasks", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["life_os_tasks"]["created"] += 1
            
            if include_timeline:
                report["timeline"].append({
                    "timestamp": task.created_at.isoformat(),
                    "type": "task_created",
                    "entity": "life_os_tasks",
                    "id": task.id,
                    "title": task.title
                })
        
        if task.updated_at and start_time <= task.updated_at <= end_time and task.updated_at != task.created_at:
            report["summary"]["entities_updated"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("life_os_tasks", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["life_os_tasks"]["updated"] = report["by_category"]["entities"]["life_os_tasks"].get("updated", 0) + 1
        
        if task.completed_at and start_time <= task.completed_at <= end_time:
            report["summary"]["tasks_completed"] += 1
            report["summary"]["total_changes"] += 1
    
    # Query Bills
    bills_query = db.query(Bill).filter(
        or_(
            time_filter(Bill.created_at),
            time_filter(Bill.updated_at),
            and_(Bill.paid_at.isnot(None), time_filter(Bill.paid_at))
        )
    )
    if household_id:
        bills_query = bills_query.filter(Bill.household_id == household_id)
    
    bills = bills_query.all()
    for bill in bills:
        if start_time <= bill.created_at <= end_time:
            report["summary"]["entities_created"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("bills", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["bills"]["created"] = report["by_category"]["entities"]["bills"].get("created", 0) + 1
        
        if bill.updated_at and start_time <= bill.updated_at <= end_time and bill.updated_at != bill.created_at:
            report["summary"]["entities_updated"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("bills", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["bills"]["updated"] = report["by_category"]["entities"]["bills"].get("updated", 0) + 1
    
    # Query Calendar Events
    calendar_query = db.query(CalendarEvent).filter(
        or_(
            time_filter(CalendarEvent.created_at),
            time_filter(CalendarEvent.updated_at)
        )
    )
    if household_id:
        calendar_query = calendar_query.filter(CalendarEvent.household_id == household_id)
    
    calendar_events = calendar_query.all()
    for event in calendar_events:
        if start_time <= event.created_at <= end_time:
            report["summary"]["entities_created"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("calendar_events", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["calendar_events"]["created"] = report["by_category"]["entities"]["calendar_events"].get("created", 0) + 1
        
        if event.updated_at and start_time <= event.updated_at <= end_time and event.updated_at != event.created_at:
            report["summary"]["entities_updated"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("calendar_events", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["calendar_events"]["updated"] = report["by_category"]["entities"]["calendar_events"].get("updated", 0) + 1
    
    # Query Income
    income_query = db.query(Income).filter(
        or_(
            time_filter(Income.created_at),
            time_filter(Income.updated_at)
        )
    )
    if household_id:
        income_query = income_query.filter(Income.household_id == household_id)
    
    income_entries = income_query.all()
    for income in income_entries:
        if start_time <= income.created_at <= end_time:
            report["summary"]["entities_created"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("income", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["income"]["created"] = report["by_category"]["entities"]["income"].get("created", 0) + 1
        
        if income.updated_at and start_time <= income.updated_at <= end_time and income.updated_at != income.created_at:
            report["summary"]["entities_updated"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("income", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["income"]["updated"] = report["by_category"]["entities"]["income"].get("updated", 0) + 1
    
    # Query Transactions
    transactions_query = db.query(Transaction).filter(
        or_(
            time_filter(Transaction.created_at),
            time_filter(Transaction.updated_at)
        )
    )
    if household_id:
        transactions_query = transactions_query.filter(Transaction.household_id == household_id)
    
    transactions = transactions_query.all()
    for transaction in transactions:
        if start_time <= transaction.created_at <= end_time:
            report["summary"]["entities_created"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("transactions", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["transactions"]["created"] = report["by_category"]["entities"]["transactions"].get("created", 0) + 1
        
        if transaction.updated_at and start_time <= transaction.updated_at <= end_time and transaction.updated_at != transaction.created_at:
            report["summary"]["entities_updated"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("transactions", {"created": 0, "updated": 0})
            report["by_category"]["entities"]["transactions"]["updated"] = report["by_category"]["entities"]["transactions"].get("updated", 0) + 1
    
    # Query Memory
    memory_query = db.query(OttoMemory).filter(
        or_(
            time_filter(OttoMemory.created_at),
            time_filter(OttoMemory.updated_at),
            and_(OttoMemory.last_used_at.isnot(None), time_filter(OttoMemory.last_used_at))
        )
    )
    if household_id:
        memory_query = memory_query.filter(OttoMemory.household_id == household_id)
    
    memories = memory_query.all()
    for memory in memories:
        if start_time <= memory.created_at <= end_time:
            report["summary"]["entities_created"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("otto_memory", {"created": 0, "updated": 0, "used": 0})
            report["by_category"]["entities"]["otto_memory"]["created"] = report["by_category"]["entities"]["otto_memory"].get("created", 0) + 1
        
        if memory.updated_at and start_time <= memory.updated_at <= end_time and memory.updated_at != memory.created_at:
            report["summary"]["entities_updated"] += 1
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("otto_memory", {"created": 0, "updated": 0, "used": 0})
            report["by_category"]["entities"]["otto_memory"]["updated"] = report["by_category"]["entities"]["otto_memory"].get("updated", 0) + 1
        
        if memory.last_used_at and start_time <= memory.last_used_at <= end_time:
            report["summary"]["total_changes"] += 1
            report["by_category"]["entities"].setdefault("otto_memory", {"created": 0, "updated": 0, "used": 0})
            report["by_category"]["entities"]["otto_memory"]["used"] = report["by_category"]["entities"]["otto_memory"].get("used", 0) + 1
    
    # Sort timeline by timestamp
    if include_timeline:
        report["timeline"].sort(key=lambda x: x["timestamp"])
    
    return report


def compare_reports(report1: Dict[str, Any], report2: Dict[str, Any]) -> Dict[str, Any]:
    """Compare two activity reports and return delta metrics"""
    summary1 = report1.get("summary", {})
    summary2 = report2.get("summary", {})
    
    deltas = {}
    for key in ["total_changes", "tasks_created", "tasks_completed", "actions_executed", "entities_created", "entities_updated"]:
        val1 = summary1.get(key, 0)
        val2 = summary2.get(key, 0)
        diff = val2 - val1
        deltas[key] = f"{'+' if diff >= 0 else ''}{diff}"
    
    # Calculate trends
    trends = {
        "activity_increased": summary2.get("total_changes", 0) > summary1.get("total_changes", 0),
        "completion_rate_improved": False  # Would need more data to calculate properly
    }
    
    # Calculate completion rate if we have the data
    tasks1_created = summary1.get("tasks_created", 0)
    tasks1_completed = summary1.get("tasks_completed", 0)
    tasks2_created = summary2.get("tasks_created", 0)
    tasks2_completed = summary2.get("tasks_completed", 0)
    
    if tasks1_created > 0 and tasks2_created > 0:
        rate1 = tasks1_completed / tasks1_created if tasks1_created > 0 else 0
        rate2 = tasks2_completed / tasks2_created if tasks2_created > 0 else 0
        trends["completion_rate_improved"] = rate2 > rate1
    
    return {
        "previous_period": {
            "start": report1.get("period", {}).get("start"),
            "end": report1.get("period", {}).get("end")
        },
        "current_period": {
            "start": report2.get("period", {}).get("start"),
            "end": report2.get("period", {}).get("end")
        },
        "deltas": deltas,
        "trends": trends
    }


@router.get("/report")
async def get_activity_report(
    start: str = Query(..., description="Start time in ISO format"),
    end: str = Query(..., description="End time in ISO format"),
    include_timeline: bool = Query(True, description="Include detailed timeline"),
    include_comparison: bool = Query(False, description="Include comparison to previous period"),
    db: Session = Depends(get_db)
):
    """Generate activity report for a custom time period"""
    try:
        start_time = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(end.replace('Z', '+00:00'))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    
    # Get household context
    otto_context = get_default_context(db)
    household_id = otto_context.household_id if otto_context else None
    
    # Generate report
    report = generate_period_report(
        db=db,
        start_time=start_time,
        end_time=end_time,
        include_timeline=include_timeline,
        household_id=household_id
    )
    
    # Add comparison if requested
    if include_comparison:
        # Find previous period report (same duration, ending at start_time)
        duration = end_time - start_time
        prev_start = start_time - duration
        prev_end = start_time
        
        prev_report = generate_period_report(
            db=db,
            start_time=prev_start,
            end_time=prev_end,
            include_timeline=False,
            household_id=household_id
        )
        
        comparison = compare_reports(prev_report, report)
        report["comparison"] = comparison
    
    return report


@router.get("/daily")
async def get_daily_report(
    target_date: Optional[str] = Query(None, description="Target date (YYYY-MM-DD), defaults to yesterday"),
    store: bool = Query(True, description="Store the report in database"),
    compare_previous: bool = Query(True, description="Compare to previous day"),
    db: Session = Depends(get_db)
):
    """Generate or retrieve daily activity report (last 24 hours)"""
    # Determine target date
    if target_date:
        try:
            target = datetime.strptime(target_date, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    else:
        # Default to yesterday
        target = (datetime.now() - timedelta(days=1)).date()
    
    # Calculate period (24 hours for that day)
    start_time = datetime.combine(target, datetime.min.time())
    end_time = start_time + timedelta(days=1)
    
    # Get household context
    otto_context = get_default_context(db)
    household_id = otto_context.household_id if otto_context else None
    
    # Check if report already exists
    existing_report = db.query(ActivityReport).filter(
        and_(
            ActivityReport.report_type == "daily",
            ActivityReport.period_start == start_time,
            ActivityReport.period_end == end_time
        )
    ).first()
    
    if existing_report and not compare_previous:
        # Return existing report
        return existing_report.report_data
    
    # Generate report
    report = generate_period_report(
        db=db,
        start_time=start_time,
        end_time=end_time,
        include_timeline=True,
        household_id=household_id
    )
    
    # Add comparison if requested
    comparison_data = None
    if compare_previous:
        # Previous day
        prev_start = start_time - timedelta(days=1)
        prev_end = start_time
        
        prev_report = generate_period_report(
            db=db,
            start_time=prev_start,
            end_time=prev_end,
            include_timeline=False,
            household_id=household_id
        )
        
        comparison = compare_reports(prev_report, report)
        report["comparison"] = comparison
        comparison_data = comparison
    
    # Store report if requested
    if store:
        summary_text = f"Daily activity report: {report['summary']['total_changes']} total changes, {report['summary']['tasks_created']} tasks created, {report['summary']['tasks_completed']} tasks completed"
        
        activity_report = ActivityReport(
            report_type="daily",
            period_start=start_time,
            period_end=end_time,
            report_data=report,
            summary=summary_text,
            comparison_data=comparison_data,
            metadata={"generated_at": datetime.now().isoformat()}
        )
        
        if existing_report:
            # Update existing
            existing_report.report_data = report
            existing_report.summary = summary_text
            existing_report.comparison_data = comparison_data
            existing_report.metadata = {"generated_at": datetime.now().isoformat()}
        else:
            db.add(activity_report)
        
        db.commit()
    
    return report


@router.get("/reports")
async def list_reports(
    report_type: Optional[str] = Query(None, description="Filter by report type"),
    limit: int = Query(30, description="Maximum number of reports to return"),
    db: Session = Depends(get_db)
):
    """List available activity reports"""
    query = db.query(ActivityReport)
    
    if report_type:
        query = query.filter(ActivityReport.report_type == report_type)
    
    reports = query.order_by(ActivityReport.created_at.desc()).limit(limit).all()
    
    return {
        "reports": [
            {
                "id": r.id,
                "report_type": r.report_type,
                "period_start": r.period_start.isoformat(),
                "period_end": r.period_end.isoformat(),
                "summary": r.summary,
                "created_at": r.created_at.isoformat()
            }
            for r in reports
        ],
        "total": len(reports)
    }


@router.get("/reports/{report_id}")
async def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific activity report by ID"""
    report = db.query(ActivityReport).filter(ActivityReport.id == report_id).first()
    
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
    
    return {
        "id": report.id,
        "report_type": report.report_type,
        "period_start": report.period_start.isoformat(),
        "period_end": report.period_end.isoformat(),
        "report_data": report.report_data,
        "summary": report.summary,
        "comparison_data": report.comparison_data,
        "metadata": report.metadata,
        "created_at": report.created_at.isoformat()
    }


@router.get("/compare")
async def compare_reports_endpoint(
    report1_id: int = Query(..., description="First report ID"),
    report2_id: int = Query(..., description="Second report ID"),
    db: Session = Depends(get_db)
):
    """Compare two activity reports"""
    report1 = db.query(ActivityReport).filter(ActivityReport.id == report1_id).first()
    report2 = db.query(ActivityReport).filter(ActivityReport.id == report2_id).first()
    
    if not report1:
        raise HTTPException(status_code=404, detail=f"Report {report1_id} not found")
    if not report2:
        raise HTTPException(status_code=404, detail=f"Report {report2_id} not found")
    
    comparison = compare_reports(report1.report_data, report2.report_data)
    
    return {
        "report1": {
            "id": report1_id,
            "period": report1.report_data.get("period"),
            "summary": report1.report_data.get("summary")
        },
        "report2": {
            "id": report2_id,
            "period": report2.report_data.get("period"),
            "summary": report2.report_data.get("summary")
        },
        "comparison": comparison
    }
