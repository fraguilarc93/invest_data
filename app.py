# Shiny App for Investment and Policy Trends and Insights (Invest.Data)
from shiny import App, Inputs, Outputs, Session, reactive, ui

# Import panel UIs and servers
from landing_panel import landing_ui, landing_server
from highlights_panel import highlights_ui, highlights_server
from foreign_capital_panel import foreign_capital_ui, foreign_capital_server
from fdi_trends_panel import fdi_trends_ui, fdi_trends_server
from bilateral_trends_panel import bilateral_trends_ui, bilateral_trends_server
from business_environment_panel import business_environment_ui, business_environment_server
from linkages_panel import linkages_ui, linkages_server
from about_panel import about_ui

# Define the UI layout
app_ui = ui.page_fluid(
    # Title
    ui.tags.head(
        ui.tags.title("Invest.Data")
    ),

    # Visual Headline
    ui.div(
        ui.HTML("""
            <h2 style="
                font-size:26px; font-weight:700; color:#0a2d45;
                margin:0 0 4px 0; line-height:1.2;
            ">
                Invest<span style="color:#3f9dd4;">.Data</span>
            </h2>
            <p style="color:#555555; font-size:14px; margin:0; line-height:1.5;">
                Investment and Policy Trends and Insights
            </p>
        """),
        style=(
            "padding:18px 30px;"
            "background:#f5f9fc;"
            "border-bottom:1px solid #d4e4ef;"
            "margin-bottom:20px;"
        )
    ),

    # Top tabs instead of sidebar buttons
    ui.navset_tab(

        # Landing Site
        landing_ui(),

        # Investment Highlights
        highlights_ui(), 

        # Foreign Capital
        foreign_capital_ui(),

        # FDI Trends
        fdi_trends_ui(),
        
        # Bilateral Trends
        bilateral_trends_ui(), 

        # Business Environment
        business_environment_ui(),

        # Linkages
        linkages_ui(),

        # WB SME & Enterprise Development, Policy and Regulations Hub
        ui.nav_panel(
            "WKPTS Hub",
            ui.HTML("<p>Redirecting…</p>"),  # never really shown
            value="wb_hub",
        ),

        # About Panel
        about_ui(),

    id="main_tabs"
    ),

    # Add JavaScript redirect script
    ui.tags.style("""
    .equal-height-row {
        display: flex;
        align-items: stretch;
        gap: 20px;               /* spacing between cards */
    }
    .equal-height-row .bslib-card {
        flex: 1;                 /* make each card take equal width */
        display: flex;
        flex-direction: column;  /* ensure content flows vertically */
        justify-content: space-between;
    }
    """),

    ui.tags.style("""             
    /* ── Tab navigation ───────────────────────────── */
    .nav-tabs {
        border-bottom: 2px solid #d4e4ef;
    }
    .nav-tabs .nav-link {
        color: #3f9dd4;
        border: none;
        border-bottom: 3px solid transparent;
        border-radius: 0;
        font-size: 14px;
        font-weight: 500;
        padding: 10px 16px;
        transition: all 0.15s ease;
        background: transparent;
    }
    .nav-tabs .nav-link:hover {
        color: #0a2d45;
        background: #f5f9fc;
        border-bottom: 3px solid #d4e4ef;
    }
    .nav-tabs .nav-link.active {
        color: #0a2d45;
        font-weight: 700;
        background: white;
        border-bottom: 3px solid #3f9dd4;
        border-top: none;
        border-left: none;
        border-right: none;
    }
    """),

    ui.tags.style("""
        .js-plotly-plot .plot-container {
            background-color: white !important;
        }
    """),

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

    # For About Accordion Panel
    ui.tags.style("""
        .accordion-button {
            font-weight: bold;
        }
    """),

    ui.tags.script("""
    document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(e) {
        const link = e.target.closest('a[href^="#appendix"]');
        if (!link) return;

        e.preventDefault(); // Stop normal jump
        const targetId = link.getAttribute('href').substring(1);
        const targetEl = document.getElementById(targetId);
        if (!targetEl) return;

        // Find the accordion item that contains this appendix
        const accordionItem = targetEl.closest('.accordion-item');
        if (accordionItem) {
        const button = accordionItem.querySelector('.accordion-button');
        // If it's collapsed, open it
        if (button && button.classList.contains('collapsed')) {
            button.click();
        }
        }

        // Wait a bit for panel to expand, then scroll smoothly
        setTimeout(() => {
        targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 400);
    });
    });
    """),

    ui.tags.style("""
    .selectize-dropdown-content .option[data-value^='────────'] {
        color: gray !important;
        font-style: italic;
    }
    """),
)
###############################################################################################################################################################################################################################################
# Define server    
def server(input: Inputs, output: Outputs, session: Session):
    landing_server(input, output, session) 
    highlights_server(input, output, session)
    foreign_capital_server(input, output, session)
    fdi_trends_server(input, output, session)
    bilateral_trends_server(input, output, session)
    business_environment_server(input, output, session)
    linkages_server(input, output, session)

    ##################################
    ## 0. Tutorial Modal
    def tutorial_step():
        return ui.modal(
            ui.HTML("""
                <div style="text-align:center; margin-bottom:20px;">
                    <h2 style="font-size:26px; font-weight:700; color:#0a2d45; margin-bottom:4px;">
                        Welcome to Invest<span style="color:#3f9dd4;">.Data</span>
                    </h2>
                    <p style="font-size:13px; color:#555555; margin:0;">
                        Investment and Policy Trends and Insights
                    </p>
                </div>

                <div style="
                    background:#e8f4fb; border:1px solid #d4e4ef;
                    border-left:4px solid #3f9dd4; border-radius:8px;
                    padding:14px 18px; margin-bottom:16px;
                ">
                    <p style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                            text-transform:uppercase; color:#3f9dd4; margin-bottom:6px;">
                        📋 About this Tool
                    </p>
                    <p style="font-size:14px; color:#333333; margin:0; line-height:1.6;">
                        Invest.Data is a product of the <b>SME and Enterprise Development,
                        Policy &amp; Regulations Unit (WKPTS)</b>, providing a dynamic view of
                        investment and policy trends across economies, regions, and income levels.
                    </p>
                </div>

                <div style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:16px;">
                    <div style="flex:1; min-width:140px; background:#f5f9fc;
                                border:1px solid #d4e4ef; border-radius:6px; padding:10px 14px;">
                        <p style="font-size:11px; font-weight:700; color:#3f9dd4;
                                text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">
                            🧭 Navigate
                        </p>
                        <p style="font-size:12px; color:#555; margin:0;">
                            Use the tabs at the top to explore FDI, bilateral trends,
                            business environment, and more.
                        </p>
                    </div>
                    <div style="flex:1; min-width:140px; background:#f5f9fc;
                                border:1px solid #d4e4ef; border-radius:6px; padding:10px 14px;">
                        <p style="font-size:11px; font-weight:700; color:#3f9dd4;
                                text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">
                            🔍 Filter
                        </p>
                        <p style="font-size:12px; color:#555; margin:0;">
                            Apply sidebar filters to tailor the data to your economy
                            or region of interest.
                        </p>
                    </div>
                    <div style="flex:1; min-width:140px; background:#f5f9fc;
                                border:1px solid #d4e4ef; border-radius:6px; padding:10px 14px;">
                        <p style="font-size:11px; font-weight:700; color:#3f9dd4;
                                text-transform:uppercase; letter-spacing:1px; margin-bottom:4px;">
                            ℹ️ Learn
                        </p>
                        <p style="font-size:12px; color:#555; margin:0;">
                            Visit the <b>About</b> tab for background,
                            methodology, and data sources.
                        </p>
                    </div>
                </div>

                <p style="font-size:12px; color:#888; text-align:center; margin:0;">
                    🔒 <b>For World Bank Group internal use only.</b>
                    Do not distribute externally.
                </p>
            """),
            title="",
            easy_close=True,
            footer=ui.input_action_button("btn_close_tutorial", "Access Invest.Data", class_="btn-primary")
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
     
app = App(app_ui, server)