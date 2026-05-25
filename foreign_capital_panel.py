"""
foreign_capital_panel.py
────────────────────────
Drop-in Foreign Capital panel for Invest.Data.

USAGE in app.py
───────────────
1. Add import:
       from foreign_capital_panel import foreign_capital_ui, foreign_capital_server

2. Replace the existing "Foreign Capital" nav_panel in the UI with:
       foreign_capital_ui(),

3. Add to server():
       foreign_capital_server(input, output, session)

4. Remove from app.py's shared imports:
       foreign_capital_df, ordered_economies_capital

5. Remove from app.py's server():
       foreign_plot(), foreign_capital(), download_foreign_capital()
"""

import io
import numpy as np
import plotly.graph_objects as go
from shiny import ui, render, reactive, Inputs, Outputs, Session
from shinywidgets import output_widget, render_widget

try:
    from shared import foreign_capital_df as _foreign_capital_df
    from shared import ordered_economies_capital as _ordered_economies_capital
except ImportError:
    _foreign_capital_df        = None
    _ordered_economies_capital = []

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
                Foreign <span style="color:{BLUE};">Capital</span> Inflows
            </h2>

            <p style="
                font-size:14px; color:{TEXT}; line-height:1.65;
                text-align:justify; margin-bottom:18px;
            ">
                Foreign capital inflows capture the full spectrum of cross-border investment
                flows into an economy — including <b>foreign direct investment (FDI)</b>,
                <b>portfolio investment</b>, and <b>other investment flows</b> — as reported
                in the IMF Balance of Payments. Tracking these flows over time helps reveal
                how economies integrate into global capital markets and how vulnerable they
                may be to external shocks.
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
                    Select an <b>economy, region, or income group</b> from the sidebar to
                    visualize net inflow trends between <b>2000 and 2024</b>. Bars show
                    inflows by component in current USD billions; the line shows inflows
                    as a share of GDP. Use the download button to export the data as CSV.
                </p>
            </div>

            <div style="display:flex; gap:24px; flex-wrap:wrap; font-size:12px; color:{MUTED};">
                <span>📅 <b>Coverage:</b> 2000–2024</span>
                <span>🔄 <b>Updated:</b> Annually</span>
                <span>📊 <b>Source:</b> IMF Balance of Payments · World Bank WDI</span>
                <span>🔒 For <b>WBG internal use only</b></span>
            </div>
        """),
        style=f"background:{BG_LIGHT}; border:1px solid {BORDER}; padding:28px 32px; margin-bottom:20px;"
    )


# ─────────────────────────────────────────────
#  Sidebar content
# ─────────────────────────────────────────────
def _sidebar():
    return ui.sidebar(

        # Sidebar title
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
                    Countries · Regions · Income groups
                </p>
            </div>
        """),

        ui.input_selectize(
            "economy_capital",
            "Select Economy:",
            choices=[""] + _ordered_economies_capital,
            selected="",
            multiple=False,
            options={"placeholder": "Choose an economy", "allowEmptyOption": True}
        ),

        # Disable separator options in dropdown
        ui.tags.script("""
        $(document).on('shiny:connected', function() {
            setTimeout(function() {
                var sel = $('#economy_capital')[0];
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

        ui.hr(style=f"border-color:{BORDER}; margin:16px 0;"),

        # Quick reference box
        ui.HTML(f"""
            <div style="
                background:{BG_BLUE}; border:1px solid {BORDER};
                border-radius:6px; padding:12px 14px;
                font-size:12px; color:{MUTED}; line-height:1.6;
            ">
                <p style="
                    font-size:11px; font-weight:700; color:{BLUE};
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;
                ">📌 Components</p>
                <p style="margin:0;">
                    <span style="
                        display:inline-block; width:10px; height:10px;
                        background:#9ecae1; border-radius:2px; margin-right:5px;
                    "></span><b>FDI</b> — Foreign Direct Investment<br>
                    <span style="
                        display:inline-block; width:10px; height:10px;
                        background:#08306b; border-radius:2px; margin-right:5px;
                    "></span><b>Portfolio</b> — Portfolio inflows<br>
                    <span style="
                        display:inline-block; width:10px; height:10px;
                        background:#cb181d; border-radius:2px; margin-right:5px;
                    "></span><b>Other</b> — Financial derivatives &amp; other<br>
                    <span style="
                        display:inline-block; width:10px; height:10px;
                        background:black; border-radius:2px; margin-right:5px;
                    "></span><b>Line</b> — Total inflows (% of GDP)
                </p>
            </div>
        """),

        width=350,
    )


# ═════════════════════════════════════════════
#  foreign_capital_ui()
# ═════════════════════════════════════════════
def foreign_capital_ui():
    return ui.nav_panel(
        "Foreign Capital",

        ui.layout_sidebar(
            _sidebar(),

            # Hero card
            _hero_card(),

            # Main chart card
            ui.card(
                ui.card_header(
                    ui.HTML(f"<h6 style='text-align:left; color:{NAVY};'><b>Foreign Capital Net Inflows (2000–2024)</b></h6>")
                ),
                output_widget("foreign_capital"),
                ui.HTML("""
                    <p style='font-size:12px; color:gray; text-align:justify; margin-top:8px;'>
                        <b>Technical note:</b> Foreign capital inflows are reported net of divestments and sales of assets
                        held by nonresidents, as recorded in the Balance of Payments and compiled by the International
                        Monetary Fund (IMF). Bars show foreign capital inflows in current prices (left axis), while the
                        trend line shows their share of GDP (right axis). GDP data are sourced from the World Bank's World
                        Development Indicators (WDI). Negative values of foreign capital inflows as a share of GDP reflect
                        net divestment by nonresidents in a given year, expressed relative to the economy's GDP in that
                        same year. Other inflows include financial derivatives and other investment flows as labeled by the
                        IMF. Aggregates for regions, income groups, and global totals are calculated by World Bank staff.
                    </p>
                    <p style='font-size:11px; color:gray; text-align:left;'>
                        <b>Source:</b> International Monetary Fund (IMF), Balance of Payments;
                        World Bank, World Development Indicators (WDI).
                    </p>
                """),
                full_screen=True,
                fill=True,
            ),

            # Disclaimer card
            ui.card(
                ui.HTML(f"""
                    <p style='font-size:13px; color:{MUTED}; text-align:justify;'>
                        <b>Technical Disclaimer:</b> <i>Foreign capital inflows are computed as reported in the IMF
                        Balance of Payments, with no further imputation performed by the World Bank staff to fill
                        missing values. Economy-year observations with missing values for any foreign capital flow
                        component/type or nominal GDP are excluded from the calculation of the overall share of
                        foreign capital inflows when aggregating economies at the income, regional and global levels.</i>
                    </p>
                """),
            ),

            # Download button
            ui.div(
                ui.download_button(
                    "download_foreign_capital",
                    "⬇ Download Foreign Capital Net Inflows Data (.csv)"
                ),
                style="text-align:center; margin-top:20px;"
            ),
        )
    )


# ═════════════════════════════════════════════
#  foreign_capital_server()
# ═════════════════════════════════════════════
def foreign_capital_server(input: Inputs, output: Outputs, session: Session):

    # ── Reactive filtered dataset ──────────────────────────────────────
    @reactive.calc
    def foreign_plot():
        selected = input.economy_capital()
        if not selected:
            return __import__("pandas").DataFrame()
        selected = selected.strip("\u00a0").strip()
        if selected.startswith("—") or selected.startswith("\u2500\u2500"):
            return __import__("pandas").DataFrame()
        return _foreign_capital_df[_foreign_capital_df["economy"] == selected]

    # ── Chart ──────────────────────────────────────────────────────────
    @output
    @render_widget
    def foreign_capital():
        dff = foreign_plot()

        if dff.empty:
            fig = go.Figure()
            fig.update_layout(
                plot_bgcolor="white", paper_bgcolor="white",
                xaxis=dict(showgrid=False, title=None),
                yaxis=dict(showgrid=True, gridcolor="lightgray", title=None),
                margin=dict(l=0, r=10, t=10, b=10),
                showlegend=False
            )
            return fig

        # Line data
        df_line = (
            dff[["year", "inflows_pct_gdp_plot", "inflows_pct_gdp_hover",
                 "gdp_wdi", "total_inflows", "economy"]]
            .drop_duplicates()
            .dropna(subset=["inflows_pct_gdp_plot"])
            .sort_values("year")
        )

        # Y-axis scale
        y1_min = dff[["stack_top", "stack_bottom"]].min().min()
        y1_max = dff[["stack_top", "stack_bottom"]].max().max()
        pad    = 0.1 * (y1_max - y1_min) if y1_max != y1_min else 1
        y1_min -= pad
        y1_max += pad

        fig = go.Figure()

        color_map   = {"FDI": "#9ecae1", "Portfolio inflows": "#08306b", "Other inflows": "#cb181d"}
        stack_order = ["FDI", "Portfolio inflows", "Other inflows"]

        for comp in stack_order:
            d = dff[dff["inflow_type_label"] == comp].copy()
            d["base"] = d["base"].fillna(0)
            fig.add_bar(
                x=d["year"],
                y=d["inflow_value"],
                base=d["base"],
                name=comp,
                marker_color=color_map[comp],
                customdata=np.stack(
                    [d["inflow_value"], d["year"], d["inflows_pct_gdp_hover"],
                     d["gdp_wdi"], d["total_inflows"], d["economy"]],
                    axis=-1
                ),
                hovertemplate=(
                    "<b>Economy:</b> %{customdata[5]}<br>"
                    "<b>Year:</b> %{customdata[1]}<br><br>"
                    "<b>Foreign capital component:</b> " + comp + "<br>"
                    "<b>Component value:</b> %{customdata[0]:,.1f} US$ bn<br><br>"
                    "<b>Total foreign capital inflows:</b> %{customdata[4]:,.1f} US$ bn<br>"
                    "<b>Total foreign capital inflows (% of GDP):</b> %{customdata[2]}<br>"
                    "<b>Nominal GDP:</b> %{customdata[3]:,.1f} US$ bn"
                    "<extra></extra>"
                )
            )

        if not df_line.empty:
            fig.add_trace(go.Scatter(
                x=df_line["year"],
                y=df_line["inflows_pct_gdp_plot"],
                mode="lines",
                name="Inflows (% of GDP)",
                yaxis="y2",
                line=dict(color="black", width=3),
                customdata=np.stack(
                    [df_line["inflows_pct_gdp_hover"], df_line["total_inflows"],
                     df_line["gdp_wdi"], df_line["economy"]],
                    axis=-1
                ),
                hovertemplate=(
                    "<b>Economy:</b> %{customdata[3]}<br>"
                    "<b>Year:</b> %{x}<br><br>"
                    "<b>Total foreign capital inflows:</b> %{customdata[1]:,.1f} US$ bn<br>"
                    "<b>Total foreign capital inflows (% of GDP):</b> %{customdata[0]}<br>"
                    "<b>Nominal GDP:</b> %{customdata[2]:,.1f} US$ bn"
                    "<extra></extra>"
                )
            ))

            y2_data_min  = df_line["inflows_pct_gdp_plot"].min()
            y2_data_max  = df_line["inflows_pct_gdp_plot"].max()
            y1_min_adj   = min(y1_min, 0)
            y1_max_adj   = max(y1_max, 0)
            zero_ratio   = abs(y1_min_adj) / (y1_max_adj - y1_min_adj) if (y1_max_adj - y1_min_adj) != 0 else 0.5
            y2_max_abs      = max(abs(y2_data_min), abs(y2_data_max), 1e-9)
            pad_y2          = 0.10 * y2_max_abs          # 10% headroom above the line
            y2_min_aligned  = -(zero_ratio / (1 - zero_ratio)) * y2_max_abs
            y2_max_aligned  = y2_max_abs + pad_y2
        else:
            y2_min_aligned = 0
            y2_max_aligned = 1
            y1_min_adj     = y1_min
            y1_max_adj     = y1_max

        economy_name = dff["economy"].iloc[0]

        fig.update_layout(
            barmode="overlay",
            plot_bgcolor="white",
            paper_bgcolor="white",
            title=dict(
                text=f"<b>{economy_name}</b><br><span style='font-size:13px;'>Foreign Capital Net Inflows, 2000–2024</span>",
                x=0.5, y=0.95, xanchor="center", yanchor="top"
            ),
            yaxis=dict(
                title="US$ billions (current prices)",
                range=[y1_min_adj, y1_max_adj],
                zeroline=True, zerolinecolor="black",
                showgrid=True, gridcolor="LightGray", tickformat=".1f"
            ),
            yaxis2=dict(
                title="Foreign capital inflows (% of GDP)",
                range=[y2_min_aligned, y2_max_aligned],
                overlaying="y", side="right", tickformat=".1f", showgrid=False
            ),
            legend=dict(orientation="h", yanchor="top", y=-0.07, xanchor="center", x=0.5),
            margin=dict(l=30, r=30, t=80, b=30),
            template="plotly_white"
        )

        fig.add_hline(y=0, line_color="black", line_width=1)
        fig.update_xaxes(
            tickmode="array",
            tickvals=[2000, 2005, 2010, 2015, 2020, 2024],
            ticktext=["2000", "2005", "2010", "2015", "2020", "2024"]
        )

        return fig

    # ── Download ───────────────────────────────────────────────────────
    @output
    @render.download(filename="foreign_capital.csv")
    def download_foreign_capital():
        buf = io.StringIO()
        _foreign_capital_df.copy().to_csv(buf, index=False)
        buf.seek(0)
        yield buf.getvalue().encode("utf-8")