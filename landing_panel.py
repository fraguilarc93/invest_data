"""
landing_panel.py
────────────────
Drop-in landing page for Invest.Data.

USAGE in app.py
───────────────
1. Add at the top of app.py:
       from landing_panel import landing_ui, landing_server

2. Add as the FIRST nav_panel inside ui.navset_tab(...):
       ui.navset_tab(
           landing_ui(),
           ui.nav_panel("What's New?", ...),
           ...
       )

3. Inside def server(input, output, session):
       landing_server(input, output, session)
       # ... rest of your existing server code
"""

from shiny import render, ui
from shinywidgets import output_widget, render_widget
import plotly.graph_objects as go

# ─────────────────────────────────────────────
#  Colour tokens — match app.py exactly
# ─────────────────────────────────────────────
BLUE     = "#3f9dd4"
NAVY     = "#0a2d45"
TEXT     = "#222222"
MUTED    = "#555555"
BORDER   = "#d4e4ef"
BG_LIGHT = "#f5f9fc"
BG_BLUE  = "#e8f4fb"


# ─────────────────────────────────────────────
#  WHAT'S NEW — edit titles, descriptions, hrefs
# ─────────────────────────────────────────────
WHATS_NEW_ITEMS = [
    {
        "tag":   "PWC",
        "title": "Annual Outlook 2026: Teetering Resilience",
        "desc":  "Growth is holding up but foundations are narrower, more concentrated, and increasingly exposed to risk.",
        "href":  "https://www.pwc.com/us/en/about-us/newsroom/press-releases/annual-outlook-2026.html", 
    },
    {
        "tag":   "UNCTAD",
        "title": "Global Investment Trends Monitor, No. 50",
        "desc":  "Based on preliminary estimates, global foreign direct investment (FDI) rose 14% in 2025 to $1.6 trillion. But a big share of the increase came from flows through global financial centres. Real investment activity remained fragile.",
        "href":  "https://unctad.org/publication/global-investment-trends-monitor-no-50", 
    },
    {
        "tag":   "McKinsey & Company",
        "title": "The great trade realignment: Asia rising",
        "desc":  "Trade flows worldwide are reconfiguring as geopolitical alignments fragment and future-shaping industries grow in importance, potentially leading to a generational shift in global trade patterns.",
        "href":  "https://www.mckinsey.com/featured-insights/future-of-asia/the-great-trade-realignment-asia-rising#/", 
    },
]


# ═════════════════════════════════════════════
#  UI HELPERS
# ═════════════════════════════════════════════

def _section_header(title: str, tag: str):
    return ui.div(
        ui.HTML(f"""
            <div style="display:flex; align-items:baseline; gap:12px; margin-bottom:20px;">
                <h4 style="font-size:20px; font-weight:600; color:{NAVY}; margin:0;">
                    {title}
                </h4>
                <span style="
                    font-size:11px; font-weight:600; letter-spacing:1.3px;
                    text-transform:uppercase; color:{BLUE};
                    background:{BG_BLUE}; padding:3px 9px;
                    border-radius:20px; border:1px solid {BORDER};
                ">{tag}</span>
            </div>
        """)
    )


# ─────────────────────────────────────────────
#  SECTION 1 — Hero / About
# ─────────────────────────────────────────────
def _hero_card():
    return ui.card(
        ui.HTML(f"""
            <h2 style="
                font-size:28px; font-weight:700; color:{NAVY};
                margin-bottom:6px; line-height:1.2;
            ">
                What is <span style="color:{BLUE};">Invest.Data</span>?
            </h2>

            <p style="
                font-size:14px; color:{TEXT}; line-height:1.65;
                text-align:justify; margin-bottom:18px;
            ">
                <b>Invest.Data</b> is the World Bank Group's centralized interactive tool that
                enables staff to <b>access, visualize, and analyze</b> consolidated data on global
                investments and related policy indicators. Developed to support Task Team Leaders
                and WBG staff, Invest.Data provides quick, evidence-based insights to strengthen
                client engagement, enhance analytical work, and guide investment-related policy
                discussions.
            </p>

            <div style="
                background:{BG_BLUE}; border:1px solid {BORDER};
                border-left:4px solid {BLUE}; border-radius:8px;
                padding:14px 18px; margin-bottom:18px;
            ">
                <p style="
                    font-size:11px; font-weight:700; letter-spacing:1.5px;
                    text-transform:uppercase; color:{BLUE}; margin-bottom:6px;
                ">🎯 Objective</p>
                <p style="font-size:14px; color:{TEXT}; margin:0; line-height:1.6;">
                    To empower WBG staff with a one-stop data platform for
                    <b>early diagnostics, benchmarking, and dialogue</b> on private investment
                    trends and policies.
                </p>
            </div>

            <div style="display:flex; gap:24px; flex-wrap:wrap; font-size:12px; color:{MUTED};">
                <span>📅 <b>Version 1.3</b> · last updated March 11, 2026</span>
                <span>🔒 For <b>WBG internal use only</b></span>
                <span>👥 Developed for <b>Task Team Leaders &amp; WBG staff</b></span>
            </div>
        """),
        style=f"background:{BG_LIGHT}; border:1px solid {BORDER}; padding:28px 32px;"
    )


# ─────────────────────────────────────────────
#  SECTION 2 — Investment Highlights (summary)
# ─────────────────────────────────────────────
def _highlights_section():
    return ui.div(
        _section_header("Investment Highlights", "2026 H1 Edition"),

        ui.card(
            ui.layout_columns(

                # ── Intro text ───────────────────────────────────────
                ui.div(
                    ui.HTML("""
                        <h2 style="font-size:22px; font-weight:600; color:#3f9dd4;
                                   margin-bottom:12px; line-height:1.25;">
                            Where global investment is headed: what the data say about digital innovation and the energy transition
                        </h2>
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
                        <a href="#"
                           onclick="
                               const tabs = document.querySelectorAll('[data-bs-toggle=tab]');
                               tabs.forEach(t => {
                                   if (t.textContent.trim() === 'Investment Highlights') t.click();
                               });
                               return false;"
                           style="
                               display:inline-block;
                               margin-top:12px;
                               padding:7px 18px;
                               background:#3f9dd4;
                               color:white;
                               border-radius:4px;
                               font-size:13px;
                               font-weight:600;
                               text-decoration:none;">
                            Read more →
                        </a>
                        <a href="#"
                           onclick="
                               const tabs = document.querySelectorAll('[data-bs-toggle=tab]');
                               tabs.forEach(t => {{
                                   if (t.textContent.trim() === 'Investment Highlights') t.click();
                               }});
                               return false;"
                           style="
                               display:inline-block;
                               margin-top:12px;
                               padding:7px 18px;
                               background:{BLUE};
                               color:white;
                               border-radius:4px;
                               font-size:13px;
                               font-weight:600;
                               text-decoration:none;">
                            Read full brief →
                        </a>
                    """),
                ),

                # ── Stat highlights ──────────────────────────────────
                ui.div(
                    ui.HTML(f"""
                        <div style="display:flex; flex-direction:column; gap:16px; padding-left:24px;
                                    border-left:3px solid {BORDER};">

                            <div>
                                <div style="font-size:28px; font-weight:700; color:{BLUE};">
                                    US$600B
                                </div>
                                <div style="font-size:12px; color:{MUTED}; line-height:1.4;">
                                    Peak announced greenfield FDI in climate &amp;<br>energy transition (2023)
                                </div>
                            </div>

                            <div>
                                <div style="font-size:28px; font-weight:700; color:{BLUE};">
                                    38%
                                </div>
                                <div style="font-size:12px; color:{MUTED}; line-height:1.4;">
                                    Global share of digital announced greenfield <br>FDI in 2025
                                </div>
                            </div>

                            <div>
                                <div style="font-size:28px; font-weight:700; color:{BLUE};">
                                    42%
                                </div>
                                <div style="font-size:12px; color:{MUTED}; line-height:1.4;">
                                    Global share of climate &amp;<br>energy transition announced FDI in 2023
                                </div>
                            </div>

                        </div>
                    """),
                ),

                col_widths=[8, 4],
            ),
            style=f"padding:8px;",
        ),
        style="margin-bottom:24px;",
    )

# ─────────────────────────────────────────────
#  SECTION 3 — FDI Choropleth Map (Plotly)
# ─────────────────────────────────────────────
def _map_ui():
    return ui.div(
        _section_header("Global FDI Concentration", "Latest Available Year"),
        ui.layout_columns(

            # ── Left: choropleth map ──────────────────────────────────
            ui.card(
                ui.card_header(
                    ui.HTML(f"""
                        <b>Inward FDI Concentration Map</b>
                        <span style="font-size:12px; color:{MUTED}; margin-left:10px;">
                            Hover for details
                        </span>
                    """)
                ),
                output_widget("landing_fdi_map"),
                ui.HTML(f"""
                    <p style='font-size:11px; color:{MUTED}; margin-top:4px; text-align:justify;'>
                        <b>Source:</b> <i>UNCTAD. Most recent year with available data.
                        Grey indicates no data available.</i>
                    </p>
                """),
                full_screen=True,
            ),

            # ── Right: Top 15 table ───────────────────────────────────
            ui.card(
                ui.card_header(
                    ui.HTML(f"<b>Top 15 FDI Recipients</b>")
                ),
                ui.output_ui("landing_top_table"),
                ui.HTML(f"""
                    <p style='font-size:11px; color:{MUTED}; margin-top:4px; text-align:justify;'>
                        <b>Source:</b> <i>UNCTAD. Net inflows in current US$ billions.</i>
                    </p>
                """),
            ),

            col_widths=[7, 5],
        ),
        ui.tags.script("""
            document.addEventListener('DOMContentLoaded', function() {
                setTimeout(function() { window.dispatchEvent(new Event('resize')); }, 300);
            });
        """),
    )


# ─────────────────────────────────────────────
#  SECTION 4 — What's New
# ─────────────────────────────────────────────
def _news_card(item: dict):
    return ui.card(
        ui.HTML(f"""
            <span style="
                font-size:10px; font-weight:700; letter-spacing:1.5px;
                text-transform:uppercase; color:{BLUE};
                background:{BG_BLUE}; padding:3px 8px;
                border-radius:4px; border:1px solid {BORDER};
            ">{item['tag']}</span>

            <h5 style="
                font-size:15px; font-weight:600; color:{NAVY};
                margin:10px 0 6px; line-height:1.35;
            ">{item['title']}</h5>

            <p style="font-size:13px; color:{MUTED}; line-height:1.55; margin-bottom:12px;">
                {item['desc']}
            </p>

            <a href="{item['href']}" target="_blank" rel="noopener noreferrer"
               style="font-size:12px; font-weight:600; color:{BLUE}; text-decoration:none;">
                Open link →
            </a>
        """),
        style=f"border:1px solid {BORDER}; padding:20px;",
    )


def _whats_new_section():
    return ui.div(
        _section_header("What's New", "Latest Updates"),
        ui.layout_columns(
            *[_news_card(item) for item in WHATS_NEW_ITEMS],
            col_widths=[4, 4, 4],
        ),
    )


# ═════════════════════════════════════════════
#  FULL landing_ui()
# ═════════════════════════════════════════════
def landing_ui():
    """Returns a ui.nav_panel('Home', ...) ready for ui.navset_tab()."""
    return ui.nav_panel(
        "Home",
        ui.div(
            ui.div(style="margin-top:24px;"),
            _hero_card(),

            ui.div(style="margin-top:36px;"),
            ui.hr(style=f"border-color:{BORDER}; margin-bottom:32px;"),
            _highlights_section(),

            ui.div(style="margin-top:36px;"),
            ui.hr(style=f"border-color:{BORDER}; margin-bottom:32px;"),
            _map_ui(),

            ui.div(style="margin-top:36px;"),
            ui.hr(style=f"border-color:{BORDER}; margin-bottom:32px;"),
            _whats_new_section(),

            ui.div(style="margin-bottom:40px;"),
            style="padding:0 10px;",
        ),
    )


# ═════════════════════════════════════════════
#  landing_server()
# ═════════════════════════════════════════════
def landing_server(input, output, session):
    """
    Registers landing_fdi_map using fdi_trends data + Plotly choropleth.

    fdi_trends is expected to have at minimum:
        - 'year'             : int
        - 'ecode_alpha3'     : ISO-3 country code  (used as Plotly 'locations')
        - 'fdi_inward_flow'  : numeric FDI value
        - 'economy'          : country/economy name for the tooltip
        - 'region_short'     : regional grouping (rows with nulls are aggregates, excluded)
        - 'incomegroup_short': income grouping    (rows with nulls are aggregates, excluded)
    """

    # ── Column name config ──────────────────────────────────────────────
    FDI_VALUE_COL    = "fdi_inward_flow_pct"  # percentile rank (0–100) of FDI concentration
    COUNTRY_NAME_COL = "economy"
    ISO_COL          = "ecode_alpha3"
    YEAR_COL         = "year"
    RAW_FDI_COL      = "fdi_inward_flow"      # raw value used in tooltip and top table
    # ────────────────────────────────────────────────────────────────────

    try:
        from shared import fdi_trends as _fdi_trends
    except ImportError:
        _fdi_trends = None

    @output
    @render_widget
    def landing_fdi_map():

        if _fdi_trends is None:
            return go.Figure()

        # Most recent year — exclude aggregate economies (missing region/income)
        latest_year = int(_fdi_trends[YEAR_COL].max())
        df = _fdi_trends.loc[_fdi_trends[YEAR_COL] == latest_year].copy()
        df = df.dropna(subset=["region_short", "incomegroup_short"])
        df = df.dropna(subset=[FDI_VALUE_COL, ISO_COL])
        df = df[df[ISO_COL].str.strip() != ""]

        iso_codes     = df[ISO_COL].tolist()
        fdi_values    = df[FDI_VALUE_COL].tolist()
        country_names = df[COUNTRY_NAME_COL].tolist() if COUNTRY_NAME_COL in df.columns else iso_codes
        net_inflows   = df[RAW_FDI_COL].tolist() if RAW_FDI_COL in df.columns else [None]*len(iso_codes)

        colorscale = [
            [0.00, "#eaf4fb"],
            [0.20, "#c3e0f2"],
            [0.40, "#7dbfdf"],
            [0.60, "#3f9dd4"],
            [0.80, "#1a6fa0"],
            [1.00, "#0a2d45"],
        ]

        customdata = list(zip(country_names, net_inflows))

        fig = go.Figure(go.Choropleth(
            locations         = iso_codes,
            z                 = fdi_values,
            customdata        = customdata,
            zmin              = 0,
            zmax              = 100,
            colorscale        = colorscale,
            marker_line_color = "#a0bfcf",
            marker_line_width = 0.4,
            colorbar=dict(
                orientation = "h",
                x           = 0.5,
                xanchor     = "center",
                y           = -0.05,
                yanchor     = "top",
                thickness   = 12,
                len         = 0.5,
                title=dict(
                    text = "FDI concentration percentile",
                    side = "bottom",
                    font = dict(size=11, color=MUTED),
                ),
                tickvals  = [0, 25, 50, 75, 100],
                ticktext  = ["0", "25th", "50th", "75th", "100th"],
                tickfont  = dict(size=10, color=MUTED),
            ),
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "FDI concentration percentile: <b>%{z:.1f}</b><br>"
                "FDI inward flow: <b>%{customdata[1]:,.1f} US$ bn</b><br>"
                f"Year: {latest_year}"
                "<extra></extra>"
            ),
        ))

        fig.update_layout(
            geo=dict(
                showframe       = False,
                showcoastlines  = True,
                coastlinecolor  = "#a0bfcf",
                showland        = True,
                landcolor       = "#f0f4f8",
                showocean       = True,
                oceancolor      = "#d6eaf8",
                showlakes       = False,
                projection_type = "equirectangular",
                bgcolor         = "white",
            ),
            margin        = dict(l=0, r=0, t=30, b=50),
            paper_bgcolor = "white",
            plot_bgcolor  = "white",
            title=dict(
                text = f"<b>Inward FDI Net Inflows — {latest_year}</b>",
                x    = 0.5,
                font = dict(size=16, color=NAVY),
            ),
            height   = 450,
            autosize = True,
        )

        return fig

    @output
    @render.ui
    def landing_top_table():

        if _fdi_trends is None:
            return ui.HTML("<p style='color:#888;'>Data unavailable.</p>")

        latest_year = int(_fdi_trends[YEAR_COL].max())
        df = _fdi_trends.loc[_fdi_trends[YEAR_COL] == latest_year].copy()
        df = df.dropna(subset=["region_short", "incomegroup_short"])
        df = df.dropna(subset=[RAW_FDI_COL, COUNTRY_NAME_COL])
        df = df.sort_values(RAW_FDI_COL, ascending=False).head(15).reset_index(drop=True)

        rows = ""
        for i, row in df.iterrows():
            rank   = i + 1
            name   = row[COUNTRY_NAME_COL]
            inflow = row[RAW_FDI_COL]
            bg = f"background:{BG_LIGHT};" if rank % 2 == 0 else ""
            rows += (
                f"<tr style='{bg}'>"
                f"<td style='padding:5px 8px; color:{MUTED}; font-size:12px;'>{rank}</td>"
                f"<td style='padding:5px 8px; font-size:13px;'>{name}</td>"
                f"<td style='padding:5px 8px; text-align:right; font-size:13px; font-weight:600;'>{inflow:,.1f}</td>"
                f"</tr>"
            )

        table_html = f"""
            <table style="width:100%; border-collapse:collapse; font-family:sans-serif;">
                <thead>
                    <tr style="border-bottom:2px solid {BORDER};">
                        <th style="padding:6px 8px; text-align:left; font-size:11px;
                                   color:{MUTED}; font-weight:600;">#</th>
                        <th style="padding:6px 8px; text-align:left; font-size:11px;
                                   color:{MUTED}; font-weight:600;">Economy</th>
                        <th style="padding:6px 8px; text-align:right; font-size:11px;
                                   color:{MUTED}; font-weight:600;">US$ bn</th>
                    </tr>
                </thead>
                <tbody>{rows}</tbody>
            </table>
        """

        return ui.HTML(table_html)