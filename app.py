import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import plotly.express as px
import plotly.graph_objects as go
from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shinywidgets import output_widget, render_widget
from ipyleaflet import Map

from shared import sorted_regions, graph1, graph2, graph3, graph4, graph5, graph6, graph7, graph8 ### Overall FDI Trends
from shared import graph9 ### FDI Components
from shared import graph10, graph11, graph12, graph13, graph14, graph15, graph16, graph17 ### Greenfield FDI

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
            """),
            ui.card(
                ui.navset_pill(
                    ui.nav_panel(
                        "Inflow",
                        output_widget("map"),
                        ui.div(
                            ui.input_slider(
                                "year_slider",
                                "Select Year",
                                min=2000,
                                max=2021,
                                value=2020,
                                step=1,
                            )
                        ),
                    ),
                    ui.nav_panel("Outflow", "Outflow Map"),
                    ui.nav_panel("Instock", "Instock Map"),
                    ui.nav_panel("Outstock", "Outstock Map"),
                    id="map_tab",
                ),
            ),
        ),

        # FDI TRENDS
        ui.nav_panel(
            "FDI Trends",
            ui.HTML("""<div style="text-align:center; margin-top:20px;"><h1><b>FDI Trends</b></h1></div>"""),
            ui.card(
                ui.card_header(ui.HTML("""<div style="text-align:left;"><h2><b>FDI Flow</b></h2></div>""")),
                ui.p(
                    ui.HTML("""<div style="text-align:left;"><h3>FDI Net Inflows Trends</h3></div>"""),
                    ui.input_select("region1", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy1", "Select up to 5 Economies", choices=[], multiple=True),
                    ui.input_checkbox("show_total_inflow", "Show Regional Median Net Inflow", value=False),
                    output_widget("fdi_graph1"),
                ),
                ui.p(
                    ui.HTML("""<div style="text-align:left;"><h3>Top 5 Sources of FDI (Net Inflow)</h3></div>"""),
                    ui.input_select("region2", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy2", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph2"),
                ),
                ui.p(
                    ui.HTML("""<div style="text-align:left;"><h3>FDI Net Outflows Trends</h3></div>"""),
                    ui.input_select("region3", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy3", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph3"),
                ),
                ui.p(
                    ui.HTML("""<div style="text-align:left;"><h3>Top 5 Destinations of FDI (Net Outflow)</h3></div>"""),
                    ui.input_select("region4", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy4", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph4"),
                ),
                full_screen=False,
                fill=True,
            ),
            ui.card(
                ui.card_header(ui.HTML("""<div style="text-align:left;"><h2><b>FDI Stock</b></h2></div>""")),
                ui.p(
                    ui.HTML("""<div style="text-align:left;"><h3>FDI Instock Trends</h3></div>"""),
                    ui.input_select("region5", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy5", "Select an Economy", choices=[], multiple=True),
                    ui.input_checkbox("show_total_instock", "Show World Median Net Instock", value=False),
                    output_widget("fdi_graph5"),
                ),
                ui.p(
                    ui.HTML("""<div style="text-align:left;"><h3>Top 5 Sources of FDI (Instock)</h3></div>"""),
                    ui.input_select("region6", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy6", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph6"),
                ),
                ui.p(
                    ui.HTML("""<div style="text-align:left;"><h3>FDI Outstock Trends</h3></div>"""),
                    ui.input_select("region7", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy7", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph7"),
                ),
                ui.p(
                    ui.HTML("""<div style="text-align:left;"><h3>Top 5 Destinations of FDI (Outstock)</h3></div>"""),
                    ui.input_select("region8", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy8", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph8"),
                ),
            ),
        ),
        
        # Bilateral FDI Trends 
        ui.nav_panel(
            "Bilateral FDI Trends",
            ui.HTML("""<div style="text-align:center; margin-top:20px;">
                        <h2><b>Bilateral FDI Trends</b></h2>
                        <p style="font-size:16px;">Placeholder for Bilateral FDI Trends graphs and controls.</p>
                    </div>""")
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

        # --- Greenfield FDI (KEPT but HIDDEN) ---
        # give the tab a fixed value="greenfield" so CSS can target it
        ui.nav_panel(
            "Greenfield FDI",
            ui.HTML('<div style="text-align:center; margin-top:20px;"><h1><b>Greenfield FDI</b></h1></div>'),

        # ---- Inward Greenfield FDI ----
            ui.card(
                ui.card_header(ui.HTML('<div style="text-align:left;"><h2><b>Inward Greenfield FDI</b></h2></div>')),
                ui.p(
                    ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Inflows</h3></div>'),
                    ui.input_select("region10", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy10", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph10"),
                ),
                ui.p(
                    ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Inflows in Services within the Manufacturing Sector</h3></div>'),
                    ui.input_select("region11", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy11", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph11"),
                ),
                ui.p(
                    ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Inflows by Business Function in the Services and Manufacturing Sectors</h3></div>'),
                    ui.input_select("region12", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy12", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph12"),
                ),
                ui.p(
                    ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Inflows in High-Technology Activities in the Manufacturing Sector</h3></div>'),
                    ui.input_select("region13", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy13", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph13"),
                ),
            ),

        # ---- Outward Greenfield FDI ----
            ui.card(
                ui.card_header(ui.HTML('<div style="text-align:left;"><h2><b>Outward Greenfield FDI</b></h2></div>')),
                ui.p(
                    ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Outflows</h3></div>'),
                    ui.input_select("region14", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy14", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph14"),
                ),
                ui.p(
                    ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Outflows in Services within the Manufacturing Sector</h3></div>'),
                    ui.input_select("region15", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy15", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph15"),
                ),
                ui.p(
                    ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Outflows by Business Function in the Services and Manufacturing Sectors</h3></div>'),
                    ui.input_select("region16", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy16", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph16"),
                ),
                ui.p(
                    ui.HTML('<div style="text-align:left;"><h3>Greenfield FDI Outflows in High-Technology Activities</h3></div>'),
                    ui.input_select("region17", "Select Region", choices=sorted_regions, selected=sorted_regions[0]),
                    ui.input_select("economy17", "Select an Economy", choices=[], multiple=True),
                    output_widget("fdi_graph17"),
                ),
            ),

            # keep this value so the CSS rule can hide the tab
            value="greenfield",
            ),

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
)


# Define server    
def server(input: Inputs, output: Outputs, session: Session): 
    # ------------------------------
    # Multi-step Tutorial Modals
    # ------------------------------
    def tutorial_step1():
        return ui.modal(
            ui.HTML("""
                <h2>👋 Welcome to the IMAT Dashboard</h2>
                <p>This dashboard lets you explore Investment and Multinational Activity trends across economies, regions, and sectors.</p>
                <p>Click <b>Next</b> to continue the tutorial.</p>
            """),
            title="",
            easy_close=True,
            footer=ui.input_action_button("btn_next_step1", "Next", class_="btn-primary")
        )

    def tutorial_step2():
        return ui.modal(
            ui.TagList(
                ui.HTML("""
                    <h2>Step 2: Explore the Dashboard</h2>
                    <p>Here you will see how to navigate the dashboard and use filters.</p>
                """),
                # Screenshot goes in project folder `www/`
                ui.img(src="placeholder.png", style="max-width:100%; height:auto;")
            ),
            title="",
            easy_close=True,
            footer=ui.input_action_button("btn_next_step2", "Next", class_="btn-primary")
        )

    def tutorial_step3():
        return ui.modal(
            ui.HTML("""
                <h2>Step 3: Get Started</h2>
                <p>This is placeholder text for the final step of the tutorial.</p>
                <p>Click <b>Finish</b> to start exploring 🚀</p>
            """),
            title="",
            easy_close=True,
            footer=ui.input_action_button("btn_finish_tutorial", "Finish", class_="btn-success")
        )

    # Show Step 1 when app loads
    @reactive.effect
    def _show_step1():
        ui.modal_show(tutorial_step1())

    # Step 1 → Step 2
    @reactive.effect
    @reactive.event(input.btn_next_step1)
    def _go_to_step2():
        ui.modal_show(tutorial_step2())

    # Step 2 → Step 3
    @reactive.effect
    @reactive.event(input.btn_next_step2)
    def _go_to_step3():
        ui.modal_show(tutorial_step3())

    # Step 3 → Close tutorial
    @reactive.effect
    @reactive.event(input.btn_finish_tutorial)
    def _close_tutorial():
        ui.modal_remove()

    # ------------------------------
    # Sidebar button → tab mapping
    # ------------------------------
    @reactive.effect
    @reactive.event(input.btn_home, input.btn_overall, input.btn_components, input.btn_greenfield,
                    input.btn_policies, input.btn_incentives, input.btn_spillover, input.btn_data_sources,
                    input.btn_investment_climate)
    def _():
        # Create a mapping of buttons to tabs
        button_to_tab = {
            "btn_home": "tab1",
            "btn_overall": "tab2",
            "btn_components": "tab3",
            "btn_greenfield": "tab4",
            "btn_policies": "tab5",
            "btn_incentives": "tab6",
            "btn_spillover": "tab10",
            "btn_data_sources": "tab11",
            "btn_investment_climate": "tab12",
        }

        # Loop through the button mappings
        for btn_id, tab_id in button_to_tab.items():
            if getattr(input, btn_id)():
                ui.update_navs("hidden_tabs", selected=tab_id)
                break  # Ensure only one update happens per click

    @render_widget
    def map():
        selected_year = int(input.year_slider())
        return Map(center=(50.6252978589571, 0.34580993652344),zoom=3)

    ##################################
    # Graph 1 - FDI Net Inflows Trends
    @reactive.effect
    def update_economies1():
        selected_region = input.region1()
        filtered_economies = (
            graph1.loc[graph1["region_dest"] == selected_region, "economy_dest"]
            .dropna()
            .unique()
        )
        ui.update_select("economy1", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph1():
        selected_economies = input.economy1()
        show_total_inflow = input.show_total_inflow()
        region = input.region1()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        selected_economies = selected_economies[:5]
        region_data = graph1[graph1["region_dest"] == region]
        region_stats = region_data.groupby("year")["net_inflow"].agg(
            max_inflow="max",
            min_inflow="min",
            median_inflow="median"
        ).reset_index()
        economy_data = region_data[region_data["economy_dest"].isin(selected_economies)]

        # Plot using plotly express for the selected economies
        fig = px.line(
            economy_data,
            x="year",
            y="net_inflow",
            color="economy_dest",
            markers=True,
            labels={"economy_dest": "Destination"},
        )

        fig.update_layout(
            # title={
            #    'text': f"FDI Net Inflow Trends for {', '.join(selected_economies)}",
            #    'y': 0.9,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=22)  # adjust font size here
            # },
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        # Add a horizontal line at y=0
        fig.add_trace(
            go.Scatter(
                x=region_stats["year"],
                y=[0] * len(region_stats),
                mode="lines",
                line=dict(color="black", width=1, dash="solid"),
                name="Zero Line",
                showlegend=False
            )
        )

        # Add shaded area between max and min inflows for the selected region
        #fig.add_traces(
        #    go.Scatter(
        #        x=region_stats["year"],
        #        y=region_stats["max_inflow"],
        #        fill='tonexty',  # Fill the area from the max line to the next y-axis
        #        fillcolor="rgba(169, 169, 169, 0.3)",  # Light gray fill with transparency
        #        line=dict(color='rgba(169, 169, 169, 1)'),  # Solid gray line
        #        name="Max Inflow"
        #    )
        #)
        #fig.add_traces(
        #    go.Scatter(
        #        x=region_stats["year"],
        #        y=region_stats["min_inflow"],
        #        fill='tonexty',  # Fill the area from the min line to the next y-axis
        #        fillcolor="rgba(169, 169, 169, 0.3)",  # Light gray fill with transparency
        #        line=dict(color='rgba(169, 169, 169, 1)'),  # Solid gray line
        #        name="Min Inflow"
        #    )
        #)

        # Add median line for the region
        #fig.add_trace(
        #    go.Scatter(
        #        x=region_stats["year"],
        #        y=region_stats["median_inflow"],
        #        mode="lines",
        #        line=dict(color='gray', dash="dash", width=2),
        #        name="Regional Median Inflow"
        #    )
        #)

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph1["year"].unique()),
            title_text="Year"
        )

        fig.update_yaxes(title_text="Net Inflow (in USD Millions)")

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig
    
    ##################################
    # Graph 2 - Top 5 Sources of FDI (Net Inflow)
    @reactive.effect
    def update_economies2():
        selected_region = input.region2() 
        economies_in_region = sorted(graph2[graph2['region_dest'] == selected_region]['economy_dest'].unique())  # Sort alphabetically
        ui.update_select("economy2", choices=economies_in_region, selected=None)

    @render_widget
    def fdi_graph2():
        selected_region = input.region2() 
        selected_economy = input.economy2() 

        if not selected_economy:
            return px.pie(title="Select an economy to view top FDI sources")

        # Filter data for the selected economy, region, and only for 2022
        economy_data = graph2[
            (graph2['economy_dest'].isin(selected_economy)) & 
            (graph2['region_dest'] == selected_region) & 
            (graph2['year'] == 2014)
        ]

        if economy_data.empty:
            return px.pie(title=f"No data available for {', '.join(selected_economy)} in 2022")

        # Aggregate net_inflow by economy_source
        top_sources = (economy_data.groupby('economy_source')['net_inflow']
                    .sum()
                    .nlargest(5)  # Get the top 5
                    .reset_index())

        # Create a category for remaining sources (Others)
        remaining_sources = economy_data[~economy_data['economy_source'].isin(top_sources['economy_source'])]
        other_category = remaining_sources['net_inflow'].sum()

        # If there are remaining sources, add an 'Others' category
        if other_category > 0:
            others_df = pd.DataFrame({'economy_source': ['Others'], 'net_inflow': [other_category]})
            top_sources = pd.concat([top_sources, others_df], ignore_index=True)

        # Create pie chart with plotly
        fig = px.pie(
            top_sources,
            names="economy_source",
            values="net_inflow",
            #title=f"Top 5 FDI Sources for {', '.join(selected_economy)} (2022)",
            color_discrete_sequence=px.colors.qualitative.Dark24,  # Custom dark color palette
            hole=0.4  # Creates a donut-style pie chart
        )

        fig.update_traces(textinfo="label+percent", hoverinfo="label+value")

         # Center the title above the pie chart
        #fig.update_layout(
            # title={
            #    "text": f"Top 5 FDI Sources for {', '.join(selected_economy)} (2022)",
            #    'y': 0.975,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=22)  # adjust font size here
            # }
        #)

        return fig
    
    ##################################
    # Graph 3 - FDI Net Outflows Trends
    @reactive.effect
    def update_economies3():
        selected_region = input.region3()  # Use region1
        filtered_economies = (
            graph3.loc[graph3["region_source"] == selected_region, "economy_source"]
            .dropna()
            .unique()
        )
        ui.update_select("economy3", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph3():
        selected_economies = input.economy3()
        show_total_inflow = input.show_total_inflow()
        region = input.region3()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        selected_economies = selected_economies[:5]
        region_data = graph3[graph3["region_source"] == region]
        region_stats = region_data.groupby("year")["net_outflow"].agg(
            max_outflow="max",
            min_outflow="min",
            median_outflow="median"
        ).reset_index()
        economy_data = region_data[region_data["economy_source"].isin(selected_economies)]

        # Plot using plotly express for the selected economies
        fig = px.line(
            economy_data,
            x="year",
            y="net_outflow",
            color="economy_source",
            markers=True,
            labels={"economy_source": "Source"},
        )

        fig.update_layout(
            #title={
            #    'text': f"FDI Net Outflow Trends for {', '.join(selected_economies)}",
            #    'y': 0.9,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=22)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        # Add a horizontal line at y=0
        fig.add_trace(
            go.Scatter(
                x=region_stats["year"],
                y=[0] * len(region_stats),
                mode="lines",
                line=dict(color="black", width=1, dash="solid"),
                name="Zero Line",
                showlegend=False
            )
        )
        # Add median line for the region
        #fig.add_trace(
        #    go.Scatter(
        #        x=region_stats["year"],
        #        y=region_stats["median_outflow"],
        #        mode="lines",
        #        line=dict(color='gray', dash="dash", width=2),
        #        name="Regional Median Outflow"
        #    )
        #)

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph3["year"].unique()),
            title_text="Year"
        )

        fig.update_yaxes(title_text="Net Outflow (in USD Millions)")

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig
    
    ##################################################
    # Graph 4 - Top 5 Destinations of FDI (Net Outflow)
    @reactive.effect
    def update_economies4():
        selected_region = input.region4()
        economies_in_region = sorted(graph4[graph4['region_source'] == selected_region]['economy_source'].unique())
        ui.update_select("economy4", choices=economies_in_region, selected=None)

    @render_widget
    def fdi_graph4():
        selected_region = input.region4()
        selected_economy = input.economy4()

        if not selected_economy:
            return px.pie(title="Select an economy to view top FDI Destinations")

        # Filter data for the selected economy, region, and only for 2022
        economy_data = graph4[
            (graph4['economy_source'].isin(selected_economy)) & 
            (graph4['region_source'] == selected_region) & 
            (graph4['year'] == 2022)
        ]

        if economy_data.empty:
            return px.pie(title=f"No data available for {', '.join(selected_economy)} in 2022")

        # Aggregate net_inflow by economy_dest
        top_destinations = (economy_data.groupby('economy_dest')['net_outflow']
                    .sum()
                    .nlargest(5)  # Get the top 5
                    .reset_index())

        # Create a category for remaining destinations (Others)
        remaining_destinations = economy_data[~economy_data['economy_dest'].isin(top_destinations['economy_dest'])]
        other_category = remaining_destinations['net_outflow'].sum()

        # If there are remaining destinations, add an 'Others' category
        if other_category > 0:
            others_df = pd.DataFrame({'economy_dest': ['Others'], 'net_outflow': [other_category]})
            top_destinations = pd.concat([top_destinations, others_df], ignore_index=True)

        # Create pie chart with plotly
        fig = px.pie(
            top_destinations,
            names="economy_dest",
            values="net_outflow",
            # title=f"Top 5 FDI Destinations for {', '.join(selected_economy)} (2022)",
            color_discrete_sequence=px.colors.qualitative.Dark24,  # Custom dark color palette
            hole=0.4  # Creates a donut-style pie chart
        )

        fig.update_traces(textinfo="label+percent", hoverinfo="label+value")

         # Center the title above the pie chart
        #fig.update_layout(
            #title={
            #    "text": f"Top 5 FDI Destinations for {', '.join(selected_economy)} (2022)",
            #    'y': 0.975,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=22)  # adjust font size here
            #}
        #)

        return fig
    
    ##############################
    # Graph 5 - FDI Instock Trends
    @reactive.effect
    def update_economies5():
        selected_region = input.region5()  # Use region1
        filtered_economies = (
            graph5.loc[graph5["region_dest"] == selected_region, "economy_dest"]
            .dropna()
            .unique()
        )
        ui.update_select("economy5", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph5():
        selected_economies = input.economy5()
        region = input.region5()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        selected_economies = selected_economies[:5]
        region_data = graph5[graph5["region_dest"] == region]
        region_stats = region_data.groupby("year")["net_instock"].agg(
            max_instock="max",
            min_instock="min",
            median_instock="median"
        ).reset_index()
        economy_data = region_data[region_data["economy_dest"].isin(selected_economies)]

        # Plot using plotly express for the selected economies
        fig = px.line(
            economy_data,
            x="year",
            y="net_instock",
            color="economy_dest",
            markers=True,
            labels={"economy_dest": "Destination"},
        )

        fig.update_layout(
            #title={
            #    'text': f"Instock FDI Trends for {', '.join(selected_economies)}",
            #    'y': 0.9,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=22)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        # Add a horizontal line at y=0
        fig.add_trace(
            go.Scatter(
                x=region_stats["year"],
                y=[0] * len(region_stats),
                mode="lines",
                line=dict(color="black", width=1, dash="solid"),
                name="Zero Line",
                showlegend=False
            )
        )

        # Add median line for the region
        #fig.add_trace(
        #    go.Scatter(
        #        x=region_stats["year"],
        #        y=region_stats["median_instock"],
        #        mode="lines",
        #        line=dict(color='gray', dash="dash", width=2),
        #        name="Regional Median Instock"
        #    )
        #)

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph5["year"].unique()),
            title_text="Year"
        )

        fig.update_yaxes(title_text="Instock FDI (in USD Millions)")

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig

    ###################################
    # Graph 6 - Top 5 Stock FDI Sources
    @reactive.effect
    def update_economies6():
        selected_region = input.region6()
        economies_in_region = sorted(graph6[graph6['region_dest'] == selected_region]['economy_dest'].unique())
        ui.update_select("economy6", choices=economies_in_region, selected=None)

    @render_widget
    def fdi_graph6():
        selected_region = input.region6()
        selected_economy = input.economy6()

        if not selected_economy:
            return px.pie(title="Select an economy to view top FDI sources")

        # Filter data for the selected economy, region, and only for 2022
        economy_data = graph6[
            (graph6['economy_dest'].isin(selected_economy)) & 
            (graph6['region_dest'] == selected_region) & 
            (graph6['year'] == 2022)
        ]

        if economy_data.empty:
            return px.pie(title=f"No data available for {', '.join(selected_economy)} in 2022")

        # Aggregate net_instock by economy_source
        top_sources = (economy_data.groupby('economy_source')['net_instock']
                    .sum()
                    .nlargest(5)  # Get the top 5
                    .reset_index())

        # Create a category for remaining sources (Others)
        remaining_sources = economy_data[~economy_data['economy_source'].isin(top_sources['economy_source'])]
        other_category = remaining_sources['net_instock'].sum()

        # If there are remaining sources, add an 'Others' category
        if other_category > 0:
            others_df = pd.DataFrame({'economy_source': ['Others'], 'net_instock': [other_category]})
            top_sources = pd.concat([top_sources, others_df], ignore_index=True)

        # Create pie chart with plotly
        fig = px.pie(
            top_sources,
            names="economy_source",
            values="net_instock",
            color_discrete_sequence=px.colors.qualitative.Dark24,  # Custom dark color palette
            hole=0.4  # Creates a donut-style pie chart
        )

        fig.update_traces(textinfo="label+percent", hoverinfo="label+value")

         # Center the title above the pie chart
        #fig.update_layout(
            #title={
        #        "text": f"Top 5 Stock FDI Sources for {', '.join(selected_economy)} (2022)",
        #        'y': 0.975,  # vertical position
        #        'x': 0.5,  # horizontal center
        #        'xanchor': 'center',
        #        'yanchor': 'top',
        #        'font': dict(size=22)  # adjust font size here
            #}
        #)

        return fig

    ##################################
    # Graph 7 - FDI Outstock Trends
    @reactive.effect
    def update_economies7():
        selected_region = input.region7()
        filtered_economies = (
            graph7.loc[graph7["region_source"] == selected_region, "economy_source"]
            .dropna()
            .unique()
        )
        ui.update_select("economy7", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph7():
        selected_economies = input.economy7()
        region = input.region7()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        selected_economies = selected_economies[:5]
        region_data = graph7[graph7["region_source"] == region]
        region_stats = region_data.groupby("year")["net_outstock"].agg(
            max_outstock="max",
            min_outstock="min",
            median_outstock="median"
        ).reset_index()
        economy_data = region_data[region_data["economy_source"].isin(selected_economies)]

        # Plot using plotly express for the selected economies
        fig = px.line(
            economy_data,
            x="year",
            y="net_outstock",
            color="economy_source",
            markers=True,
            labels={"economy_source": "Source"},
        )

        fig.update_layout(
            #title={
            #    'text': f"Outstock FDI Trends for {', '.join(selected_economies)}",
            #    'y': 0.9,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=22)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        # Add a horizontal line at y=0
        fig.add_trace(
            go.Scatter(
                x=region_stats["year"],
                y=[0] * len(region_stats),
                mode="lines",
                line=dict(color="black", width=1, dash="solid"),
                name="Zero Line",
                showlegend=False
            )
        )
        # Add median line for the region
        #fig.add_trace(
        #    go.Scatter(
        #        x=region_stats["year"],
        #        y=region_stats["median_outstock"],
        #        mode="lines",
        #        line=dict(color='gray', dash="dash", width=2),
        #        name="Regional Median Outstock"
        #    )
        #)

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph7["year"].unique()),
            title_text="Year"
        )

        fig.update_yaxes(title_text="Outstock FDI (in USD Millions)")

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig
   
    ##################################################
    # Graph 8 - Top 5 Stock FDI Destinations
    @reactive.effect
    def update_economies8():
        selected_region = input.region8()
        economies_in_region = sorted(graph8[graph8['region_source'] == selected_region]['economy_source'].unique())
        ui.update_select("economy8", choices=economies_in_region, selected=None)

    @render_widget
    def fdi_graph8():
        selected_region = input.region8()
        selected_economy = input.economy8()

        if not selected_economy:
            return px.pie(title="Select an economy to view top FDI Destinations")

        # Filter data for the selected economy, region, and only for 2022
        economy_data = graph8[
            (graph8['economy_source'].isin(selected_economy)) & 
            (graph8['region_source'] == selected_region) & 
            (graph8['year'] == 2022)
        ]

        if economy_data.empty:
            return px.pie(title=f"No data available for {', '.join(selected_economy)} in 2022")

        # Aggregate net_inflow by economy_dest
        top_destinations = (economy_data.groupby('economy_dest')['net_outstock']
                    .sum()
                    .nlargest(5)  # Get the top 5
                    .reset_index())

        # Create a category for remaining destinations (Others)
        remaining_destinations = economy_data[~economy_data['economy_dest'].isin(top_destinations['economy_dest'])]
        other_category = remaining_destinations['net_outstock'].sum()

        # If there are remaining destinations, add an 'Others' category
        if other_category > 0:
            others_df = pd.DataFrame({'economy_dest': ['Others'], 'net_outstock': [other_category]})
            top_destinations = pd.concat([top_destinations, others_df], ignore_index=True)

        # Create pie chart with plotly
        fig = px.pie(
            top_destinations,
            names="economy_dest",
            values="net_outstock",
            color_discrete_sequence=px.colors.qualitative.Dark24,  # Custom dark color palette
            hole=0.4  # Creates a donut-style pie chart
        )

        fig.update_traces(textinfo="label+percent", hoverinfo="label+value")

         # Center the title above the pie chart
        #fig.update_layout(
            #title={
        #        "text": f"Top 5 Stock FDI Destinations for {', '.join(selected_economy)} (2022)",
        #        'y': 0.975,  # vertical position
        #        'x': 0.5,  # horizontal center
        #        'xanchor': 'center',
        #        'yanchor': 'top',
        #        'font': dict(size=22)  # adjust font size here
        #    }
        #)

        return fig

    ######################### ######################### ######################### #########################

    #########################
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
    
    ################################
    # Graph 10 - Greenfield FDI Inflows
    @reactive.effect
    def update_economies10():
        selected_region = input.region10()
        filtered_economies = (
            graph10.loc[graph10["region_dest"] == selected_region, "economy_dest"]
            .dropna()
            .unique()
        )
        ui.update_select("economy10", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget 
    def fdi_graph10():
        selected_economies = input.economy10()
        region = input.region10()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        selected_economies = selected_economies[:5]
        region_data = graph10[graph10["region_dest"] == region]
        region_stats = region_data.groupby("year")["capexusm"].agg(
            max_capexusm="max",
            min_capexusm="min",
            median_capexusm="median"
        ).reset_index()
        economy_data = region_data[region_data["economy_dest"].isin(selected_economies)]
            
        fig = px.line(
            economy_data,
            x="year",
            y="capexusm",
            color="economy_dest",
            markers=True,
            labels={"economy_dest": "Destination"},
        )      

        fig.update_layout(
            #title={
            #    'text': f"Greenfield FDI Inflows in {', '.join(selected_economies)}",
            #    'y': 0.9,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=22)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        # Add a horizontal line at y=0
        fig.add_trace(
            go.Scatter(
                x=region_stats["year"],
                y=[0] * len(region_stats),
                mode="lines",
                line=dict(color="black", width=1, dash="solid"),
                name="Zero Line",
                showlegend=False
            )
        )

        # Add median line for the region
        #fig.add_trace(
        #    go.Scatter(
        #        x=region_stats["year"],
        #        y=region_stats["median_capexusm"],
        #        mode="lines",
        #        line=dict(color='gray', dash="dash", width=2),
        #        name="Regional Median CapEx Flow"
        #    )
        #)

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph10["year"].unique()),
            title_text="Year"
        )

        fig.update_yaxes(title_text="CapEx Flow (in USD Millions)")

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig
    
    ####################################################################
    # Graph 11 - Grrenfield FDI Inflows in Services within Manufacturing
    @reactive.effect
    def update_economies11():
        selected_region = input.region11()
        filtered_economies = (
            graph11.loc[graph11["region_dest"] == selected_region, "economy_dest"]
            .dropna()
            .unique()
        )
        ui.update_select("economy11", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph11():
        selected_economies = input.economy11()
        region = input.region11()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        if isinstance(selected_economies, str):
            selected_economies = [selected_economies]

        filtered_df = graph11[graph11["economy_dest"].isin(selected_economies)]

        # Define your color gradient from light to dark blue
        serv_manu_colors = {
            "Services": "#4CAF50",         # Green
            "Manufacturing": "#9C27B0",  # Purple
            "Other Non-Services": "#FF9800", # Orange
        }

        fig = px.area(
            filtered_df,
            x="year",
            y="share_capex",  # Plot the share of capex
            color="serv_manu",
            color_discrete_map=serv_manu_colors,  # Different colors for Services, Manufacturing, and Other Non-Services
            labels={"share_capex": "Share of CapEx Flow",
                    "serv_manu": "Business Function",
                    "year": "Year"
            },
            hover_data=["serv_manu"],
            category_orders={
                "serv_manu": [
                    "Services", 
                    "Manufacturing", 
                    "Other Non-Services"
                ]
            },
        )

        fig.update_layout(
            #title={
            #    'text': f"Greenfield FDI Inflow in Services within the Manufacturing Sector in {', '.join(selected_economies)}",
            #    'y': 0.96,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=20)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph11["year"].unique()),  # Ensure correct years are displayed
            title_text="Year"
        )

        fig.update_yaxes(title_text="Share of CapEx Flow", range=[0, 1])  # Y-axis represents percentage

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig

   ##################################################################################################
   # Graph 12 - Greenfield FDI Inflows by Business Function in the Services and Manufacturing Sectors
    @reactive.effect
    def update_economies12():
        selected_region = input.region12()
        filtered_economies = (
            graph12.loc[graph12["region_dest"] == selected_region, "economy_dest"]
            .dropna()
            .unique()
        )
        ui.update_select("economy12", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph12():
        selected_economies = input.economy12()
        region = input.region12()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        if isinstance(selected_economies, str):
            selected_economies = [selected_economies]

        filtered_df = graph12[graph12["economy_dest"].isin(selected_economies)]

        fig = px.line(
            filtered_df,
            x="year",
            y="capexusm",
            color="businessfunction",
            markers=True,
            labels={"economy_dest": "Destination",
                    "businessfunction": "Business Function"},
        )

        fig.update_layout(
            #title={
            #    'text': f"Greenfield FDI Inflow by Business Function in Services and Manufacturing in {', '.join(selected_economies)}",
            #    'y': 0.96,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=20)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )
        
        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph12["year"].unique()),  # Ensure correct years are displayed
            title_text="Year"
        )

        fig.update_yaxes(title_text="CapEx Flow (in USD Millions)")

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig
    
    #################################################################
    # Graph 13 - Greenfield FDI Inflows in High-Technology Activities
    @reactive.effect
    def update_economies13():
        selected_region = input.region13()
        filtered_economies = (
            graph13.loc[graph13["region_dest"] == selected_region, "economy_dest"]
            .dropna()
            .unique()
        )
        ui.update_select("economy13", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph13():
        selected_economies = input.economy13()
        region = input.region13()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        if isinstance(selected_economies, str):
            selected_economies = [selected_economies]

        filtered_df = graph13[graph13["economy_dest"].isin(selected_economies)]

        # Define your color gradient from light to dark blue
        blue_gradient = {
            "Low-technology": "#cce5ff",         # Lightest blue
            "Medium-low-technology": "#99ccff",  # A bit darker
            "Medium-high-technology": "#3399ff", # Darker
            "High-technology": "#0066cc"         # Darkest blue
        }

        # Create the stacked bar chart
        fig = px.bar(
            filtered_df,
            x="year",
            y="percentage",  # The percentage share of capexUSm
            color="man_tech", 
            labels={
                "percentage": "Percentage of Total CapEx Flow",
                "man_tech": "Technology",
                "year": "Year"
            },
            hover_data=["man_tech"],  # Show relevant info on hover
            category_orders={
                "man_tech": [
                    "Low-technology", 
                    "Medium-low-technology", 
                    "Medium-high-technology", 
                    "High-technology"
                ]
            },  # Ensure consistent order for man_tech categories
            color_discrete_map=blue_gradient,  # Apply custom blue gradient
            barmode="stack",  # Stack the bars
        )

        fig.update_layout(
            #title={
            #    'text': f"Greenfield FDI Inflow in Manufacturing High-Tech Activities in {', '.join(selected_economies)}",
            #    'y': 0.96,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=20)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph13["year"].unique()),  # Ensure correct years are displayed
            title_text="Year"
        )

        fig.update_yaxes(title_text="Share of CapEx Flow", range=[0, 100])  # Y-axis is percentage, 0-100%

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig

    ################################
    # Graph 14 - Greenfield FDI Outflows
    @reactive.effect
    def update_economies14():
        selected_region = input.region14()
        filtered_economies = (
            graph14.loc[graph14["region_source"] == selected_region, "economy_source"]
            .dropna()
            .unique()
        )
        ui.update_select("economy14", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget 
    def fdi_graph14():
        selected_economies = input.economy14()
        region = input.region14()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        selected_economies = selected_economies[:5]
        region_data = graph14[graph14["region_source"] == region]
        region_stats = region_data.groupby("year")["capexusm"].agg(
            max_capexusm="max",
            min_capexusm="min",
            median_capexusm="median"
        ).reset_index()
        economy_data = region_data[region_data["economy_source"].isin(selected_economies)]
            
        fig = px.line(
            economy_data,
            x="year",
            y="capexusm",
            color="economy_source",
            markers=True,
            labels={"economy_source": "Source"},
        )      

        fig.update_layout(
            #title={
            #    'text': f"Greenfield FDI Outflows from {', '.join(selected_economies)}",
            #    'y': 0.9,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=22)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        # Add a horizontal line at y=0
        fig.add_trace(
            go.Scatter(
                x=region_stats["year"],
                y=[0] * len(region_stats),
                mode="lines",
                line=dict(color="black", width=1, dash="solid"),
                name="Zero Line",
                showlegend=False
            )
        )

        # Add median line for the region
        #fig.add_trace(
        #    go.Scatter(
        #        x=region_stats["year"],
        #        y=region_stats["median_capexusm"],
        #        mode="lines",
        #        line=dict(color='gray', dash="dash", width=2),
        #        name="Regional Median CapEx Flow"
        #    )
        #)

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph14["year"].unique()),
            title_text="Year"
        )

        fig.update_yaxes(title_text="CapEx Flow (in USD Millions)")

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig
    
    ####################################################################
    # Graph 15 - Greenfield FDI Outflows in Services within Manufacturing
    @reactive.effect
    def update_economies15():
        selected_region = input.region15()
        filtered_economies = (
            graph15.loc[graph15["region_source"] == selected_region, "economy_source"]
            .dropna()
            .unique()
        )
        ui.update_select("economy15", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph15():
        selected_economies = input.economy15()
        region = input.region15()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        if isinstance(selected_economies, str):
            selected_economies = [selected_economies]

        filtered_df = graph15[graph15["economy_source"].isin(selected_economies)]

        # Define your color gradient from light to dark blue
        serv_manu_colors = {
            "Services": "#4CAF50",         # Green
            "Manufacturing": "#9C27B0",  # Purple
            "Other Non-Services": "#FF9800", # Orange
        }

        fig = px.area(
            filtered_df,
            x="year",
            y="share_capex",  # Plot the share of capex
            color="serv_manu",
            color_discrete_map=serv_manu_colors,  # Different colors for Services, Manufacturing, and Other Non-Services
            labels={"share_capex": "Share of CapEx Flow",
                    "serv_manu": "Business Function",
                    "year": "Year"
            },
            hover_data=["serv_manu"],
            category_orders={
                "serv_manu": [
                    "Services", 
                    "Manufacturing", 
                    "Other Non-Services"
                ]
            },
        )

        fig.update_layout(
            #title={
            #    'text': f"Greenfield FDI Outflow in Services within the Manufacturing Sector from {', '.join(selected_economies)}",
            #    'y': 0.96,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=20)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph15["year"].unique()),  # Ensure correct years are displayed
            title_text="Year"
        )

        fig.update_yaxes(title_text="Share of CapEx Flow", range=[0, 1])  # Y-axis represents percentage

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig

    ##################################################################################################
    # Graph 16 - Greenfield FDI Outflows by Business Function in the Services and Manufacturing Sectors
    @reactive.effect
    def update_economies16():
        selected_region = input.region16()
        filtered_economies = (
            graph16.loc[graph16["region_source"] == selected_region, "economy_source"]
            .dropna()
            .unique()
        )
        ui.update_select("economy16", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph16():
        selected_economies = input.economy16()
        region = input.region16()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        if isinstance(selected_economies, str):
            selected_economies = [selected_economies]

        filtered_df = graph16[graph16["economy_source"].isin(selected_economies)]

        fig = px.line(
            filtered_df,
            x="year",
            y="capexusm",
            color="businessfunction",
            markers=True,
            labels={"economy_dest": "Destination",
                    "businessfunction": "Business Function"},
        )

        fig.update_layout(
            #title={
            #    'text': f"Greenfield FDI Outflow by Business Function in Services and Manufacturing from {', '.join(selected_economies)}",
            #    'y': 0.96,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=20)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )
        
        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph16["year"].unique()),  # Ensure correct years are displayed
            title_text="Year"
        )

        fig.update_yaxes(title_text="CapEx Flow (in USD Millions)")

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig

    #################################################################
    # Graph 17 - Greenfield FDI Outflows in High-Technology Activities
    @reactive.effect
    def update_economies17():
        selected_region = input.region17()
        filtered_economies = (
            graph17.loc[graph17["region_source"] == selected_region, "economy_source"]
            .dropna()
            .unique()
        )
        ui.update_select("economy17", choices=sorted(filtered_economies.tolist()), selected=None)

    @render_widget
    def fdi_graph17():
        selected_economies = input.economy17()
        region = input.region17()

        if not selected_economies:
            return px.line(title="Select at least one economy to view trends")
        
        if isinstance(selected_economies, str):
            selected_economies = [selected_economies]

        filtered_df = graph17[graph17["economy_source"].isin(selected_economies)]

        # Define your color gradient from light to dark blue
        blue_gradient = {
            "Low-technology": "#cce5ff",         # Lightest blue
            "Medium-low-technology": "#99ccff",  # A bit darker
            "Medium-high-technology": "#3399ff", # Darker
            "High-technology": "#0066cc"         # Darkest blue
        }

        # Create the stacked bar chart
        fig = px.bar(
            filtered_df,
            x="year",
            y="percentage",  # The percentage share of capexUSm
            color="man_tech", 
            labels={
                "percentage": "Percentage of Total CapEx Flow",
                "man_tech": "Technology",
                "year": "Year"
            },
            hover_data=["man_tech"],  # Show relevant info on hover
            category_orders={
                "man_tech": [
                    "Low-technology", 
                    "Medium-low-technology", 
                    "Medium-high-technology", 
                    "High-technology"
                ]
            },  # Ensure consistent order for man_tech categories
            color_discrete_map=blue_gradient,  # Apply custom blue gradient
            barmode="stack",  # Stack the bars
        )

        fig.update_layout(
            # title={
            #    'text': f"Greenfield FDI Outflow in Manufacturing High-Tech Activities from {', '.join(selected_economies)}",
            #    'y': 0.96,  # vertical position
            #    'x': 0.5,  # horizontal center
            #    'xanchor': 'center',
            #    'yanchor': 'top',
            #    'font': dict(size=20)  # adjust font size here
            #},
            legend=dict(
                orientation="h",  # Horizontal legend
                yanchor="top",  # Align legend to the top
                y=-0.35,  # Move legend below the graph
                xanchor="center",  # Align legend to the center
                x=0.5,  # Horizontal position of the legend
                tracegroupgap=5,  # Space between different legend items
                font=dict(size=12)  # Optional: change font size of the legend items
            )
        )

        fig.update_xaxes(
            tickmode="array",
            tickvals=sorted(graph17["year"].unique()),  # Ensure correct years are displayed
            title_text="Year"
        )

        fig.update_yaxes(title_text="Share of CapEx Flow", range=[0, 100])  # Y-axis is percentage, 0-100%

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
            paper_bgcolor="white",  # White card background
            margin=dict(l=40, r=40, t=50, b=40)  # Prevents stretching
        )

        return fig 

app = App(app_ui, server)