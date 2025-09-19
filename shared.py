from pathlib import Path
import pandas as pd
import geopandas as gpd
import numpy as np
import os


app_dir = Path(__file__).parent

### For fDi Markets
# fdi_markets = pd.read_csv(app_dir/'data/fdi_markets_03_25.csv', low_memory=False)

# fdi_markets.loc[fdi_markets['economy_dest'] == 'Singapore', 'region_dest'] = 'Middle East & North Africa'
# fdi_markets.loc[fdi_markets['economy_source'] == 'Singapore', 'region_source'] = 'Middle East & North Africa'

# ### For UNCTAD
# ## 1. Inflow
# un_inflow = pd.read_csv(app_dir/'data/un_inflow.csv', low_memory=False)
# # un_inflow.loc[un_inflow['economy_dest'] == 'Singapore', 'region_dest'] = 'Middle East & North Africa'
# # un_inflow.loc[un_inflow['economy_source'] == 'Singapore', 'region_source'] = 'Middle East & North Africa'

# ## 2. Outflow
# un_outflow = pd.read_csv(app_dir/'data/un_outflow.csv', low_memory=False)
# # un_outflow.loc[un_outflow['economy_dest'] == 'Singapore', 'region_dest'] = 'Middle East & North Africa'
# # un_outflow.loc[un_outflow['economy_source'] == 'Singapore', 'region_source'] = 'Middle East & North Africa'

# ## 3. Instock
# un_instock = pd.read_csv(app_dir/'data/un_instock.csv', low_memory=False)
# # un_instock.loc[un_instock['economy_dest'] == 'Singapore', 'region_dest'] = 'Middle East & North Africa'
# # un_instock.loc[un_instock['economy_source'] == 'Singapore', 'region_source'] = 'Middle East & North Africa'

# ## 4. Outstock
# un_outstock = pd.read_csv(app_dir/'data/un_outstock.csv', low_memory=False)
# # un_outstock.loc[un_outstock['economy_dest'] == 'Singapore', 'region_dest'] = 'Middle East & North Africa'
# # un_outstock.loc[un_outstock['economy_source'] == 'Singapore', 'region_source'] = 'Middle East & North Africa'


#########################################################################
## 1. UNCTAD FDI (All data) + World Bank Official Boundaries Representative Points
world_path = app_dir/"data/world map/fdi_panel.shp"
fdi_panel = gpd.read_file(world_path)

#########################################################################
## 2. FDI Trends
fdi_trends = pd.read_csv(app_dir/'data/fdi_trends.csv', low_memory=False)

### For IMF
imf = pd.read_csv(app_dir/'data/imf_fdi.csv', low_memory=False)
# imf.loc[imf['economy_dest'] == 'Singapore', 'region_dest'] = 'Middle East & North Africa'

### Regions (unique list)
regions = pd.read_csv(app_dir/'data/regions.csv', low_memory=False)
regions = regions.loc[regions['wb_region'] == 1]
sorted_regions = sorted(regions['region'].unique())


### Graphs

# # Graph 1 - FDI Net Inflows Trends - with UNCTAD
# graph1 = un_inflow.groupby(['year', 'economy_dest', 'region_dest', 'inc_level_dest'])['net_inflow'].sum().reset_index()
# # graph1 = graph1[graph1['inc_level_dest'] == 'Developing']

# # Graph 2 - Top 5 FDI Sources (Inflow) - with UNCTAD
# graph2 = un_inflow[['year', 'economy_source', 'economy_dest', 'region_dest', 'net_inflow']]

# # Graph 3 - FDI Net Outflows Trends - with UNCTAD
# graph3 = un_outflow.groupby(['year', 'economy_source', 'region_source', 'inc_level_source'])['net_outflow'].sum().reset_index()

# # Graph 4 - Top 5 FDI Destinations - with UNCTAD
# graph4 = un_outflow[['year', 'economy_dest', 'economy_source', 'region_source', 'net_outflow']]

# # Graph 5 - FDI Instock Trends - with UNCTAD
# graph5 = un_instock.groupby(['year', 'economy_dest', 'region_dest', 'inc_level_dest'])['net_instock'].sum().reset_index()

# # Graph 6 - Top 5 Stock FDI Sources - with UNCTAD
# graph6 = un_instock[['year', 'economy_source', 'economy_dest', 'region_dest', 'net_instock']]

# # Graph 7 - FDI Outstock Trends - with UNCTAD
# graph7 = un_outstock.groupby(['year', 'economy_source', 'region_source', 'inc_level_source'])['net_outstock'].sum().reset_index()

# # Graph 8 - Top 5 Stock FDI Destinations - with UNCTAD
# graph8 = un_outstock[['year', 'economy_dest', 'economy_source', 'region_source', 'net_outstock']]

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