"""
highlights_panel.py
────────────────────
Drop-in Investment Highlights panel for Invest.Data.

USAGE in app.py
───────────────
1. Update import line:
       from highlights_panel import highlights_ui, highlights_server

2. Replace the existing "Investment Highlights" nav_panel in the UI with:
       highlights_ui(),

3. Add to server():
       highlights_server(input, output, session)

4. Remove from app.py's shared imports block:
       df_fig1_2026_1, df_fig2a_2026_1, df_fig2b_2026_1,
       df_fig3a_2026_1, df_fig3b_2026_1

5. Remove from app.py's server() the five @render_widget functions:
       fig1_2026_1, fig2a_2026_1, fig2b_2026_1, fig3a_2026_1, fig3b_2026_1
"""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from shiny import ui
from shinywidgets import output_widget, render_widget

try:
    from shared import (
        df_fig1_2026_1,
        df_fig2a_2026_1,
        df_fig2b_2026_1,
        df_fig3a_2026_1,
        df_fig3b_2026_1,
    )
except ImportError:
    df_fig1_2026_1  = None
    df_fig2a_2026_1 = None
    df_fig2b_2026_1 = None
    df_fig3a_2026_1 = None
    df_fig3b_2026_1 = None

# ─────────────────────────────────────────────
#  Colour tokens
# ─────────────────────────────────────────────
BLUE     = "#3f9dd4"
NAVY     = "#0a2d45"
MUTED    = "#555555"
BORDER   = "#d4e4ef"
BG_BLUE  = "#e8f4fb"
BG_LIGHT = "#f5f9fc"
TEXT     = "#333333"
LINK     = "#1f77b4"


# ─────────────────────────────────────────────
#  Hero card
# ─────────────────────────────────────────────
def _highlights_hero():
    return ui.card(
        ui.HTML(f"""
            <h2 style="
                font-size:28px; font-weight:700; color:{NAVY};
                margin-bottom:6px; line-height:1.2;
            ">
                Investment <span style="color:{BLUE};">Highlights</span>
            </h2>

            <p style="
                font-size:14px; color:{TEXT}; line-height:1.65;
                text-align:justify; margin-bottom:18px;
            ">
                The <b>Investment Highlights</b> series provides timely, evidence-based analysis
                of global investment trends, with a focus on emerging sectors,
                regional dynamics, and the evolving landscape of capital flows.
                Each edition draws on the latest available data to surface patterns relevant
                to WBG operational work and client engagement.
            </p>

            <div style="
                background:{BG_BLUE}; border:1px solid {BORDER};
                border-left:4px solid {BLUE}; border-radius:8px;
                padding:14px 18px; margin-bottom:18px;
            ">
                <p style="
                    font-size:11px; font-weight:700; letter-spacing:1.5px;
                    text-transform:uppercase; color:{BLUE}; margin-bottom:6px;
                ">📋 About this Series</p>
                <p style="font-size:14px; color:{TEXT}; margin:0; line-height:1.6;">
                    Published <b>biannually</b> by the
                    <b>SME and Enterprise Development, Policy &amp; Regulations Unit (WKPTS).</b>
                    New editions are released each semester to reflect the
                    most recent investment data and emerging global trends.
                </p>
            </div>

            <div style="display:flex; gap:24px; flex-wrap:wrap; font-size:12px; color:{MUTED};">
                <span>📅 <b>Latest Edition:</b> 2026 H1</span>
                <span>🔒 For <b>WBG internal use only</b></span>
            </div>
        """),
        style=f"background:{BG_LIGHT}; border:1px solid {BORDER}; padding:28px 32px;"
    )


# ─────────────────────────────────────────────
#  Accordion
# ─────────────────────────────────────────────
def _highlights_accordion():
    return ui.accordion(
 
        ###############################################################
        # 1. 2026 H1
        ###############################################################
        ui.accordion_panel(
            ui.HTML("""
                <span style="display:flex; align-items:center; gap:10px;">
                    <span style="
                        background:#3f9dd4; color:white;
                        font-size:11px; font-weight:700;
                        letter-spacing:1px; text-transform:uppercase;
                        padding:3px 9px; border-radius:4px;
                    ">2026 H1</span>
                    <span style="font-size:15px; font-weight:600; color:#0a2d45;">
                        Investment Highlights
                    </span>
                </span>
            """),
 
            ui.HTML("""
                <h2 style="
                    font-size:22px; font-weight:600; color:#3f9dd4;
                    margin-bottom:12px; line-height:1.25;
                ">
                    Where global investment is headed: what the data say about digital innovation and the energy transition
                </h2>
            """),
 
            ui.HTML("""
                <p style="font-size:14px; color:#222; text-align:justify; line-height:1.55;">
                    In December 2024 in Hanoi,
                    <a href="https://fortune.com/2025/10/29/nvidia-first-5-trillion-company-ceo-jensen-huang-500-billion-revenue-blackwell-rubin-gpus-china/"
                    target="_blank" rel="noopener noreferrer"
                    style="color:#1f77b4; text-decoration:underline;">
                        the recently regarded world's first $5 trillion company, NVIDIA</a>,
                    signed an agreement with the government of Viet Nam to build the
                    <a href="https://www.extremetech.com/computing/nvidia-to-build-its-first-ai-research-center-in-vietnam"
                    target="_blank" rel="noopener noreferrer"
                    style="color:#1f77b4; text-decoration:underline;">
                        Viet Nam Research and Development Center.</a>
                    The research and development (R&D) facility will serve as a platform for
                    <a href="https://www.reuters.com/technology/nvidia-signs-ai-cooperation-agreement-with-vietnamese-government-2024-12-05/"
                    target="_blank" rel="noopener noreferrer"
                    style="color:#1f77b4; text-decoration:underline;">
                        NVIDIA to expand its partnerships with Viet Nam's top tech firms</a>
                    and support the country in training talent for developing artificial intelligence (AI) and digital infrastructure.
                    Not far away,
                    <a href="https://www.reuters.com/world/asia-pacific/vietnams-auto-manufacturer-establish-130-million-ev-battery-plant-with-chinas-2026-01-27/"
                    target="_blank" rel="noopener noreferrer"
                    style="color:#1f77b4; text-decoration:underline;">
                        Viet Nam's auto manufacturer Kim Long Motor is partnering with China's BYD to build a
                        US$130&nbsp;million electric-vehicle battery plant on about 4.4&nbsp;hectares in central Viet Nam</a>.
                    Together, these recent developments in Viet Nam mirror a broader shift in Foreign Direct Investment (FDI) toward
                    sectors that drive both technological innovation and sustainable, low-carbon growth.
                    Importantly, they may be also signaling an impending reconfiguration of job creation: one that may expand opportunities, but unevenly
                    across economies.
                    </p>
                <p style="font-size:14px; color:#222; text-align:justify; line-height:1.55;">
                    Data from the
                    <a href="https://www.ftlocations.com/products-and-services/fdi-markets" target="_blank"
                    style="color:#1f77b4; text-decoration:underline;">Financial Times' fDi Markets</a>
                    reveal that announced
                    <a href="https://sdgpulse.unctad.org/glossary/greenfield/" target="_blank"
                    style="color:#1f77b4; text-decoration:underline;">greenfield investments</a>
                    in climate and energy transition surged steadily over the past several years, reaching a peak in 2023 at
                    US$600&nbsp;billion (figure 1). Over this period, the global share of such investments increased from
                    12&nbsp;% in 2016 to 42&nbsp;% in 2023, a shift largely associated with the expansion of projects in renewable
                    energy and clean technologies.
                    Meanwhile, digital investments encompassing cutting-edge areas such as AI and cloud computing
                    have shown a robust upward trajectory, with their share growing from 9&nbsp;% in 2016
                    to 38&nbsp;% in 2025.
                </p>
            """),
 
            # Figure 1
            ui.card(
                ui.HTML("""
                    <p style="font-size:13px; color:#555; margin:0;">
                        <b>Figure 1.</b> Global inward greenfield foreign direct investment per technology type, 2016–2025.
                    </p>
                """),
                ui.card(
                    ui.layout_columns(
                        ui.div(),
                        ui.div(output_widget("fig1_2026_1")),
                        ui.div(),
                        col_widths=[3, 6, 3]
                    ),
                ),
                ui.HTML("""
                    <p style='font-size:12px; color:gray; text-align:justify; margin-top:8px;'>
                        <b>Source:</b> <i>World Bank staff calculations based on information from The Financial Times Ltd,
                        fDi Markets (www.fdimarkets.com).</i><br>
                        <b>Note:</b> <i>The figure shows the aggregated inward CAPEX per technology type over 2016-2025.
                        Digital infrastructure and services, and climate and energy transition are identified based on FT's
                        proprietary project tags. The "Both" category includes projects tagged with both digital infrastructure
                        and services and climate and energy transition using FT's proprietary project tags and is included to
                        avoid double counting across technology types.</i>
                    </p>
                """),
            ),
 
            ui.HTML("""
                <p style="font-size:14px; color:#222; text-align:justify; line-height:1.55;">
                    But FDI growth is not happening evenly around the world; rather, it's a story of a sharp contrast,
                    both in terms of regions and sectors. Advanced economies in North America, Europe and East Asia
                    dominate in total investment share, often driven by capital-intensive projects in digital
                    technology and energy (figure 2). 
                    In fact, Emerging Markets & Developing Economies (EMDEs) average share of announced FDI decreased from 58% to 47% 
                    in 2021-2025 compared to the previous 5 years, suggesting FDI is shifting towards advanced 
                    economies, and competition has become more intense in recent years. 
                    Emerging markets such as Middle East, North Africa, Afghanistan and Pakistan (MENAAP) region, are seeing 
                    explosive growth rates in energy transition investments, though their performance in digital technology remains small.
                    Emerging economies in Sub-Saharan Africa  and Europe and Central Asia are playing catch-up in digital technology, 
                    with lower investment shares and growth; similar to South Asia for climate and energy transition. 
                    Bottom line? FDI is pouring into select hotspots, leaving many countries, especially emerging 
                    and developing ones, scrambling to keep pace in the race to host investors in what is referred 
                    to as disruptive technologies.
                </p>
            """),
 
            # Figure 2
            ui.card(
                ui.HTML("""
                    <p style="font-size:13px; color:#555; margin-bottom:8px;">
                        <b>Figure 2.</b> Share in digital infrastructure and services inward greenfield investment,
                        growth rate and average project size, by region and EMDE status (2016–2025).
                    </p>
                """),
                ui.card(
                    ui.layout_columns(
                        ui.div(),
                        ui.div(
                            ui.layout_columns(
                                ui.div(output_widget("fig2a_2026_1")),
                                ui.div(output_widget("fig2b_2026_1")),
                                col_widths=[6, 6]
                            )
                        ),
                        ui.div(),
                        col_widths=[1, 10, 1]
                    ),
                ),
                ui.HTML("""
                    <p style='font-size:12px; color:gray; text-align:justify; margin-top:8px;'>
                        <b>Source:</b> <i>World Bank staff calculations based on information from The Financial Times Ltd,
                        fDi Markets (www.fdimarkets.com).</i><br>
                        <b>Note:</b> <i>The figure shows the share of inward CAPEX, growth rates, and average project size
                        of digital infrastructure and services greenfield projects by region and EMDE status. Bubble size
                        reflects the average project size over 2016–2025. Growth rates compare cumulative CAPEX in 2021–2025
                        relative to 2016–2020. Digital infrastructure and services, as well as climate and energy transition
                        investments are as previously defined. Advanced Economies (AEs) and Emerging and developing economies
                        (EMDEs) are defined according to the World Bank's Global Economic Prospects (GEP), June 2025 edition.
                        Regional groupings are defined as follows: East Asia and Pacific (EAP), Europe and Central Asia (ECA),
                        Latin America and the Caribbean (LAC), Middle East, North Africa, Afghanistan and Pakistan (MENAAP), 
                        North America (NAR), South Asia (SAR), and Sub-Saharan Africa (SSA). Dashed lines denote median values.</i>
                    </p>
                """),
            ),
 
            ui.HTML("""
                <p style="font-size:14px; color:#222; text-align:justify; line-height:1.55;">
                    Meanwhile, EMDEs are no longer just FDI destinations, but are increasingly becoming
                    <a href="https://www.imf.org/-/media/files/publications/wp/2024/english/wpiea2024076-print-pdf.pdf"
                        target="_blank" style="color:#1f77b4; text-decoration:underline;">
                    sources or connectors</a>
                    of capital across the Global South. In both digital and climate-related investments, several EMDE regions
                    show disproportionately stronger growth in outbound greenfield investments (figure&nbsp;3). East Asia and
                    the Middle East, North Africa, Afghanistan & Pakistan (MENAAP)  stand out in digital, while the MENAAP region, 
                    Europe & Central Asia, and Sub-Saharan Africa lead in climate. Together with the previous
                    results on inflows, these regions appear to act as regional hubs that channel investments to other
                    developing markets. It is also worth noting that this shift is powered by few presumably mega projects
                    evidence of slow but deepening web of South-South FDI. 
                </p>
            """),
 
            # Figure 3
            ui.card(
                ui.HTML("""
                    <p style="font-size:13px; color:#555; margin-bottom:8px;">
                        <b>Figure 3.</b> FDI inflows and outflows growth in digital infrastructure and services (left) and climate
                        and energy transition (right), 2021-2025 vs. 2016-2020; bubble size reflects number of projects,
                        cumulative 2016-2025.
                    </p>
                """),
                ui.card(
                    ui.layout_columns(
                        ui.div(),
                        ui.div(
                            ui.layout_columns(
                                ui.div(output_widget("fig3a_2026_1")),
                                ui.div(output_widget("fig3b_2026_1")),
                                col_widths=[6, 6]
                            )
                        ),
                        ui.div(),
                        col_widths=[1, 10, 1]
                    ),
                ),
                ui.HTML("""
                    <p style='font-size:12px; color:gray; text-align:justify; margin-top:8px;'>
                        <b>Source:</b> <i>World Bank staff calculations based on information from The Financial Times Ltd,
                        fDi Markets (www.fdimarkets.com).</i><br>
                        <b>Note:</b> <i>Bubble size reflects the cumulative number of projects over 2016-2025. Digital
                        infrastructure and services, as well as climate and energy transition investments are as previously
                        defined. Advanced Economies (AEs) and Emerging and developing economies (EMDEs) are defined according
                        to the World Bank's Global Economic Prospects (GEP), June 2025 edition. Regional groupings are defined
                        as follows: East Asia and Pacific (EAP), Europe and Central Asia (ECA), Latin America and the Caribbean
                        (LAC), Middle East, North Africa, Afghanistan and Pakistan (MENAAP), North America (NAR), South Asia (SAR), 
                        and Sub-Saharan Africa (SSA). Dashed line denote equal growth rates in inflows and outflows.</i>
                    </p>
                """),
            ),
 
            ui.HTML("""
                <p style="font-size:14px; color:#222; text-align:justify; line-height:1.55;">
                    <a href="https://www.weforum.org/publications/the-future-of-jobs-report-2025/in-full/1-drivers-of-labour-market-transformation/"
                        target="_blank" style="color:#1f77b4; text-decoration:underline;">
                        The recent shifts in greenfield FDI will shape jobs and growth sooner than later.</a>
                    Implicitly, what these trends show is that investors are clearly betting on future demand, not current income,
                    channeling capital into digital infrastructure and low-carbon economy whose payoffs are still uncertain,
                    non-traditional, and tied to markets that are still being formed. That raises the stakes: returns hinge on
                    data flows, power grids, skills and policies catching up fast.
 
                    <a href="https://www.worldbank.org/en/publication/dptr2025-ai-foundations"
                        target="_blank" style="color:#1f77b4; text-decoration:underline;">
                    The upside is significant: new jobs, new capabilities, and new growth paths;</a>
                    but the risks are real, from stranded assets to widening gaps between economies that can absorb these
                    investments and those that cannot. Clearly, FDI is no longer just following growth; it is trying to create it.
                </p>
            """),
            value="2026_h1",
        ),
 
        open="2026_h1"
    )
 
 
# ═════════════════════════════════════════════
#  highlights_ui()
# ═════════════════════════════════════════════
def highlights_ui():
    return ui.nav_panel(
        "Investment Highlights",
        ui.div(
            ui.div(style="margin-top:20px;"),
            _highlights_hero(),
            ui.div(style="margin-top:24px;"),
            _highlights_accordion(),
        ),
    )
 
 
# ═════════════════════════════════════════════
#  highlights_server()
# ═════════════════════════════════════════════
def highlights_server(input, output, session):
 
    # ── Figure 1 ──────────────────────────────────────────────────────────
    @output
    @render_widget
    def fig1_2026_1():
        df_plot = df_fig1_2026_1
 
        df_line = (
            df_plot
            .loc[df_plot["tech_type"].isin(["green", "digital", "both"])]
            .groupby("year", as_index=False)
            .agg(share=("capex_year_share", "sum"))
            .sort_values("year")
        )
 
        stack_order = ["green", "digital", "both", "neither"]
        color_map   = {"green": "#5dade2", "digital": "#d95f5f", "both": "#000000", "neither": "#cccccc"}
        pattern_map = {"green": "\\",      "digital": "/",        "both": "",        "neither": ""}
        label_map   = {"green": "Climate & Energy Transition", "digital": "Digital", "both": "Both", "neither": "Others"}
        legend_rank = {"green": 1, "digital": 2, "both": 3, "neither": 4}
 
        fig = go.Figure()
 
        for comp in stack_order:
            d = df_plot[df_plot["tech_type"] == comp]
            fig.add_bar(
                x=d["year"],
                y=d["value"],
                name=label_map[comp],
                marker=dict(color=color_map[comp], pattern=dict(shape=pattern_map[comp])),
                legendrank=legend_rank[comp],
                customdata=np.column_stack([d["value_bn"], d["capex_year_share"]]),
                hovertemplate=(
                    "<b>Year:</b> %{x}<br>"
                    "<b>Technology Type:</b> " + label_map[comp] + "<br>"
                    "<b>Total Announced CAPEX:</b> US$%{customdata[0]:.1f} bn<br>"
                    "<b>Share of total Announced CAPEX:</b> %{customdata[1]:.1f}%"
                    "<extra></extra>"
                )
            )
 
        fig.add_trace(go.Scatter(
            x=df_line["year"], y=df_line["share"],
            mode="lines", name="Total % of Digital and Climate (right axis)",
            yaxis="y2", line=dict(color="black", width=2), marker=dict(size=6),
            hovertemplate=(
                "<b>Year:</b> %{x}<br>"
                "<b>Digital + Climate Announced CAPEX Global Share:</b> %{y:.1f}%"
                "<extra></extra>"
            ),
            showlegend=True
        ))
 
        y1_max = df_plot.groupby("year")["value"].sum().max() * 1.1
 
        fig.update_layout(
            barmode="stack", plot_bgcolor="white", paper_bgcolor="white",
            title=dict(text="", x=0.5),
            yaxis=dict(title="Current USD (trillions)", zeroline=True, zerolinecolor="black",
                       showgrid=True, gridcolor="LightGray", tickformat=",.1f", range=[0, y1_max]),
            yaxis2=dict(title="Share of total CAPEX (%)", overlaying="y", side="right",
                        showgrid=False, tickformat=".0f", range=[0, 60]),
            xaxis=dict(tickmode="array", tickvals=[2016, 2018, 2020, 2022, 2024],
                       ticktext=["2016", "2018", "2020", "2022", "2024"]),
            legend=dict(orientation="h", yanchor="top", y=-0.18, xanchor="center", x=0.5, traceorder="normal"),
            margin=dict(l=60, r=50, t=40, b=70),
            template="plotly_white"
        )
        return fig
 
    # ── Figure 2a ─────────────────────────────────────────────────────────
    @output
    @render_widget
    def fig2a_2026_1():
        df = df_fig2a_2026_1.copy()
 
        fig = px.scatter(
            df, x="share", y="growth_rate",
            color="emde_label", color_discrete_map={"AE": "#5dade2", "EMDE": "#d95f5f"},
            symbol="emde_label", symbol_map={"AE": "circle", "EMDE": "diamond"},
            text="region_shortdestination", hover_name="hover_group",
            size="avg_size", size_max=35,
            labels={"share": "Share of total CAPEX (%)", "growth_rate": "Growth rate vs 2016-2020 (%)",
                    "avg_size": "Average project size (USD Millions)", "emde_label": "EMDE Status",
                    "top3_economysource": "Top 3 Investment Sources", "n_projects": "Number of Projects",
                    "capex_total": "Total Announced CAPEX (2016-2025)"},
            custom_data=["share", "growth_rate", "avg_size", "n_projects",
                         "top3_economysource", "emde_label", "capex_total"]
        )
        fig.update_traces(
            marker=dict(opacity=0.7), textposition="top center", textfont_size=11,
            hovertemplate=(
                "<b>%{hovertext}</b><br>" +
                "Share of Global CAPEX: %{customdata[0]:,.1f}%<br>" +
                "Total Announced CAPEX: US$%{customdata[6]:,.1f} bn<br>" +
                "Number of projects: %{customdata[3]:,d}<br>" +
                "Average project size: US$%{customdata[2]:,.1f} m<br>" +
                "Growth rate vs 2016–2020: %{customdata[1]:,.1f}%<br>" +
                "Top 3 investment sources: %{customdata[4]}<br>" +
                "<extra></extra>"
            )
        )
        fig.update_layout(
            autosize=True, plot_bgcolor="white", paper_bgcolor="white",
            title=dict(text="a) Digital infrastructure and services", x=0.5, xanchor="center",
                       y=0.97, yanchor="top", font=dict(size=14, color="black")),
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5,
                        title=dict(text="Income Group:", font=dict(size=14)), font=dict(size=14)),
            margin=dict(l=40, r=30, t=60, b=40), template="plotly_white"
        )
        fig.update_xaxes(range=[0, 40], tickvals=list(range(0, 41, 5)),
                         ticktext=[f"{v}%" for v in range(0, 41, 5)],
                         showgrid=True, gridcolor="LightGray", showline=True)
        fig.update_yaxes(range=[0, 500], tickvals=list(range(100, 501, 100)),
                         ticktext=[f"{v}%" for v in range(100, 501, 100)],
                         showgrid=True, gridcolor="LightGray", showline=True)
        
        median_x = df["share"].median()
        median_y = df["growth_rate"].median()

        fig.add_vline(x=median_x, line_dash="dash", line_color="gray")
        fig.add_hline(y=median_y, line_dash="dash", line_color="gray")

        return fig
 
    # ── Figure 2b ─────────────────────────────────────────────────────────
    @output
    @render_widget
    def fig2b_2026_1():
        df = df_fig2b_2026_1.copy()
 
        fig = px.scatter(
            df, x="share", y="growth_rate",
            color="emde_label", color_discrete_map={"AE": "#5dade2", "EMDE": "#d95f5f"},
            symbol="emde_label", symbol_map={"AE": "circle", "EMDE": "diamond"},
            text="region_shortdestination", hover_name="hover_group",
            size="avg_size", size_max=35,
            labels={"share": "Share of total CAPEX (%)", "growth_rate": "Growth rate vs 2016-2020 (%)",
                    "avg_size": "Average project size (USD Millions)", "emde_label": "EMDE Status",
                    "top3_economysource": "Top 3 Investment Sources", "n_projects": "Number of Projects",
                    "capex_total": "Total Announced CAPEX (2016-2025)"},
            custom_data=["share", "growth_rate", "avg_size", "n_projects",
                         "top3_economysource", "emde_label", "capex_total"]
        )
        fig.update_traces(
            marker=dict(opacity=0.7), textposition="top center", textfont_size=11,
            hovertemplate=(
                "<b>%{hovertext}</b><br>" +
                "Share of Global CAPEX: %{customdata[0]:,.1f}%<br>" +
                "Total Announced CAPEX: US$%{customdata[6]:,.1f} bn<br>" +
                "Number of projects: %{customdata[3]:,d}<br>" +
                "Average project size: US$%{customdata[2]:,.1f} m<br>" +
                "Growth rate vs 2016–2020: %{customdata[1]:,.1f}%<br>" +
                "Top 3 investment sources: %{customdata[4]}<br>" +
                "<extra></extra>"
            )
        )
        fig.update_layout(
            autosize=True, plot_bgcolor="white", paper_bgcolor="white",
            title=dict(text="b) Climate and energy transition", x=0.5, xanchor="center",
                       y=0.97, yanchor="top", font=dict(size=14, color="black")),
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5,
                        title=dict(text="Income Group:", font=dict(size=14)), font=dict(size=14)),
            margin=dict(l=40, r=30, t=60, b=40), template="plotly_white"
        )
        fig.update_xaxes(range=[0, 30], tickvals=list(range(0, 31, 5)),
                         ticktext=[f"{v}%" for v in range(0, 31, 5)],
                         showgrid=True, gridcolor="LightGray", showline=True)
        fig.update_yaxes(range=[0, 600], tickvals=list(range(100, 601, 100)),
                         ticktext=[f"{v:,}%" for v in range(100, 601, 100)],
                         showgrid=True, gridcolor="LightGray", showline=True)
        
        median_x = df["share"].median()
        median_y = df["growth_rate"].median()

        fig.add_vline(x=median_x, line_dash="dash", line_color="gray")
        fig.add_hline(y=median_y, line_dash="dash", line_color="gray")
        return fig
 
    # ── Figure 3a ─────────────────────────────────────────────────────────
    @output
    @render_widget
    def fig3a_2026_1():
        df = df_fig3a_2026_1.copy()
 
        fig = px.scatter(
            df, x="outflow_log_growth", y="inflow_log_growth",
            size="n_projects_total_stock", size_max=35,
            color="emde_label", color_discrete_map={"AE": "#5dade2", "EMDE": "#d95f5f"},
            symbol="emde_label", symbol_map={"AE": "circle", "EMDE": "diamond"},
            hover_name="hover_group", text="region_short",
            custom_data=["emde_label",
                         "outflow_capex_2016_2020", "outflow_capex_2021_2025", "outflow_log_growth",
                         "top3_outflow_2016_2020",  "top3_outflow_2021_2025",
                         "inflow_capex_2016_2020",  "inflow_capex_2021_2025",  "inflow_log_growth",
                         "top3_inflow_2016_2020",   "top3_inflow_2021_2025",
                         "n_projects_total_stock"],
            labels={"outflow_log_growth": "Outflow growth vs 2016–2020 (log)",
                    "inflow_log_growth":  "Inflow growth vs 2016–2020 (log)",
                    "emde_label": "EMDE Status"}
        )
        fig.update_traces(
            marker=dict(opacity=0.7), textposition="top center", textfont_size=12,
            hovertemplate=(
                "<b>%{hovertext}</b><br><br>" +
                "<b>Outflows</b><br>" +
                "CAPEX 2016–2020: %{customdata[1]:,.0f}<br>" +
                "CAPEX 2021–2025: %{customdata[2]:,.0f}<br>" +
                "Log growth: %{x:.2f}<br>" +
                "Top investors (2016–2020): %{customdata[4]}<br>" +
                "Top investors (2021–2025): %{customdata[5]}<br><br>" +
                "<b>Inflows</b><br>" +
                "CAPEX 2016–2020: %{customdata[6]:,.0f}<br>" +
                "CAPEX 2021–2025: %{customdata[7]:,.0f}<br>" +
                "Log growth: %{y:.2f}<br>" +
                "Top recipients (2016–2020): %{customdata[9]}<br>" +
                "Top recipients (2021–2025): %{customdata[10]}<br><br>" +
                "<b>Total projects (stock, 2025)</b><br>%{customdata[11]:,.0f}" +
                "<extra></extra>"
            )
        )
        fig.add_shape(type="line", x0=-1, y0=-1, x1=5, y1=5,
                      line=dict(dash="dash", color="gray"))
        fig.update_layout(
            autosize=True, plot_bgcolor="white", paper_bgcolor="white",
            title=dict(text="a) Digital infrastructure and services", x=0.5, xanchor="center",
                       y=0.97, yanchor="top", font=dict(size=14, color="black")),
            legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="center", x=0.5,
                        title=dict(text="Income Group:", font=dict(size=14)), font=dict(size=14)),
            margin=dict(l=30, r=30, t=30, b=30)
        )
        fig.update_xaxes(range=[0, 3.5], tickvals=list(range(0, 5, 1)),
                         showgrid=True, gridwidth=0.5, gridcolor="LightGray",
                         showline=True, linewidth=1, linecolor="black", title_font=dict(size=14))
        fig.update_yaxes(range=[0, 3.5], tickvals=list(range(0, 5, 1)),
                         showgrid=True, gridwidth=0.5, gridcolor="lightgray",
                         showline=True, linewidth=1, linecolor="black", title_font=dict(size=14))
        return fig
 
    # ── Figure 3b ─────────────────────────────────────────────────────────
    @output
    @render_widget
    def fig3b_2026_1():
        df = df_fig3b_2026_1.copy()
 
        fig = px.scatter(
            df, x="outflow_log_growth", y="inflow_log_growth",
            size="n_projects_total_stock", size_max=35,
            color="emde_label", color_discrete_map={"AE": "#5dade2", "EMDE": "#d95f5f"},
            symbol="emde_label", symbol_map={"AE": "circle", "EMDE": "diamond"},
            hover_name="hover_group", text="region_short",
            custom_data=["emde_label",
                         "outflow_capex_2016_2020", "outflow_capex_2021_2025", "outflow_log_growth",
                         "top3_outflow_2016_2020",  "top3_outflow_2021_2025",
                         "inflow_capex_2016_2020",  "inflow_capex_2021_2025",  "inflow_log_growth",
                         "top3_inflow_2016_2020",   "top3_inflow_2021_2025",
                         "n_projects_total_stock"],
            labels={"outflow_log_growth": "Outflow growth vs 2016–2020 (log)",
                    "inflow_log_growth":  "Inflow growth vs 2016–2020 (log)",
                    "emde_label": "EMDE Status"}
        )
        fig.update_traces(
            marker=dict(opacity=0.7), textposition="top center", textfont_size=12,
            hovertemplate=(
                "<b>%{hovertext}</b><br><br>" +
                "<b>Outflows</b><br>" +
                "CAPEX 2016–2020: %{customdata[1]:,.0f}<br>" +
                "CAPEX 2021–2025: %{customdata[2]:,.0f}<br>" +
                "Log growth: %{x:.2f}<br>" +
                "Top investors (2016–2020): %{customdata[4]}<br>" +
                "Top investors (2021–2025): %{customdata[5]}<br><br>" +
                "<b>Inflows</b><br>" +
                "CAPEX 2016–2020: %{customdata[6]:,.0f}<br>" +
                "CAPEX 2021–2025: %{customdata[7]:,.0f}<br>" +
                "Log growth: %{y:.2f}<br>" +
                "Top recipients (2016–2020): %{customdata[9]}<br>" +
                "Top recipients (2021–2025): %{customdata[10]}<br><br>" +
                "<b>Total projects (stock, 2025)</b><br>%{customdata[11]:,.0f}" +
                "<extra></extra>"
            )
        )
        fig.add_shape(type="line", x0=-1, y0=-1, x1=5, y1=5,
                      line=dict(dash="dash", color="gray"))
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            title=dict(text="b) Climate and energy transition", x=0.5, xanchor="center",
                       y=0.97, yanchor="top", font=dict(size=14, color="black")),
            legend=dict(orientation="h", yanchor="top", y=-0.16, xanchor="center", x=0.5,
                        title=dict(text="Income Group:", font=dict(size=14)), font=dict(size=14)),
            margin=dict(l=30, r=30, t=30, b=30)
        )
        fig.update_xaxes(range=[0, 3], tickvals=list(range(0, 4, 1)),
                         showgrid=True, gridwidth=0.5, gridcolor="LightGray",
                         showline=True, linewidth=1, linecolor="black", title_font=dict(size=14))
        fig.update_yaxes(range=[0, 3], tickvals=list(range(0, 4, 1)),
                         showgrid=True, gridwidth=0.5, gridcolor="lightgray",
                         showline=True, linewidth=1, linecolor="black", title_font=dict(size=14))
        return fig