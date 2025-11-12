
"""
LangGraph Agents Module

This module provides LangGraph-based implementations of analytical agents
for enhanced processing and coordination.
"""

# Import pure versions of agents and orchestrators
from .level1_graph_agent_pure import Level1GraphAgentPure as Level1GraphAgent
from .level1_graph_orchestrator_pure import Level1GraphOrchestratorPure

# Global instances for easy access
level1_graph_agent = Level1GraphAgent()
level1_graph_orchestrator = Level1GraphOrchestratorPure()
