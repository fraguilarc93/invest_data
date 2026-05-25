"""
fdi_concentration_map.py
────────────────
Drop-in FDI Concentration Map panel for Invest.Data.

USAGE in app.py
───────────────
1. Add at the top of app.py:
       from fdi_concentration_map import fdi_map_ui, fdi_map_server

2. Add as a nav_panel inside ui.navset_tab(...):
       ui.navset_tab(
           ...
           fdi_map_ui(),
           ...
       )

3. Inside def server(input, output, session):
       fdi_map_server(input, output, session)
       # ... rest of your existing server code

DEPENDENCIES
────────────
- ipyleaflet
- ipywidgets
- shiny / shinywidgets
- shared.py  →  fdi_panel (DataFrame), fdi_legend_html (str)
"""

import json

from shiny import ui, render, Inputs, Outputs, Session
from shinywidgets import output_widget, render_widget
from ipyleaflet import Map, basemaps, GeoJSON, WidgetControl
from ipywidgets import Layout, HTML


# ═════════════════════════════════════════════
#  fdi_map_ui()
# ═════════════════════════════════════════════
def fdi_map_ui():
    return ui.nav_panel(
        "FDI Concentration Map",

        # ── About card ───────────────────────────────────────────────
        ui.div(
            ui.card(
                ui.card_header(
                    ui.HTML("<h6 style='text-align:left;'><b>About this Map</b></h6>")
                ),
                ui.HTML("""
                    <p style='font-size:14px; color:black; text-align:left;'>
                        This map provides an <b>overview of FDI inflow trends across economies
                        between 2000 and 2024</b>. Economies are shaded according to their
                        <b>percentile rank of annual net inflows</b>, allowing for intuitive
                        cross-economy comparisons. Use the year slider to explore changes over
                        time and click on any economy to view detailed FDI information.
                    </p>
                    <p style='font-size:13px; color:gray; text-align:justify;'>
                        FDI inflow data is sourced from the <b>United Nations Conference on
                        Trade and Development (UNCTAD)</b>. Additional economy-level information
                        is drawn from the <b>World Bank Enterprise Survey (WBES)</b>,
                        corresponding to the latest available survey year for each country.
                        More economy-level data will be integrated in future updates.
                    </p>
                """),
            ),
            style="margin-top:20px;",
        ),

        # ── Map + year slider ─────────────────────────────────────────
        ui.div(
            output_widget("map"),
            ui.div(
                ui.input_slider(
                    "year_slider",
                    "Select Year",
                    min=2000,
                    max=2024,
                    value=2024,
                    step=1,
                    sep="",
                ),
                id="year_overlay",
            ),
            id="home_map_wrap",
        ),
    )


# ═════════════════════════════════════════════
#  fdi_map_server()
# ═════════════════════════════════════════════
def fdi_map_server(input: Inputs, output: Outputs, session: Session):

    try:
        from shared import fdi_panel as _fdi_panel
    except ImportError:
        _fdi_panel = None

    try:
        from shared import fdi_legend_html as _fdi_legend_html
    except ImportError:
        _fdi_legend_html = "<p style='font-size:11px;'>Legend unavailable</p>"

    @output
    @render_widget
    def map():

        # Fallback: empty map if data not available
        if _fdi_panel is None:
            return Map(
                center=(0.0, 0.0),
                zoom=2,
                basemap=basemaps.CartoDB.Positron,
                layout=Layout(width="100%", height="695px"),
            )

        year = int(input.year_slider())

        df           = _fdi_panel.loc[_fdi_panel["year"] == year].copy().set_index("ecode_dest")
        geojson_data = json.loads(df.to_json())
        popup_html   = HTML()

        geo_layer = GeoJSON(
            data=geojson_data,
            style={
                "color":       "black",
                "weight":      0,
                "fillOpacity": 0.6,
            },
            style_callback=lambda feat: {
                "fillColor": feat["properties"].get("fillColor", "lightgray")
            },
            hover_style={
                "fillColor":   "yellow",
                "fillOpacity": 0.7,
            },
            popup=popup_html,
        )

        m = Map(
            center=(0.0, 0.0),
            zoom=2.75,
            basemap=basemaps.CartoDB.Positron,
            layout=Layout(width="100%", height="695px"),
        )
        m.add_layer(geo_layer)

        def update_popup(event, feature, **kwargs):
            popup_html.value = feature["properties"].get("popup", "Unavailable")

        geo_layer.on_click(update_popup)

        legend = HTML(_fdi_legend_html)
        m.add_control(WidgetControl(widget=legend, position="bottomright"))

        return m