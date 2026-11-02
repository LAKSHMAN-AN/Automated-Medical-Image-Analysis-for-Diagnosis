"""
LangGraph Multi-Agent State Machine Workflow
Sequential state graph: Perception -> Reasoning -> Planning -> Risk -> HITL Doctor Approval.
"""

from typing import Dict, Any, List
from backend.app.agent.agents.clinical_agents import SupervisorAgent

class LangGraphDiagnosticWorkflow:
    """LangGraph State Machine for autonomous diagnostic reasoning."""

    def __init__(self):
        self.supervisor = SupervisorAgent()

    def execute(self, patient_code: str, image_id: str) -> Dict[str, Any]:
        """Executes full multi-agent state transition graph."""
        return self.supervisor.run_workflow(patient_code, image_id)
