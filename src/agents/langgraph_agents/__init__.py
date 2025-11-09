
"""
LangGraph Agents Module

This module provides LangGraph-based implementations of analytical agents
for enhanced processing and coordination.
"""

from .level2_graph_agent import Level2GraphAgent
from .level2_graph_orchestrator import Level2GraphOrchestrator
from .level3_graph_agent import Level3GraphAgent
from .level3_graph_orchestrator import Level3GraphOrchestrator
from .level4_graph_agent import Level4GraphAgent
from .level4_graph_orchestrator import Level4GraphOrchestrator

# Global instances for easy access
level2_graph_agent = Level2GraphAgent()
level2_graph_orchestrator = Level2GraphOrchestrator()
level3_graph_agent = Level3GraphAgent()
level3_graph_orchestrator = Level3GraphOrchestrator()
level4_graph_agent = Level4GraphAgent()
level4_graph_orchestrator = Level4GraphOrchestrator()
