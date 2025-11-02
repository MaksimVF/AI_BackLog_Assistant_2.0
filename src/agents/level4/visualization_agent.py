




"""
Visualization Agent Module

This module generates visualizations using plotly for charts and graphs.
"""

import logging
import json
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel
from datetime import datetime

# Configure logging
logger = logging.getLogger(__name__)

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    logger.warning("Plotly not available, visualizations will be disabled")
    PLOTLY_AVAILABLE = False

class VisualizationResult(BaseModel):
    """Data model for visualization results"""
    chart_type: str
    chart_data: Union[Dict[str, Any], List[Dict[str, Any]]]
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
            name='Task Scores',
            line_color='blue',
            marker=dict(color='rgba(0, 128, 255, 0.7)')
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10],
                    tickfont=dict(size=12),
                    gridcolor='lightgray'
                ),
                angularaxis=dict(
                    tickfont=dict(size=12)
                )
            ),
            title="Task Analysis Scores",
            title_font=dict(size=16),
            paper_bgcolor='white',
            plot_bgcolor='white'
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
            name='Scores',
            marker_color='rgb(55, 83, 109)'
        ))

        fig.update_layout(
            title="Task Analysis Comparison",
            xaxis_title="Metrics",
            yaxis_title="Scores (0-10)",
            title_font=dict(size=16),
            xaxis=dict(tickfont=dict(size=12)),
            yaxis=dict(tickfont=dict(size=12)),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        # Generate HTML
        chart_html = fig.to_html(full_html=False)

        return VisualizationResult(
            chart_type="bar",
            chart_data=data,
            chart_html=chart_html
        )

    def _generate_status_pie_chart(self, status_data: Dict[str, int]) -> VisualizationResult:
        """Generate a pie chart for task status distribution"""
        if not self.plotly_available:
            return VisualizationResult(
                chart_type="pie",
                chart_data=status_data,
                chart_html="<div>Plotly not available</div>"
            )

        # Create pie chart
        labels = list(status_data.keys())
        values = list(status_data.values())

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            textinfo='percent',
            textfont=dict(size=12),
            marker=dict(colors=px.colors.qualitative.Plotly)
        )])

        fig.update_layout(
            title="Task Status Distribution",
            title_font=dict(size=16),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        # Generate HTML
        chart_html = fig.to_html(full_html=False)

        return VisualizationResult(
            chart_type="pie",
            chart_data=status_data,
            chart_html=chart_html
        )

    def _generate_trend_line_chart(self, trend_data: List[Dict[str, Any]]) -> VisualizationResult:
        """Generate a line chart for trend analysis"""
        if not self.plotly_available:
            return VisualizationResult(
                chart_type="line",
                chart_data=trend_data,
                chart_html="<div>Plotly not available</div>"
            )

        # Prepare data
        dates = [entry['date'] for entry in trend_data]
        values = [entry['value'] for entry in trend_data]
        metric = trend_data[0]['metric'] if trend_data else 'Metric'

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=dates,
            y=values,
            mode='lines+markers',
            name=metric,
            line=dict(color='rgb(55, 83, 109)', width=2),
            marker=dict(size=6)
        ))

        fig.update_layout(
            title=f"{metric} Trend Over Time",
            xaxis_title="Date",
            yaxis_title=metric,
            title_font=dict(size=16),
            xaxis=dict(tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=10)),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        # Generate HTML
        chart_html = fig.to_html(full_html=False)

        return VisualizationResult(
            chart_type="line",
            chart_data=trend_data,
            chart_html=chart_html
        )

    def _generate_resource_allocation_chart(self, resource_data: Dict[str, Dict[str, int]]) -> VisualizationResult:
        """Generate a grouped bar chart for resource allocation"""
        if not self.plotly_available:
            return VisualizationResult(
                chart_type="grouped_bar",
                chart_data=resource_data,
                chart_html="<div>Plotly not available</div>"
            )

        # Prepare data
        categories = []
        values = []
        labels = []

        for team, tasks in resource_data.items():
            for task_type, count in tasks.items():
                categories.append(team)
                values.append(count)
                labels.append(task_type)

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            text=labels,
            textposition='auto',
            marker_color='rgb(55, 83, 109)'
        ))

        fig.update_layout(
            title="Resource Allocation by Team",
            xaxis_title="Teams",
            yaxis_title="Number of Tasks",
            title_font=dict(size=16),
            xaxis=dict(tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=10)),
            paper_bgcolor='white',
            plot_bgcolor='white'
        )

        # Generate HTML
        chart_html = fig.to_html(full_html=False)

        return VisualizationResult(
            chart_type="grouped_bar",
            chart_data=resource_data,
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

        # Generate additional visualizations if data is available
        results = {
            "radar_chart": radar_result.model_dump(),
            "bar_chart": bar_result.model_dump(),
            "scores": scores
        }

        # Add status distribution if available
        if "status_distribution" in analysis_data:
            status_pie = self._generate_status_pie_chart(analysis_data["status_distribution"])
            results["status_pie"] = status_pie.model_dump()

        # Add trend analysis if available
        if "trend_data" in analysis_data:
            trend_line = self._generate_trend_line_chart(analysis_data["trend_data"])
            results["trend_line"] = trend_line.model_dump()

        # Add resource allocation if available
        if "resource_allocation" in analysis_data:
            resource_chart = self._generate_resource_allocation_chart(analysis_data["resource_allocation"])
            results["resource_allocation"] = resource_chart.model_dump()

        return results

# Create a global instance for easy access
visualization_agent = VisualizationAgent()
