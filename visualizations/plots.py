import plotly.express as px

def tracer_bar_chart(data, x_col, y_col, titre, color_col=None):
    """Représentation synthétique en bâtons."""
    fig = px.bar(data, x=x_col, y=y_col, title=titre, color=color_col if color_col else x_col, text_auto='.2s')
    fig.update_layout(
        title_font_size=16, 
        font_family="Segoe UI",
        xaxis_title_font_family="Segoe UI",
        yaxis_title_font_family="Segoe UI"
    )
    fig.show()
    
def tracer_pie_chart(data, names_col, titre):
    """Représentation des parts de notre patientèle."""
    fig = px.pie(data, names=names_col, title=titre, hole=0.3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(
        title_font_size=16, 
        font_family="Segoe UI"
    )
    fig.show()

def tracer_scatter_trend(data, x_col, y_col, color_col, titre, labels_dict=None):
    """Représentation en nuage de points avec ligne de tendance OLS."""
    fig = px.scatter(data, x=x_col, y=y_col, color=color_col, trendline="ols", title=titre, labels=labels_dict)
    fig.update_layout(
        title_font_size=16, 
        font_family="Segoe UI",
        xaxis_title_font_family="Segoe UI",
        yaxis_title_font_family="Segoe UI"
    )
    fig.show()

def tracer_boxplot(data, x_col, y_col, color_col, titre):
    """Représentation en boîte à moustaches pour analyser l'écart type."""
    fig = px.box(data, x=x_col, y=y_col, color=color_col, title=titre)
    fig.update_layout(
        title_font_size=16, 
        font_family="Segoe UI",
        xaxis_title_font_family="Segoe UI",
        yaxis_title_font_family="Segoe UI"
    )
    fig.show()
