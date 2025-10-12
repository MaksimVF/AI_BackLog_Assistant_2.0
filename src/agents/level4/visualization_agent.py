




"""
Visualization Agent Module

This module generates visualizations using plotly for charts and graphs.
"""

import logging
import json
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Configure logging
logger = logging.getLogger(__name__)

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    logger.warning("Plotly not available, visualizations will be disabled")
    PLOTLY_AVAILABLE = False

class VisualizationResult(BaseModel):
    """Data model for visualization results"""
    chart_type: str
    chart_data: Dict[str, Any]
    chart_html: Optional[str] = None

class VisualizationAgent:
    """Agent for generating visualizations"""

    def __init__(self):
        """Initialize the Visualization Agent"""
        logger.info("Initializing Visualization Agent")
        self.plotly_available = PLOTLY_AVAILABLE

    def _generate_radar_chart(self, scores: Dict[str, float]) -> VisualizationResult:
        """Generate a radar chart for score visualization"""
        if not self.plotly_available:
            return VisualizationResult(
                chart_type="radar",
                chart_data=scores,
                chart_html="<div>Plotly not available</div>"
            )

        # Create radar chart
        categories = list(scores.keys())
        values = list(scores.values())

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Task Scores'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            title="Task Analysis Scores"
        )

        # Generate HTML
        chart_html = fig.to_html(full_html=False)

        return VisualizationResult(
            chart_type="radar",
            chart_data=scores,
            chart_html=chart_html
        )

    def _generate_bar_chart(self, data: Dict[str, float]) -> VisualizationResult:
        """Generate a bar chart for comparison"""
        if not self.plotly_available:
            return VisualizationResult(
                chart_type="bar",
                chart_data=data,
                chart_html="<div>Plotly not available</div>"
            )

        # Create bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=list(data.keys()),
            y=list(data.values()),
            name='Scores'
        ))

        fig.update_layout(
            title="Task Analysis Comparison",
            xaxis_title="Metrics",
            yaxis_title="Scores (0-10)"
        )

        # Generate HTML
        chart_html = fig.to_html(full_html=False)

        return VisualizationResult(
            chart_type="bar",
            chart_data=data,
            chart_html=chart_html
        )

    def generate_visualization(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate visualizations based on analysis data

        Args:
            analysis_data: Analysis data to visualize

        Returns:
            Visualization results
        """
        # Extract scores for visualization
        scores = {
            "Risk": analysis_data.get("risk_score", 0),
            "Impact": analysis_data.get("impact_score", 0),
            "Urgency": analysis_data.get("urgency", 0),
            "Confidence": analysis_data.get("confidence", 0) * 10  # Scale to 0-10
        }

        # Generate radar chart
        radar_result = self._generate_radar_chart(scores)

        # Generate bar chart
        bar_result = self._generate_bar_chart(scores)

        return {
            "radar_chart": radar_result.model_dump(),
            "bar_chart": bar_result.model_dump(),
            "scores": scores
        }

# Create a global instance for easy access
visualization_agent = VisualizationAgent()
