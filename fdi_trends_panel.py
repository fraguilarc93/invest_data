"""
fdi_trends_panel.py
────────────────────
Drop-in FDI Trends panel for Invest.Data.

USAGE in app.py
───────────────
1. Add import:
       from fdi_trends_panel import fdi_trends_ui, fdi_trends_server

2. Replace the existing "FDI Trends" nav_panel in the UI with:
       fdi_trends_ui(),

3. Add to server():
       fdi_trends_server(input, output, session)

4. Remove from app.py's shared imports:
       fdi_trends, fdi_iqr, ordered_economies

5. Remove from app.py's server():
       indicator_map, fdi_trends_graph(), fdi_trends_bar(), download_fdi_trends()
"""

import io
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shiny import ui, render, Inputs, Outputs, Session
from shinywidgets import output_widget, render_widget

try:
    from shared import fdi_trends as _fdi_trends
    from shared import fdi_iqr    as _fdi_iqr
    from shared import ordered_economies as _ordered_economies
except ImportError:
    _fdi_trends        = None
    _fdi_iqr           = None
    _ordered_economies = []

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
#  Indicator map
# ─────────────────────────────────────────────
INDICATOR_MAP = {
    "US$ billions (current prices)": {
        ("Inward",  "Flow"):  "fdi_inward_flow",
        ("Outward", "Flow"):  "fdi_outward_flow",
        ("Inward",  "Stock"): "fdi_inward_stock",
        ("Outward", "Stock"): "fdi_outward_stock",
    },
    "% change from 2000 baseline (US$ billions)": {
        ("Inward",  "Flow"):  "fdi_inward_flow_pct_change",
        ("Outward", "Flow"):  "fdi_outward_flow_pct_change",
        ("Inward",  "Stock"): "fdi_inward_stock_pct_change",
        ("Outward", "Stock"): "fdi_outward_stock_pct_change",
    },
    "Share of Global Total": {
        ("Inward",  "Flow"):  "fdi_pct_inward_flow",
        ("Outward", "Flow"):  "fdi_pct_outward_flow",
        ("Inward",  "Stock"): "fdi_pct_inward_stock",
        ("Outward", "Stock"): "fdi_pct_outward_stock",
    },
    "Share of Gross Domestic Product (GDP)": {
        ("Inward",  "Flow"):  "fdi_gdp_inward_flow",
        ("Outward", "Flow"):  "fdi_gdp_outward_flow",
        ("Inward",  "Stock"): "fdi_gdp_inward_stock",
        ("Outward", "Stock"): "fdi_gdp_outward_stock",
    },
}

def _is_separator(val: str) -> bool:
    v = val.strip()
    return v.startswith("—") or v.startswith("\u2500\u2500")

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
                FDI <span style="color:{BLUE};">Trends</span>
            </h2>

            <p style="
                font-size:14px; color:{TEXT}; line-height:1.65;
                text-align:justify; margin-bottom:18px;
            ">
                Foreign Direct Investment (FDI) flows and stocks reflect the long-term
                commitment of investors to productive assets across borders. This tab allows
                to track <b>inward and outward FDI trends</b> across economies, regions,
                and income groups — comparing performance over time and benchmarking against
                global peers using multiple indicators.
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
                    Select up to <b>five economies</b> from the sidebar, then choose the
                    <b>direction</b> (Inward / Outward), <b>type</b> (Flow / Stock), and
                    <b>indicator</b>. The left chart shows trends from 2000 to 2024 with
                    a global IQR reference band. The right chart benchmarks selected economies
                    in the most recent year available.
                </p>
            </div>

            <div style="display:flex; gap:24px; flex-wrap:wrap; font-size:12px; color:{MUTED};">
                <span>📅 <b>Coverage:</b> 2000–2024</span>
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
                    🌍 Economies of Interest
                </p>
                <p style="font-size:11px; margin:4px 0 0 0; opacity:0.8;">
                    Select up to 5 · Countries · Regions · Income groups
                </p>
            </div>
        """),

        ui.input_selectize(
            "economy_trends",
            "Select Economies:",
            choices=_ordered_economies,
            multiple=True,
            options={
                "maxItems": 5,
                "placeholder": "Choose up to 5 economies"
            }
        ),

        # Disable separator options
        ui.tags.script("""
        $(document).on('shiny:connected', function() {
            setTimeout(function() {
                var sel = $('#economy_trends')[0];
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
                ↔ FDI Direction
            </p>
        """),
        ui.input_radio_buttons(
            "fdi_direction",
            None,
            choices=["Inward", "Outward"],
            selected="Inward"
        ),

        ui.hr(style=f"border-color:{BORDER}; margin:14px 0;"),

        ui.HTML(f"""
            <p style="font-size:12px; font-weight:700; color:{NAVY};
                      text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">
                📦 FDI Type
            </p>
        """),
        ui.input_radio_buttons(
            "fdi_type",
            None,
            choices=["Flow", "Stock"],
            selected="Flow"
        ),

        ui.hr(style=f"border-color:{BORDER}; margin:14px 0;"),

        ui.HTML(f"""
            <p style="font-size:12px; font-weight:700; color:{NAVY};
                      text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">
                📈 Indicator
            </p>
        """),
        ui.input_radio_buttons(
            "fdi_indicator",
            None,
            choices=[
                "US$ billions (current prices)",
                "% change from 2000 baseline (US$ billions)",
                "Share of Global Total",
                "Share of Gross Domestic Product (GDP)",
            ],
            selected="US$ billions (current prices)"
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
                    <b>Left chart</b> — trends over time<br>
                    <b>Right chart</b> — latest year snapshot<br>
                    <span style="color:#888;">░░</span> Shaded band = Global IQR<br>
                    <span style="border-bottom:2px dashed #666; display:inline-block; width:18px; margin-bottom:2px;"></span>
                    Dashed line = Global Median
                </p>
            </div>
        """),

        width=350,

        style="max-height:85vh; overflow-y:auto;"
    )


# ═════════════════════════════════════════════
#  fdi_trends_ui()
# ═════════════════════════════════════════════
def fdi_trends_ui():
    return ui.nav_panel(
        "FDI Trends",

        ui.layout_sidebar(
            _sidebar(),

            # Hero card
            _hero_card(),

            # Two-column chart area
            ui.div(
                ui.layout_columns(

                    # Left: Line chart
                    ui.card(
                        ui.card_header(
                            ui.HTML(f"<h6 style='text-align:left; color:{NAVY};'><b>FDI Trends (2000–2024)</b></h6>")
                        ),
                        ui.HTML(f"<p style='font-size:13px; color:{MUTED};'>Select filters from the sidebar to generate the chart.</p>"),
                        output_widget("fdi_trends_graph"),
                        ui.HTML("""
                            <p style='font-size:11px; color:gray; text-align:left; margin-top:6px;'>
                                <b>Source:</b> UNCTAD.
                            </p>
                        """),
                        full_screen=True,
                        fill=True,
                    ),

                    # Right: Bar chart
                    ui.card(
                        ui.card_header(
                            ui.HTML(f"<h6 style='text-align:left; color:{NAVY};'><b>FDI Benchmarking</b></h6>")
                        ),
                        ui.HTML(f"<p style='font-size:13px; color:{MUTED};'>FDI values for selected economies in the latest available year.</p>"),
                        output_widget("fdi_trends_bar"),
                        ui.HTML("""
                            <p style='font-size:11px; color:gray; text-align:left; margin-top:6px;'>
                                <b>Source:</b> UNCTAD.
                            </p>
                        """),
                        full_screen=True,
                        fill=True,
                    ),

                    col_widths=(6, 6)
                ),

                ui.div(
                    ui.download_button(
                        "download_fdi_trends",
                        "⬇ Download FDI Trends Data (.csv)"
                    ),
                    style="text-align:center; margin-top:20px;"
                )
            )
        )
    )


# ═════════════════════════════════════════════
#  fdi_trends_server()
# ═════════════════════════════════════════════
def fdi_trends_server(input: Inputs, output: Outputs, session: Session):

    # ── Line chart ────────────────────────────────────────────────────
    @output
    @render_widget
    def fdi_trends_graph():
        # AFTER
        economies = [e.strip("\u00a0").strip() for e in input.economy_trends() if not _is_separator(e)]
        direction = input.fdi_direction()
        fdi_type  = input.fdi_type()
        indicator = input.fdi_indicator()

        var = INDICATOR_MAP[indicator][(direction, fdi_type)]
        df  = _fdi_trends[_fdi_trends["economy"].isin(economies)].copy()

        if df.empty:
            fig = go.Figure()
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                xaxis=dict(showgrid=False, title=None),
                yaxis=dict(showgrid=True, gridcolor="lightgray", title=None),
                margin=dict(l=40, r=40, t=60, b=40),
                showlegend=False
            )
            return fig

        fig = px.line(
            df, x="year", y=var, color="economy",
            title=f"{indicator} ({direction} {fdi_type})",
            labels={"year": "Year", var: indicator},
            color_discrete_sequence=px.colors.qualitative.Safe,
        )

        if indicator == "US$ billions (current prices)":
            hover_template = (
                "<b>%{fullData.name}</b><br>"
                "Year: %{x}<br>"
                f"{indicator}: %{{y:,.2f}}<extra></extra>"
            )
        else:
            hover_template = (
                "<b>%{fullData.name}</b><br>"
                "Year: %{x}<br>"
                f"{indicator}: %{{y:,.2f}}%<extra></extra>"
            )

        fig.update_traces(mode="lines+markers", hovertemplate=hover_template)

        # IQR and Median
        iqr_q25    = f"{var}_q25"
        iqr_median = f"{var}_median"
        iqr_q75    = f"{var}_q75"

        if all(c in _fdi_iqr.columns for c in [iqr_q25, iqr_median, iqr_q75]):
            iqr_df = _fdi_iqr[["year", iqr_q25, iqr_median, iqr_q75]].copy()

            fig.add_trace(go.Scatter(
                x=list(iqr_df["year"]) + list(iqr_df["year"][::-1]),
                y=list(iqr_df[iqr_q75]) + list(iqr_df[iqr_q25][::-1]),
                fill="toself",
                fillcolor="rgba(150,150,150,0.25)",
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                showlegend=True,
                name="Global IQR"
            ))

            fig.add_trace(go.Scatter(
                x=iqr_df["year"],
                y=iqr_df[iqr_median],
                mode="lines",
                line=dict(color="rgba(50,50,50,0.7)", width=2, dash="dash"),
                name="Global Median"
            ))

        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(showgrid=False, gridcolor="lightgray", title=None),
            yaxis=dict(showgrid=True, gridcolor="lightgray"),
            legend=dict(
                title="Economy", orientation="v",
                x=1.05, y=0.5, xanchor="left", yanchor="middle"
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            title_x=0.5, title_y=0.98,
            title_font=dict(size=16, family="Segoe UI", color="black")
        )

        fig.add_hline(y=0, line_dash="solid", line_color="black", opacity=0.9)

        return fig

    # ── Bar chart ─────────────────────────────────────────────────────
    @output
    @render_widget
    def fdi_trends_bar():
        economies = [
            e.strip("\u00a0").strip()
            for e in input.economy_trends()
            if not (e.strip("\u00a0").strip().startswith("—") or
                    e.strip("\u00a0").strip().startswith("\u2500\u2500"))
        ]
        direction = input.fdi_direction()
        fdi_type  = input.fdi_type()
        indicator = input.fdi_indicator()

        var         = INDICATOR_MAP[indicator][(direction, fdi_type)]
        latest_year = _fdi_trends["year"].max()
        df          = _fdi_trends[
            (_fdi_trends["year"] == latest_year) &
            (_fdi_trends["economy"].isin(economies))
        ].copy()

        if df.empty:
            fig = go.Figure()
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                xaxis=dict(showgrid=False, title=None),
                yaxis=dict(showgrid=True, gridcolor="lightgray", title=None),
                margin=dict(l=40, r=40, t=60, b=40),
                showlegend=False,
                title_x=0.5, title_y=1,
                title_font=dict(size=16, family="Segoe UI", color="black")
            )
            return fig

        if indicator == "US$ billions (current prices)":
            df["label_val"] = df[var].apply(lambda v: f"{v:,.2f}" if pd.notna(v) else "NA")
        else:
            def fmt_pct(v):
                if pd.isna(v):
                    return "NA"
                return f"{v:,.2f}%" if abs(v) < 1 else f"{v:,.1f}%"
            df["label_val"] = df[var].apply(fmt_pct)

        fig = px.bar(
            df, x="economy", y=var, text="label_val", color="economy",
            title=f"{indicator} ({direction} {fdi_type}) in {latest_year}",
            color_discrete_sequence=px.colors.qualitative.Safe,
        )

        fig.update_traces(
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            hovertemplate=f"<b>%{{x}}</b><br>{indicator}: %{{text}}<extra></extra>"
        )

        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            xaxis=dict(title=None, showgrid=False),
            yaxis=dict(title=None, showgrid=True, gridcolor="lightgray"),
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40),
            title_x=0.5, title_y=0.98,
            title_font=dict(size=16, family="Segoe UI", color="black")
        )

        fig.add_hline(y=0, line_color="black", opacity=0.8)

        return fig

    # ── Download ───────────────────────────────────────────────────────
    @output
    @render.download(filename="fdi_trends.csv")
    def download_fdi_trends():
        buf = io.StringIO()
        _fdi_trends.to_csv(buf, index=False)
        buf.seek(0)
        yield buf.getvalue().encode("utf-8")