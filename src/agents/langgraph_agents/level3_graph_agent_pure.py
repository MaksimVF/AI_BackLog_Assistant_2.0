


"""
Level 3 Graph Agent - Pure LangGraph Implementation

This module implements the Level 3 agents using LangGraph without depending on old agents.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage

# Configure logging
logger = logging.getLogger(__name__)

class GraphState(BaseModel):
    """State for the Level 3 graph processing"""
    input_text: str
    confidence_urgency_result: Optional[Dict[str, Any]] = None
    risk_assessment_result: Optional[Dict[str, Any]] = None
    impact_potential_result: Optional[Dict[str, Any]] = None
    resource_availability_result: Optional[Dict[str, Any]] = None
    prioritization_result: Optional[Dict[str, Any]] = None
    messages: List[Any] = []

class Level3GraphAgentPure:
    """Agent that uses LangGraph to coordinate Level 3 processing without old agents"""

    def __init__(self):
        """Initialize the Level 3 Graph Agent"""
        logger.info("Initializing Level 3 Graph Agent (Pure LangGraph)")

        # Create the graph
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create the LangGraph for Level 3 processing"""
        graph = StateGraph(GraphState)

        # Add nodes for each processing step
        graph.add_node("confidence_urgency", self._run_confidence_urgency)
        graph.add_node("risk_assessment", self._run_risk_assessment)
        graph.add_node("impact_potential", self._run_impact_potential)
        graph.add_node("resource_availability", self._run_resource_availability)
        graph.add_node("prioritization", self._run_prioritization)

        # Define the execution flow without cycles
        graph.set_entry_point("confidence_urgency")
        graph.add_edge("confidence_urgency", "risk_assessment")
        graph.add_edge("risk_assessment", "impact_potential")
        graph.add_edge("impact_potential", "resource_availability")
        graph.add_edge("resource_availability", "prioritization")
        graph.set_finish_point("prioritization")  # Set final node

        return graph

    def _run_confidence_urgency(self, state: GraphState) -> GraphState:
        """Run confidence and urgency scoring"""
        if state.confidence_urgency_result is None:
            # Implement confidence and urgency logic directly
            result = self._calculate_confidence_urgency(state.input_text)
            state.confidence_urgency_result = result
            state.messages.append(AIMessage(content="Confidence and urgency scoring completed"))

        return state

    def _run_risk_assessment(self, state: GraphState) -> GraphState:
        """Run risk assessment"""
        if state.risk_assessment_result is None and state.confidence_urgency_result:
            # Implement risk assessment logic directly
            result = self._assess_risk(state.input_text)
            state.risk_assessment_result = result
            state.messages.append(AIMessage(content="Risk assessment completed"))

        return state

    def _run_impact_potential(self, state: GraphState) -> GraphState:
        """Run impact potential analysis"""
        if state.impact_potential_result is None and state.risk_assessment_result:
            # Implement impact potential logic directly
            result = self._assess_impact_potential(state.input_text, state.risk_assessment_result)
            state.impact_potential_result = result
            state.messages.append(AIMessage(content="Impact potential analysis completed"))

        return state

    def _run_resource_availability(self, state: GraphState) -> GraphState:
        """Run resource availability analysis"""
        if state.resource_availability_result is None and state.impact_potential_result:
            # Implement resource availability logic directly
            result = self._assess_resource_availability(state.input_text, state.impact_potential_result)
            state.resource_availability_result = result
            state.messages.append(AIMessage(content="Resource availability analysis completed"))

        return state

    def _run_prioritization(self, state: GraphState) -> GraphState:
        """Run task prioritization"""
        if state.prioritization_result is None and state.resource_availability_result:
            # Implement prioritization logic directly
            result = self._prioritize_task(
                state.input_text,
                state.confidence_urgency_result,
                state.risk_assessment_result,
                state.impact_potential_result,
                state.resource_availability_result
            )
            state.prioritization_result = result
            state.messages.append(AIMessage(content="Task prioritization completed"))

        return state

    def _calculate_confidence_urgency(self, input_text: str) -> Dict[str, Any]:
        """Calculate confidence and urgency scores"""
        # Base scores
        confidence = 0.7  # default confidence
        urgency = 3.0  # default urgency

        # Increase urgency for time-sensitive keywords
        urgency_keywords = ["urgent", "immediate", "ASAP", "deadline", "critical", "blocker"]
        for keyword in urgency_keywords:
            if keyword in input_text.lower():
                urgency += 2.0

        # Increase confidence for clear, detailed descriptions
        detail_indicators = ["steps", "plan", "requirements", "specification", "detailed"]
        for indicator in detail_indicators:
            if indicator in input_text.lower():
                confidence = min(0.95, confidence + 0.1)

        # Cap urgency at 10
        urgency = min(10.0, urgency)

        return {
            "confidence": confidence,
            "urgency": urgency,
            "rationale": "Calculated based on keywords and text analysis"
        }

    def _assess_risk(self, input_text: str) -> Dict[str, Any]:
        """Assess risk using simple heuristics"""
        # Simple heuristic: longer texts and certain keywords increase risk
        risk = 3.0  # base risk

        # Increase risk for certain keywords
        keywords = ["urgent", "critical", "blocker", "security", "vulnerability", "deadline"]
        for keyword in keywords:
            if keyword in input_text.lower():
                risk += 1.5

        # Increase risk for longer texts (more complexity)
        word_count = len(input_text.split())
        if word_count > 100:
            risk += 1.0
        if word_count > 200:
            risk += 1.0

        # Cap at 10
        risk = min(10.0, risk)

        return {
            "score": risk,
            "method": "heuristic",
            "details": {
                "keywords_detected": [kw for kw in keywords if kw in input_text.lower()],
                "word_count": word_count
            }
        }

    def _assess_impact_potential(self, input_text: str, risk_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess impact potential"""
        # Base impact on risk score
        risk_score = risk_result.get("score", 3.0)
        base_impact = risk_score * 0.7  # Impact correlates with risk

        # Increase impact for certain keywords
        impact_keywords = ["all users", "entire system", "core functionality", "major", "significant"]
        for keyword in impact_keywords:
            if keyword in input_text.lower():
                base_impact += 1.5

        # Cap impact at 10
        impact_score = min(10.0, base_impact)

        return {
            "score": impact_score,
            "method": "heuristic",
            "details": {
                "base_impact": base_impact,
                "impact_keywords": [kw for kw in impact_keywords if kw in input_text.lower()]
            }
        }

    def _assess_resource_availability(self, input_text: str, impact_result: Dict[str, Any]) -> Dict[str, Any]:
        """Assess resource availability"""
        # Base resource score (higher means more resources available)
        resource_score = 7.0  # default

        # Decrease resources for complex tasks
        complexity_keywords = ["complex", "difficult", "challenging", "multiple teams", "cross-functional"]
        for keyword in complexity_keywords:
            if keyword in input_text.lower():
                resource_score -= 1.5

        # Cap resource score between 1 and 10
        resource_score = min(10.0, max(1.0, resource_score))

        return {
            "score": resource_score,
            "method": "heuristic",
            "details": {
                "complexity_keywords": [kw for kw in complexity_keywords if kw in input_text.lower()]
            }
        }

    def _prioritize_task(self, input_text: str, confidence_result: Dict[str, Any], risk_result: Dict[str, Any], impact_result: Dict[str, Any], resource_result: Dict[str, Any]) -> Dict[str, Any]:
        """Prioritize task based on all factors"""
        # Extract scores
        confidence = confidence_result.get("confidence", 0.7)
        urgency = confidence_result.get("urgency", 3.0)
        risk = risk_result.get("score", 3.0)
        impact = impact_result.get("score", 3.0)
        resources = resource_result.get("score", 7.0)

        # Calculate priority score
        # Weighted formula: (risk + impact) * confidence - (10 - resources) + urgency
        priority_score = (risk + impact) * confidence - (10 - resources) + urgency

        # Determine priority level
        if priority_score > 15:
            priority_level = "High"
        elif priority_score > 8:
            priority_level = "Medium"
        else:
            priority_level = "Low"

        return {
            "priority_score": priority_score,
            "priority_level": priority_level,
            "details": {
                "confidence": confidence,
                "urgency": urgency,
                "risk": risk,
                "impact": impact,
                "resources": resources
            }
        }

    def analyze_task(self, input_text: str, task_type: str = "general") -> Dict[str, Any]:
        """
        Analyze task using pure LangGraph

        Args:
            input_text: Text to analyze
            task_type: Type of task (from Level 2)

        Returns:
            Analysis results
        """
        # Initialize state
        initial_state = GraphState(
            input_text=input_text,
            messages=[HumanMessage(content="Analyzing task with Level 3")]
        )

        # Compile and run the graph
        compiled_graph = self.graph.compile()
        result = compiled_graph.invoke(initial_state)

        # The result is a dictionary, extract the values
        return {
            "confidence_urgency": result.get("confidence_urgency_result"),
            "risk_assessment": result.get("risk_assessment_result"),
            "impact_potential": result.get("impact_potential_result"),
            "resource_availability": result.get("resource_availability_result"),
            "prioritization": result.get("prioritization_result"),
            "messages": [msg.model_dump() for msg in result.get("messages", [])]
        }

# Create a global instance for easy access
level3_graph_agent_pure = Level3GraphAgentPure()


