"""
linkages_panel.py
──────────────────
Drop-in Foreign Linkages panel for Invest.Data.

USAGE in app.py
───────────────
1. Add import:
       from linkages_panel import linkages_ui, linkages_server

2. Replace the existing "Linkages" nav_panel in the UI with:
       linkages_ui(),

3. Add to server():
       linkages_server(input, output, session)

4. Remove from app.py's shared imports:
       linkages_averages

5. Remove from app.py's server():
       linkages_timeseries(), filtered_linkages_averages(),
       linkages_averages_bar(), download_linkages_averages_data()

6. Once this module is in place, you can also remove assign_ordered_colors()
   from app.py — it is now fully self-contained here and in
   business_environment_panel.py.
"""

import io
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from shiny import ui, render, reactive, Inputs, Outputs, Session
from shinywidgets import output_widget, render_widget

try:
    from shared import linkages_averages as _linkages_averages
except ImportError:
    _linkages_averages = None


def _build_country_year_list():
    """
    Build a flat ordered list for ui.input_selectize with region names
    as unclickable separator headers, grouped by region then country_year.
    Matches the bilateral_trends pattern.
    """
    if _linkages_averages is None:
        return []

    if "region" not in _linkages_averages.columns:
        return [""] + sorted(_linkages_averages["country_year"].dropna().unique().tolist())

    ordered = [""]
    for region_name, grp in _linkages_averages.groupby("region", sort=True):
        ordered.append(f"\u2500\u2500 {region_name} \u2500\u2500")
        for cy in sorted(grp["country_year"].dropna().unique().tolist()):
            ordered.append(f"\u00a0\u00a0\u00a0\u00a0{cy}")

    return ordered


def _build_comparator_list():
    """
    Same as _build_country_year_list but without the leading empty string,
    used for the comparator multi-select.
    """
    if _linkages_averages is None:
        return []

    if "region" not in _linkages_averages.columns:
        return sorted(_linkages_averages["country_year"].dropna().unique().tolist())

    ordered = []
    for region_name, grp in _linkages_averages.groupby("region", sort=True):
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
    "ownership":    "% of Foreign-Owned Firms (ownership)",
    "foreign_tech": "% of Firms Using Foreign-Licensed Technology (foreign_tech)",
    "qa_cert":      "% of Firms with an Internationally-Recognized Quality Certification (qa_cert)",
    "exporter":     "% of Exporting Firms (exporter)",
    "gvc_manuf":    "% of GVC Firms, only manufacturing (gvc_manuf)",
}

DESCRIPTION_MAP = {
    "ownership":    "Share of firms with at least 10% foreign ownership.",
    "foreign_tech": "Share of firms that use technology licensed from a foreign company.",
    "qa_cert":      "Share of firms with an internationally-recognized quality certification.",
    "exporter":     "Share of firms that export directly or indirectly at least 10% of sales.",
    "gvc_manuf":    "Share of manufacturing firms integrated into global value chains.",
}

N_MAP = {
    "ownership":    "N_owner",
    "foreign_tech": "N_tech",
    "qa_cert":      "N_qacert",
    "exporter":     "N_export",
    "gvc_manuf":    "N_gvc",
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
                Foreign <span style="color:{BLUE};">Linkages</span>
            </h2>

            <p style="
                font-size:14px; color:{TEXT}; line-height:1.65;
                text-align:justify; margin-bottom:18px;
            ">
                Foreign linkages capture how deeply firms in an economy are integrated
                into international business networks — through <b>foreign ownership</b>,
                <b>technology transfer</b>, <b>quality certification</b>, <b>export activity</b>,
                and participation in <b>global value chains (GVCs)</b>. These indicators,
                drawn from the
                <a href="https://www.enterprisesurveys.org/en/enterprisesurveys"
                target="_blank" style="color:{BLUE}; text-decoration:none; font-weight:500;">
                World Bank Enterprise Survey (WBES)</a>,
                provide a firm-level lens on the depth of FDI integration beyond capital flows.
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
                    Select an <b>economy and survey year</b>, a <b>foreign linkages indicator</b>,
                    and up to <b>4 comparator economies</b> from the sidebar. The left chart
                    shows how the indicator has evolved across available survey rounds; the right
                    chart benchmarks the selected economy against comparators.
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
            "country_year_select",
            "Select Economy and Year:",
            choices=_choices,
            selected="",
            multiple=False,
            options={"placeholder": "Choose an economy-year", "allowEmptyOption": True}
        ),

        _disable_separators_js("country_year_select"),

        ui.hr(style=f"border-color:{BORDER}; margin:14px 0;"),

        ui.HTML(f"""
            <p style="font-size:12px; font-weight:700; color:{NAVY};
                      text-transform:uppercase; letter-spacing:0.8px; margin-bottom:6px;">
                🔗 Indicator of Interest
            </p>
        """),
        ui.input_select(
            "indep_select",
            None,
            choices={
                "ownership":    "Foreign-Owned Firm (ownership)",
                "foreign_tech": "Use of Foreign-Licensed Technology (foreign_tech)",
                "qa_cert":      "Internationally-Recognized Quality Certification (qa_cert)",
                "exporter":     "Exporting Firm (exporter)",
                "gvc_manuf":    "GVC Firm, only manufacturing (gvc_manuf)",
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
            "comparator_countries_linkages",
            "Select up to 4 comparators (economy-year):",
            choices=_comparator_choices,
            multiple=True,
            selected=[],
            options={"maxItems": 4, "placeholder": "Select comparators"},
        ),

        _disable_separators_js("comparator_countries_linkages"),

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
                    <b>ownership</b> — Share of firms with ≥10% foreign ownership<br>
                    <b>foreign_tech</b> — Share of firms using foreign-licensed technology<br>
                    <b>qa_cert</b> — Share of firms with an internationally-recognized quality certification<br>
                    <b>exporter</b> — Share of firms exporting ≥10% of sales<br>
                    <b>gvc_manuf</b> — Share of manufacturing firms integrated into global value chains<br>
                </p>
            </div>
        """),

        width=350,
    )


# ═════════════════════════════════════════════
#  linkages_ui()
# ═════════════════════════════════════════════
def linkages_ui():
    return ui.nav_panel(
        "Linkages",

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
                            ui.HTML(f"<h6 style='text-align:left; color:{NAVY};'><b>Foreign Linkages Indicators Over Time</b></h6>")
                        ),
                        ui.HTML(f"<p style='font-size:13px; color:{MUTED};'>Trend of selected indicator over available WBES survey years.</p>"),
                        output_widget("linkages_timeseries"),
                        ui.HTML("""
                            <p style='font-size:12px; color:gray; text-align:justify; margin-top:8px;'>
                                <b>Technical note:</b> Indicators show weighted averages of firm responses
                                per economy-year, computed using survey weights. Comparisons are limited
                                to economies with available WBES data.
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
                            ui.HTML(f"<h6 style='text-align:left; color:{NAVY};'><b>Foreign Linkages Benchmarking</b></h6>")
                        ),
                        ui.HTML(f"<p style='font-size:13px; color:{MUTED};'>Weighted averages of selected indicator across comparator economies.</p>"),
                        output_widget("linkages_averages_bar"),
                        ui.HTML("""
                            <p style='font-size:12px; color:gray; text-align:justify; margin-top:8px;'>
                                <b>Technical note:</b> Indicators show weighted averages of firm responses
                                per economy-year, computed using survey weights. Comparisons are limited
                                to economies with available WBES data.
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
            ),

            ui.div(
                ui.download_button(
                    "download_linkages_averages_data",
                    "⬇ Download Foreign Linkages Data (.csv)"
                ),
                style="text-align:center; margin-top:25px;"
            )
        )
    )


# ═════════════════════════════════════════════
#  linkages_server()
# ═════════════════════════════════════════════
def linkages_server(input: Inputs, output: Outputs, session: Session):

    # Ensure consistent data types at runtime
    if _linkages_averages is not None:
        _linkages_averages["year"]         = _linkages_averages["year"].astype(int)
        _linkages_averages["country_name"] = _linkages_averages["country_name"].astype(str)

    # ── Time series chart ──────────────────────────────────────────────
    @output
    @render_widget
    def linkages_timeseries():
        variable = input.indep_select()
        selected = input.country_year_select().strip("\u00a0").strip()

        if not variable or not selected or _is_separator(selected):
            return _empty_fig()

        country = selected.split("(")[0].strip()
        df = _linkages_averages[_linkages_averages["country_name"] == country].copy()

        if df.empty:
            return _empty_fig()

        df    = df.sort_values("year")
        n_col = N_MAP.get(variable)

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
    def filtered_linkages_averages():
        selected_country_year = input.country_year_select().strip("\u00a0").strip()
        comparators = [
            c.strip("\u00a0").strip()
            for c in (input.comparator_countries_linkages() or [])
            if not _is_separator(c)
        ]
        variable = input.indep_select()

        if not selected_country_year or _is_separator(selected_country_year) or not variable:
            return pd.DataFrame()

        n_col = N_MAP.get(variable)
        df    = _linkages_averages[
            _linkages_averages["country_year"].isin([selected_country_year] + comparators)
        ].copy()

        if df.empty:
            return df

        df = df[[
            "country_name", "year", "country_year", variable, "N_obs", n_col
        ]].rename(columns={variable: "value", n_col: "N_valid"})

        return df.replace({np.nan: None})

    # ── Benchmarking chart ─────────────────────────────────────────────
    @output
    @render_widget
    def linkages_averages_bar():
        df = filtered_linkages_averages()
        if df.empty:
            return _empty_fig()

        variable           = input.indep_select()
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

        selected_country = input.country_year_select().strip("\u00a0").strip().split("(")[0].strip()
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
                showline=True, linecolor="black"
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
    @render.download(filename="linkages_averages_data.csv")
    def download_linkages_averages_data():
        buf = io.StringIO()
        _linkages_averages.copy().to_csv(buf, index=False)
        buf.seek(0)
        yield buf.getvalue().encode("utf-8")