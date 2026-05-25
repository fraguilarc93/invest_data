from pathlib import Path
import pandas as pd
import geopandas as gpd

app_dir = Path(__file__).parent

#########################################################################
# 1. H1 2026: Where Capital is Headed...
#########################################################################
df_fig1_2026_1 = pd.read_csv(app_dir/'data/2026_1_Fig1.csv', low_memory=False)
df_fig2a_2026_1 = pd.read_csv(app_dir/'data/2026_1_Fig2a.csv', low_memory=False)
df_fig2b_2026_1 = pd.read_csv(app_dir/'data/2026_1_Fig2b.csv', low_memory=False)
df_fig3a_2026_1 = pd.read_csv(app_dir/'data/2026_1_Fig3a.csv', low_memory=False)
df_fig3b_2026_1 = pd.read_csv(app_dir/'data/2026_1_Fig3b.csv', low_memory=False)

#########################################################################
# 1. Foreign Capital Inflows
#########################################################################
foreign_capital_df = pd.read_csv(app_dir / 'data/foreign_capital.csv', low_memory=False)
 
# ── World ────────────────────────────────────────────────────────────
world_list_capital = ["World"]
 
# ── Regions ──────────────────────────────────────────────────────────
regions_list_capital = foreign_capital_df["region"].dropna().unique().tolist()
 
if "European Union" in foreign_capital_df["economy"].unique():
    regions_list_capital.append("European Union")
 
regions_list_capital = sorted(set(regions_list_capital))
 
# ── Income groups ─────────────────────────────────────────────────────
income_order = ["Low income", "Lower middle income", "Upper middle income", "High income"]
income_list_capital = [
    i for i in income_order
    if i in foreign_capital_df["incomegroup"].unique()
]
 
# ── Economies grouped by region (full name), alphabetical within region
_cap_econ_df = (
    foreign_capital_df[
        foreign_capital_df["region_short"].notna() &
        foreign_capital_df["incomegroup_short"].notna()
    ][["economy", "region"]]
    .drop_duplicates()
)
_cap_econ_df = _cap_econ_df[
    ~_cap_econ_df["economy"].isin(
        world_list_capital + regions_list_capital + income_list_capital
    )
].sort_values(["region", "economy"])
 
# ── Final ordered list ────────────────────────────────────────────────
ordered_economies_capital = world_list_capital + ["— Regions —"]
 
for region in regions_list_capital:
    ordered_economies_capital.append(f"\u00a0\u00a0\u00a0\u00a0{region}")
 
ordered_economies_capital += ["— Income Levels —"]
 
for income in income_list_capital:
    ordered_economies_capital.append(f"\u00a0\u00a0\u00a0\u00a0{income}")
 
ordered_economies_capital += ["— Economies —"]
 
for region_name, group in _cap_econ_df.groupby("region", sort=True):
    ordered_economies_capital.append(f"\u2500\u2500 {region_name} \u2500\u2500")
    for econ in group["economy"].tolist():
        ordered_economies_capital.append(f"\u00a0\u00a0\u00a0\u00a0{econ}")

#########################################################################
## 2. FDI Concentration Map
world_path = app_dir / "data/fdi_panel.parquet"
fdi_panel = gpd.read_parquet(world_path)

with open(app_dir / "data/fdi_legend.html", "r") as f:
    fdi_legend_html = f.read()

#########################################################################
# 3. FDI Trends
#########################################################################
fdi_trends = pd.read_csv(app_dir / 'data/fdi_trends.csv', low_memory=False)
fdi_iqr    = pd.read_csv(app_dir / 'data/fdi_iqr.csv',    low_memory=False)
 
# ── World ─────────────────────────────────────────────────────────────
world_list = ["World"]
 
# ── Regions ───────────────────────────────────────────────────────────
regions_list = fdi_trends["region"].dropna().unique().tolist()
 
if "European Union" in fdi_trends["economy"].unique():
    regions_list.append("European Union")
 
regions_list = sorted(set(regions_list))
 
# ── Income groups ─────────────────────────────────────────────────────
income_order = ["Low income", "Lower middle income", "Upper middle income", "High income"]
income_list  = [i for i in income_order if i in fdi_trends["incomegroup"].unique()]
 
# ── Economies grouped by region (full name), alphabetical within region
_fdi_econ_df = (
    fdi_trends[
        fdi_trends["region_short"].notna() &
        fdi_trends["incomegroup_short"].notna()
    ][["economy", "region"]]
    .drop_duplicates()
)
_fdi_econ_df = _fdi_econ_df[
    ~_fdi_econ_df["economy"].isin(
        world_list + regions_list + income_list
    )
].sort_values(["region", "economy"])
 
# ── Final ordered list ────────────────────────────────────────────────
ordered_economies = world_list + ["— Regions —"]
 
for region in regions_list:
    ordered_economies.append(f"\u00a0\u00a0\u00a0\u00a0{region}")
 
ordered_economies += ["— Income Levels —"]
 
for income in income_list:
    ordered_economies.append(f"\u00a0\u00a0\u00a0\u00a0{income}")
 
ordered_economies += ["— Economies —"]
 
for region_name, group in _fdi_econ_df.groupby("region", sort=True):
    ordered_economies.append(f"\u2500\u2500 {region_name} \u2500\u2500")
    for econ in group["economy"].tolist():
        ordered_economies.append(f"\u00a0\u00a0\u00a0\u00a0{econ}")

#########################################################################
## 4. FDI Bilateral Trends
bilateral_inflow = pd.read_csv(app_dir/'data/bilateral_inflow.csv', low_memory=False)
bilateral_outflow = pd.read_csv(app_dir/'data/bilateral_outflow.csv', low_memory=False)
bilateral_instock = pd.read_csv(app_dir/'data/bilateral_instock.csv', low_memory=False)
bilateral_outstock = pd.read_csv(app_dir/'data/bilateral_outstock.csv', low_memory=False)
bilateral_economies = pd.read_csv(app_dir/'data/economies_bilateral.csv', low_memory=False)


#########################################################################
## 5. Business Environment
business_environment_averages = pd.read_csv(app_dir/'data/business_environment_averages.csv', low_memory=False)

#########################################################################
## 6. Linkages
linkages_averages = pd.read_csv(app_dir/'data/linkages_averages.csv', low_memory=False)