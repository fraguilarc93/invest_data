import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import output_widget, render_widget
from ipywidgets import Layout, FloatSlider, ToggleButtons, VBox, HTML
from ipyleaflet import Map, basemaps, Choropleth, GeoJSON, Popup, WidgetControl
from branca.colormap import linear
import json

from shared import fdi_panel, fdi_trends, bilateral_inflow, bilateral_outflow, bilateral_instock, bilateral_outstock, bilateral_economies, fdi_components

# Define the UI layout
app_ui = ui.page_fluid(
    ui.panel_title("IMAT Dashboard", "IMAT Dashboard"),
    ui.markdown("Investment and Multinational Activity Trends"),

    # Add a style block to hide the Greenfield tab by its data-value
    ui.tags.style("""
        /* Hide the 'Greenfield FDI' tab from the top nav */
        #main_tabs .nav-link[data-value="greenfield"] { display: none !important; }
    """),

    # Top tabs instead of sidebar buttons
    ui.navset_tab(

        # HOME
        ui.nav_panel(
            "Home",
            ui.div(
                output_widget("map"),

                ui.div(
                    ui.input_slider(
                        "year_slider",
                        "Select Year",
                        min=2000,
                        max=2023,
                        value=2023,
                        step=1,
                        sep=""
                    ),
                    id="year_overlay",
                ),
                id="home_map_wrap",
            ),

            # Card below the map with margin
            ui.div(
                ui.card(
                    ui.card_header(
                        ui.HTML("<h6 style='text-align:left;'><b>About this Map</b></h6>") 
                    ),
                    ui.HTML("""
                    <p style='font-size:14px; color:black; text-align:left;'>
                    This map provides an overview of investment and multinational enterprise activities
                    across economies from 2000 to 2023. Countries are shaded by percentile ranks of annual
                    net inflows, allowing for easier comparison across economies. Use the slider to select
                    a year and explore country-level investment patterns.
                    </p>
                    <p style='font-size:14px; color:black; text-align:left; margin-top:10px;'>
                    Data sources: United Nations Conference on Trade and Development (UNCTAD),
                    International Monetary Fund (IMF), World Bank <i>Business Ready</i> report,
                    and the Multinational Revenue, Employment, and Investment Database (MREID)
                    of the U.S. International Trade Commission.
                    </p>
                    """),
                ),
                style="margin-top:20px;",
            )
        ),

        # FDI TRENDS
        ui.nav_panel(
            "FDI Trends",

            ui.layout_sidebar(
                ui.sidebar(

                    # Multi-select with selectize (max 5 economies)
                    ui.input_selectize(
                        "economy_trends",
                        "Select Economies (up to 5):",
                        choices=sorted(fdi_trends["economy"].dropna().unique().tolist()),
                        multiple=True,
                        options={"maxItems": 5}
                    ),

                    # Imward vs Outward
                    ui.input_radio_buttons(
                        "fdi_direction",
                        "Select Direction:",
                        choices=["Inward", "Outward"],
                        selected="Inward"
                    ),

                    # Flow vs Stock
                    ui.input_radio_buttons(
                        "fdi_type",
                        "Select Type:",
                        choices=["Flow", "Stock"],
                        selected="Flow"
                    ),

                    # Radio buttons for indicator (only one option allowed)
                    ui.input_radio_buttons(
                        "fdi_indicator",
                        "Select Indicator:",
                        choices=[
                            "US$ billions (current prices)",
                            "% change from 2000 baseline (US$ billions)",
                            "Share of Global Total",
                            "Share of Gross Domestic Product (GDP)",
                            "Share of Gross Fixed Capital Formation (GFCF)"
                        ],
                        selected="US$ billions (current prices)"
                    ),
                
                ),

                # Main area: description card + graph below
                ui.div(
                    ui.card(
                        ui.card_header(
                            ui.HTML("<h6 style='text-align:left;'><b>Foreign Direct Investment (FDI) trends</b></h6>")
                        ),
                        ui.HTML("<p style='font-size:14px; color:black;'>Select filters from the sidebar to generate the FDI Trends graph.</p>"),
                        output_widget("fdi_trends_graph"),
                        ui.HTML("<p style='font-size:11px; color:gray; text-align:center;'>Source: United Nations Conference on Trade and Development (UNCTAD)</p>"),
                        full_screen=False,
                        fill=True,
                    ),
                )
            )
        ),
        
        # Bilateral FDI Trends 
        ui.nav_panel(
            "Bilateral Trends",

            ui.layout_sidebar(
                ui.sidebar(

                    # Single economy select
                    ui.input_selectize(
                        "economy_bilateral",
                        "Select Economy:",
                        choices=bilateral_economies,
                        multiple=False
                    ),

                    # Flow vs Stock
                    ui.input_radio_buttons(
                        "bilateral_type",
                        "Select Type:",
                        choices=["Flow", "Stock"],
                        selected="Flow"
                    ),

                    # Year Slider
                    ui.input_slider(
                        "bilateral_year",
                        "Select Year:",
                        min=2000,
                        max=2023,
                        value=2022,
                        step=1,
                        sep=""
                    ),
                ),

                # Main areas: two graph cards (Inward + Outward)
                ui.layout_columns(
                    ui.card(
                        ui.card_header(
                            ui.HTML("<h6 style='text-align:left;'><b>Inward FDI</b></h6>")
                        ),
                        ui.HTML("<p style='font-size:14px; color:black;'>Top 5 economies investing in the selected economy.</p>"),
                        output_widget("bilateral_inward_graph"),
                        ui.HTML("<p style='font-size:11px; color:gray; text-align:center;'>Source: United Nations Conference on Trade and Development (UNCTAD)</p>"),
                        full_screen=True,
                        fill=True,
                        style="min-height:500px;" 
                    ),
                    ui.card(
                        ui.card_header(
                            ui.HTML("<h6 style='text-align:left;'><b>Outward FDI</b></h6>")
                        ),
                        ui.HTML("<p style='font-size:14px; color:black;'>Top 5 economies where the selected economy invests.</p>"),
                        output_widget("bilateral_outward_graph"),
                        ui.HTML("<p style='font-size:11px; color:gray; text-align:center;'>Source: United Nations Conference on Trade and Development (UNCTAD)</p>"),
                        full_screen=True,
                        fill=True,
                        style="min-height:500px;" 
                    ),
                    col_widths=(6,6)
                )
            )
        ),

        # FDI Components
        ui.nav_panel(
            "FDI Components",

            ui.layout_sidebar(
                ui.sidebar(

                    # Single economy select
                    ui.input_selectize(
                        "economy_component",
                        "Select Economy:",
                        choices=bilateral_economies,
                        multiple=False
                    ),

                    # Select components
                    ui.input_checkbox_group(
                        "component",
                        "Select Inward FDI Component",
                        choices={
                            "share_debt_instruments": "Share of Debt Instruments",
                            "share_equity": "Equity",
                            "share_reinv_earnings": "Reinvested Earnings"
                        },
                        selected=[
                            "share_debt_instruments",
                            "share_equity",
                            "share_reinv_earnings"
                        ]
                    ),

                ),

                ui.div(
                    ui.card(
                        ui.card_header(
                            ui.HTML("<h6 style='text-align:left;'><b>Net FDI Inflows by Component</b></h6>")
                        ),
                        ui.HTML("<p style='font-size:14px; color:black;'>Use the sidebar filters to generate the Net FDI Inflows by Component trends graph.</p>"),
                        output_widget("fdi_component"),
                        ui.HTML(
                            "<p style='font-size:11px; color:gray; text-align:center;'>"
                            "Source: International Monetary Fund (IMF), Balance of Payments"
                            "</p>"
                        ),
                        ui.HTML(
                            "<p style='font-size:11px; color:gray; text-align:center;'>"
                            "Note: In some economies and years, the shares of FDI components "
                            "(Equity, Debt Instruments, Reinvested Earnings) may exceed 100% or appear negative. "
                            "This occurs because FDI inflows are measured on a net basis, which accounts for both new investments "
                            "and disinvestments/withdrawals. As a result, large disinvestments in one component (e.g., equity) "
                            "can make its share negative, while the other components may exceed 100% of net inflows."
                            "</p>"
                        ),
                    ),
                )
            )

        ),

        # MNE Activity
        ui.nav_panel(
            "MNE Activity",
            ui.HTML("""<div style="text-align:center; margin-top:20px;">
                        <h2><b>MNE Activity Trends</b></h2>
                        <p style="font-size:16px;">Placeholder for MNE Activity Trends graphs and controls.</p>
                    </div>""")
        ),

        # Policies
        ui.nav_panel(
            "Investment Policy",
            ui.HTML("""<div style="text-align:center; margin-top:20px;">
                        <h2><b>Investment Policy</b></h2>
                        <p style="font-size:16px;">Placeholder for Investment Policy graphs and controls.</p>
                    </div>""")
        ),

        # Incentives
        ui.nav_panel(
            "Incentives",
            ui.HTML("""<div style="text-align:center; margin-top:20px;">
                        <h2><b>CIT Incentives</b></h2>
                        <p style="font-size:16px;">Placeholder for CIT Incentives graphs and controls.</p>
                    </div>""")
        ),

        # FDI Spillover Toolkit
        ui.nav_panel(
            "Spillovers",
            ui.HTML("""<div style="text-align:center; margin-top:20px;">
                        <h2><b>Spillovers</b></h2>
                        <p style="font-size:16px;">Placeholder for FDI Spillovers graphs and controls.</p>
                    </div>""")
        ),

        # WB Investment Climate Hub
        ui.nav_panel(
            "WB Investment Climate Hub",
            ui.HTML("<p>Redirecting…</p>"),  # never really shown
            value="wb_hub",
        ),

        # About
        ui.nav_panel(
            "About",
            ui.div(
                ui.div(style="margin-top:20px;"),
                ui.card(
                    ui.card_header(
                     ui.HTML("<h6 style='text-align:left;'><b>What is the IMAT Dashboard?</b></h6>")    
                    ),
                    ui.HTML("""
                        <p>
                            The Investment and Multinational Activity Trends (IMAT) Dashboard is a centralized 
                            dashboard for WBG staff to quickly access, visualize, and analyze data on foreign 
                            direct investment (FDI), multinational enterprise (MNE) activities, and investment 
                            policies. The objective is to make it easier for staff to identify barriers to 
                            investment in client countries and form priority areas for deeper analysis 
                            (e.g., at the firm- and/or sector-levels) to promote early engagement with client 
                            countries in facilitating private investment. The IMAT Dashboard is currently for 
                            internal use only.
                        </p>
                    """),
                ),

                ui.card(
                    ui.card_header(
                     ui.HTML("<h6 style='text-align:left;'><b>What Can You Find on the IMAT Dashboard?</b></h6>")    
                    ),
                    ui.HTML("""
                        <p>
                            WBG staff can obtain an overview of countries’ private investment activities and trends, 
                            MNE activities, and FDI spillovers. Staff will be able to benchmark countries against 
                            elected peers, visualize the distribution of FDI flows and stocks by country and/or over 
                            time, disaggregate balance of payments (BOP) accounts into their constituent components 
                            (e.g., equity, reinvested earnings, and intra-company debt), and aggregate multinational 
                            enterprise activities (e.g., output, employment and number of enterprises). 
                            Functions to download customized charts and visuals are available as well.
                        </p>
                    """),
                ),
                
                ui.card(
                    ui.card_header(
                     ui.HTML("<h6 style='text-align:left;'><b>What Can You <i>Not</i> Find on the IMAT Dashboard?</b></h6>")    
                    ),
                    ui.HTML("""
                        <p>
                            The IMAT Dashboard serves as a “first scan” diagnostic tool to assess a country’s 
                            investment climate and initiate dialogue with policymakers on driving evidence-based 
                            policy reform. To access more granular firm-level and sector-specific analyses and bridge 
                            high-level investment trends with actionable reform agendas, please contact the WBG’s 
                            Investment Climate team (ETIIC) at <b>[CONTACT INFO]</b>. The Investment Climate is well equipped 
                            to support client countries in diagnosing bottlenecks to investment and designing policy 
                            reforms to create an investment climate that is conducive to private investment.
                        </p>
                    """),
                ),

                ui.card(
                    ui.card_header(
                        ui.HTML("<h6 style='text-align:left;'><b> What is the current version of the IMAT Dashboard?</b></h6>")
                    ),
                    ui.HTML("""
                        <p>
                            Current release: Dashboard Version 1.0 (last updated September 26, 2025).
                        </p>
                    """),
                ),

                ui.card(
                    ui.card_header(
                     ui.HTML("<h6 style='text-align:left;'><b>Definitions</b></h6>")    
                    ),

                    ui.HTML("""

                            <h6 style="font-weight:bold;">Foreign Direct Investment (FDI)</h6>
                            <p>
                                Foreign direct investment reflects the objective of establishing a <em>lasting interest</em> by a resident 
                                enterprise in one economy (direct investor) in an enterprise (direct investment enterprise) that is 
                                resident in an economy other than that of the direct investor (OECD Benchmark Definition of Foreign 
                                Direct Investment).
                            </p>
                            <p>
                                The lasting interest implies the existence of a long-term relationship between the 
                                direct investor and the direct investment enterprise and a significant degree of influence on the 
                                management of the enterprise. The direct or indirect ownership of 10% or more of the voting power 
                                of an enterprise resident in one economy by an investor resident in another economy is evidence of 
                                such a relationship (Fifth Edition, paragraph 65).
                            </p>

                            <h6 style="font-weight:bold;">Gross Fixed Capital Formation</h6>
                            <p>
                                Acquisitions of fixed assets, net of disposals, during the accounting period. This includes 
                                specified expenditures on services that enhance the value of non-produced assets. 
                                (OECD Benchmark Definition of Foreign Direct Investment, Fifth Edition)
                            </p>

                            <h6 style="font-weight:bold;">Inward FDI Flow</h6>
                            <p>
                                According to the OECD, inward FDI flows represent the value of cross-border direct investment transactions 
                                received by a reporting economy within a given year. This indicator can be further disaggregated by source 
                                economy and may also be expressed on a net basis when accounting for investment withdrawals.
                            </p>

                            <h6 style="font-weight:bold;">Inward FDI Stock</h6>
                            <p>
                                According to the OECD, inward FDI stock represents the total accumulated value of foreign direct investment held in a reporting economy at a given point in time. 
                            </p>

                            <h6 style="font-weight:bold;">Multinational Enterprise (MNE)?</h6>
                            <p>
                                A multinational enterprise is a legal entity that has at least one non-resident affiliate or branch, 
                                and exercises control over its affiliate(s) or branch(es) either directly—by holding over 50% of the 
                                voting power—or indirectly through transmission of control. The MNE is the ultimate controlling parent— 
                                the direct investor at the top of the control chain.
                            </p>

                            <h6 style="font-weight:bold;">Multinational Enteprise (MNE) Activty</h6>
                            <p>
                                An MNE exists when a resident investor in one economy establishes a lasting interest in an enterprise located in another economy, 
                                generally demonstrated by owning at least 10% of the voting power. This implies a long-term relationship and a significant degree 
                                of influence over management of the foreign enterprise.
                            </p>
                            <p>
                                MNE activities include setting up or acquiring subsidiaries, branches, or joint ventures abroad, as well as expanding production, 
                                services, or sales across multiple countries. They also encompass reinvested earnings, intra-company loans, and the coordination 
                                of operations across affiliates. In practice, MNEs internalize transactions such as capital, technology, and knowledge transfers 
                                within their global corporate network, optimizing costs, efficiency, and market access.
                            </p>

                            <h6 style="font-weight:bold;">Outward FDI Flow</h6>
                            <p>
                                XXXX
                            </p>

                            <h6 style="font-weight:bold;">Outward FDI Stock</h6>
                            <p>
                                XXXX
                            </p>

                    """),
                ),
                
                ui.card(
                    ui.card_header(
                    ui.HTML("<h6 style='text-align:left;'><b>Data Sources</b></h6>")    
                    ),

                    ui.HTML(""" 
                            <h6 style="font-weight:bold;">United Nations Conference on Trade and Development (UNCTAD)</h6>
                            <p>
                                The United Nations Conference Trade and Development (UNCTAD) complies and publishes data on Foreign
                                Direct Investment (FDI) for more than 200 economies worldwide. UNCTAD reports both flows (new investment
                                moving in or out during a given period) and stocks (the accumulated value of investment at a point in time).
                                The data are widely used to track global and regional investment trends. 
                            </p>
                            <p>
                                The main value of UNCTAD's FDI data lies in its broad geographical coverage, long time series, and 
                                disaggregation by type and region. It is important to note that figures may vary across economies 
                                due to differences in reporting practices, possible revisions, and the presence of pass-through 
                                economies that channel investment flows. Despite these limitations, UNCTAD's databases and the 
                                <i>World Investment Report</i>, which is informed by this data, remain leading references for 
                                policymakers, researchers, and analysts studying international investment.
                            </p>
                    """),
                ),
            ),
        ),
    id="main_tabs"
    ),

    # Add JavaScript redirect script
    ui.tags.script("""
    document.addEventListener('click', function (e) {
      const link = e.target.closest('#main_tabs .nav-link[data-value="wb_hub"]');
      if (link) {
        e.preventDefault();
        window.open('https://worldbankgroup.sharepoint.com/sites/ICHUB', '_blank');
      }
    }, true);
    """),

    ui.tags.style("""
    /* Wrapper provides positioning context */
    #home_map_wrap { position: relative; width: 100%; }

    /* Put slider ON TOP of the map & controls */
    #year_overlay {
        position: absolute;
        left: 50%;
        bottom: 12px;
        transform: translateX(-50%);
        background: rgba(255,255,255,0.85);
        padding: 6px 10px;
        border-radius: 8px;
        z-index: 2147483647;          /* max it out */
        pointer-events: auto;          /* ensure it captures clicks */
    }

    /* Keep the map under the overlay */
    #home_map_wrap .leaflet-container,
    #home_map_wrap .jupyter-widget {
        position: relative;
        z-index: 0;
    }
    """),

    ui.tags.style("""
    #year_overlay { cursor: grab; }
    #year_overlay.dragging { cursor: grabbing; }
    """),

    ui.tags.script("""
    (function() {
    const WRAP_ID = 'home_map_wrap';
    const PANEL_ID = 'year_overlay';

    function makeDraggable(panel, wrap) {
        let dragging = false, startX = 0, startY = 0, origLeft = 0, origTop = 0;

        const getXY = (e) => ({
        x: e.touches ? e.touches[0].clientX : e.clientX,
        y: e.touches ? e.touches[0].clientY : e.clientY
        });

        const onDown = (e) => {
        dragging = true;
        panel.classList.add('dragging');

        const wrapRect = wrap.getBoundingClientRect();
        const rect = panel.getBoundingClientRect();
        origLeft = rect.left - wrapRect.left;
        origTop  = rect.top  - wrapRect.top;

        const { x, y } = getXY(e);
        startX = x; startY = y;

        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup', onUp);
        document.addEventListener('touchmove', onMove, { passive: false });
        document.addEventListener('touchend', onUp);
        };

        const onMove = (e) => {
        if (!dragging) return;
        if (e.cancelable) e.preventDefault();

        const { x, y } = getXY(e);
        const dx = x - startX, dy = y - startY;

        const wrapRect = wrap.getBoundingClientRect();
        const maxLeft = wrapRect.width  - panel.offsetWidth;
        const maxTop  = wrapRect.height - panel.offsetHeight;

        let left = Math.max(0, Math.min(origLeft + dx, maxLeft));
        let top  = Math.max(0, Math.min(origTop  + dy, maxTop));

        panel.style.left = left + 'px';
        panel.style.top  = top  + 'px';
        panel.style.right = 'auto';
        panel.style.bottom = 'auto';
        panel.style.transform = 'none';
        };

        const onUp = () => {
        dragging = false;
        panel.classList.remove('dragging');
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
        document.removeEventListener('touchmove', onMove);
        document.removeEventListener('touchend', onUp);
        };

        panel.addEventListener('mousedown', onDown);
        panel.addEventListener('touchstart', onDown, { passive: true });
    }

    function init() {
        const wrap = document.getElementById(WRAP_ID);
        const panel = document.getElementById(PANEL_ID);
        if (wrap && panel && !panel.dataset.draggableInit) {
        panel.dataset.draggableInit = '1';
        makeDraggable(panel, wrap);
        }
    }

    if (document.readyState !== 'loading') init();
    else document.addEventListener('DOMContentLoaded', init);
    new MutationObserver(init).observe(document.body, { childList: true, subtree: true });
    })();
    """),

    # Add this just once in your UI (outside or after the slider)
    ui.tags.script("""
    document.addEventListener("DOMContentLoaded", function() {
    const labels = document.querySelectorAll("#year_slider .irs-grid-text");
    labels.forEach(l => l.textContent = l.textContent.replace(",", ""));
    });
    """),
)


# Define server    
def server(input: Inputs, output: Outputs, session: Session): 

    ##################################
    ## 1. Tutorial Modal
    def tutorial_step():
        return ui.modal(
            ui.HTML("""
                <h2>🌐 Welcome to the IMAT Dashboard</h2>
                <p>The IMAT Dashboard 📊 is a product of the Investment Climate Global Unit, 
                providing an interactive view of investment and multinational activity trends
                across economies, regions, and sectors.</p>
                <p>🧭 Use the navigation tabs to explore different topics, 
                and apply filters to tailor the data to your needs.</p>
                <p>ℹ️ For background and methodology, visit the <b>About</b> tab.</p>
                <p style="margin-top:15px;"><i>🚀 Click <b>Access</b> below to begin.</i></p>
            """),
            title="",
            easy_close=True,
            footer=ui.input_action_button("btn_close_tutorial", "Access", class_="btn-primary")
        )

    # Show tutorial when app loads
    @reactive.effect
    def _show_tutorial():
        ui.modal_show(tutorial_step())

    # Close tutorial when button clicked
    @reactive.effect
    @reactive.event(input.btn_close_tutorial)
    def _close_tutorial():
        ui.modal_remove()

    ##################################
    ## 2. Home Map
    @render_widget
    def map():
        year = int(input.year_slider())
        df = fdi_panel.loc[fdi_panel["year"] == year].copy()
        df = df.set_index("ecode_dest")

        # Compute min/max and build colormap
        vmin, vmax = df["net_inflow_pct"].min(), df["net_inflow_pct"].max()
        cmap = linear.PuBuGn_09.scale(vmin, vmax)
        cmap.caption = "FDI Inflow (Percentile Ranking)"
        cmap = cmap.to_step(index=[0, 25, 50, 75, 100])

        # Convert df to GeoJSON and add popup + fillColor property
        geojson_data = json.loads(df.to_json())
        for feat in geojson_data["features"]:
            props = feat["properties"]
            inflow = props.get("net_inflow")

            if inflow is None or pd.isna(inflow):
                inflow_str = "N/A"
                fillColor = "lightgray"
            else:
                inflow_str = f"{inflow:,.0f}"
                fillColor = cmap(inflow)

            # Build popup content
            props["popup"] = (
                f"<div style='font-size:11px; line-height:1.3; padding:6px; "
                f"width:380px; white-space:normal;'>"

                f"<b>{props.get('economy','')}</b><br>"
                f"Year: {year}<br>"
                f"Net inflow (billions USD): "
                f"{'N/A' if inflow is None or pd.isna(inflow) else '{:.1f}'.format(inflow)}<br><br>"

                # Table layout for sources, top source, and MNEs
                f"<table style='width:100%; font-size:11px;'>"
                f"<tr>"
                f"<td><b>Sources:</b> "
                f"{'N/A' if pd.isna(props.get('sources')) else int(props.get('sources'))}</td>"
                f"<td><b>Top Source:</b> {props.get('top_source','N/A')}</td>"
                f"</tr>"
                f"<tr>"
                f"<td colspan='2'><b>MNEs:</b> "
                f"{'N/A' if pd.isna(props.get('extensive_total')) else format(int(props.get('extensive_total')), ',')}</td>"
                f"</tr>"
                f"</table><br>"

                # Shares in two columns
                f"<b>Share of Net Inflow FDI by Component</b><br>"
                f"<table style='width:100%; font-size:11px;'>"
                f"<tr>"
                f"<td>Debt Instruments: "
                f"{'N/A' if pd.isna(props.get('share_debt_instruments')) else '{:.1f}'.format(props.get('share_debt_instruments'))}%</td>"
                f"<td>Equity: "
                f"{'N/A' if pd.isna(props.get('share_equity')) else '{:.1f}'.format(props.get('share_equity'))}%</td>"
                f"</tr>"
                f"<tr>"
                f"<td colspan='2'>Reinvested Earnings: "
                f"{'N/A' if pd.isna(props.get('share_reinv_earnings')) else '{:.1f}'.format(props.get('share_reinv_earnings'))}%</td>"
                f"</tr>"
                f"</table><br>"

                # Business Ready in table
                f"<b>B-Ready Business Entry Scores</b><br>"
                f"<table style='width:100%; font-size:11px;'>"
                f"<tr>"
                f"<td>Regulatory Quality: {props.get('bentry_reg_quality','N/A')}</td>"
                f"<td>Digital Services: {props.get('bentry_dig_trans','N/A')}</td>"
                f"</tr>"
                f"<tr>"
                f"<td colspan='2'>Operational Efficiency: {props.get('bentry_op_efficiency','N/A')}</td>"
                f"</tr>"
                f"</table><br>"

                # Note
                f"<i>Note: If 'None' or 'N/A' appears, it means the data is unavailable.</i>"
                f"</div>"
            )

            props["fillColor"] = fillColor

        # --- One reusable HTML widget for popups ---
        popup_html = HTML()

        # --- GeoJSON layer with per-feature style + popup ---
        geo_layer = GeoJSON(
            data=geojson_data,
            style={"color": "black", "weight": 0, "fillOpacity": 0.6},
            style_callback=lambda feat: {
                "fillColor": feat["properties"].get("fillColor", "lightgray")
            },
            hover_style={"fillColor": "yellow", "fillOpacity": 0.7},
            popup=popup_html
        )

        # --- Map ---
        m = Map(
            center=(0.0, 0.0),
            zoom=2.75,
            basemap=basemaps.CartoDB.Positron,
            layout=Layout(width="100%", height="695px"),
        )
        m.add_layer(geo_layer)

        # Update the HTML content on click
        def update_popup(event, feature, **kwargs):
            props = feature["properties"]
            popup_html.value = props.get("popup", "No data")

        geo_layer.on_click(update_popup)

        # --- Legend ---
        legend = HTML(cmap._repr_html_())
        m.add_control(WidgetControl(widget=legend, position="bottomright"))

        return m

    ##################################
    ## 3. FDI Trends
    indicator_map = {
        "US$ billions (current prices)": {
            ("Inward", "Flow"): "fdi_inward_flow",
            ("Outward", "Flow"): "fdi_outward_flow",
            ("Inward", "Stock"): "fdi_inward_stock",
            ("Outward", "Stock"): "fdi_outward_stock",
        },
        "% change from 2000 baseline (US$ billions)": {
            ("Inward", "Flow"): "fdi_inward_flow_pct_change",
            ("Outward", "Flow"): "fdi_outward_flow_pct_change",
            ("Inward", "Stock"): "fdi_inward_stock_pct_change",
            ("Outward", "Stock"): "fdi_outward_stock_pct_change",
        },
        "Share of Global Total": {
            ("Inward", "Flow"): "fdi_pct_inward_flow",
            ("Outward", "Flow"): "fdi_pct_outward_flow",
            ("Inward", "Stock"): "fdi_pct_inward_stock",
            ("Outward", "Stock"): "fdi_pct_outward_stock",
        },
        "Share of Gross Domestic Product (GDP)": {
            ("Inward", "Flow"): "fdi_gdp_inward_flow",
            ("Outward", "Flow"): "fdi_gdp_outward_flow",
            ("Inward", "Stock"): "fdi_gdp_inward_stock",
            ("Outward", "Stock"): "fdi_gdp_outward_stock",
        },
        "Share of Gross Fixed Capital Formation (GFCF)": {
            ("Inward", "Flow"): "fdi_fkf_inward_flow",
            ("Outward", "Flow"): "fdi_fkf_outward_flow",
            ("Inward", "Stock"): "fdi_fkf_inward_stock",
            ("Outward", "Stock"): "fdi_fkf_outward_stock",
        },
    }

    @output
    @render_widget
    def fdi_trends_graph():
        # Inputs
        economies = input.economy_trends()
        direction = input.fdi_direction()
        fdi_type = input.fdi_type()
        indicator = input.fdi_indicator()

        # Indicator
        var = indicator_map[indicator][(direction, fdi_type)]

        # Filter dataframe
        df = fdi_trends[fdi_trends["economy"].isin(economies)].copy()

        # Custom formatting rules for hover
        if indicator == "US$ billions (current prices)":
            # Always 1 decimal, with comma separator
            df.loc[:, "hover_val"] = df[var].apply(
                lambda v: f"{v:,.1f}" if pd.notna(v) else "NA"
            )
        else:
            # All % indicators 
            def fmt_pct(v):
                if pd.isna(v):
                    return "NA"
                return f"{v:,.2f}%" if abs(v) < 1 else f"{v:,.1f}%"
            df.loc[:, "hover_val"] = df[var].apply(fmt_pct)

        # Graph
        fig = px.line(
            df,
            x="year",
            y=var,
            color="economy",
            title=f"{indicator} ({direction} {fdi_type})",
            labels={"year": "Year", var: indicator},
            color_discrete_sequence=px.colors.qualitative.Safe,
            custom_data=["hover_val"], # send performatted values to hovertemplate
        )

        # Apply hover template
        fig.update_traces(
            mode="lines+markers",
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Year: %{x}<br>"
                f"{indicator}: " + "%{customdata[0]}<extra></extra>"              
            )
        )

        # Clean Layout
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                showgrid=False,
                gridcolor='lightgray',
                title=None
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="lightgray"
            ),
            legend=dict(
                title="Economy",
                orientation="v",
                x=1.05,
                y=0.5,
                xanchor="left",
                yanchor="middle"
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            title_x=0.5,
            title_y=0.95,
            title_font=dict(size=16, family="Segoe UI", color="black")
        )

        # Horizontal line at y=0
        fig.add_hline(
            y=0,
            line_dash="solid",
            line_color="black",
            opacity=0.9
        )

        return fig

    ##################################
    ## 4. FDI Bilateral Trends

    # Inward graph
    @render_widget
    def bilateral_inward_graph():
        economy = input.economy_bilateral()
        year = int(input.bilateral_year())
        fdi_type = input.bilateral_type()

        # Select dataset
        if fdi_type == "Flow":
            df = bilateral_inflow.copy()
            econ_label = "Net Inflow (USD Billions)"
        else:
            df = bilateral_instock.copy()
            econ_label = "Inward Stock (USD Billions)"

        # Filter by economy + year
        df_plot = df[(df["economy_dest"] == economy) & (df["year"] == year)].copy()

        if df_plot.empty:
            return px.scatter(title="No data available")
        
        # Recompute shares to be safe
        df_plot["share"] = df_plot["value"] / df_plot["value"].sum()

        # Pie chart
        fig = px.pie(
            df_plot,
            values="value",
            names="economy_source",
            custom_data=["share"],
            labels={
                "value": econ_label,
                "economy_source": "Source Economy",
                "share": "Share"
            },
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                        econ_label + ": %{value:,.2f}<br>" +
                        "Share: %{customdata[0]:.1%}<extra></extra>",
            textinfo="percent",
            textposition="inside",
            insidetextorientation="radial",
            automargin=True
        )
        fig.update_layout(
            showlegend=True,           # bring back legend
            legend_title="Economy",
            legend=dict(
                orientation="v",       # vertical
                x=1.05,                # push legend to right
                xanchor="left",
                y=0.5,                 # center at half of pie vertically
                yanchor="middle"
            ),
            margin=dict(l=20, r=100, t=80, b=60),
            autosize=True,
            title=dict(
                text=f"Sources of Inward FDI {fdi_type} into {economy} ({year})",
                x=0.5, xanchor="center", yanchor="top"
            )
        )
        return fig
    
    # Outward Graph
    @render_widget
    def bilateral_outward_graph():
        economy = input.economy_bilateral()
        year = int(input.bilateral_year())
        fdi_type = input.bilateral_type()

        # Select dataset
        if fdi_type == "Flow":
            df = bilateral_outflow.copy()
            econ_label = "Net Outflow (USD Billions)"
        else:
            df = bilateral_outstock.copy()
            econ_label = "Outward Stock (USD Billions)"

        # Filter by economy + year
        df_plot = df[(df["economy_source"] == economy) & (df["year"] == year)].copy()

        if df_plot.empty:
            return px.scatter(title="No data available")

        # Recompute shares
        df_plot["share"] = df_plot["value"] / df_plot["value"].sum()

        # Pie chart
        fig = px.pie(
            df_plot,
            values="value",
            names="economy_dest",
            custom_data=["share"],
            labels={
                "value": econ_label,
                "economy_dest": "Destination Economy",
                "share": "Share"
            },
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>" +
                        econ_label + ": %{value:,.2f}<br>" +
                        "Share: %{customdata[0]:.1%}<extra></extra>",
            textinfo="percent",
            textposition="inside",
            insidetextorientation="radial",
            automargin=True
        )
        fig.update_layout(
            showlegend=True,           # bring back legend
            legend_title="Economy",
            legend=dict(
                orientation="v",       # vertical
                x=1.05,                # push legend to right
                xanchor="left",
                y=0.5,                 # center at half of pie vertically
                yanchor="middle"
            ),
            margin=dict(l=20, r=100, t=80, b=60),
            autosize=True,
            title=dict(
                text=f"Destinations of Outward FDI {fdi_type} from {economy} ({year})",
                x=0.5, xanchor="center", yanchor="top"
            )
        )
        return fig
    
    ##################################
    ## 5. FDI Components

    # Component Labels Mapping
    component_labels = {
    "share_debt_instruments": "Share of Debt Instruments",
    "share_equity": "Equity",
    "share_reinv_earnings": "Reinvested Earnings"
    }

    @render_widget
    def fdi_component():
        # Get inputs
        economy = input.economy_component()
        selected_components = input.component()

        # Filter dataset
        df_filtered = fdi_components[
            (fdi_components["economy"] == economy) &
            (fdi_components["component"].isin(selected_components))
        ].copy()

        # If no data matches, return empty figure with message
        if df_filtered.empty:
            fig = px.line()
            fig.add_annotation(
                text="No data available for this selection",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14, color="red")
            )
            fig.update_layout(template="plotly_white")
            return fig

        # Map components to human-readable labels
        df_filtered["component"] = df_filtered["component"].map(component_labels)

        # Create graph
        fig = px.line(
            df_filtered,
            x="year",
            y="fdi_value",
            color="component",
            title=f"Net FDI Inflows by Component - {economy}",
            labels={"year": "Year", "fdi_value": "Share (%)"},
            color_discrete_sequence=px.colors.qualitative.Safe,
            custom_data=["fdi_value"],  # to format hover
        )

        # Hover template
        fig.update_traces(
            mode="lines+markers",
            hovertemplate=(
                "<b>%{fullData.name}</b><br>"
                "Year: %{x}<br>"
                "Value: %{customdata[0]:,.2f}%<extra></extra>"
            )
        )

        # Layout styling
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis=dict(
                showgrid=False,
                gridcolor="lightgray",
                title=None
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="lightgray"
            ),
            legend=dict(
                title="Component",
                orientation="v",
                x=1.05,
                y=0.5,
                xanchor="left",
                yanchor="middle"
            ),
            margin=dict(l=40, r=40, t=60, b=40),
            title_x=0.5,
            title_y=0.95,
            title_font=dict(size=16, family="Segoe UI", color="black")
        )

        # Horizontal reference line
        fig.add_hline(
            y=0,
            line_dash="solid",
            line_color="black",
            opacity=0.9
        )

        return fig

app = App(app_ui, server)