import pandas as pd
import geopandas as gpd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import plotly.express as px
import plotly.graph_objects as go
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import output_widget, render_widget
from ipywidgets import Layout, FloatSlider, ToggleButtons, VBox, HTML
from ipyleaflet import Map, basemaps, Choropleth, GeoJSON, Popup, WidgetControl
from branca.colormap import linear
import json

# from shared import sorted_regions, graph1, graph2, graph3, graph4, graph5, graph6, graph7, graph8 ### Overall FDI Trends
# from shared import graph9 ### FDI Components
# from shared import graph10, graph11, graph12, graph13, graph14, graph15, graph16, graph17 ### Greenfield FDI

from shared import fdi_panel, sorted_regions, fdi_trends, graph9, bilateral_inflow, bilateral_outflow, bilateral_instock, bilateral_outstock, bilateral_economies

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
                            "US$ Millions at Current Prices",
                            "% Change from 2000 (US$ Million)",
                            "% of Global Total",
                            "% of Gross Domestic Product",
                            "% of Gross Fixed Capital Formation"
                        ],
                        selected="US$ Millions at Current Prices"
                    ),
                
                ),

                # Main area: description card + graph below
                ui.div(
                    ui.card(
                        ui.card_header(
                            ui.HTML("<h6 style='text-align:left;'><b>Foreign Direct Investment (FDI) trends</b></h6>")
                        ),
                        ui.HTML("<p style='font-size:11px; color:black;'>Select filters from the sidebar to generate the FDI Trends graph.</p>"),
                        full_screen=False,
                        fill=True,
                    ),

                    # Graph placeholder
                    ui.card( 
                        output_widget("fdi_trends_graph")
                    ),
                )
            )
        ),
        
        # Bilateral FDI Trends 
        ui.nav_panel(
            "Bilateral FDI Trends",

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
                        ui.HTML("<p style='font-size:11px; color:black;'>Top 5 economies investing in the selected economy.</p>"),
                        output_widget("bilateral_inward_graph"),
                        ui.HTML("<p style='font-size:10px; color:gray; text-align:center;'>Source: United Nations Conference on Trade and Development (UNCTAD)</p>"),
                        full_screen=True,
                        fill=True,
                        style="min-height:500px;" 
                    ),
                    ui.card(
                        ui.card_header(
                            ui.HTML("<h6 style='text-align:left;'><b>Outward FDI</b></h6>")
                        ),
                        ui.HTML("<p style='font-size:11px; color:black;'>Top 5 economies where the selected economy invests.</p>"),
                        output_widget("bilateral_outward_graph"),
                        ui.HTML("<p style='font-size:10px; color:gray; text-align:center;'>Source: United Nations Conference on Trade and Development (UNCTAD)</p>"),
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
            ui.card(
                ui.card_header(ui.HTML("""<div style="text-align:center; margin-top:20px;"><h2><b>FDI Inflows by Component</b></h2></div>""")),
                ui.p(
                    ui.HTML("""<div style="text-align:left;"><h3>Inflow by Debt Instruments, Equity, or Reinvested Earnings</h3></div>"""),
                    ui.input_select("region9", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy9", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph9"),
                ),
            ),
        ),

        # MNE Activity Trends
        ui.nav_panel(
            "MNE Activity Trends",
            ui.HTML("""<div style="text-align:center; margin-top:20px;">
                        <h2><b>MNE Activity Trends</b></h2>
                        <p style="font-size:16px;">Placeholder for MNE Activity Trends graphs and controls.</p>
                    </div>""")
        ),

        # # --- Greenfield FDI (KEPT but HIDDEN) ---
        # # give the tab a fixed value="greenfield" so CSS can target it
        # ui.nav_panel(
        #     "Greenfield FDI",
        #     ui.HTML('<div style="text-align:center; margin-top:20px;"><h1><b>Greenfield FDI</b></h1></div>'),

        # # ---- Inward Greenfield FDI ----
        #     ui.card(
        #         ui.card_header(ui.HTML('<div style="text-align:left;"><h2><b>Inward Greenfield FDI</b></h2></div>')),
        #         ui.p(
        #             ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Inflows</h3></div>'),
        #             ui.input_select("region10", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
        #             ui.input_select("economy10", "Select an Economy", choices=[], multiple=True),
        #             output_widget("fdi_graph10"),
        #         ),
        #         ui.p(
        #             ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Inflows in Services within the Manufacturing Sector</h3></div>'),
        #             ui.input_select("region11", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
        #             ui.input_select("economy11", "Select an Economy", choices=[], multiple=True),
        #             output_widget("fdi_graph11"),
        #         ),
        #         ui.p(
        #             ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Inflows by Business Function in the Services and Manufacturing Sectors</h3></div>'),
        #             ui.input_select("region12", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
        #             ui.input_select("economy12", "Select an Economy", choices=[], multiple=True),
        #             output_widget("fdi_graph12"),
        #         ),
        #         ui.p(
        #             ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Inflows in High-Technology Activities in the Manufacturing Sector</h3></div>'),
        #             ui.input_select("region13", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
        #             ui.input_select("economy13", "Select an Economy", choices=[], multiple=True),
        #             output_widget("fdi_graph13"),
        #         ),
        #     ),

        # # ---- Outward Greenfield FDI ----
        #     ui.card(
        #         ui.card_header(ui.HTML('<div style="text-align:left;"><h2><b>Outward Greenfield FDI</b></h2></div>')),
        #         ui.p(
        #             ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Outflows</h3></div>'),
        #             ui.input_select("region14", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
        #             ui.input_select("economy14", "Select an Economy", choices=[], multiple=True),
        #             output_widget("fdi_graph14"),
        #         ),
        #         ui.p(
        #             ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Outflows in Services within the Manufacturing Sector</h3></div>'),
        #             ui.input_select("region15", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
        #             ui.input_select("economy15", "Select an Economy", choices=[], multiple=True),
        #             output_widget("fdi_graph15"),
        #         ),
        #         ui.p(
        #             ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Outflows by Business Function in the Services and Manufacturing Sectors</h3></div>'),
        #             ui.input_select("region16", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
        #             ui.input_select("economy16", "Select an Economy", choices=[], multiple=True),
        #             output_widget("fdi_graph16"),
        #         ),
        #         ui.p(
        #             ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Outflows in High-Technology Activities</h3></div>'),
        #             ui.input_select("region17", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
        #             ui.input_select("economy17", "Select an Economy", choices=[], multiple=True),
        #             output_widget("fdi_graph17"),
        #         ),
        #     ),

        #     # keep this value so the CSS rule can hide the tab
        #     value="greenfield",
        #     ),

        # Policies
        ui.nav_panel("Policies", ui.HTML("<p>Policies content goes here.</p>")),

        # Incentives
        ui.nav_panel("Incentives", ui.HTML("<p>Incentives content goes here.</p>")),

        # FDI Spillover Toolkit
        ui.nav_panel("FDI Spillover Toolkit", ui.HTML("<p>FDI Spillover Toolkit content goes here.</p>")),

        # Data Sources
        ui.nav_panel(
            "Data Sources",
            ui.HTML("""
                <div>
                    <h1>UN Trade and Development (UNCTAD)</h1>
                    <p>This is placeholder text UNCTAD.</p>
                    <h1>International Monetary Fund (IMF)</h1>
                    <p>This is placeholder text for IMF.</p>
                    <h1>fDi Markets</h1>
                    <p>This is placeholder text for fDi Markets.</p>
                </div>
            """)
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
            ui.HTML("""
                <div style="margin-top:20px;"> 
                    <h3 style="font-weight:bold;">What is Foreign Direct Investment (FDI)?</h3>
                    <p style="font-size:16px;">
                        Foreign direct investment reflects the objective of establishing a lasting interest by a resident 
                        enterprise in one economy (direct investor) in an enterprise (direct investment enterprise) that is 
                        resident in an economy other than that of the direct investor (OECD Benchmark Definition of Foreign 
                        Direct Investment). 
                    </p>
                    <p style="font-size:16px;">
                        The lasting interest implies the existence of a long-term relationship between the 
                        direct investor and the direct investment enterprise and a significant degree of influence on the 
                        management of the enterprise. The direct or indirect ownership of 10% or more of the voting power 
                        of an enterprise resident in one economy by an investor resident in another economy is evidence of 
                        such a relationship (Fifth Edition, paragraph 65).
                    </p>

                    <h3 style="font-weight:bold;">What is a Multinational Enterprise (MNE)?</h3>
                    <p style="font-size:16px;">
                        Legal entity that has at least one non-resident affiliate or branch, and exercises
                        control over its affiliate(s) or branch(es) either directly—by having over 50% of the voting power in the
                        unit—or by indirect transmission of control. The multinational enterprise is the ultimate controlling parent—
                        the direct investor at the top of the control chain.
                    </p>

                    <h3 style="font-weight:bold;">What are MNE activities?</h3>
                    <p style="font-size:16px;">
                    An MNE exists when a resident investor in one economy establishes a “lasting interest” in an enterprise located in another economy, 
                    generally demonstrated by owning at least 10% of the voting power. This lasting interest implies a long-term relationship and a 
                    significant degree of influence over the management of the foreign enterprise. MNE activities therefore include setting up or 
                    acquiring subsidiaries, branches, or joint ventures abroad, as well as expanding production, services, or sales across multiple countries.
                    </p>
                    <p style="font-size:16px;">
                    These activities go beyond the initial equity stake: they also encompass reinvested earnings, intra-company loans, 
                    and the coordination of operations across affiliates. In practice, MNEs integrate and internalize transactions 
                    such as capital, technology, and knowledge transfers within their global corporate network, 
                    optimizing costs, efficiency, and market access. As such, MNE activities under the OECD framework are 
                    not limited to investment flows, but extend to the full range of cross-border economic operations and management structures 
                    that tie together global value chains.
                    </p>

                    <h3 style="font-weight:bold;">What does the IMAT Dashboard include?</h3>
                    <p style="font-size:16px;">Definition</p>

                    <h3 style="font-weight:bold;">How is the IMAT Dashboard organized?</h3>
                    <p style="font-size:16px;">Definition</p>

                    <h3 style="font-weight:bold;">How can the IMAT Dashboard be used?</h3>
                    <p style="font-size:16px;">Definition</p>

                    <h3 style="font-weight:bold;">Why do we need the IMAT Dashboard?</h3>
                    <p style="font-size:16px;">Definition</p>

                    <h3 style="font-weight:bold;">What is the current version of the Dashboard?</h3>
                    <p style="font-size:16px;">Definition</p>

                </div>
            """)
        ),

        id="main_tabs",
        
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
    """)
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
                across countries, regions, and sectors.</p>
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
        vmin, vmax = df["net_inflow"].min(), df["net_inflow"].max()
        cmap = linear.PuBuGn_09.scale(vmin, vmax)
        cmap.caption = "FDI Inflow (USD millions)"

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

            props["popup"] = (
                f"<div style='font-size:11px; line-height:1.2; padding:2px;'>"
                f"<b>{props.get('economy','')}</b><br>"
                f"Year: {year}<br>"
                f"Net inflow: {inflow_str}"
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
            zoom=2,
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
        "US$ Millions at Current Prices": {
            ("Inward", "Flow"): "fdi_inward_flow",
            ("Outward", "Flow"): "fdi_outward_flow",
            ("Inward", "Stock"): "fdi_inward_stock",
            ("Outward", "Stock"): "fdi_outward_stock",
        },
        "% Change from 2000 (US$ Million)": {
            ("Inward", "Flow"): "fdi_inward_flow_pct_change",
            ("Outward", "Flow"): "fdi_outward_flow_pct_change",
            ("Inward", "Stock"): "fdi_inward_stock_pct_change",
            ("Outward", "Stock"): "fdi_outward_stock_pct_change",
        },
        "% of Global Total": {
            ("Inward", "Flow"): "fdi_pct_inward_flow",
            ("Outward", "Flow"): "fdi_pct_outward_flow",
            ("Inward", "Stock"): "fdi_pct_inward_stock",
            ("Outward", "Stock"): "fdi_pct_outward_stock",
        },
        "% of Gross Domestic Product": {
            ("Inward", "Flow"): "fdi_gdp_inward_flow",
            ("Outward", "Flow"): "fdi_gdp_outward_flow",
            ("Inward", "Stock"): "fdi_gdp_inward_stock",
            ("Outward", "Stock"): "fdi_gdp_outward_stock",
        },
        "% of Gross Fixed Capital Formation": {
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
        df = fdi_trends[fdi_trends["economy"].isin(economies)]

        # Graph
        fig = px.line(
            df,
            x="year",
            y=var,
            color="economy",
            title=f"{indicator} ({direction} {fdi_type})",
            labels={"year": "Year", var: indicator},
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
            econ_label = "Net Inflow (USD Millions)"
        else:
            df = bilateral_instock.copy()
            econ_label = "Inward Stock (USD Millions)"

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
                        econ_label + ": %{value:,.1f}<br>" +
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
            econ_label = "Net Outflow (USD Millions)"
        else:
            df = bilateral_outstock.copy()
            econ_label = "Outward Stock (USD Millions)"

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
                        econ_label + ": %{value:,.1f}<br>" +
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
                text=f"Sources of Outward FDI {fdi_type} from {economy} ({year})",
                x=0.5, xanchor="center", yanchor="top"
            )
        )
        return fig

#     #########################
    # Graph 9 - FDI Composition (Equity, Reinvestment, Debt)
    @reactive.effect
    def update_economies9():
        selected_region = input.region9()
        filtered_economies = graph9[graph9["region_dest"] == selected_region]["economy_dest"].unique()
        ui.update_select("economy9", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph9():
        selected_economies = input.economy9()
        selected_region = input.region9()

        if not selected_economies:
            return px.area(title="Select at least one economy to view trends")
        
        # Filter data for selected economies from the transformed melted graph
        economy_data = graph9[graph9["economy_dest"].isin(selected_economies)]

        # Ensure the correct order of the components in the 'component' column
        component_order = ["debt_instruments", "equity", "reinv_earn"]

        # Create a mapping for readable component names
        label_map = {
            "debt_instruments": "Debt Instruments",
            "equity": "Equity",
            "reinv_earn": "Reinvested Earnings"
        }

        # Replace internal labels with readable ones
        economy_data["component"] = economy_data["component"].map(label_map)

        # Define the new display order
        component_order = ["Debt Instruments", "Equity", "Reinvested Earnings"]

        # Create the stacked bar chart
        fig = px.bar(
            economy_data,
            x="year",
            y="fdi_value", 
            color="component",
            barmode="relative",  # Stack bars (handles positive & negative)
            category_orders={"component": component_order},
            color_discrete_map={
                "Debt Instruments": "blue",
                "Equity": "orange",
                "Reinvested Earnings": "gray"
            },
            labels={"fdi_value": "FDI Value (USD)", "year": "Year"}
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", 
            paper_bgcolor="white",
            xaxis=dict(
                showline=True, 
                linecolor="black", 
                zeroline=False,
                tickmode="array",
                tickvals=sorted(economy_data["year"].unique()),
                ticktext=[str(year) for year in sorted(economy_data["year"].unique())]
            ),
            yaxis=dict(
                zeroline=True,
                zerolinewidth=2,
                zerolinecolor="black",
                showline=True,
                linecolor="black"
            ),
            #title={
            #    'text': f"FDI Composition in {', '.join(selected_economies)}",
            #    'y': 0.96,
            #    'x': 0.5,
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=22)
            #},
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.35,
                xanchor="center",
                x=0.5,
                tracegroupgap=5,
                font=dict(size=12)
            )
        )

        return fig

    ######################### ######################### ######################### #########################
    
#     ################################
#     # Graph 10 - Greenfield FDI Inflows
#     @reactive.effect
#     def update_economies10():
#         selected_region = input.region10()
#         filtered_economies = (
#             graph10.loc[graph10["region_dest"] == selected_region, "economy_dest"]
#             .dropna()
#             .unique()
#         )
#         ui.update_select("economy10", choices=sorted(filtered_economies.tolist()), selected=None)

#     @render_widget 
#     def fdi_graph10():
#         selected_economies = input.economy10()
#         region = input.region10()

#         if not selected_economies:
#             return px.line(title="Select at least one economy to view trends")
        
#         selected_economies = selected_economies[:5]
#         region_data = graph10[graph10["region_dest"] == region]
#         region_stats = region_data.groupby("year")["capexusm"].agg(
#             max_capexusm="max",
#             min_capexusm="min",
#             median_capexusm="median"
#         ).reset_index()
#         economy_data = region_data[region_data["economy_dest"].isin(selected_economies)]
            
#         fig = px.line(
#             economy_data,
#             x="year",
#             y="capexusm",
#             color="economy_dest",
#             markers=True,
#             labels={"economy_dest": "Destination"},
#         )      

#         fig.update_layout(
#             #title={
#             #    'text': f"Greenfield FDI Inflows in {', '.join(selected_economies)}",
#             #    'y': 0.9,  # vertical position
#             #    'x': 0.5,  # horizontal center
#             #    'xanchor': 'center',
#             #    'yanchor': 'top',
#             #    'font': dict(size=22)  # adjust font size here
#             #},
#             legend=dict(
#                 orientation="h",  # Horizontal legend
#                 yanchor="top",  # Align legend to the top
#                 y=-0.35,  # Move legend below the graph
#                 xanchor="center",  # Align legend to the center
#                 x=0.5,  # Horizontal position of the legend
#                 tracegroupgap=5,  # Space between different legend items
#                 font=dict(size=12)  # Optional: change font size of the legend items
#             )
#         )

#         # Add a horizontal line at y=0
#         fig.add_trace(
#             go.Scatter(
#                 x=region_stats["year"],
#                 y=[0] * len(region_stats),
#                 mode="lines",
#                 line=dict(color="black", width=1, dash="solid"),
#                 name="Zero Line",
#                 showlegend=False
#             )
#         )

#         # Add median line for the region
#         #fig.add_trace(
#         #    go.Scatter(
#         #        x=region_stats["year"],
#         #        y=region_stats["median_capexusm"],
#         #        mode="lines",
#         #        line=dict(color='gray', dash="dash", width=2),
#         #        name="Regional Median CapEx Flow"
#         #    )
#         #)

#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=sorted(graph10["year"].unique()),
#             title_text="Year"
#         )

#         fig.update_yaxes(title_text="CapEx Flow (in USD Millions)")

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
#             paper_bgcolor="white",  # White card background
#             margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
#         )

#         return fig
    
#     ####################################################################
#     # Graph 11 - Grrenfield FDI Inflows in Services within Manufacturing
#     @reactive.effect
#     def update_economies11():
#         selected_region = input.region11()
#         filtered_economies = (
#             graph11.loc[graph11["region_dest"] == selected_region, "economy_dest"]
#             .dropna()
#             .unique()
#         )
#         ui.update_select("economy11", choices=sorted(filtered_economies.tolist()), selected=None)

#     @render_widget
#     def fdi_graph11():
#         selected_economies = input.economy11()
#         region = input.region11()

#         if not selected_economies:
#             return px.line(title="Select at least one economy to view trends")
        
#         if isinstance(selected_economies, str):
#             selected_economies = [selected_economies]

#         filtered_df = graph11[graph11["economy_dest"].isin(selected_economies)]

#         # Define your color gradient from light to dark blue
#         serv_manu_colors = {
#             "Services": "#4CAF50",         # Green
#             "Manufacturing": "#9C27B0",  # Purple
#             "Other Non-Services": "#FF9800", # Orange
#         }

#         fig = px.area(
#             filtered_df,
#             x="year",
#             y="share_capex",  # Plot the share of capex
#             color="serv_manu",
#             color_discrete_map=serv_manu_colors,  # Different colors for Services, Manufacturing, and Other Non-Services
#             labels={"share_capex": "Share of CapEx Flow",
#                     "serv_manu": "Business Function",
#                     "year": "Year"
#             },
#             hover_data=["serv_manu"],
#             category_orders={
#                 "serv_manu": [
#                     "Services", 
#                     "Manufacturing", 
#                     "Other Non-Services"
#                 ]
#             },
#         )

#         fig.update_layout(
#             #title={
#             #    'text': f"Greenfield FDI Inflow in Services within the Manufacturing Sector in {', '.join(selected_economies)}",
#             #    'y': 0.96,  # vertical position
#             #    'x': 0.5,  # horizontal center
#             #    'xanchor': 'center',
#             #    'yanchor': 'top',
#             #    'font': dict(size=20)  # adjust font size here
#             #},
#             legend=dict(
#                 orientation="h",  # Horizontal legend
#                 yanchor="top",  # Align legend to the top
#                 y=-0.35,  # Move legend below the graph
#                 xanchor="center",  # Align legend to the center
#                 x=0.5,  # Horizontal position of the legend
#                 tracegroupgap=5,  # Space between different legend items
#                 font=dict(size=12)  # Optional: change font size of the legend items
#             )
#         )

#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=sorted(graph11["year"].unique()),  # Ensure correct years are displayed
#             title_text="Year"
#         )

#         fig.update_yaxes(title_text="Share of CapEx Flow", range=[0, 1])  # Y-axis represents percentage

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
#             paper_bgcolor="white",  # White card background
#             margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
#         )

#         return fig

#    ##################################################################################################
#    # Graph 12 - Greenfield FDI Inflows by Business Function in the Services and Manufacturing Sectors
#     @reactive.effect
#     def update_economies12():
#         selected_region = input.region12()
#         filtered_economies = (
#             graph12.loc[graph12["region_dest"] == selected_region, "economy_dest"]
#             .dropna()
#             .unique()
#         )
#         ui.update_select("economy12", choices=sorted(filtered_economies.tolist()), selected=None)

#     @render_widget
#     def fdi_graph12():
#         selected_economies = input.economy12()
#         region = input.region12()

#         if not selected_economies:
#             return px.line(title="Select at least one economy to view trends")
        
#         if isinstance(selected_economies, str):
#             selected_economies = [selected_economies]

#         filtered_df = graph12[graph12["economy_dest"].isin(selected_economies)]

#         fig = px.line(
#             filtered_df,
#             x="year",
#             y="capexusm",
#             color="businessfunction",
#             markers=True,
#             labels={"economy_dest": "Destination",
#                     "businessfunction": "Business Function"},
#         )

#         fig.update_layout(
#             #title={
#             #    'text': f"Greenfield FDI Inflow by Business Function in Services and Manufacturing in {', '.join(selected_economies)}",
#             #    'y': 0.96,  # vertical position
#             #    'x': 0.5,  # horizontal center
#             #    'xanchor': 'center',
#             #    'yanchor': 'top',
#             #    'font': dict(size=20)  # adjust font size here
#             #},
#             legend=dict(
#                 orientation="h",  # Horizontal legend
#                 yanchor="top",  # Align legend to the top
#                 y=-0.35,  # Move legend below the graph
#                 xanchor="center",  # Align legend to the center
#                 x=0.5,  # Horizontal position of the legend
#                 tracegroupgap=5,  # Space between different legend items
#                 font=dict(size=12)  # Optional: change font size of the legend items
#             )
#         )
        
#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=sorted(graph12["year"].unique()),  # Ensure correct years are displayed
#             title_text="Year"
#         )

#         fig.update_yaxes(title_text="CapEx Flow (in USD Millions)")

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
#             paper_bgcolor="white",  # White card background
#             margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
#         )

#         return fig
    
#     #################################################################
#     # Graph 13 - Greenfield FDI Inflows in High-Technology Activities
#     @reactive.effect
#     def update_economies13():
#         selected_region = input.region13()
#         filtered_economies = (
#             graph13.loc[graph13["region_dest"] == selected_region, "economy_dest"]
#             .dropna()
#             .unique()
#         )
#         ui.update_select("economy13", choices=sorted(filtered_economies.tolist()), selected=None)

#     @render_widget
#     def fdi_graph13():
#         selected_economies = input.economy13()
#         region = input.region13()

#         if not selected_economies:
#             return px.line(title="Select at least one economy to view trends")
        
#         if isinstance(selected_economies, str):
#             selected_economies = [selected_economies]

#         filtered_df = graph13[graph13["economy_dest"].isin(selected_economies)]

#         # Define your color gradient from light to dark blue
#         blue_gradient = {
#             "Low-technology": "#cce5ff",         # Lightest blue
#             "Medium-low-technology": "#99ccff",  # A bit darker
#             "Medium-high-technology": "#3399ff", # Darker
#             "High-technology": "#0066cc"         # Darkest blue
#         }

#         # Create the stacked bar chart
#         fig = px.bar(
#             filtered_df,
#             x="year",
#             y="percentage",  # The percentage share of capexUSm
#             color="man_tech", 
#             labels={
#                 "percentage": "Percentage of Total CapEx Flow",
#                 "man_tech": "Technology",
#                 "year": "Year"
#             },
#             hover_data=["man_tech"],  # Show relevant info on hover
#             category_orders={
#                 "man_tech": [
#                     "Low-technology", 
#                     "Medium-low-technology", 
#                     "Medium-high-technology", 
#                     "High-technology"
#                 ]
#             },  # Ensure consistent order for man_tech categories
#             color_discrete_map=blue_gradient,  # Apply custom blue gradient
#             barmode="stack",  # Stack the bars
#         )

#         fig.update_layout(
#             #title={
#             #    'text': f"Greenfield FDI Inflow in Manufacturing High-Tech Activities in {', '.join(selected_economies)}",
#             #    'y': 0.96,  # vertical position
#             #    'x': 0.5,  # horizontal center
#             #    'xanchor': 'center',
#             #    'yanchor': 'top',
#             #    'font': dict(size=20)  # adjust font size here
#             #},
#             legend=dict(
#                 orientation="h",  # Horizontal legend
#                 yanchor="top",  # Align legend to the top
#                 y=-0.35,  # Move legend below the graph
#                 xanchor="center",  # Align legend to the center
#                 x=0.5,  # Horizontal position of the legend
#                 tracegroupgap=5,  # Space between different legend items
#                 font=dict(size=12)  # Optional: change font size of the legend items
#             )
#         )

#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=sorted(graph13["year"].unique()),  # Ensure correct years are displayed
#             title_text="Year"
#         )

#         fig.update_yaxes(title_text="Share of CapEx Flow", range=[0, 100])  # Y-axis is percentage, 0-100%

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
#             paper_bgcolor="white",  # White card background
#             margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
#         )

#         return fig

#     ################################
#     # Graph 14 - Greenfield FDI Outflows
#     @reactive.effect
#     def update_economies14():
#         selected_region = input.region14()
#         filtered_economies = (
#             graph14.loc[graph14["region_source"] == selected_region, "economy_source"]
#             .dropna()
#             .unique()
#         )
#         ui.update_select("economy14", choices=sorted(filtered_economies.tolist()), selected=None)

#     @render_widget 
#     def fdi_graph14():
#         selected_economies = input.economy14()
#         region = input.region14()

#         if not selected_economies:
#             return px.line(title="Select at least one economy to view trends")
        
#         selected_economies = selected_economies[:5]
#         region_data = graph14[graph14["region_source"] == region]
#         region_stats = region_data.groupby("year")["capexusm"].agg(
#             max_capexusm="max",
#             min_capexusm="min",
#             median_capexusm="median"
#         ).reset_index()
#         economy_data = region_data[region_data["economy_source"].isin(selected_economies)]
            
#         fig = px.line(
#             economy_data,
#             x="year",
#             y="capexusm",
#             color="economy_source",
#             markers=True,
#             labels={"economy_source": "Source"},
#         )      

#         fig.update_layout(
#             #title={
#             #    'text': f"Greenfield FDI Outflows from {', '.join(selected_economies)}",
#             #    'y': 0.9,  # vertical position
#             #    'x': 0.5,  # horizontal center
#             #    'xanchor': 'center',
#             #    'yanchor': 'top',
#             #    'font': dict(size=22)  # adjust font size here
#             #},
#             legend=dict(
#                 orientation="h",  # Horizontal legend
#                 yanchor="top",  # Align legend to the top
#                 y=-0.35,  # Move legend below the graph
#                 xanchor="center",  # Align legend to the center
#                 x=0.5,  # Horizontal position of the legend
#                 tracegroupgap=5,  # Space between different legend items
#                 font=dict(size=12)  # Optional: change font size of the legend items
#             )
#         )

#         # Add a horizontal line at y=0
#         fig.add_trace(
#             go.Scatter(
#                 x=region_stats["year"],
#                 y=[0] * len(region_stats),
#                 mode="lines",
#                 line=dict(color="black", width=1, dash="solid"),
#                 name="Zero Line",
#                 showlegend=False
#             )
#         )

#         # Add median line for the region
#         #fig.add_trace(
#         #    go.Scatter(
#         #        x=region_stats["year"],
#         #        y=region_stats["median_capexusm"],
#         #        mode="lines",
#         #        line=dict(color='gray', dash="dash", width=2),
#         #        name="Regional Median CapEx Flow"
#         #    )
#         #)

#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=sorted(graph14["year"].unique()),
#             title_text="Year"
#         )

#         fig.update_yaxes(title_text="CapEx Flow (in USD Millions)")

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
#             paper_bgcolor="white",  # White card background
#             margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
#         )

#         return fig
    
#     ####################################################################
#     # Graph 15 - Greenfield FDI Outflows in Services within Manufacturing
#     @reactive.effect
#     def update_economies15():
#         selected_region = input.region15()
#         filtered_economies = (
#             graph15.loc[graph15["region_source"] == selected_region, "economy_source"]
#             .dropna()
#             .unique()
#         )
#         ui.update_select("economy15", choices=sorted(filtered_economies.tolist()), selected=None)

#     @render_widget
#     def fdi_graph15():
#         selected_economies = input.economy15()
#         region = input.region15()

#         if not selected_economies:
#             return px.line(title="Select at least one economy to view trends")
        
#         if isinstance(selected_economies, str):
#             selected_economies = [selected_economies]

#         filtered_df = graph15[graph15["economy_source"].isin(selected_economies)]

#         # Define your color gradient from light to dark blue
#         serv_manu_colors = {
#             "Services": "#4CAF50",         # Green
#             "Manufacturing": "#9C27B0",  # Purple
#             "Other Non-Services": "#FF9800", # Orange
#         }

#         fig = px.area(
#             filtered_df,
#             x="year",
#             y="share_capex",  # Plot the share of capex
#             color="serv_manu",
#             color_discrete_map=serv_manu_colors,  # Different colors for Services, Manufacturing, and Other Non-Services
#             labels={"share_capex": "Share of CapEx Flow",
#                     "serv_manu": "Business Function",
#                     "year": "Year"
#             },
#             hover_data=["serv_manu"],
#             category_orders={
#                 "serv_manu": [
#                     "Services", 
#                     "Manufacturing", 
#                     "Other Non-Services"
#                 ]
#             },
#         )

#         fig.update_layout(
#             #title={
#             #    'text': f"Greenfield FDI Outflow in Services within the Manufacturing Sector from {', '.join(selected_economies)}",
#             #    'y': 0.96,  # vertical position
#             #    'x': 0.5,  # horizontal center
#             #    'xanchor': 'center',
#             #    'yanchor': 'top',
#             #    'font': dict(size=20)  # adjust font size here
#             #},
#             legend=dict(
#                 orientation="h",  # Horizontal legend
#                 yanchor="top",  # Align legend to the top
#                 y=-0.35,  # Move legend below the graph
#                 xanchor="center",  # Align legend to the center
#                 x=0.5,  # Horizontal position of the legend
#                 tracegroupgap=5,  # Space between different legend items
#                 font=dict(size=12)  # Optional: change font size of the legend items
#             )
#         )

#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=sorted(graph15["year"].unique()),  # Ensure correct years are displayed
#             title_text="Year"
#         )

#         fig.update_yaxes(title_text="Share of CapEx Flow", range=[0, 1])  # Y-axis represents percentage

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
#             paper_bgcolor="white",  # White card background
#             margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
#         )

#         return fig

#     ##################################################################################################
#     # Graph 16 - Greenfield FDI Outflows by Business Function in the Services and Manufacturing Sectors
#     @reactive.effect
#     def update_economies16():
#         selected_region = input.region16()
#         filtered_economies = (
#             graph16.loc[graph16["region_source"] == selected_region, "economy_source"]
#             .dropna()
#             .unique()
#         )
#         ui.update_select("economy16", choices=sorted(filtered_economies.tolist()), selected=None)

#     @render_widget
#     def fdi_graph16():
#         selected_economies = input.economy16()
#         region = input.region16()

#         if not selected_economies:
#             return px.line(title="Select at least one economy to view trends")
        
#         if isinstance(selected_economies, str):
#             selected_economies = [selected_economies]

#         filtered_df = graph16[graph16["economy_source"].isin(selected_economies)]

#         fig = px.line(
#             filtered_df,
#             x="year",
#             y="capexusm",
#             color="businessfunction",
#             markers=True,
#             labels={"economy_dest": "Destination",
#                     "businessfunction": "Business Function"},
#         )

#         fig.update_layout(
#             #title={
#             #    'text': f"Greenfield FDI Outflow by Business Function in Services and Manufacturing from {', '.join(selected_economies)}",
#             #    'y': 0.96,  # vertical position
#             #    'x': 0.5,  # horizontal center
#             #    'xanchor': 'center',
#             #    'yanchor': 'top',
#             #    'font': dict(size=20)  # adjust font size here
#             #},
#             legend=dict(
#                 orientation="h",  # Horizontal legend
#                 yanchor="top",  # Align legend to the top
#                 y=-0.35,  # Move legend below the graph
#                 xanchor="center",  # Align legend to the center
#                 x=0.5,  # Horizontal position of the legend
#                 tracegroupgap=5,  # Space between different legend items
#                 font=dict(size=12)  # Optional: change font size of the legend items
#             )
#         )
        
#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=sorted(graph16["year"].unique()),  # Ensure correct years are displayed
#             title_text="Year"
#         )

#         fig.update_yaxes(title_text="CapEx Flow (in USD Millions)")

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
#             paper_bgcolor="white",  # White card background
#             margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
#         )

#         return fig

#     #################################################################
#     # Graph 17 - Greenfield FDI Outflows in High-Technology Activities
#     @reactive.effect
#     def update_economies17():
#         selected_region = input.region17()
#         filtered_economies = (
#             graph17.loc[graph17["region_source"] == selected_region, "economy_source"]
#             .dropna()
#             .unique()
#         )
#         ui.update_select("economy17", choices=sorted(filtered_economies.tolist()), selected=None)

#     @render_widget
#     def fdi_graph17():
#         selected_economies = input.economy17()
#         region = input.region17()

#         if not selected_economies:
#             return px.line(title="Select at least one economy to view trends")
        
#         if isinstance(selected_economies, str):
#             selected_economies = [selected_economies]

#         filtered_df = graph17[graph17["economy_source"].isin(selected_economies)]

#         # Define your color gradient from light to dark blue
#         blue_gradient = {
#             "Low-technology": "#cce5ff",         # Lightest blue
#             "Medium-low-technology": "#99ccff",  # A bit darker
#             "Medium-high-technology": "#3399ff", # Darker
#             "High-technology": "#0066cc"         # Darkest blue
#         }

#         # Create the stacked bar chart
#         fig = px.bar(
#             filtered_df,
#             x="year",
#             y="percentage",  # The percentage share of capexUSm
#             color="man_tech", 
#             labels={
#                 "percentage": "Percentage of Total CapEx Flow",
#                 "man_tech": "Technology",
#                 "year": "Year"
#             },
#             hover_data=["man_tech"],  # Show relevant info on hover
#             category_orders={
#                 "man_tech": [
#                     "Low-technology", 
#                     "Medium-low-technology", 
#                     "Medium-high-technology", 
#                     "High-technology"
#                 ]
#             },  # Ensure consistent order for man_tech categories
#             color_discrete_map=blue_gradient,  # Apply custom blue gradient
#             barmode="stack",  # Stack the bars
#         )

#         fig.update_layout(
#             # title={
#             #    'text': f"Greenfield FDI Outflow in Manufacturing High-Tech Activities from {', '.join(selected_economies)}",
#             #    'y': 0.96,  # vertical position
#             #    'x': 0.5,  # horizontal center
#             #    'xanchor': 'center',
#             #    'yanchor': 'top',
#             #    'font': dict(size=20)  # adjust font size here
#             #},
#             legend=dict(
#                 orientation="h",  # Horizontal legend
#                 yanchor="top",  # Align legend to the top
#                 y=-0.35,  # Move legend below the graph
#                 xanchor="center",  # Align legend to the center
#                 x=0.5,  # Horizontal position of the legend
#                 tracegroupgap=5,  # Space between different legend items
#                 font=dict(size=12)  # Optional: change font size of the legend items
#             )
#         )

#         fig.update_xaxes(
#             tickmode="array",
#             tickvals=sorted(graph17["year"].unique()),  # Ensure correct years are displayed
#             title_text="Year"
#         )

#         fig.update_yaxes(title_text="Share of CapEx Flow", range=[0, 100])  # Y-axis is percentage, 0-100%

#         fig.update_layout(
#             plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
#             paper_bgcolor="white",  # White card background
#             margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
#         )

#         return fig 

app = App(app_ui, server)