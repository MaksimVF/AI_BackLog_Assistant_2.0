
"""
LangGraph Agents Module

This module provides LangGraph-based implementations of analytical agents
for enhanced processing and coordination.
"""

from .level2_graph_agent import Level2GraphAgent
from .level2_graph_orchestrator import Level2GraphOrchestrator

# Global instances for easy access
level2_graph_agent = Level2GraphAgent()
level2_graph_orchestrator = Level2GraphOrchestrator()
