"""
business_environment_panel.py
──────────────────────────────
Drop-in Business Environment panel for Invest.Data.

USAGE in app.py
───────────────
1. Add import:
       from business_environment_panel import business_environment_ui, business_environment_server

2. Replace the existing "Business Environment" nav_panel in the UI with:
       business_environment_ui(),

3. Add to server():
       business_environment_server(input, output, session)

4. Remove from app.py's shared imports:
       business_environment_averages

5. Remove from app.py's server():
       assign_ordered_colors() [if only used by BE and Linkages — check first],
       business_env_timeseries(), filtered_business_environment_averages(),
       wbes_snapshot_graph(), download_business_avg()

NOTE: assign_ordered_colors() is also used by Linkages — keep it in app.py
      until linkages_panel.py is also extracted, then remove it from both.
"""

import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shiny import ui, render, reactive, Inputs, Outputs, Session
from shinywidgets import output_widget, render_widget

try:
    from shared import business_environment_averages as _be_averages
except ImportError:
    _be_averages = None


def _build_country_year_list():
    """
    Build a flat ordered list for ui.input_selectize with region names
    as unclickable separator headers, grouped by region then country_year.
    Matches the bilateral_trends pattern.
    """
    if _be_averages is None:
        return []

    if "region" not in _be_averages.columns:
        return [""] + sorted(_be_averages["country_year"].dropna().unique().tolist())

    ordered = [""]
    for region_name, grp in _be_averages.groupby("region", sort=True):
        ordered.append(f"\u2500\u2500 {region_name} \u2500\u2500")
        for cy in sorted(grp["country_year"].dropna().unique().tolist()):
            ordered.append(f"\u00a0\u00a0\u00a0\u00a0{cy}")

    return ordered


def _build_comparator_list():
    """
    Same as _build_country_year_list but without the leading empty string,
    used for the comparator multi-select.
    """
    if _be_averages is None:
        return []

    if "region" not in _be_averages.columns:
        return sorted(_be_averages["country_year"].dropna().unique().tolist())

    ordered = []
    for region_name, grp in _be_averages.groupby("region", sort=True):
        ordered.append(f"\u2500\u2500 {region_name} \u2500\u2500")
        for cy in sorted(grp["country_year"].dropna().unique().tolist()):
            ordered.append(f"\u00a0\u00a0\u00a0\u00a0{cy}")

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
#  Shared lookup tables
# ─────────────────────────────────────────────
LABEL_MAP = {
    "reg1":         "% of time in a week spent dealing with regulations (reg1)",
    "reg6":         "Firm visited or required to meet with tax officials (reg6)",
    "bus3":         "Days to obtain a construction permit (bus3)",
    "bus4":         "Days to obtain an occupancy license (bus4)",
    "bus2":         "Days to obtain an operating license (bus2)",
    "regeff_index": "Regulatory Efficiency Index (regeff_index)",
    "bus1":         "Days to obtain an import license (bus1)",
    "tr2":          "Days to clear imports through customs (tr2)",
    "tr1":          "Days to clear exports through customs (tr1)",
    "impexp_index": "Imports/Exports Efficiency Index (impexp_index)",
}

DESCRIPTION_MAP = {
    "reg1":         "Average percentage of senior management's time in a typical week spent dealing with regulations.",
    "reg6":         "Share of firms visited or required to meet with tax officials.",
    "bus1":         "Average number of days to obtain an import license.",
    "bus2":         "Average number of days to obtain an operating license.",
    "bus3":         "Average number of days to obtain a construction permit.",
    "bus4":         "Average number of days to obtain occupancy permit.",
    "tr1":          "Average number of days to clear exports.",
    "tr2":          "Average number of days to clear imports.",
    "regeff_index": "Average number of days to obtain regulatory approvals (construction, occupancy, operating).",
    "impexp_index": "Average number of days to obtain import/export approvals (import license, import/export customs clearance).",
}

N_MAP = {
    "reg1":         "N_reg1",
    "reg6":         "N_reg6",
    "bus1":         "N_bus1",
    "bus2":         "N_bus2",
    "bus3":         "N_bus3",
    "bus4":         "N_bus4",
    "tr1":          "N_tr1",
    "tr2":          "N_tr2",
    "regeff_index": "N_regeff_index",
    "impexp_index": "N_impexp_index",
}


# ─────────────────────────────────────────────
#  Helper: consistent bar colors
# ─────────────────────────────────────────────
def _assign_ordered_colors(df, selected_country):
    SAFE = px.colors.qualitative.Safe
    ordered = [selected_country] + [
        c for c in df["country_name"].unique().tolist() if c != selected_country
    ]
    color_map = {c: SAFE[i % len(SAFE)] for i, c in enumerate(ordered)}
    return [color_map[c] for c in df["country_name"]]


# ─────────────────────────────────────────────
#  Helper: empty figure
# ─────────────────────────────────────────────
def _empty_fig():
    fig = go.Figure()
    fig.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        xaxis=dict(showgrid=False, title=None),
        yaxis=dict(showgrid=True, gridcolor="lightgray", title=None),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=False
    )
    return fig


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
                Business <span style="color:{BLUE};">Environment</span>
            </h2>

            <p style="
                font-size:14px; color:{TEXT}; line-height:1.65;
                text-align:justify; margin-bottom:18px;
            ">
                The business environment shapes the conditions under which firms operate and
                investors make decisions. This tab draws on the
                <a href="https://www.enterprisesurveys.org/en/enterprisesurveys"
                target="_blank" style="color:{BLUE}; text-decoration:none; font-weight:500;">
                World Bank Enterprise Survey (WBES)</a>
                to track key <b>regulatory</b> and <b>trade efficiency indicators</b> — including
                licensing times, permit requirements, customs clearance, and composite indexes —
                across economies and over time.
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
                    Select an <b>economy and survey year</b>, a <b>business environment indicator</b>,
                    and up to <b>4 comparator economies</b> from the sidebar. The left chart shows
                    how the indicator has evolved over time; the right chart benchmarks the selected
                    economy against comparators for the chosen survey year.
                </p>
            </div>

            <div style="display:flex; gap:24px; flex-wrap:wrap; font-size:12px; color:{MUTED};">
                <span>📅 <b>Coverage:</b> Multiple WBES rounds</span>
                <span>🔄 <b>Updated:</b> Per survey availability</span>
                <span>📊 <b>Source:</b> World Bank Enterprise Surveys</span>
                <span>🔒 For <b>WBG internal use only</b></span>
            </div>
        """),
        style=f"background:{BG_LIGHT}; border:1px solid {BORDER}; padding:28px 32px; margin-bottom:20px;"
    )


# ─────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────
def _sidebar():
    _choices            = _build_country_year_list()
    _comparator_choices = _build_comparator_list()

    # Shared JS to disable separator headers in a selectize input
    def _disable_separators_js(input_id):
        return ui.tags.script(f"""
        $(document).on('shiny:connected', function() {{
            setTimeout(function() {{
                var sel = $('#{input_id}')[0];
                if (sel && sel.selectize) {{
                    function disableSeparators() {{
                        sel.selectize.$dropdown_content.find('.option').each(function() {{
                            var val = $(this).attr('data-value');
                            if (val && (val.startsWith('\u2014') || val.startsWith('\u2500\u2500'))) {{
                                $(this).css({{
                                    'color': '#888',
                                    'font-weight': '600',
                                    'font-style': 'normal',
                                    'pointer-events': 'none',
                                    'cursor': 'default',
                                    'background': '#f4f8fb'
                                }});
                            }}
                        }});
                    }}
                    sel.selectize.on('dropdown_open', disableSeparators);
                    sel.selectize.on('type', disableSeparators);
                }}
            }}, 500);
        }});
        """)

    return ui.sidebar(

        ui.HTML(f"""
            <div style="
                background:{NAVY}; color:white;
                padding:10px 14px; border-radius:6px;
                margin-bottom:14px;
            ">
                <p style="font-size:13px; font-weight:700; margin:0; letter-spacing:0.5px;">
                    🏭 Economy of Interest
                </p>
                <p style="font-size:11px; margin:4px 0 0 0; opacity:0.8;">
                    Select an economy and survey year
                </p>
            </div>
        """),

        ui.input_selectize(
            "country_year_select_be",
            "Select Economy and Year:",
            choices=_choices,
            selected="",
            multiple=False,
            options={"placeholder": "Choose an economy-year", "allowEmptyOption": True}
        ),

        _disable_separators_js("country_year_select_be"),

        ui.hr(style=f"border-color:{BORDER}; margin:14px 0;"),

        ui.HTML(f"""
            <p style="font-size:12px; font-weight:700; color:{NAVY};
                      text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">
                📊 Indicator of Interest
            </p>
        """),
        ui.input_select(
            "reg_variable",
            None,
            choices={
                "reg1":         "% of time in a week spent dealing with regulations (reg1)",
                "reg6":         "Firm visited or required to meet with tax officials (reg6)",
                "bus3":         "Days to obtain a construction permit (bus3)",
                "bus4":         "Days to obtain an occupancy license (bus4)",
                "bus2":         "Days to obtain an operating license (bus2)",
                "regeff_index": "Regulatory Efficiency Index (regeff_index)",
                "bus1":         "Days to obtain an import license (bus1)",
                "tr2":          "Days to clear imports through customs (tr2)",
                "tr1":          "Days to clear exports through customs (tr1)",
                "impexp_index": "Imports/Exports Efficiency Index (impexp_index)",
            },
            selected="",
        ),

        ui.hr(style=f"border-color:{BORDER}; margin:14px 0;"),

        ui.HTML(f"""
            <p style="font-size:12px; font-weight:700; color:{NAVY};
                      text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">
                🌍 Comparator Economies
            </p>
        """),
        ui.input_selectize(
            "comparator_countries_be",
            "Select up to 4 comparators (economy-year):",
            choices=_comparator_choices,
            multiple=True,
            selected=[],
            options={"maxItems": 4, "placeholder": "Select comparators"},
        ),

        _disable_separators_js("comparator_countries_be"),

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
                ">📌 Indicators</p>
                <p style="margin:0;">
                    <b>reg1</b> — Share of management time spent dealing with regulations<br>
                    <b>reg6</b> — Share of firms visited or required to meet with tax officials<br>
                    <b>bus1</b> — Avg. days to obtain an import license<br>
                    <b>bus2</b> — Avg. days to obtain an operating license<br>
                    <b>bus3</b> — Avg. days to obtain a construction permit<br>
                    <b>bus4</b> — Avg. days to obtain an occupancy license<br>
                    <b>tr1</b> — Avg. days to clear exports through customs<br>
                    <b>tr2</b> — Avg. days to clear imports through customs<br>
                    <b>regeff_index</b> — Avg. days to obtain regulatory approvals (bus2, bus3, bus4)<br>
                    <b>impexp_index</b> — Avg. days to obtain import/export approvals (bus1, tr1, tr2)
                </p>
            </div>
            <div style="
                background:{BG_BLUE}; border:1px solid {BORDER};
                border-radius:6px; padding:12px 14px;
                font-size:12px; color:{MUTED}; line-height:1.7;
                margin-top:10px;
            ">
                <p style="
                    font-size:11px; font-weight:700; color:{BLUE};
                    text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;
                ">💡 Interpretation</p>
                <p style="margin:0;">
                    All indicators are <b>weighted averages</b> of firm-level responses
                    using WBES survey weights.<br><br>
                    <b>Lower values = better performance</b> (fewer days, less time spent).
                </p>
            </div>
        """),
 
        width=350,
    )


# ═════════════════════════════════════════════
#  business_environment_ui()
# ═════════════════════════════════════════════
def business_environment_ui():
    return ui.nav_panel(
        "Business Environment",

        ui.layout_sidebar(
            _sidebar(),

            # Hero card
            _hero_card(),

            # Two charts
            ui.div(
                ui.layout_columns(

                    # Left: Time series
                    ui.card(
                        ui.card_header(
                            ui.HTML(f"<h6 style='text-align:left; color:{NAVY};'><b>Business Environment Indicators Over Time</b></h6>")
                        ),
                        ui.HTML(f"<p style='font-size:13px; color:{MUTED};'>Trend of selected indicator over available WBES survey years.</p>"),
                        output_widget("business_env_timeseries"),
                        ui.HTML("""
                            <p style='font-size:12px; color:gray; text-align:justify; margin-top:8px;'>
                                <b>Technical note:</b> Indicators show weighted averages of firm responses per economy-year,
                                computed using survey weights. The Regulatory Efficiency Index averages days to obtain a
                                construction permit, occupancy license, and operating license (when available). The
                                Imports/Exports Efficiency Index averages days to obtain an import license, clear imports
                                through customs, and clear exports through customs (when available). Lower values indicate
                                better (more efficient) regulatory and trade processes.
                            </p>
                            <p style='font-size:11px; color:gray; text-align:left;'>
                                <b>Source:</b> World Bank Enterprise Surveys.
                            </p>
                        """),
                        full_screen=True,
                        fill=True,
                    ),

                    # Right: Benchmarking
                    ui.card(
                        ui.card_header(
                            ui.HTML(f"<h6 style='text-align:left; color:{NAVY};'><b>Business Environment Benchmarking</b></h6>")
                        ),
                        ui.HTML(f"<p style='font-size:13px; color:{MUTED};'>Weighted averages of selected indicator across comparator economies.</p>"),
                        output_widget("wbes_snapshot_graph"),
                        ui.HTML("""
                            <p style='font-size:12px; color:gray; text-align:justify; margin-top:8px;'>
                                <b>Technical note:</b> Indicators show weighted averages of firm responses per economy-year,
                                computed using survey weights. Comparisons are limited to economies with available WBES data.
                            </p>
                            <p style='font-size:11px; color:gray; text-align:left;'>
                                <b>Source:</b> World Bank Enterprise Surveys.
                            </p>
                        """),
                        full_screen=True,
                        fill=True,
                    ),

                    col_widths=(6, 6)
                ),

                ui.div(
                    ui.download_button(
                        "download_business_avg",
                        "⬇ Download Business Environment Data (.csv)"
                    ),
                    style="text-align:center; margin-top:25px;"
                )
            )
        )
    )


# ═════════════════════════════════════════════
#  business_environment_server()
# ═════════════════════════════════════════════
def business_environment_server(input: Inputs, output: Outputs, session: Session):

    # ── Time series chart ──────────────────────────────────────────────
    @output
    @render_widget
    def business_env_timeseries():
        variable = input.reg_variable()
        selected = input.country_year_select_be().strip("\u00a0").strip()

        if not variable or not selected or _is_separator(selected):
            return _empty_fig()

        country = selected.split("(")[0].strip()
        df = _be_averages[_be_averages["country_name"] == country].copy()

        if df.empty:
            return _empty_fig()

        df      = df.sort_values("year")
        n_col   = N_MAP.get(variable)

        customdata = np.stack([
            df["country_year"].astype(str),
            df.apply(lambda _: DESCRIPTION_MAP.get(variable), axis=1),
            df[variable].apply(lambda v: f"{v:.3f}" if pd.notna(v) else "NA"),
            df["N_obs"].apply(lambda n: f"{int(n):,}" if pd.notna(n) else "NA"),
            df[n_col].apply(lambda n: f"{int(n):,}" if pd.notna(n) else "NA"),
        ], axis=-1)

        marker_colors  = _assign_ordered_colors(df, country)
        selected_color = marker_colors[0]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["year"],
            y=df[variable],
            marker_color=selected_color,
            text=df[variable].apply(lambda v: f"{v:.2f}" if pd.notna(v) else ""),
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br><br>"
                f"<b>Indicator:</b> {LABEL_MAP.get(variable, variable)}<br>"
                "<b>Description:</b> %{customdata[1]}<br>"
                "<b>Weighted Avg:</b> %{customdata[2]}<br>"
                "<b>Valid Observations:</b> %{customdata[4]}<br>"
                "<b>Survey Size:</b> %{customdata[3]}<extra></extra>"
            )
        ))

        fig.update_layout(
            template="simple_white",
            title=dict(
                text=f"{country}: {LABEL_MAP.get(variable, variable)} over time",
                x=0.5, y=0.98, xanchor="center", yanchor="top",
                font=dict(size=16, family="Segoe UI", color="black")
            ),
            xaxis=dict(
                title="Year", showline=True, linecolor="black",
                tickmode="array", tickvals=df["year"].tolist()
            ),
            yaxis=dict(title="Weighted Average", showline=True, linecolor="black"),
            margin=dict(l=40, r=40, t=60, b=40)
        )

        return fig

    # ── Reactive filtered data ─────────────────────────────────────────
    @reactive.calc
    def filtered_business_environment_averages():
        country_year = input.country_year_select_be().strip("\u00a0").strip()
        if not country_year or _is_separator(country_year):
            return pd.DataFrame()

        comparators = [
            c.strip("\u00a0").strip()
            for c in (input.comparator_countries_be() or [])
            if not _is_separator(c)
        ]
        variable       = input.reg_variable()
        selected_values = [country_year] + comparators if comparators else [country_year]

        df = _be_averages[_be_averages["country_year"].isin(selected_values)].copy()
        if df.empty:
            return pd.DataFrame()

        n_col = N_MAP.get(variable)
        df = df[[
            "country_name", "year", "country_year", variable, "N_obs", n_col
        ]].rename(columns={variable: "value", n_col: "N_valid"})

        return df.replace({np.nan: None})

    # ── Benchmarking chart ─────────────────────────────────────────────
    @output
    @render_widget
    def wbes_snapshot_graph():
        df = filtered_business_environment_averages()
        if df.empty:
            return _empty_fig()

        variable           = input.reg_variable()
        indicator_label    = LABEL_MAP.get(variable, variable)
        indicator_desc     = DESCRIPTION_MAP.get(variable)

        df["label_val"] = df["value"].apply(lambda v: f"{v:,.2f}" if pd.notna(v) else "NA")

        customdata = np.stack([
            df["country_year"].astype(str),
            df.apply(lambda _: indicator_desc, axis=1),
            df["label_val"].astype(str),
            df["N_obs"].apply(lambda n: f"{int(n):,}" if pd.notna(n) else "NA"),
            df["N_valid"].apply(lambda n: f"{int(n):,}" if pd.notna(n) else "NA"),
        ], axis=-1)

        selected_country = input.country_year_select_be().strip("\u00a0").strip().split("(")[0].strip()
        marker_colors    = _assign_ordered_colors(df, selected_country)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df["country_year"],
            y=df["value"],
            text=df["label_val"],
            marker_color=marker_colors,
            textposition="inside",
            insidetextanchor="middle",
            textfont=dict(color="white"),
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br><br>"
                f"<b>Indicator:</b> {indicator_label}<br>"
                "<b>Description:</b> %{customdata[1]}<br>"
                "<b>Weighted Avg:</b> %{customdata[2]}<br>"
                "<b>Valid Observations:</b> %{customdata[4]}<br>"
                "<b>Survey Size:</b> %{customdata[3]}<extra></extra>"
            )
        ))

        fig.update_layout(
            template="simple_white",
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                title="Economy (selected year)", showgrid=False,
                showline=True, linewidth=1, linecolor="black"
            ),
            yaxis=dict(title="Weighted Average", showline=True, linecolor="black"),
            showlegend=False,
            margin=dict(l=40, r=40, t=60, b=40),
            title=dict(
                text=f"Benchmarking on {indicator_label}",
                x=0.5, y=0.98, xanchor="center", yanchor="top",
                font=dict(size=16, family="Segoe UI", color="black")
            )
        )

        return fig

    # ── Download ───────────────────────────────────────────────────────
    @output
    @render.download(filename="business_environment_averages_data.csv")
    def download_business_avg():
        buf = io.StringIO()
        _be_averages.copy().to_csv(buf, index=False)
        buf.seek(0)
        yield buf.getvalue().encode("utf-8")