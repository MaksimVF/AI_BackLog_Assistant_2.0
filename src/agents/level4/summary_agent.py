





"""
Summary Agent Module

This module generates final recommendations and summaries based on aggregated analysis.
"""

import logging
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from src.utils.llm_client import llm_client
from src.utils.prompts import SUMMARY_PROMPT, RISK_MITIGATION_PROMPT, RESOURCE_OPTIMIZATION_PROMPT

# Configure logging
logger = logging.getLogger(__name__)

class SummaryResult(BaseModel):
    """Data model for summary results"""
    recommendation: str
    rationale: str
    priority: str  # High, Medium, Low
    next_steps: Optional[List[str]] = None

class SummaryAgent:
    """Agent for generating final summaries and recommendations"""

    def __init__(self):
        """Initialize the Summary Agent"""
        logger.info("Initializing Summary Agent")

    def _generate_recommendation(self, analysis: Dict[str, Any]) -> str:
        """Generate a recommendation based on analysis"""
        overall_score = analysis.get("overall_score", 0)
        confidence = analysis.get("confidence", 0.5)

        if confidence < 0.4:
            return "Needs clarification before proceeding"
        elif overall_score > 7:
            return "Implement immediately"
        elif overall_score > 4:
            return "Schedule for next sprint"
        else:
            return "Consider for backlog"

    def _generate_rationale(self, analysis: Dict[str, Any]) -> str:
        """Generate rationale for the recommendation"""
        risk = analysis.get("risk_score", 0)
        impact = analysis.get("impact_score", 0)
        urgency = analysis.get("urgency", 0)

        rationale_parts = []

        if risk > 7:
            rationale_parts.append(f"High risk score ({risk:.1f})")
        if impact > 7:
            rationale_parts.append(f"High impact potential ({impact:.1f})")
        if urgency > 7:
            rationale_parts.append(f"High urgency ({urgency:.1f})")

        if not rationale_parts:
            rationale_parts.append("Standard task with balanced metrics")

        return " - ".join(rationale_parts)

    def _generate_priority(self, analysis: Dict[str, Any]) -> str:
        """Generate priority level"""
        overall_score = analysis.get("overall_score", 0)

        if overall_score > 7:
            return "High"
        elif overall_score > 4:
            return "Medium"
        else:
            return "Low"

    def _generate_next_steps(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate suggested next steps"""
        recommendation = analysis.get("recommendation", "")
        priority = analysis.get("priority", "Low")

        steps = []

        if priority == "High":
            steps.extend([
                "Assign to senior developer",
                "Schedule immediate review",
                "Prepare implementation plan"
            ])
        elif priority == "Medium":
            steps.extend([
                "Add to sprint backlog",
                "Estimate effort",
                "Plan for next iteration"
            ])
        else:
            steps.extend([
                "Add to idea backlog",
                "Revisit during next planning session"
            ])

        return steps

    def _generate_risk_mitigation(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate risk mitigation strategies for high-risk tasks"""
        risk_score = analysis.get("risk_score", 0)

        if risk_score < 6:
            return {
                "mitigation_strategies": ["No specific mitigation needed"],
                "alternative_approaches": []
            }

        try:
            # Use LLM for risk mitigation strategies
            analysis_str = str(analysis)
            prompt = RISK_MITIGATION_PROMPT.format(analysis_data=analysis_str)
            response = llm_client.generate_json(prompt)

            if response and "mitigation_strategies" in response:
                return {
                    "mitigation_strategies": response.get("mitigation_strategies", []),
                    "alternative_approaches": response.get("alternative_approaches", [])
                }

        except Exception as e:
            logger.warning(f"LLM risk mitigation failed, using heuristic: {e}")
            # Fallback to heuristic
            strategies = []
            alternatives = []

            if risk_score > 8:
                strategies.extend([
                    "Conduct thorough risk assessment",
                    "Implement in controlled environment",
                    "Add comprehensive testing"
                ])
                alternatives.append("Consider alternative implementation approach")

            return {
                "mitigation_strategies": strategies,
                "alternative_approaches": alternatives
            }

        return {
            "mitigation_strategies": [],
            "alternative_approaches": []
        }

    def _generate_resource_optimization(self, analysis: Dict[str, Any], team_workload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate resource optimization recommendations"""
        try:
            # Use LLM for resource optimization
            analysis_str = str(analysis)
            workload_str = str(team_workload)
            prompt = RESOURCE_OPTIMIZATION_PROMPT.format(
                analysis_data=analysis_str,
                team_workload=workload_str
            )
            response = llm_client.generate_json(prompt)

            if response and "team_assignments" in response:
                return {
                    "team_assignments": response.get("team_assignments", {}),
                    "reallocation_suggestions": response.get("reallocation_suggestions", [])
                }

        except Exception as e:
            logger.warning(f"LLM resource optimization failed, using heuristic: {e}")
            # Fallback to heuristic
            return {
                "team_assignments": {
                    "Backend Team": ["bug_fixes", "api_integration"],
                    "Frontend Team": ["ui_improvements"],
                    "QA Team": ["testing"]
                },
                "reallocation_suggestions": ["Consider reallocating resources from lower priority tasks"]
            }

        return {
            "team_assignments": {},
            "reallocation_suggestions": []
        }

    def _generate_contextual_recommendation(self, analysis: Dict[str, Any], project_timeline: Dict[str, Any], team_workload: Dict[str, Any]) -> Dict[str, Any]:
        """Generate contextual recommendation considering project timeline and team workload"""
        try:
            # Use LLM for contextual recommendation
            analysis_str = str(analysis)
            timeline_str = str(project_timeline)
            workload_str = str(team_workload)

            prompt = CONTEXTUAL_RECOMMENDATION_PROMPT.format(
                analysis_data=analysis_str,
                project_timeline=timeline_str,
                team_workload=workload_str
            )
            response = llm_client.generate_json(prompt)

            if response and "recommendation" in response:
                return {
                    "recommendation": response.get("recommendation", "Needs review"),
                    "rationale": response.get("rationale", "Contextual analysis"),
                    "priority": response.get("priority", "Medium"),
                    "next_steps": response.get("next_steps", [])
                }

        except Exception as e:
            logger.warning(f"LLM contextual recommendation failed, using heuristic: {e}")
            # Fallback to heuristic
            return {
                "recommendation": self._generate_recommendation(analysis),
                "rationale": self._generate_rationale(analysis),
                "priority": self._generate_priority(analysis),
                "next_steps": self._generate_next_steps(analysis)
            }

        return {
            "recommendation": "Needs review",
            "rationale": "Contextual analysis failed",
            "priority": "Medium",
            "next_steps": []
        }

    def generate_summary(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive summary and recommendation

        Args:
            analysis: Aggregated analysis data

        Returns:
            Summary result
        """
        # Try to use LLM for summary generation if available
        try:
            # Prepare analysis data for LLM
            analysis_str = str(analysis)

            # Use LLM for summary generation
            prompt = SUMMARY_PROMPT.format(analyzed_data=analysis_str)
            response = llm_client.generate_json(prompt)

            if response and "recommendation" in response and not response.get("error"):
                # Parse LLM response
                return {
                    "recommendation": response.get("recommendation", "Needs review"),
                    "rationale": response.get("reason", "LLM-based analysis"),
                    "priority": analysis.get("priority", "Medium"),
                    "next_steps": response.get("next_steps", []),
                    "analysis": analysis,
                    "method": "llm"
                }

        except Exception as e:
            logger.warning(f"LLM summary generation failed, falling back to heuristic: {e}")
            # Fallback to heuristic
            # Generate recommendation
            recommendation = self._generate_recommendation(analysis)

            # Generate rationale
            rationale = self._generate_rationale(analysis)

            # Generate priority
            priority = self._generate_priority(analysis)

            # Generate next steps
            next_steps = self._generate_next_steps(analysis)

            return {
                "recommendation": recommendation,
                "rationale": rationale,
                "priority": priority,
                "next_steps": next_steps,
                "analysis": analysis,
                "method": "heuristic_fallback"
            }

        # Fallback to heuristic if LLM response is not usable
        # Generate recommendation
        recommendation = self._generate_recommendation(analysis)

        # Generate rationale
        rationale = self._generate_rationale(analysis)

        # Generate priority
        priority = self._generate_priority(analysis)

        # Generate next steps
        next_steps = self._generate_next_steps(analysis)

        return {
            "recommendation": recommendation,
            "rationale": rationale,
            "priority": priority,
            "next_steps": next_steps,
            "analysis": analysis,
            "method": "heuristic_fallback"
        }

    def generate_enhanced_recommendation(self, analysis: Dict[str, Any], project_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Generate an enhanced recommendation with risk mitigation, resource optimization, and contextual analysis

        Args:
            analysis: Aggregated analysis data
            project_context: Optional project context including timeline and team workload

        Returns:
            Enhanced recommendation with additional insights
        """
        # Basic summary
        summary = self.generate_summary(analysis)

        # Add risk mitigation
        risk_mitigation = self._generate_risk_mitigation(analysis)

        # Add resource optimization (if project context available)
        resource_optimization = {}
        if project_context and "team_workload" in project_context:
            resource_optimization = self._generate_resource_optimization(analysis, project_context["team_workload"])

        # Add contextual recommendation (if project context available)
        contextual_recommendation = {}
        if project_context and "project_timeline" in project_context and "team_workload" in project_context:
            contextual_recommendation = self._generate_contextual_recommendation(
                analysis, project_context["project_timeline"], project_context["team_workload"]
            )

        # Combine all recommendations
        enhanced_result = {
            "summary": summary,
            "risk_mitigation": risk_mitigation,
            "resource_optimization": resource_optimization,
            "contextual_recommendation": contextual_recommendation,
            "analysis": analysis
        }

        return enhanced_result

# Create a global instance for easy access
summary_agent = SummaryAgent()
