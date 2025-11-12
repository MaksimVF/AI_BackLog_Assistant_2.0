

"""
Level 4 Graph Agent

This module implements the Level 4 agents using LangGraph for enhanced
coordination and processing.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage

# Import existing agents for integration
from src.agents.level4.aggregator_agent import AggregatorAgent
from src.agents.level4.summary_agent import SummaryAgent
from src.agents.level4.visualization_agent import VisualizationAgent

# Configure logging
logger = logging.getLogger(__name__)

class GraphState(BaseModel):
    """State for the Level 4 graph processing"""
    level3_data: Dict[str, Any]
    aggregation_result: Optional[Dict[str, Any]] = None
    visualization_result: Optional[Dict[str, Any]] = None
    summary_result: Optional[Dict[str, Any]] = None
    enhanced_summary: Optional[Dict[str, Any]] = None
    messages: List[Any] = []

class Level4GraphAgent:
    """Agent that uses LangGraph to coordinate Level 4 processing"""

    def __init__(self):
        """Initialize the Level 4 Graph Agent"""
        logger.info("Initializing Level 4 Graph Agent")

        # Initialize component agents
        self.aggregator_agent = AggregatorAgent()
        self.summary_agent = SummaryAgent()
        self.visualization_agent = VisualizationAgent()

        # Create the graph
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create the LangGraph for Level 4 processing"""
        graph = StateGraph(GraphState)

        # Add nodes for each processing step
        graph.add_node("aggregation", self._run_aggregation)
        graph.add_node("visualization", self._run_visualization)
        graph.add_node("summary", self._run_summary)
        graph.add_node("enhanced_summary", self._run_enhanced_summary)

        # Define the execution flow without cycles
        graph.set_entry_point("aggregation")
        graph.add_edge("aggregation", "visualization")
        graph.add_edge("visualization", "summary")
        graph.add_edge("summary", "enhanced_summary")
        graph.set_finish_point("enhanced_summary")  # Set final node

        return graph

    def _run_aggregation(self, state: GraphState) -> GraphState:
        """Run data aggregation"""
        if state.aggregation_result is None:
            result = self.aggregator_agent.generate_summary(state.level3_data)
            state.aggregation_result = result
            state.messages.append(AIMessage(content="Aggregation completed"))

        return state

    def _run_visualization(self, state: GraphState) -> GraphState:
        """Run visualization generation"""
        if state.visualization_result is None and state.aggregation_result:
            # Enhance data for visualization
            enhanced_data = self._enhance_analysis_data(state.aggregation_result)
            result = self.visualization_agent.generate_visualization(enhanced_data)
            state.visualization_result = result
            state.messages.append(AIMessage(content="Visualization generated"))

        return state

    def _run_summary(self, state: GraphState) -> GraphState:
        """Run summary generation"""
        if state.summary_result is None and state.aggregation_result:
            result = self.summary_agent.generate_summary(state.aggregation_result)
            state.summary_result = result
            state.messages.append(AIMessage(content="Summary generated"))

        return state

    def _run_enhanced_summary(self, state: GraphState) -> GraphState:
        """Run enhanced summary generation"""
        if state.enhanced_summary is None and state.aggregation_result:
            # Get project context
            project_context = self._get_project_context()

            # Generate enhanced recommendation
            result = self.summary_agent.generate_enhanced_recommendation(
                state.aggregation_result, project_context
            )
            state.enhanced_summary = result
            state.messages.append(AIMessage(content="Enhanced summary generated"))

        return state

    def _get_project_context(self) -> Dict[str, Any]:
        """Get project context data for enhanced recommendations"""
        # Sample project context data - in a real implementation, this would come from a database
        return {
            "project_timeline": {
                "current_sprint_end": "2025-11-15",
                "next_milestone": "2025-12-01",
                "project_deadline": "2026-01-31"
            },
            "team_workload": {
                "Backend Team": {
                    "current_tasks": 12,
                    "capacity": 15,
                    "skills": ["Python", "Django", "PostgreSQL"]
                },
                "Frontend Team": {
                    "current_tasks": 8,
                    "capacity": 12,
                    "skills": ["React", "JavaScript", "CSS"]
                },
                "QA Team": {
                    "current_tasks": 6,
                    "capacity": 10,
                    "skills": ["Testing", "Automation", "QA"]
                }
            },
            "resource_constraints": {
                "budget_remaining": 5000,
                "available_hours": 240
            }
        }

    def _enhance_analysis_data(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance analysis data with additional information for visualizations"""
        # Add sample status distribution data
        enhanced_data = analysis_data.copy()

        # Add status distribution for pie chart
        enhanced_data["status_distribution"] = {
            "new": 5,
            "in_progress": 8,
            "completed": 12,
            "on_hold": 3,
            "cancelled": 1
        }

        # Add trend data for line chart
        from datetime import datetime, timedelta
        today = datetime.now()
        enhanced_data["trend_data"] = [
            {
                "date": (today - timedelta(days=i)).strftime("%Y-%m-%d"),
                "value": 3 + i,
                "metric": "Task Completion Rate"
            }
            for i in range(7)
        ]

        # Add resource allocation data for grouped bar chart
        enhanced_data["resource_allocation"] = {
            "Backend Team": {"bugs": 3, "features": 5, "refactoring": 2},
            "Frontend Team": {"bugs": 2, "features": 4, "design": 3},
            "QA Team": {"testing": 6, "automation": 2}
        }

        return enhanced_data

    def process_recommendations(self, level3_data: Dict[str, Any], max_iterations: int = 3) -> Dict[str, Any]:
        """
        Process Level 4 recommendations and visualizations using LangGraph

        Args:
            level3_data: Outputs from Level 3 agents
            max_iterations: Maximum number of graph iterations

        Returns:
            Recommendations and visualizations
        """
        # Initialize state
        initial_state = GraphState(
            level3_data=level3_data,
            messages=[HumanMessage(content="Processing Level 4 recommendations")]
        )

        # Compile and run the graph
        compiled_graph = self.graph.compile()
        result = compiled_graph.invoke(initial_state)

        # The result is a dictionary, extract the values
        return {
            "aggregation": result.get("aggregation_result"),
            "visualization": result.get("visualization_result"),
            "summary": result.get("summary_result"),
            "enhanced_summary": result.get("enhanced_summary"),
            "messages": [msg.model_dump() for msg in result.get("messages", [])]
        }

# Create a global instance for easy access
level4_graph_agent = Level4GraphAgent()

