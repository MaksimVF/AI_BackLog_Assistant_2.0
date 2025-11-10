
"""
Orchestrator Module

This module coordinates the workflow between different agents and levels.
"""

from .main_orchestrator import main_orchestrator
from .main_orchestrator_langgraph_full import main_orchestrator_langgraph_full
from .main_orchestrator_langgraph_pure import main_orchestrator_langgraph_pure

# Global instances for easy access
main_orchestrator = main_orchestrator
main_orchestrator_langgraph = main_orchestrator_langgraph_full
main_orchestrator_langgraph_pure = main_orchestrator_langgraph_pure

# Set the default orchestrator to use pure LangGraph for Level 4
default_orchestrator = main_orchestrator_langgraph_pure
