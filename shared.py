from pathlib import Path
import pandas as pd
import geopandas as gpd
import numpy as np
import os

app_dir = Path(__file__).parent

#########################################################################
## 1. UNCTAD FDI (All data) + World Bank Official Boundaries Representative Points
world_path = app_dir / "data/fdi_panel.parquet"
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

#########################################################################
## 4. FDI Components
fdi_components = pd.read_csv(app_dir/'data/fdi_components.csv', low_memory=False)