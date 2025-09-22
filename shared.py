from pathlib import Path
import pandas as pd
import geopandas as gpd
import numpy as np
import os


app_dir = Path(__file__).parent

#########################################################################
## 1. UNCTAD FDI (All data) + World Bank Official Boundaries Representative Points
world_path = app_dir / "data/world_map/fdi_panel.parquet"
fdi_panel = gpd.read_parquet(world_path)

#########################################################################
## 2. FDI Trends
fdi_trends = pd.read_csv(app_dir/'data/fdi_trends.csv', low_memory=False)

#########################################################################
## 3. FDI Bilateral Trends
bilateral_inflow = pd.read_csv(app_dir/'data/bilateral_inflow.csv', low_memory=False)
bilateral_outflow = pd.read_csv(app_dir/'data/bilateral_outflow.csv', low_memory=False)
bilateral_instock = pd.read_csv(app_dir/'data/bilateral_instock.csv', low_memory=False)
bilateral_outstock = pd.read_csv(app_dir/'data/bilateral_outstock.csv', low_memory=False)
bilateral_economies = pd.read_csv(app_dir/'data/economies_bilateral.csv', low_memory=False)
bilateral_economies = bilateral_economies["economy"].dropna().tolist()

### For IMF
imf = pd.read_csv(app_dir/'data/imf_fdi.csv', low_memory=False)
# imf.loc[imf['economy_dest'] == 'Singapore', 'region_dest'] = 'Middle East & North Africa'

### Regions (unique list)
regions = pd.read_csv(app_dir/'data/regions.csv', low_memory=False)
regions = regions.loc[regions['wb_region'] == 1]
sorted_regions = sorted(regions['region'].unique())

# #############################################################

# Graph 9 - FDI Inflows by Components
# Example of preparing graph9 from imf
graph9 = imf.melt(
    id_vars=['economy_dest', 'ecode_dest', 'inc_level_dest', 'region_dest', 'region_short_dest', 'year'],
    value_vars=['equity', 'debt_instruments', 'reinv_earn'],
    var_name='component',
    value_name='fdi_value' 
)

# #############################################################

# # Graph 10 - Greenfield FDI Inflows - with fDi Markets
# graph10 = fdi_markets[['year', 'economy_source', 'economy_dest', 'region_dest', 'capexusm']]
# graph10 = graph10.groupby(['year', 'economy_dest', 'region_dest'])['capexusm'].sum().reset_index()

# # Graph 11 - Greenfield FDI Inflows in Services within the Manufacturing Sector
# graph11 = fdi_markets[['year', 'economy_source', 'economy_dest', 'region_dest', 'capexusm', 'isic_section', 'businessfunction']].copy()
# graph11 = graph11[graph11['isic_section'] == 'C']
# services = [
#    "Business Services", "Customer Contact Centre", "Logistics, Distribution & Transportation",
#    "Maintenance & Servicing", "Recycling", "Retail", "Sales, Marketing & Support",
#    "Shared Services Centre", "Technical Support Centre"
# ]
# manufacturing = ["Manufacturing"]
# other = ["Extraction", "ICT & Internet Infrastructure", "Research & Development"]

# conditions = [
#    graph11['businessfunction'].isin(services),
#    graph11['businessfunction'].isin(manufacturing),
#    graph11['businessfunction'].isin(other)
# ]

# values = ['Services', 'Manufacturing', 'Other Non-Services']

# graph11['serv_manu'] = np.select(conditions, values, default='unknown')
# graph11 = graph11[graph11['serv_manu'] != 'unknown']

# graph11 = graph11.groupby(['year', 'economy_dest', 'region_dest', 'serv_manu'], as_index=False)['capexusm'].sum()
# graph11['total_capex'] = graph11.groupby(['year', 'economy_dest'])['capexusm'].transform('sum')
# graph11['share_capex'] = graph11['capexusm'] / graph11['total_capex']

# # Graph 12 - Greenfield FDI Inflows by Business Function in the Services and Manufacturing Sectors
# graph12 = fdi_markets[['year', 'economy_source', 'economy_dest', 'region_dest', 'capexusm', 'isic_section', 'businessfunction']].copy()
# graph12 = graph12[graph12['isic_section'].isin(['C', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])]
# graph12 = graph12.groupby(['year', 'economy_dest', 'region_dest','businessfunction'], as_index=False)['capexusm'].sum()

# # Graph 13 - Greenfield FDI Inflows in High-Technology Activities
# graph13 = fdi_markets[['year', 'economy_source', 'economy_dest', 'region_dest', 'capexusm', 'isic_section', 'man_tech']].copy()
# graph13 = graph13[graph13['isic_section'] == 'C']
# graph13 = graph13.groupby(['year', 'man_tech', 'economy_dest', 'region_dest'])['capexusm'].sum().reset_index()
# graph13['total_capex'] = graph13.groupby(['year', 'economy_dest'])['capexusm'].transform('sum')
# graph13['percentage'] = (graph13['capexusm'] / graph13['total_capex']) * 100

# # Graph 14 - Greenfield FDI Outflows
# graph14 = fdi_markets[['year', 'economy_source', 'economy_dest', 'region_source', 'capexusm']]
# graph14 = graph14.groupby(['year', 'economy_source', 'region_source'])['capexusm'].sum().reset_index()

# # Graph 15 - Greenfield FDI Outflows in Services within the Manufacturing Sector
# graph15 = fdi_markets[['year', 'economy_source', 'economy_dest', 'region_source', 'capexusm', 'isic_section', 'businessfunction']].copy()
# graph15 = graph15[graph15['isic_section'] == 'C']
# services = [
#    "Business Services", "Customer Contact Centre", "Logistics, Distribution & Transportation",
#    "Maintenance & Servicing", "Recycling", "Retail", "Sales, Marketing & Support",
#    "Shared Services Centre", "Technical Support Centre"
# ]
# manufacturing = ["Manufacturing"]
# other = ["Extraction", "ICT & Internet Infrastructure", "Research & Development"]

# conditions = [
#    graph15['businessfunction'].isin(services),
#    graph15['businessfunction'].isin(manufacturing),
#    graph15['businessfunction'].isin(other)
# ]

# values = ['Services', 'Manufacturing', 'Other Non-Services']

# graph15['serv_manu'] = np.select(conditions, values, default='unknown')
# graph15 = graph15[graph15['serv_manu'] != 'unknown']

# graph15 = graph15.groupby(['year', 'economy_source', 'region_source', 'serv_manu'], as_index=False)['capexusm'].sum()
# graph15['total_capex'] = graph15.groupby(['year', 'economy_source'])['capexusm'].transform('sum')
# graph15['share_capex'] = graph15['capexusm'] / graph15['total_capex']

# # Graph 16 - Greenfield FDI Outflows by Business Function in the Services and Manufacturing Sectors
# graph16 = fdi_markets[['year', 'economy_source', 'economy_dest', 'region_source', 'capexusm', 'isic_section', 'businessfunction']].copy()
# graph16 = graph16[graph16['isic_section'].isin(['C', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'])]
# graph16 = graph16.groupby(['year', 'economy_source', 'region_source','businessfunction'], as_index=False)['capexusm'].sum()

# # Graph 17 - Greenfield FDI Outflows in High-Technology Activities
# graph17 = fdi_markets[['year', 'economy_source', 'economy_dest', 'region_source', 'capexusm', 'isic_section', 'man_tech']].copy()
# graph17 = graph17[graph17['isic_section'] == 'C']
# graph17 = graph17.groupby(['year', 'man_tech', 'economy_source', 'region_source'])['capexusm'].sum().reset_index()
# graph17['total_capex'] = graph17.groupby(['year', 'economy_source'])['capexusm'].transform('sum')
# graph17['percentage'] = (graph17['capexusm'] / graph17['total_capex']) * 100