"""
Pages Module - Import all pages
"""

from . import (
    dashboard, network_graph, entity_profile, timeline, cross_case,
    ai_copilot, alerts, simulation, heatmap, export, security
)

# Export render functions
dashboard_render = dashboard.render
network_graph_render = network_graph.render
entity_profile_render = entity_profile.render
timeline_render = timeline.render
cross_case_render = cross_case.render
ai_copilot_render = ai_copilot.render
alerts_render = alerts.render
simulation_render = simulation.render
heatmap_render = heatmap.render
export_render = export.render
security_render = security.render
