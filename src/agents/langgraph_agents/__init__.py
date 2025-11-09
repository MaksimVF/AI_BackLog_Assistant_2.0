
"""
LangGraph Agents Module

This module provides LangGraph-based implementations of analytical agents
for enhanced processing and coordination.
"""

from .level1_graph_agent import Level1GraphAgent
from .level1_graph_orchestrator import Level1GraphOrchestrator

# Global instances for easy access
level1_graph_agent = Level1GraphAgent()
level1_graph_orchestrator = Level1GraphOrchestrator()
