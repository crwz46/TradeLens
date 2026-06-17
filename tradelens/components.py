import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


DARK_THEME = {
    "paper_bgcolor": "#0d1117",
    "plot_bgcolor": "#0d1117",
    "font_color": "#c9d1d9",
    "grid_color": "#21262d",
}


def metric_card(label: str, value: str, delta: str = None, help_text: str = None):
    col = st.columns([1])[0]
    with col:
        st.markdown(
            f"""
            <div style="background:#161b22; border:1px solid #30363d; border-radius:8px; padding:16px; margin:4px 0;">
                <div style="color:#8b949e; font-size:13px;">{label}</div>
                <div style="color:#e6edf3; font-size:28px; font-weight:700;">{value}</div>
                {f'<div style="color:#3fb950; font-size:14px;">▲ {delta}</div>' if delta else ''}
                {f'<div style="color:#8b949e; font-size:11px; margin-top:4px;">{help_text}</div>' if help_text else ''}
            </div>
            """,
            unsafe_allow_html=True,
        )


def section_header(title: str, subtitle: str = ""):
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"<div style='color:#8b949e; margin-bottom:20px;'>{subtitle}</div>",
                     unsafe_allow_html=True)


def dark_fig(fig):
    fig.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font_color="#c9d1d9",
        xaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d"),
        yaxis=dict(gridcolor="#21262d", zerolinecolor="#30363d"),
        legend=dict(bgcolor="#161b22", bordercolor="#30363d"),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return fig


def plot_gauge(value: float, max_val: float, title: str, color: str = "#58a6ff"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"font": {"color": "#e6edf3", "size": 28}},
        title={"text": title, "font": {"color": "#8b949e", "size": 14}},
        gauge={
            "axis": {"range": [0, max_val], "tickcolor": "#8b949e", "gridcolor": "#21262d"},
            "bar": {"color": color},
            "bgcolor": "#161b22",
            "borderwidth": 0,
            "steps": [
                {"range": [0, max_val * 0.33], "color": "#21262d"},
                {"range": [max_val * 0.33, max_val * 0.66], "color": "#21262d"},
                {"range": [max_val * 0.66, max_val], "color": "#21262d"},
            ],
        },
    ))
    return dark_fig(fig)


def plot_pie(labels: list, values: list, title: str):
    fig = go.Figure(data=[go.Pie(
        labels=labels, values=values, hole=0.4,
        marker=dict(colors=px.colors.sequential.Blues_r + px.colors.sequential.Emrld_r),
        textfont=dict(color="#c9d1d9"),
    )])
    fig.update_layout(title=dict(text=title, font=dict(color="#58a6ff")), showlegend=True)
    return dark_fig(fig)


def plot_bar(x: list, y: list, title: str, xlabel: str = "", ylabel: str = ""):
    fig = go.Figure(data=[go.Bar(x=x, y=y, marker_color="#58a6ff", marker_line_color="#1f6feb")])
    fig.update_layout(
        title=dict(text=title, font=dict(color="#58a6ff")),
        xaxis_title=xlabel, yaxis_title=ylabel,
    )
    return dark_fig(fig)


def plot_line(x: list, y: list, title: str, color: str = "#58a6ff"):
    fig = go.Figure(data=[go.Scatter(x=x, y=y, mode="lines", line=dict(color=color, width=2))])
    fig.update_layout(title=dict(text=title, font=dict(color="#58a6ff")), showlegend=False)
    return dark_fig(fig)


def plot_heatmap(z: list, x: list, y: list, title: str):
    fig = go.Figure(data=go.Heatmap(
        z=z, x=x, y=y, colorscale="RdYlGn_r",
        hovertemplate="Hour: %{x}<br>Type: %{y}<br>$%{z}M<extra></extra>",
    ))
    fig.update_layout(title=dict(text=title, font=dict(color="#58a6ff")))
    fig.update_xaxes(tickangle=45)
    return dark_fig(fig)


def status_badge(text: str, color: str):
    return f"<span style='background:{color}22; color:{color}; padding:2px 10px; border-radius:12px; font-weight:600; font-size:13px;'>{text}</span>"
