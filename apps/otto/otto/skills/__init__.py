"""
Otto skills module
"""

from .repo_lister import RepoListerSkill
from .repo_audit import RepoAuditSkill
from .otto_runs import OttoRunsSkill
from .env_status import EnvStatusSkill
from .self_test import SelfTestSkill
from .bill_reminder import BillReminderSkill
from .symbioz import SymbiozSkill
from .task_management import TaskManagementSkill
from .calendar import CalendarSkill
from .bill_management import BillManagementSkill
from .income_tracking import IncomeTrackingSkill
from .transaction import TransactionSkill
from .tax_brain import TaxBrainSkill
from .scheduling import SchedulingSkill
from .reminder import ReminderSkill
from .memory import OttoMemorySkill
from .deployment_status import DeploymentStatusSkill
from .deployment_automation import DeploymentAutomationSkill
from .launcher_diagnostic import LauncherDiagnosticSkill
from .activity_reporting import ActivityReportingSkill
from .monitor_repair_redeploy import MonitorRepairRedeploySkill

def get_all_skills():
    """Get all available Otto skills"""
    return [
        RepoListerSkill(),
        RepoAuditSkill(),
        OttoRunsSkill(),
        EnvStatusSkill(),
        SelfTestSkill(),
        BillReminderSkill(),
        SymbiozSkill(),
        TaskManagementSkill(),
        CalendarSkill(),
        BillManagementSkill(),
        IncomeTrackingSkill(),
        TransactionSkill(),
        TaxBrainSkill(),
        SchedulingSkill(),
        ReminderSkill(),
        OttoMemorySkill(),
        DeploymentStatusSkill(),
        DeploymentAutomationSkill(),
        LauncherDiagnosticSkill(),
        ActivityReportingSkill(),
        MonitorRepairRedeploySkill(),
    ]

