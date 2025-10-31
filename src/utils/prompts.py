
"""
Prompts Module

This module contains all the LLM prompts used across different levels
for consistent and maintainable prompt management.
"""

# Level 2 Prompts
REFLECTION_PROMPT = """
Classify the following text as either "idea", "bug", or "feedback":
{input_text}

Return only the classification type.
"""

CONTEXTUALIZA_PROMPT = """
Extract entities and determine the domain from the following text:
{input_text}

Return a JSON object with "entities" (list of entity objects with type, text, and confidence)
and "domain" (string).
"""

# Level 3 Prompts
RISK_ASSESSMENT_PROMPT = """
Assess the risk (0-10) for the following task:
{input_text}

Return only the risk score as a number.
"""

RESOURCE_AVAILABILITY_PROMPT = """
Estimate the resource needs for the following task:
{input_text}

Return a JSON object with resource categories and estimated amounts.
"""

IMPACT_POTENTIAL_PROMPT = """
Measure the potential impact (0-10) for the following task:
{input_text}

Return only the impact score as a number.
"""

CONFIDENCE_URGENCY_PROMPT = """
Score the confidence and urgency (0-10) for the following task:
{input_text}

Return a JSON object with "confidence" and "urgency" scores.
"""

# Level 4 Prompts
SUMMARY_PROMPT = """
Based on the following analysis data, recommend whether to implement or delay the task:
{analyzed_data}

Return a JSON object with "recommendation" (implement/delay) and "reason".
"""

RISK_MITIGATION_PROMPT = """
Given the following task analysis with high risk score, suggest specific risk mitigation strategies:
{analysis_data}

Return a JSON object with "mitigation_strategies" (list of strategies) and "alternative_approaches" (list).
"""

RESOURCE_OPTIMIZATION_PROMPT = """
Based on the following task analysis and team workload, recommend optimal resource allocation:
{analysis_data}
{team_workload}

Return a JSON object with "team_assignments" (dict of team:tasks) and "reallocation_suggestions" (list).
"""

CONTEXTUAL_RECOMMENDATION_PROMPT = """
Considering the following task analysis, project timeline, and team workload, provide a comprehensive recommendation:
{analysis_data}
{project_timeline}
{team_workload}

Return a JSON object with "recommendation", "rationale", "priority", and "next_steps".
"""
