"""
bilateral_trends_panel.py
──────────────────────────
Drop-in Bilateral Trends panel for Invest.Data.

USAGE in app.py
───────────────
1. Add import:
       from bilateral_trends_panel import bilateral_trends_ui, bilateral_trends_server

2. Replace the existing "Bilateral Trends" nav_panel in the UI with:
       bilateral_trends_ui(),

3. Add to server():
       bilateral_trends_server(input, output, session)

4. Remove from app.py's shared imports:
       bilateral_inflow, bilateral_outflow, bilateral_instock,
       bilateral_outstock, bilateral_economies

5. Remove from app.py's server():
       bilateral_inward_graph(), bilateral_outward_graph(),
       download_bilateral_inflow(), download_bilateral_instock(),
       download_bilateral_outflow(), download_bilateral_outstock()
"""

import io
import plotly.express as px
import plotly.graph_objects as go
from shiny import ui, render, Inputs, Outputs, Session
from shinywidgets import output_widget, render_widget

try:
    from shared import bilateral_inflow    as _bilateral_inflow
    from shared import bilateral_outflow   as _bilateral_outflow
    from shared import bilateral_instock   as _bilateral_instock
    from shared import bilateral_outstock  as _bilateral_outstock
    from shared import bilateral_economies as _bilateral_economies
except ImportError:
    _bilateral_inflow    = None
    _bilateral_outflow   = None
    _bilateral_instock   = None
    _bilateral_outstock  = None
    _bilateral_economies = None


def _build_economy_list():
    """
    Build a flat ordered list for ui.input_selectize with region names
    as unclickable separator headers, matching the fdi_trends pattern.
    """
    import pandas as pd

    if _bilateral_economies is None:
        return []

    df = _bilateral_economies if isinstance(_bilateral_economies, pd.DataFrame) else pd.DataFrame({"economy": _bilateral_economies})

    if "region" not in df.columns:
        return sorted(df["economy"].dropna().unique().tolist())

    ordered = []
    for region_name, grp in df.groupby("region", sort=True):
        ordered.append(f"\u2500\u2500 {region_name} \u2500\u2500")
        for econ in sorted(grp["economy"].dropna().unique().tolist()):
            ordered.append(f"\u00a0\u00a0\u00a0\u00a0{econ}")

    return ordered


def _is_separator(val: str) -> bool:
    v = val.strip()
    return v.startswith("\u2014") or v.startswith("\u2500\u2500")

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


# ─────────────────────────────────────────────
#  Hero card
# ─────────────────────────────────────────────
def _hero_card():
    return ui.card(
        ui.HTML(f"""
            <h2 style="
                font-size:28px; font-weight:700; color:{NAVY};
                margin-bottom:6px; line-height:1.2;
            ">
                Bilateral <span style="color:{BLUE};">Trends</span>
            </h2>

            <p style="
                font-size:14px; color:{TEXT}; line-height:1.65;
                text-align:justify; margin-bottom:18px;
            ">
                Bilateral FDI data reveal the <b>origin and destination of investment flows</b>
                between specific country pairs — going beyond aggregate totals to show
                <em>who invests where</em>. This tab identifies the <b>top 5 source economies</b>
                channeling FDI into a selected economy, and the <b>top 5 destinations</b> where
                that economy invests abroad, for both flows and stocks. A sixth category,
                <b>Rest of the World</b>, aggregates all remaining investor or destination
                economies not captured in the top 5, providing a complete picture of the
                bilateral investment landscape.
            </p>

            <div style="
                background:{BG_BLUE}; border:1px solid {BORDER};
                border-left:4px solid {BLUE}; border-radius:8px;
                padding:14px 18px; margin-bottom:18px;
            ">
                <p style="
                    font-size:11px; font-weight:700; letter-spacing:1.5px;
                    text-transform:uppercase; color:{BLUE}; margin-bottom:6px;
                ">📋 How to use this tab</p>
                <p style="font-size:14px; color:{TEXT}; margin:0; line-height:1.6;">
                    Select an <b>economy</b>, a <b>year</b> (2003–2023), and a <b>type</b>
                    (Flow or Stock) from the sidebar. The left chart shows the top 5 inward FDI
                    sources plus <b>Rest of the World</b>; the right chart shows the top 5 outward
                    FDI destinations plus <b>Rest of the World</b>. Hover over any slice for
                    precise values and shares. Download buttons are available for each dataset.
                </p>
            </div>

            <div style="display:flex; gap:24px; flex-wrap:wrap; font-size:12px; color:{MUTED};">
                <span>📅 <b>Coverage:</b> 2003–2023</span>
                <span>🔄 <b>Updated:</b> Annually</span>
                <span>📊 <b>Source:</b> UNCTAD</span>
                <span>🔒 For <b>WBG internal use only</b></span>
            </div>
        """),
        style=f"background:{BG_LIGHT}; border:1px solid {BORDER}; padding:28px 32px; margin-bottom:20px;"
    )

# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
def _sidebar():
    return ui.sidebar(

        ui.HTML(f"""
            <div style="
                background:{NAVY}; color:white;
                padding:10px 14px; border-radius:6px;
                margin-bottom:14px;
            ">
                <p style="font-size:13px; font-weight:700; margin:0; letter-spacing:0.5px;">
                    🌍 Economy of Interest
                </p>
                <p style="font-size:11px; margin:4px 0 0 0; opacity:0.8;">
                    Select one economy to explore its bilateral FDI relationships
                </p>
            </div>
        """),

        ui.input_selectize(
            "economy_bilateral",
            "Select Economy:",
            choices=[""] + _build_economy_list(),
            selected="",
            multiple=False,
            options={"placeholder": "Choose an economy", "allowEmptyOption": True}
        ),

        # Disable region separator headers
        ui.tags.script("""
        $(document).on('shiny:connected', function() {
            setTimeout(function() {
                var sel = $('#economy_bilateral')[0];
                if (sel && sel.selectize) {
                    function disableSeparators() {
                        sel.selectize.$dropdown_content.find('.option').each(function() {
                            var val = $(this).attr('data-value');
                            if (val && (val.startsWith('\u2014') || val.startsWith('\u2500\u2500'))) {
                                $(this).css({
                                    'color': '#888',
                                    'font-weight': '600',
                                    'font-style': 'normal',
                                    'pointer-events': 'none',
                                    'cursor': 'default',
                                    'background': '#f4f8fb'
                                });
                            }
                        });
                    }
                    sel.selectize.on('dropdown_open', disableSeparators);
                    sel.selectize.on('type', disableSeparators);
                }
            }, 500);
        });
        """),

        ui.hr(style=f"border-color:{BORDER}; margin:14px 0;"),

        ui.HTML(f"""
            <p style="font-size:12px; font-weight:700; color:{NAVY};
                      text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">
                📦 FDI Type
            </p>
        """),
        ui.input_radio_buttons(
            "bilateral_type",
            None,
            choices=["Stock", "Flow"],
            selected="Stock",
        ),

        ui.hr(style=f"border-color:{BORDER}; margin:14px 0;"),

        ui.HTML(f"""
            <p style="font-size:12px; font-weight:700; color:{NAVY};
                      text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">
                📅 Year of Interest
            </p>
        """),
        ui.input_slider(
            "bilateral_year",
            None,
            min=2003,
            max=2023,
            value=2023,
            step=1,
            sep=""
        ),

        ui.hr(style=f"border-color:{BORDER}; margin:14px 0;"),

        # Quick reference box
        ui.HTML(f"""
            <div style="
                background:{BG_BLUE}; border:1px solid {BORDER};
                border-radius:6px; padding:12px 14px;
                font-size:12px; color:{MUTED}; line-height:1.7;
            ">
                <p style="
                    font-size:11px; font-weight:700; color:{BLUE};
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;
                ">📌 Chart guide</p>
                <p style="margin:0;">
                    <b>Left chart</b> — Top 5 economies <em>investing into</em> the selected economy<br>
                    <b>Right chart</b> — Top 5 economies where the selected economy <em>invests abroad</em><br><br>
                    <b>Flow</b> = annual net FDI flows<br>
                    <b>Stock</b> = cumulative FDI position
                </p>
            </div>
        """),

        width=350,
    )


# ═════════════════════════════════════════════
#  bilateral_trends_ui()
# ═════════════════════════════════════════════
def bilateral_trends_ui():
    return ui.nav_panel(
        "Bilateral Trends",

        ui.layout_sidebar(
            _sidebar(),

            # Hero card
            _hero_card(),

            # Two pie charts
            ui.layout_columns(
                ui.div(
                    ui.card(
                        ui.card_header(
                            ui.HTML(f"<h6 style='text-align:left; color:{NAVY};'><b>Top 5 FDI Sources</b></h6>")
                        ),
                        ui.HTML(f"<p style='font-size:13px; color:{MUTED};'>Top 5 economies investing in the selected economy.</p>"),
                        output_widget("bilateral_inward_graph"),
                        ui.HTML("""
                            <p style='font-size:11px; color:gray; text-align:left; margin-top:6px;'>
                                <b>Source:</b> UNCTAD.
                            </p>
                        """),
                        full_screen=True,
                        fill=True,
                    ),
                ),
                ui.div(
                    ui.card(
                        ui.card_header(
                            ui.HTML(f"<h6 style='text-align:left; color:{NAVY};'><b>Top 5 FDI Destinations</b></h6>")
                        ),
                        ui.HTML(f"<p style='font-size:13px; color:{MUTED};'>Top 5 economies where the selected economy invests.</p>"),
                        output_widget("bilateral_outward_graph"),
                        ui.HTML("""
                            <p style='font-size:11px; color:gray; text-align:left; margin-top:6px;'>
                                <b>Source:</b> UNCTAD.
                            </p>
                        """),
                        full_screen=True,
                        fill=True,
                    ),
                ),
                col_widths=(6, 6)
            ),

            # Disclaimer
            ui.card(
                ui.HTML(f"""
                    <p style='font-size:13px; color:{MUTED}; text-align:justify;'>
                        <b>Technical Disclaimer:</b> <i>UNCTAD's bilateral data reproduce what economies publish
                        through their central banks or statistical offices, or report directly. UNCTAD does not
                        modify these figures through adjustments, imputations, or model-based estimates apart from
                        excluding <b>special purpose entities (SPEs)</b> when available, and does not reconcile
                        discrepancies between inward and outward data or between flows and stocks beyond the work
                        of primary compilers.<br><br>
                        Bilateral figures follow the <b>immediate-investor</b> principle, which may obscure ultimate
                        investor patterns when investment is routed through conduit economies. The inclusion or
                        exclusion of SPEs and financial centers can also significantly affect reported levels
                        and volatility.</i>
                    </p>
                """),
            ),

            # Download buttons
            ui.layout_columns(
                ui.div(
                    ui.div(
                        ui.download_button("download_bilateral_inflow",  "⬇ Download Bilateral Inflow Data (.csv)"),
                        style="text-align:center; margin-top:15px;"
                    ),
                    ui.div(
                        ui.download_button("download_bilateral_instock", "⬇ Download Bilateral Instock Data (.csv)"),
                        style="text-align:center; margin-top:8px;"
                    ),
                ),
                ui.div(
                    ui.div(
                        ui.download_button("download_bilateral_outflow",  "⬇ Download Bilateral Outflow Data (.csv)"),
                        style="text-align:center; margin-top:15px;"
                    ),
                    ui.div(
                        ui.download_button("download_bilateral_outstock", "⬇ Download Bilateral Outstock Data (.csv)"),
                        style="text-align:center; margin-top:8px;"
                    ),
                ),
                col_widths=(6, 6)
            ),
        )
    )


# ═════════════════════════════════════════════
#  bilateral_trends_server()
# ═════════════════════════════════════════════
def bilateral_trends_server(input: Inputs, output: Outputs, session: Session):

    def _empty_fig(msg="Select an economy to see data"):
        fig = go.Figure()
        fig.add_annotation(
            text=msg, showarrow=False,
            x=0.5, y=0.5, xref="paper", yref="paper",
            font=dict(size=16, color="gray")
        )
        fig.update_layout(
            template="simple_white", plot_bgcolor="white", paper_bgcolor="white",
            xaxis_visible=False, yaxis_visible=False,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        return fig

    # ── Inward pie chart ──────────────────────────────────────────────
    @output
    @render_widget
    def bilateral_inward_graph():
        economy  = input.economy_bilateral().strip("\u00a0").strip()
        year     = int(input.bilateral_year())
        fdi_type = input.bilateral_type()

        if not economy:
            return _empty_fig()

        if fdi_type == "Flow":
            df         = _bilateral_inflow.copy()
            econ_label = "Net Inflow (USD Billions)"
        else:
            df         = _bilateral_instock.copy()
            econ_label = "Inward Stock (USD Billions)"

        df_plot = df[(df["economy_dest"] == economy) & (df["year"] == year)].copy()

        if df_plot.empty:
            return _empty_fig("No data available for this selection")

        fig = px.pie(
            df_plot,
            values="value",
            names="economy_source",
            custom_data=["share"],
            labels={"value": econ_label, "economy_source": "Source Economy", "share": "Share"},
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        fig.for_each_trace(
            lambda t: t.update(labels=[
                "Rest of the World" if lbl == "Others" else lbl
                for lbl in t.labels
            ])
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{label}</b><br>" +
                econ_label + ": %{value:,.2f}<br>" +
                "Share: %{customdata[0]:.1%}<extra></extra>"
            ),
            textinfo="percent",
            textposition="inside",
            insidetextorientation="radial",
            automargin=True
        )

        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(
                title="Investor economy", orientation="v",
                x=1.05, y=0.5, xanchor="left", yanchor="middle"
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            title=dict(
                text=f"Sources of Inward FDI {fdi_type} into {economy} ({year})",
                x=0.50, y=0.98, xanchor="center", yanchor="top",
                font=dict(size=16, family="Segoe UI", color="black")
            ),
        )

        return fig

    # ── Outward pie chart ─────────────────────────────────────────────
    @output
    @render_widget
    def bilateral_outward_graph():
        economy  = input.economy_bilateral().strip("\u00a0").strip()
        year     = int(input.bilateral_year())
        fdi_type = input.bilateral_type()

        if not economy:
            return _empty_fig()

        if fdi_type == "Flow":
            df         = _bilateral_outflow.copy()
            econ_label = "Net Outflow (USD Billions)"
        else:
            df         = _bilateral_outstock.copy()
            econ_label = "Outward Stock (USD Billions)"

        df_plot = df[(df["economy_source"] == economy) & (df["year"] == year)].copy()

        if df_plot.empty:
            return _empty_fig("No data available for this selection")

        fig = px.pie(
            df_plot,
            values="value",
            names="economy_dest",
            custom_data=["share"],
            labels={"value": econ_label, "economy_dest": "Destination economy", "share": "Share"},
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        fig.for_each_trace(
            lambda t: t.update(labels=[
                "Rest of the World" if lbl == "Others" else lbl
                for lbl in t.labels
            ])
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{label}</b><br>" +
                econ_label + ": %{value:,.2f}<br>" +
                "Share: %{customdata[0]:.1%}<extra></extra>"
            ),
            textinfo="percent",
            textposition="inside",
            insidetextorientation="radial",
            automargin=True
        )

        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            legend=dict(
                title="Destination economy", orientation="v",
                x=1.05, y=0.5, xanchor="left", yanchor="middle"
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            title=dict(
                text=f"Destinations of Outward FDI {fdi_type} from {economy} ({year})",
                x=0.50, y=0.98, xanchor="center", yanchor="top",
                font=dict(size=16, family="Segoe UI", color="black")
            ),
        )

        return fig

    # ── Downloads ──────────────────────────────────────────────────────
    @output
    @render.download(filename="Bilateral_FDI_Inflow.csv")
    def download_bilateral_inflow():
        buf = io.StringIO()
        _bilateral_inflow.to_csv(buf, index=False)
        buf.seek(0)
        yield buf.getvalue().encode("utf-8")

    @output
    @render.download(filename="Bilateral_FDI_Instock.csv")
    def download_bilateral_instock():
        buf = io.StringIO()
        _bilateral_instock.to_csv(buf, index=False)
        buf.seek(0)
        yield buf.getvalue().encode("utf-8")

    @output
    @render.download(filename="Bilateral_FDI_Outflow.csv")
    def download_bilateral_outflow():
        buf = io.StringIO()
        _bilateral_outflow.to_csv(buf, index=False)
        buf.seek(0)
        yield buf.getvalue().encode("utf-8")

    @output
    @render.download(filename="Bilateral_FDI_Outstock.csv")
    def download_bilateral_outstock():
        buf = io.StringIO()
        _bilateral_outstock.to_csv(buf, index=False)
        buf.seek(0)
        yield buf.getvalue().encode("utf-8")