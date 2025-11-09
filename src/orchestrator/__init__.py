
"""
Orchestrator Module

This module coordinates the workflow between different agents and levels.
"""

from .main_orchestrator import main_orchestrator
from .main_orchestrator_langgraph_full import main_orchestrator_langgraph_full

# Global instances for easy access
main_orchestrator = main_orchestrator
main_orchestrator_langgraph = main_orchestrator_langgraph_full

# Set the default orchestrator to use LangGraph
default_orchestrator = main_orchestrator_langgraph_full
