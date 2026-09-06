"""
Pages Module
"""

from . import dashboard
from . import network_graph
from . import entity_profile
from . import timeline
from . import cross_case
from . import ai_copilot
from . import alerts
from . import simulation
from . import heatmap
from . import export
from . import security

# Import render functions for easy access
from .dashboard import render as dashboard_render
from .network_graph import render as network_graph_render
from .entity_profile import render as entity_profile_render
from .timeline import render as timeline_render
from .cross_case import render as cross_case_render
from .ai_copilot import render as ai_copilot_render
from .alerts import render as alerts_render
from .simulation import render as simulation_render
from .heatmap import render as heatmap_render
from .export import render as export_render
from .security import render as security_render

# Define exports
dashboard = dashboard_render
network_graph = network_graph_render
entity_profile = entity_profile_render
timeline = timeline_render
cross_case = cross_case_render
ai_copilot = ai_copilot_render
alerts = alerts_render
simulation = simulation_render
heatmap = heatmap_render
export = export_render
security = security_render
