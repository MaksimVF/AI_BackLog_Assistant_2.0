


"""
Level 2 Graph Agent - Pure LangGraph Implementation

This module implements the Level 2 agents using LangGraph without depending on old agents.
"""

import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from langgraph.graph import StateGraph
from langchain_core.messages import HumanMessage, AIMessage

# Configure logging
logger = logging.getLogger(__name__)

class GraphState(BaseModel):
    """State for the Level 2 graph processing"""
    input_text: str
    classification_result: Optional[Dict[str, Any]] = None
    contextualization_result: Optional[Dict[str, Any]] = None
    reflection_result: Optional[Dict[str, Any]] = None
    messages: List[Any] = []

class Level2GraphAgentPure:
    """Agent that uses LangGraph to coordinate Level 2 processing without old agents"""

    def __init__(self):
        """Initialize the Level 2 Graph Agent"""
        logger.info("Initializing Level 2 Graph Agent (Pure LangGraph)")

        # Create the graph
        self.graph = self._create_graph()

    def _create_graph(self) -> StateGraph:
        """Create the LangGraph for Level 2 processing"""
        graph = StateGraph(GraphState)

        # Add nodes for each processing step
        graph.add_node("classification", self._run_classification)
        graph.add_node("contextualization", self._run_contextualization)
        graph.add_node("reflection", self._run_reflection)

        # Define the execution flow without cycles
        graph.set_entry_point("classification")
        graph.add_edge("classification", "contextualization")
        graph.add_edge("contextualization", "reflection")
        graph.set_finish_point("reflection")  # Set final node

        return graph

    def _run_classification(self, state: GraphState) -> GraphState:
        """Run task classification"""
        if state.classification_result is None:
            # Implement classification logic directly
            result = self._classify_task(state.input_text)
            state.classification_result = result
            state.messages.append(AIMessage(content="Task classification completed"))

        return state

    def _run_contextualization(self, state: GraphState) -> GraphState:
        """Run contextualization"""
        if state.contextualization_result is None and state.classification_result:
            # Implement contextualization logic directly
            result = self._contextualize_task(state.input_text, state.classification_result)
            state.contextualization_result = result
            state.messages.append(AIMessage(content="Contextualization completed"))

        return state

    def _run_reflection(self, state: GraphState) -> GraphState:
        """Run reflection analysis"""
        if state.reflection_result is None and state.contextualization_result:
            # Implement reflection logic directly
            result = self._reflect_on_task(state.input_text, state.classification_result, state.contextualization_result)
            state.reflection_result = result
            state.messages.append(AIMessage(content="Reflection analysis completed"))

        return state

    def _classify_task(self, input_text: str) -> Dict[str, Any]:
        """Classify the task type using rule-based approach"""
        # Simple keyword-based classification
        text_lower = input_text.lower()

        # Define patterns for different task types
        patterns = {
            "bug": ["bug", "error", "issue", "problem", "defect", "failure", "crash"],
            "idea": ["idea", "feature", "proposal", "improvement", "enhancement"],
            "feedback": ["feedback", "comment", "suggestion", "opinion"],
            "question": ["question", "ask", "how", "what", "why", "when", "where", "who"],
            "request": ["request", "need", "require", "please", "can you", "could you"]
        }

        # Check for patterns
        detected_type = "general"
        confidence = 0.5

        for task_type, keywords in patterns.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_type = task_type
                    confidence = 0.8
                    break
            if detected_type != "general":
                break

        return {
            "task_type": detected_type,
            "confidence": confidence,
            "sub_category": None,
            "metadata": {
                "input_length": len(input_text),
                "keyword_detected": detected_type != "general",
                "method": "rule_based"
            }
        }

    def _classify_task_with_llm(self, input_text: str) -> Dict[str, Any]:
        """Classify the task type using LLM for more nuanced understanding"""
        from src.utils.llm_client import llm_client

        prompt = f"""
        Classify the following task into one of these categories: bug, idea, feedback, question, request.
        Provide your response as JSON with fields: task_type, confidence, rationale.

        Task: {input_text}
        """

        try:
            llm_response = llm_client.generate_json(prompt)

            # Validate the response
            if "error" in llm_response:
                logger.warning(f"LLM classification error: {llm_response['error']}")
                # Fall back to rule-based approach
                return self._classify_task(input_text)

            return {
                "task_type": llm_response.get("task_type", "general"),
                "confidence": llm_response.get("confidence", 0.75),
                "sub_category": None,
                "metadata": {
                    "input_length": len(input_text),
                    "method": "llm_based",
                    "rationale": llm_response.get("rationale", "LLM analysis")
                }
            }
        except Exception as e:
            logger.warning(f"LLM classification failed: {e}")
            # Fall back to rule-based approach
            return self._classify_task(input_text)

    def _run_classification(self, state: GraphState) -> GraphState:
        """Run task classification with LLM enhancement and fallback"""
        if state.classification_result is None:
            # Try LLM-based classification first, fall back to rule-based if needed
            result = self._classify_task_with_llm(state.input_text)
            state.classification_result = result
            state.messages.append(AIMessage(content="Task classification completed"))

        return state

    def _contextualize_task(self, input_text: str, classification_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract context from the task using rule-based approach"""
        task_type = classification_result.get("task_type", "general")

        # Simple entity extraction
        entities = []
        words = input_text.split()

        # Extract potential entities (simple approach)
        for i, word in enumerate(words):
            if len(word) > 3 and word[0].isupper():  # Simple proper noun detection
                entities.append({
                    "entity_type": "potential_entity",
                    "text": word,
                    "start_index": sum(len(w) + 1 for w in words[:i]),
                    "end_index": sum(len(w) + 1 for w in words[:i]) + len(word),
                    "confidence": 0.7
                })

        # Determine domain based on keywords
        domain = "general"
        tech_keywords = ["api", "database", "server", "frontend", "backend", "code", "python", "javascript"]
        business_keywords = ["sales", "marketing", "finance", "customer", "revenue", "profit"]

        text_lower = input_text.lower()
        if any(keyword in text_lower for keyword in tech_keywords):
            domain = "technology"
        elif any(keyword in text_lower for keyword in business_keywords):
            domain = "business"

        return {
            "domain": domain,
            "entities": entities,
            "metadata": {
                "task_type": task_type,
                "entity_count": len(entities),
                "method": "rule_based"
            }
        }

    def _contextualize_task_with_llm(self, input_text: str, classification_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract context from the task using LLM for advanced NLP"""
        from src.utils.llm_client import llm_client

        task_type = classification_result.get("task_type", "general")

        prompt = f"""
        Analyze the following task and extract context information.
        Identify entities, determine the domain, and provide any relevant context.
        Provide your response as JSON with fields: domain, entities, rationale.

        Task: {input_text}
        Task Type: {task_type}
        """

        try:
            llm_response = llm_client.generate_json(prompt)

            # Validate the response
            if "error" in llm_response:
                logger.warning(f"LLM contextualization error: {llm_response['error']}")
                # Fall back to rule-based approach
                return self._contextualize_task(input_text, classification_result)

            return {
                "domain": llm_response.get("domain", "general"),
                "entities": llm_response.get("entities", []),
                "metadata": {
                    "task_type": task_type,
                    "method": "llm_based",
                    "rationale": llm_response.get("rationale", "LLM analysis")
                }
            }
        except Exception as e:
            logger.warning(f"LLM contextualization failed: {e}")
            # Fall back to rule-based approach
            return self._contextualize_task(input_text, classification_result)

    def _run_contextualization(self, state: GraphState) -> GraphState:
        """Run contextualization with LLM enhancement and fallback"""
        if state.contextualization_result is None and state.classification_result:
            # Try LLM-based contextualization first, fall back to rule-based if needed
            result = self._contextualize_task_with_llm(state.input_text, state.classification_result)
            state.contextualization_result = result
            state.messages.append(AIMessage(content="Contextualization completed"))

        return state

    def _reflect_on_task(self, input_text: str, classification_result: Dict[str, Any], contextualization_result: Dict[str, Any]) -> Dict[str, Any]:
        """Perform reflection analysis on the task using rule-based approach"""
        task_type = classification_result.get("task_type", "general")
        domain = contextualization_result.get("domain", "general")

        # Generate insights based on task type and domain
        insights = []
        recommendations = []

        if task_type == "bug":
            insights.append("This appears to be a technical issue that needs resolution")
            recommendations.append("Assign to technical team for investigation")
        elif task_type == "idea":
            insights.append("This is a potential new feature or improvement")
            recommendations.append("Evaluate feasibility and impact")
        elif task_type == "feedback":
            insights.append("This is user feedback that should be considered")
            recommendations.append("Review and categorize feedback")

        if domain == "technology":
            insights.append("This relates to technical aspects of the project")
            recommendations.append("Consult with technical lead")
        elif domain == "business":
            insights.append("This has business implications")
            recommendations.append("Review with business stakeholders")

        return {
            "insights": insights,
            "recommendations": recommendations,
            "metadata": {
                "task_type": task_type,
                "domain": domain,
                "method": "rule_based"
            }
        }

    def _reflect_on_task_with_llm(self, input_text: str, classification_result: Dict[str, Any], contextualization_result: Dict[str, Any]) -> Dict[str, Any]:
        """Perform reflection analysis using LLM for deeper insights"""
        from src.utils.llm_client import llm_client

        task_type = classification_result.get("task_type", "general")
        domain = contextualization_result.get("domain", "general")
        entities = contextualization_result.get("entities", [])

        # Prepare context for LLM
        context = f"""
        Task: {input_text}
        Task Type: {task_type}
        Domain: {domain}
        Entities: {entities}
        """

        prompt = f"""
        Analyze the following task and provide deep insights and recommendations.
        Consider the task type, domain, and any identified entities.
        Provide your response as JSON with fields: insights, recommendations, rationale.

        {context}
        """

        try:
            llm_response = llm_client.generate_json(prompt)

            # Validate the response
            if "error" in llm_response:
                logger.warning(f"LLM reflection error: {llm_response['error']}")
                # Fall back to rule-based approach
                return self._reflect_on_task(input_text, classification_result, contextualization_result)

            return {
                "insights": llm_response.get("insights", []),
                "recommendations": llm_response.get("recommendations", []),
                "metadata": {
                    "task_type": task_type,
                    "domain": domain,
                    "method": "llm_based",
                    "rationale": llm_response.get("rationale", "LLM analysis")
                }
            }
        except Exception as e:
            logger.warning(f"LLM reflection failed: {e}")
            # Fall back to rule-based approach
            return self._reflect_on_task(input_text, classification_result, contextualization_result)

    def _run_reflection(self, state: GraphState) -> GraphState:
        """Run reflection analysis with LLM enhancement and fallback"""
        if state.reflection_result is None and state.contextualization_result:
            # Try LLM-based reflection first, fall back to rule-based if needed
            result = self._reflect_on_task_with_llm(
                state.input_text,
                state.classification_result,
                state.contextualization_result
            )
            state.reflection_result = result
            state.messages.append(AIMessage(content="Reflection analysis completed"))

        return state

    def analyze_text(self, input_text: str) -> Dict[str, Any]:
        """
        Analyze text using pure LangGraph

        Args:
            input_text: Text to analyze

        Returns:
            Analysis results
        """
        # Initialize state
        initial_state = GraphState(
            input_text=input_text,
            messages=[HumanMessage(content="Analyzing text with Level 2")]
        )

        # Compile and run the graph
        compiled_graph = self.graph.compile()
        result = compiled_graph.invoke(initial_state)

        # The result is a dictionary, extract the values
        return {
            "classification": result.get("classification_result"),
            "contextualization": result.get("contextualization_result"),
            "reflection": result.get("reflection_result"),
            "messages": [msg.model_dump() for msg in result.get("messages", [])]
        }

# Create a global instance for easy access
level2_graph_agent_pure = Level2GraphAgentPure()


