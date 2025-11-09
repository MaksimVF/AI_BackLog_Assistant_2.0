
"""
Level 3 Graph Agent

This module implements the Level 3 agents using LangGraph for enhanced
coordination and processing of risk assessment, resource analysis,
impact evaluation, and task prioritization.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage

# Import existing agents for integration
from src.agents.level3.risk_assessment_agent import risk_assessment_agent
from src.agents.level3.resource_availability_agent import resource_availability_agent
from src.agents.level3.impact_potential_agent import impact_potential_agent
from src.agents.level3.confidence_urgency_agent import confidence_urgency_agent
from src.agents.level3.task_prioritization_agent import task_prioritization_agent

# Configure logging
logger = logging.getLogger(__name__)

class GraphState(BaseModel):
    """State for the Level 3 graph processing"""
    input_text: str
    task_type: str = "general"
    risk_result: Optional[Dict[str, Any]] = None
    resource_analysis: Optional[Dict[str, Any]] = None
    impact_evaluation: Optional[Dict[str, Any]] = None
    confidence_urgency: Optional[Dict[str, Any]] = None
    prioritization: Optional[Dict[str, Any]] = None
    messages: List[Any] = []

class Level3GraphAgent:
    """Agent that uses LangGraph to coordinate Level 3 processing"""

    def __init__(self):
        """Initialize the Level 3 Graph Agent"""
        logger.info("Initializing Level 3 Graph Agent")

        # Create the graph
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create the LangGraph for Level 3 processing"""
        graph = StateGraph(GraphState)

        # Add nodes for each processing step
        graph.add_node("assess_risk", self._run_risk_assessment)
        graph.add_node("resource_analysis", self._run_resource_analysis)
        graph.add_node("impact_evaluation", self._run_impact_evaluation)
        graph.add_node("confidence_urgency", self._run_confidence_urgency)
        graph.add_node("task_prioritization", self._run_task_prioritization)

        # Define the execution flow without cycles
        graph.set_entry_point("assess_risk")
        graph.add_edge("assess_risk", "resource_analysis")
        graph.add_edge("resource_analysis", "impact_evaluation")
        graph.add_edge("impact_evaluation", "confidence_urgency")
        graph.add_edge("confidence_urgency", "task_prioritization")
        graph.set_finish_point("task_prioritization")  # Set final node

        return graph

    def _run_risk_assessment(self, state: GraphState) -> GraphState:
        """Run risk assessment"""
        if state.risk_result is None:
            result = risk_assessment_agent.evaluate_risk(state.input_text)
            state.risk_result = result
            state.messages.append(AIMessage(content=f"Risk assessment: {result['risk_score']}"))
        return state

    def _run_resource_analysis(self, state: GraphState) -> GraphState:
        """Run resource analysis"""
        if state.resource_analysis is None:
            result = resource_availability_agent.assess_resources(state.input_text)
            state.resource_analysis = result
            state.messages.append(AIMessage(content="Resource analysis completed"))
        return state

    def _run_impact_evaluation(self, state: GraphState) -> GraphState:
        """Run impact evaluation"""
        if state.impact_evaluation is None:
            result = impact_potential_agent.assess_impact(state.input_text)
            state.impact_evaluation = result
            state.messages.append(AIMessage(content=f"Impact score: {result['impact_score']}"))
        return state

    def _run_confidence_urgency(self, state: GraphState) -> GraphState:
        """Run confidence and urgency analysis"""
        if state.confidence_urgency is None:
            result = confidence_urgency_agent.score_task(state.input_text)
            state.confidence_urgency = result
            state.messages.append(AIMessage(content=f"Confidence: {result['confidence']}, Urgency: {result['urgency']}"))
        return state

    def _run_task_prioritization(self, state: GraphState) -> GraphState:
        """Run task prioritization"""
        if state.prioritization is None:
            result = task_prioritization_agent.prioritize_task(state.input_text, state.task_type)
            state.prioritization = result
            state.messages.append(AIMessage(content=f"Priority score: {result['priority_score']}"))
        return state

    def analyze_task(self, text: str, task_type: str = "general", max_iterations: int = 5) -> Dict[str, Any]:
        """
        Analyze task using the LangGraph-based Level 3 pipeline

        Args:
            text: Input text to analyze
            task_type: Type of task (bug, idea, feedback, etc.)
            max_iterations: Maximum number of graph iterations

        Returns:
            Analysis results with all agent outputs
        """
        # Initialize state
        initial_state = GraphState(
            input_text=text,
            task_type=task_type,
            messages=[HumanMessage(content=text)]
        )

        # Compile and run the graph
        compiled_graph = self.graph.compile()
        result = compiled_graph.invoke(initial_state)

        # The result is a dictionary, extract the values
        return {
            "input_text": result.get("input_text", initial_state.input_text),
            "task_type": result.get("task_type", initial_state.task_type),
            "risk": result.get("risk_assessment"),
            "resources": result.get("resource_analysis"),
            "impact": result.get("impact_evaluation"),
            "confidence_urgency": result.get("confidence_urgency"),
            "prioritization": result.get("prioritization"),
            "messages": [msg.model_dump() for msg in result.get("messages", [])]
        }

# Create a global instance for easy access
level3_graph_agent = Level3GraphAgent()
