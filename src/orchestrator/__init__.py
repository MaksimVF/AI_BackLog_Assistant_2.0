
"""
Orchestrator Module

This module coordinates the workflow between different agents and levels.
"""

# Note: Only importing modules that actually exist
from .main_orchestrator_langgraph_pure import main_orchestrator_langgraph_pure
from .main_orchestrator_pure import main_orchestrator_pure

# Global instances for easy access
# Using main_orchestrator_pure as the default main_orchestrator
main_orchestrator = main_orchestrator_pure
main_orchestrator_langgraph_pure = main_orchestrator_langgraph_pure
main_orchestrator_pure = main_orchestrator_pure

# Set the default orchestrator to use pure LangGraph for all levels
default_orchestrator = main_orchestrator_pure
