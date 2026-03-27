import plotly.io as pio

def apply_custom_theme():
    """Applique un thème personnalisé et professionnel pour Plotly."""
    pio.templates.default = "plotly_white"
    
    # Configuration globale des polices et couleurs par défaut
    pio.templates["plotly_white"].layout.font = dict(family="Segoe UI, Arial, sans-serif", size=14, color="#2c3e50")
    pio.templates["plotly_white"].layout.title = dict(font=dict(size=18, color="#1e3c72"))
