"""
about_panel.py
──────────────
Drop-in About panel for Invest.Data.

USAGE in app.py
───────────────
1. Add at the top of app.py:
       from about_panel import about_ui

2. Add as the last nav_panel inside ui.navset_tab(...):
       ui.navset_tab(
           ...
           about_ui(),
       )

NOTE: No server logic needed — this panel is UI only.
"""

from shiny import ui

# ─────────────────────────────────────────────
#  Colour tokens — match app.py exactly
# ─────────────────────────────────────────────
BLUE     = "#3f9dd4"
NAVY     = "#0a2d45"
MUTED    = "#555555"
BORDER   = "#d4e4ef"
BG_BLUE  = "#e8f4fb"
BG_LIGHT = "#f5f9fc"
LINK     = "#0072B2"


# ═════════════════════════════════════════════
#  about_ui()
# ═════════════════════════════════════════════
def about_ui():
    return ui.nav_panel(
        "About",
        ui.div(

            # ── Hero banner ───────────────────────────────────────────
            ui.div(
                ui.HTML(f"""
                    <div style="display:flex; align-items:center;
                                justify-content:space-between; flex-wrap:wrap; gap:12px;">
                        <div>
                            <h2 style="font-size:26px; font-weight:700; color:{NAVY};
                                       margin:0 0 4px 0; line-height:1.2;">
                                About <span style="color:{BLUE};">Invest.Data</span>
                            </h2>
                        </div>
                        <div style="display:flex; gap:10px; flex-wrap:wrap;">
                            <span style="font-size:11px; font-weight:600;
                                         letter-spacing:1.2px; text-transform:uppercase;
                                         color:{BLUE}; background:{BG_BLUE};
                                         padding:4px 12px; border-radius:20px;
                                         border:1px solid {BORDER};">
                                Version 1.3
                            </span>
                            <span style="font-size:11px; font-weight:600;
                                         letter-spacing:1.2px; text-transform:uppercase;
                                         color:{MUTED}; background:{BG_LIGHT};
                                         padding:4px 12px; border-radius:20px;
                                         border:1px solid {BORDER};">
                                🔒 WBG Internal
                            </span>
                        </div>
                    </div>
                """),
                style=(
                    f"padding:20px 28px;"
                    f"background:{BG_LIGHT};"
                    f"border:1px solid {BORDER};"
                    f"border-left:4px solid {BLUE};"
                    f"border-radius:8px;"
                    f"margin-bottom:20px;"
                    f"margin-top:20px;"
                ),
            ),

            # ── Accordion ─────────────────────────────────────────────
            ui.accordion(

                # 1. What is Invest.Data?
                ui.accordion_panel(
                    "1. What is Invest.Data?",
                    ui.HTML(f"""
                        <div style="font-size:14px; text-align:justify; line-height:1.65;
                                    color:{MUTED};">
                            <p>
                                <b style="color:#222;">Invest.Data</b> is the
                                <b style="color:#222;">World Bank Group's centralized interactive
                                tool</b> that enables staff to
                                <b style="color:#222;">access, visualize, and analyze</b>
                                consolidated data on global investments and related policy indicators.
                                Developed to support <b style="color:#222;">Task Team Leaders</b>
                                and <b style="color:#222;">WBG staff</b>, Invest.Data provides
                                <b style="color:#222;">quick, evidence-based insights</b> to
                                strengthen client engagement, enhance analytical work, and guide
                                investment-related policy discussions.
                            </p>
                            <div style="background:{BG_BLUE}; border:1px solid {BORDER};
                                        border-left:4px solid {BLUE}; border-radius:8px;
                                        padding:14px 18px; margin:14px 0;">
                                <p style="font-size:11px; font-weight:700; letter-spacing:1.5px;
                                           text-transform:uppercase; color:{BLUE};
                                           margin-bottom:6px;">
                                    🎯 Objective
                                </p>
                                <p style="font-size:14px; color:#222; margin:0; line-height:1.6;">
                                    To empower WBG staff with a one-stop data platform for
                                    <b>early diagnostics, benchmarking, and dialogue</b> on private
                                    investment trends and policies.
                                </p>
                            </div>
                            <p style="font-size:13px; color:{MUTED}; font-style:italic; margin:0;">
                                Current release: Version 1.3 (last updated March 11, 2026).
                                The online and interactive tool is for WBG internal use only but
                                may evolve with external sharing mechanisms over time, subject to
                                licensing and access conditions.
                            </p>
                        </div>
                    """)
                ),

                # 2. Why Use Invest.Data?
                ui.accordion_panel(
                    "2. Why Use Invest.Data?",
                    ui.HTML(f"""
                        <div style="font-size:14px; line-height:1.65; text-align:justify;
                                    color:{MUTED};">
                            <p style="color:#222;">
                                <b>Invest.Data</b> helps WBG teams move from data to dialogue ➡️
                                faster and smarter!
                            </p>
                            <p style="margin-bottom:8px; color:#222;"><b>Key Benefits:</b></p>
                            <ul style="list-style:none; padding-left:0; margin:0; display:flex;
                                       flex-direction:column; gap:8px;">
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    ⏱️ <b style="color:#222;">Save Time:</b>
                                    Consolidates multiple data sources into one easy-to-navigate
                                    platform.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🤝 <b style="color:#222;">Strengthen Engagement:</b>
                                    Enables data-backed conversations with clients and partners.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🌍 <b style="color:#222;">Country Strategies:</b>
                                    Provides macro-to-micro insights for SCDs, CPFs, and lending
                                    operations.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🛠️ <b style="color:#222;">Inform Project Design:</b>
                                    Identifies investment drivers, risks, and opportunities early
                                    in the engagement cycle.
                                </li>
                            </ul>
                        </div>
                    """)
                ),

                # 3. What Can You Find on Invest.Data?
                ui.accordion_panel(
                    "3. What Can You Find on Invest.Data?",
                    ui.HTML(f"""
                        <div style="font-size:14px; line-height:1.65; text-align:justify;
                                    color:{MUTED};">
                            <p>
                                <b style="color:#222;">Invest.Data</b> integrates trusted WBG and
                                external data repositories to offer a comprehensive
                                <b style="color:#222;">view of countries' investment landscapes.</b>
                            </p>
                            <p style="margin-bottom:8px; color:#222;"><b>Core Features:</b></p>
                            <ul style="list-style:none; padding-left:0; margin:0; display:flex;
                                       flex-direction:column; gap:8px;">
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    📊 <b style="color:#222;">Country Benchmarking:</b>
                                    Compare investment and policy metrics across peers or regions.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🌐 <b style="color:#222;">FDI Analysis:</b>
                                    Track foreign direct investment (FDI) flows and stocks by
                                    source, destination, and over time.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🏢 <b style="color:#222;">Firm-Level Insights:</b>
                                    Analyze company-level performance linked to FDI exposure,
                                    value chain participation, and the business environment.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    📈 <b style="color:#222;">Custom Visualizations:</b>
                                    Create, export, and download charts and tables tailored to
                                    specific analytical needs.
                                </li>
                            </ul>
                            <div style="margin-top:12px; padding:10px 14px;
                                        background:{BG_BLUE}; border:1px solid {BORDER};
                                        border-radius:6px; font-size:13px;">
                                🗺️ <b><a href="#appendix1"
                                    style="text-decoration:none; color:{LINK};">
                                    Appendix 1:</a></b> How to navigate Invest.Data.
                                &nbsp;|&nbsp;
                                📑 <b><a href="#appendix2"
                                    style="text-decoration:none; color:{LINK};">
                                    Appendix 2:</a></b> Description of indicators.
                            </div>
                        </div>
                    """)
                ),

                # 4. What Can You Not Find on Invest.Data?
                ui.accordion_panel(
                    "4. What Can You Not Find on Invest.Data?",
                    ui.HTML(f"""
                        <div style="font-size:14px; line-height:1.65; text-align:justify;
                                    color:{MUTED};">
                            <p>
                                While <b style="color:#222;">Invest.Data</b> offers a powerful
                                first-scan diagnostic, it does
                                <b style="color:#222;">NOT</b> include:
                            </p>
                            <ul style="list-style:none; padding-left:0; margin:0; display:flex;
                                       flex-direction:column; gap:8px;">
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    📚 <b style="color:#222;">Country case studies</b> or tailored
                                    <b style="color:#222;">reform recommendations</b>
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    💡 <b style="color:#222;">Proprietary</b> or
                                    <b style="color:#222;">confidential data</b> sources
                                </li>
                            </ul>
                            <p style="margin-top:12px; padding:10px 14px;
                                      background:{BG_BLUE}; border:1px solid {BORDER};
                                      border-left:4px solid {BLUE}; border-radius:6px;">
                                Use Invest.Data to
                                <b style="color:#222;">frame the conversation</b>, then build on it
                                through deeper diagnostics and technical analysis.
                            </p>
                        </div>
                    """)
                ),

                # 5. How Can Invest.Data Support Business Development?
                ui.accordion_panel(
                    "5. How Can Invest.Data Support Business Development?",
                    ui.HTML(f"""
                        <div style="font-size:14px; line-height:1.65; text-align:justify;
                                    color:{MUTED};">
                            <p>
                                <b style="color:#222;">Invest.Data</b> is a strategic tool for
                                <b style="color:#222;">business development</b> and
                                <b style="color:#222;">early engagement</b>.
                            </p>
                            <p style="color:#222;"><b>TTL Use Cases Include:</b></p>
                            <ul style="list-style:none; padding-left:0; margin:0; display:flex;
                                       flex-direction:column; gap:8px;">
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🚪 Identifying <b style="color:#222;">entry points</b> for
                                    investment policy reform in new engagements.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    📝 Supporting <i>initial</i>
                                    <b style="color:#222;">Investment Climate Assessments</b> and
                                    <b style="color:#222;">Country Private Sector Diagnostics
                                    (CPSDs)</b>.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    📑 Integrating investment metrics into
                                    <b style="color:#222;">Country Partnership Frameworks
                                    (CPFs)</b> and policy operations.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🎨 Preparing
                                    <b style="color:#222;">client presentations</b> using dynamic,
                                    exportable visuals.
                                </li>
                            </ul>
                        </div>
                    """)
                ),

                # 6. Need Deeper Analytical Support?
                ui.accordion_panel(
                    "6. Need Deeper Analytical Support?",
                    ui.HTML(f"""
                        <div style="font-size:14px; line-height:1.65; text-align:justify;
                                    color:{MUTED};">
                            <p>
                                For more tailored analysis that connects investment trends with
                                actionable reform agendas, contact the
                                <a href="https://ICHUB" target="_blank"
                                   style="text-decoration:none; color:{LINK};">
                                    <b>SME and Enterprise Development, Policy &amp; Regulations
                                    Unit (WKPTS)</b>
                                </a>.
                            </p>
                            <p style="color:#222;"><b>WKPTS Services Include:</b></p>
                            <ul style="list-style:none; padding-left:0; margin:0; display:flex;
                                       flex-direction:column; gap:8px;">
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🕵️ Comprehensive
                                    <b style="color:#222;">diagnostics</b> of investment
                                    constraints.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🛠️ <b style="color:#222;">Policy reform design</b> and
                                    implementation support.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🧑‍💼 <b style="color:#222;">Advisory services</b> for
                                    governments to foster private investment and competitiveness.
                                </li>
                            </ul>
                            <p style="margin-top:12px; padding:10px 14px;
                                      background:{BG_BLUE}; border:1px solid {BORDER};
                                      border-radius:6px; font-size:13px;">
                                📘 <b><a href="#appendix3"
                                    style="text-decoration:none; color:{LINK};">
                                    Appendix 3:</a></b> Summary of WKPTS Service Offerings.
                            </p>
                        </div>
                    """)
                ),

                # 7. Getting Started
                ui.accordion_panel(
                    "7. Getting Started",
                    ui.HTML(f"""
                        <div style="font-size:14px; line-height:1.65; color:{MUTED};">
                            <ul style="list-style:none; padding-left:0; margin:0; display:flex;
                                       flex-direction:column; gap:8px;">
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🔗 <b style="color:#222;">Access the Platform:</b>
                                    <a href="https://datanalytics-int.worldbank.org/IDD/"
                                       target="_blank"
                                       style="text-decoration:none; color:{LINK};">
                                        Invest.Data Interactive Tool
                                    </a>
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    🎓 <b style="color:#222;">Training &amp; Support:</b>
                                    Contact
                                    <a href="mailto:abrucal@worldbank.org"
                                       style="text-decoration:none; color:{LINK};">
                                        Arlan Brucal</a>,
                                    <a href="mailto:faguilarcisneros@worldbank.org"
                                       style="text-decoration:none; color:{LINK};">
                                        Francisco Aguilar Cisneros</a>, or
                                    <a href="mailto:knannichi@worldbank.org"
                                       style="text-decoration:none; color:{LINK};">
                                        Kanako Nannichi</a>.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    💬 <b style="color:#222;">Feedback:</b>
                                    <a href="https://forms.office.com/r/M1Nc8KLSUt"
                                       target="_blank"
                                       style="text-decoration:none; color:{LINK};">
                                        Share your user experience
                                    </a>
                                    to help us improve future releases.
                                </li>
                            </ul>
                        </div>
                    """)
                ),

                # Appendix 1
                ui.accordion_panel(
                    "Appendix 1: Quick Navigation Guide to the Invest.Data Interactive Tool",
                    ui.HTML(f"""
                        <div id="appendix1">
                            <table style="width:100%; border-collapse:collapse;
                                          font-size:14px; text-align:left;">
                                <thead style="background-color:{BG_BLUE};">
                                    <tr>
                                        <th colspan="2" style="padding:10px;
                                            border:1px solid {BORDER}; text-align:center;
                                            color:{NAVY};">Information Needed</th>
                                        <th style="padding:10px; border:1px solid {BORDER};
                                            text-align:center; color:{NAVY};">Tab to Use</th>
                                        <th style="padding:10px; border:1px solid {BORDER};
                                            text-align:center; color:{NAVY};">
                                            What You Will Find</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <td rowspan="4" style="padding:10px;
                                            border:1px solid {BORDER}; vertical-align:middle;
                                            background-color:{BG_LIGHT}; font-weight:bold;
                                            color:{NAVY};">Investments</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Country / Regional / Income Level trends</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            FDI Trends</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            <ul style="margin-left:18px; padding-left:0;
                                                       margin-bottom:0; line-height:1.4;">
                                                <li><b>Data:</b> Country, regional, income-level
                                                FDI inflow, outflow, inward stock, outward stock
                                                (2000–2024).</li>
                                                <li><i>Example:</i> How much FDI inflows did
                                                Botswana receive over the past few years?</li>
                                                <li><b>Source:</b> UNCTAD</li>
                                            </ul>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Benchmarked performance</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            FDI Trends</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            <ul style="margin-left:18px; padding-left:0;
                                                       margin-bottom:0; line-height:1.4;">
                                                <li><b>Data:</b> FDI inflow, outflow, inward/outward
                                                stock by year (2000–2024).</li>
                                                <li><i>Example:</i> How is Kenya performing compared
                                                to peers in Sub-Saharan Africa?</li>
                                                <li><b>Source:</b> UNCTAD</li>
                                            </ul>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Bilateral FDI flows and stocks</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Bilateral Trends</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            <ul style="margin-left:18px; padding-left:0;
                                                       margin-bottom:0; line-height:1.4;">
                                                <li><b>Data:</b> Bilateral FDI inflow and outflow,
                                                inward and outward stock (2003–2023).</li>
                                                <li><i>Example:</i> Which countries invest the most
                                                in Thailand in a specific year?</li>
                                                <li><b>Source:</b> UNCTAD</li>
                                            </ul>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Components by financial instruments</td>
                                        <td style="padding:8px; border:1px solid {BORDER};
                                            color:gray; font-style:italic;">
                                            FDI Components<br>Launching soon</td>
                                        <td style="padding:8px; border:1px solid {BORDER};
                                            color:gray; font-style:italic;">
                                            <ul style="margin-left:18px; padding-left:0;
                                                       margin-bottom:0; line-height:1.4;">
                                                <li>Data: FDI by debt instruments, equity, and/or
                                                reinvested earnings.</li>
                                                <li><i>Example:</i> How much did reinvested earnings
                                                make up total FDI in 2023 for El Salvador?</li>
                                                <li><b>Source:</b> IMF</li>
                                            </ul>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td rowspan="1" style="padding:10px;
                                            border:1px solid {BORDER}; vertical-align:middle;
                                            background-color:{BG_LIGHT}; font-weight:bold;
                                            color:{NAVY};">Policies</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Policies affecting investments</td>
                                        <td style="padding:8px; border:1px solid {BORDER};
                                            color:gray; font-style:italic;">
                                            Policies<br>Launching soon</td>
                                        <td style="padding:8px; border:1px solid {BORDER};
                                            color:gray; font-style:italic;">
                                            <ul style="margin-left:18px; padding-left:0;
                                                       margin-bottom:0; line-height:1.4;">
                                                <li>Data: Country FDI and selected policy metrics
                                                (2000–2024).</li>
                                                <li><i>Example:</i> How many days are needed to
                                                obtain an operating license in Serbia?</li>
                                                <li><b>Source:</b> UNCTAD</li>
                                            </ul>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td rowspan="2" style="padding:10px;
                                            border:1px solid {BORDER}; vertical-align:middle;
                                            background-color:{BG_LIGHT}; font-weight:bold;
                                            color:{NAVY};">Firms</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Firm-level performance in relation to broader business
                                            environment (2006–2025).</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Business Environment</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            <ul style="margin-left:18px; padding-left:0;
                                                       margin-bottom:0; line-height:1.4;">
                                                <li><b>Data:</b> Firm characteristics and business
                                                environment indicators.</li>
                                                <li><i>Example:</i> In India, does time spent on
                                                regulations influence annual employment growth?</li>
                                                <li><b>Source:</b> WBES / ICA 2.0 methodology.</li>
                                            </ul>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Firm-level performance in relation to FDI connectedness
                                            and exposure</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            Linkages</td>
                                        <td style="padding:8px; border:1px solid {BORDER};">
                                            <ul style="margin-left:18px; padding-left:0;
                                                       margin-bottom:0; line-height:1.4;">
                                                <li><b>Data:</b> Estimated productivity and
                                                employment premia from linkages to FDI/GVC
                                                (2006–2025).</li>
                                                <li><i>Example:</i> In Vietnam, how do firms with
                                                foreign-licensed technologies perform relative to
                                                other firms?</li>
                                                <li><b>Source:</b> WBES / ICA 2.0 methodology.</li>
                                            </ul>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    """)
                ),

                # Appendix 2
                ui.accordion_panel(
                    "Appendix 2: Description of Invest.Data Indicators",
                    ui.HTML(f"""
                        <div id="appendix2" style="font-size:14px; line-height:1.65;
                                                    text-align:justify; color:{MUTED};">
                            <p>
                                <b style="color:#222;">Foreign Direct Investment (FDI):</b>
                                A type of cross-border investment in which an enterprise in one
                                economy (the <i>direct investor</i>) invests in an enterprise in
                                another economy (the <i>direct investment enterprise</i>) to
                                establish a lasting interest (<i>OECD Benchmark Definition of
                                Foreign Direct Investment</i>). This is evidenced by direct or
                                indirect ownership of at least 10% of the voting power.
                                <i>Example:</i> A British firm acquiring a Kenyan power plant.
                            </p>
                            <ul style="list-style:none; padding-left:20px; margin-top:4px;
                                       margin-bottom:0; display:flex; flex-direction:column;
                                       gap:4px;">
                                <li>➡️ <b style="color:#222;">Flow:</b> The value of FDI during
                                a specific period (e.g., fresh water pouring into a tub).</li>
                                <li>➡️ <b style="color:#222;">Stock:</b> The total value of FDI
                                at a particular point in time (e.g., overall water level of a
                                tub).</li>
                                <li>➡️ <b style="color:#222;">Source:</b> The origin economy of
                                the investment.</li>
                                <li>➡️ <b style="color:#222;">Destination:</b> The economy
                                receiving the investment.</li>
                            </ul>
                            <p style="margin-top:12px;">
                                <b style="color:#222;">Firm Performance:</b> Captures how well
                                firms evolve in their productivity, employment, investment, and
                                innovation — influenced by their participation in global value
                                chains, access to foreign knowledge and capital, and the quality
                                of the domestic business environment.
                            </p>
                            <p>
                                <b style="color:#222;">Business Environment:</b> The set of
                                rules, infrastructure, and conditions that affect how easily
                                firms can operate.
                            </p>
                            <p>
                                <b style="color:#222;">Foreign Linkages:</b> Connections between
                                local and foreign firms or markets that help firms access new
                                knowledge, technology, and opportunities.
                            </p>
                        </div>
                    """)
                ),

                # Appendix 3
                ui.accordion_panel(
                    "Appendix 3: Key Offerings by the SME and Enterprise Development, Policy & Regulations Unit (WKPTS)",
                    ui.HTML(f"""
                        <div id="appendix3" style="font-size:14px; line-height:1.65;
                                                    text-align:justify; color:{MUTED};">
                            <ul style="list-style:none; padding-left:0; margin:0; display:flex;
                                       flex-direction:column; gap:10px;">
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    ➡️ <b><a href="https://worldbankgroup.sharepoint.com/sites/ICHUB/SitePages/PublishingPages/ICA%20Conceptual%20Frame-1739412083625.aspx"
                                        target="_blank"
                                        style="text-decoration:none; color:{LINK};">
                                        Investment Climate Assessments (ICA) 2.0</a>:</b>
                                    A toolkit that helps identify policy reforms that unlock the
                                    untapped potential of the private sector to increase aggregate
                                    productivity growth and private investment, and create more
                                    and better jobs.
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    ➡️ <b style="color:#222;">Investment policy and promotion
                                    related analytical and implementation activities</b> are
                                    offered at every stage of the investment project lifecycle.
                                    <ul style="list-style:none; padding-left:16px; margin-top:8px;
                                               display:flex; flex-direction:column; gap:6px;">
                                        <li>➡️ <b><a href="https://documents1.worldbank.org/curated/en/099040009302225750/pdf/P1755370c5dafe0440b2e40efcc6443b101.pdf"
                                            target="_blank"
                                            style="text-decoration:none; color:{LINK};">
                                            The FDI Competitiveness Sector Scans</a>:</b>
                                            Identifies sectors ready for proactive FDI promotion.
                                        </li>
                                        <li>➡️ <b><a href="https://worldbankgroup.sharepoint.com/sites/ICHUB/SitePages/PublishingPages/Investment%20Linkages-1711353125755.aspx"
                                            target="_blank"
                                            style="text-decoration:none; color:{LINK};">
                                            The FDI Linkages and Spillover Toolkit</a>:</b>
                                            Helps countries strengthen FDI linkages by assessing
                                            opportunities and reforming policy constraints.
                                        </li>
                                        <li>➡️ <b><a href="https://tab.worldbank.org/t/WBG/views/tax_incentives/CITIncentivesHeatmap"
                                            target="_blank"
                                            style="text-decoration:none; color:{LINK};">
                                            The Corporate Income Tax (CIT) Incentive
                                            Database</a>:</b>
                                            Supports monitoring of tax systems and facilitates
                                            CIT reform efforts.
                                        </li>
                                    </ul>
                                </li>
                                <li style="background:{BG_LIGHT}; border:1px solid {BORDER};
                                            border-radius:6px; padding:10px 14px;">
                                    ➡️ <b style="color:#222;">Investment Facilitation
                                    Implementation Summary Guide:</b> Supports implementation
                                    of the WTO's <i>Agreement on Investment Facilitation for
                                    Development (IFD Agreement)</i>.
                                </li>
                            </ul>
                            <p style="margin-top:14px; font-size:13px;">
                                For further information or coordination, please contact the
                                <a href="https://worldbankgroup.sharepoint.com/sites/ICHUB"
                                   target="_blank"
                                   style="text-decoration:none; color:{LINK};">
                                    SME and Enterprise Development, Policy &amp; Regulations
                                    Unit (WKPTS)
                                </a>.
                            </p>
                        </div>
                    """)
                ),

                open="1. What is Invest.Data?",
            ),

            style="margin-bottom:30px;",
        ),
    )