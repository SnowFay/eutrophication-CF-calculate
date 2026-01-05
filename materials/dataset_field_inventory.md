# HydroSHEDS / HydroATLAS dataset inventory

Generated 2025-11-21 06:46 UTC

This file is auto-created by `scripts/inspect_hydro_datasets.py`.

## HydroRIVERS v1.0 – Asia subset

Data source: `/Users/snowfay/CF_calculate/data/HydroSHEDS data/HydroRIVERS_v10_as_shp/HydroRIVERS_v10_as_shp/HydroRIVERS_v10_as.shp`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/HydroRIVERS_v10_as_shp/HydroRIVERS_TechDoc_v10.pdf`

### Layer: HydroRIVERS_v10_as

- Driver: `ESRI Shapefile`
- Geometry type: `LineString`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 1428959

| Field | Type | Meaning |
| --- | --- | --- |
| `HYRIV_ID` | int32:9 | Permanent HydroRIVERS/HydroATLAS river reach identifier. |
| `NEXT_DOWN` | int32:9 | HYRIV_ID of the immediate downstream reach (0 = ocean outlet). |
| `MAIN_RIV` | int32:9 | Identifier for the main river stem that the reach belongs to. |
| `LENGTH_KM` | float:7.2 | Reach length in kilometers (planform). |
| `DIST_DN_KM` | float:7.1 | Distance from the reach outlet to the ocean (km). |
| `DIST_UP_KM` | float:7.1 | Distance from headwaters to the reach inlet (km). |
| `CATCH_SKM` | float:7.2 | Surface area (km²) of the local catchment draining directly to the reach. |
| `UPLAND_SKM` | float:10.1 | Surface area (km²) of the entire upstream drainage area. |
| `ENDORHEIC` | int32:4 | 1 if the reach drains to an inland sink, 0 otherwise. |
| `DIS_AV_CMS` | float:10.3 | Long-term average discharge in cubic meters per second at the reach outlet. |
| `ORD_STRA` | int32:4 | Strahler stream order of the reach. |
| `ORD_CLAS` | int32:4 | HydroSHEDS level-based stream order. |
| `ORD_FLOW` | int32:4 | Shreve (flow-based) stream order. |
| `HYBAS_L12` | int:11 | Identifier of the intersecting HydroBASINS level-12 polygon. |


## HydroLAKES v1.0 – polygons

Data source: `/Users/snowfay/CF_calculate/data/HydroSHEDS data/HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10_shp/HydroLAKES_polys_v10.shp`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/HydroLAKES_polys_v10_shp/HydroLAKES_TechDoc_v10.pdf`

### Layer: HydroLAKES_polys_v10

- Driver: `ESRI Shapefile`
- Geometry type: `Polygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 1427688

| Field | Type | Meaning |
| --- | --- | --- |
| `Hylak_id` | int32:9 | Primary HydroLAKES identifier. |
| `Lake_name` | str:40 | Lake/reservoir name (if assigned). |
| `Country` | str:35 | Primary ISO-3 country code (may be multi-valued). |
| `Continent` | str:15 | Continent tag used by HydroLAKES. |
| `Poly_src` | str:10 | Source dataset for the polygon geometry. |
| `Lake_type` | int32:4 | HydroLAKES classification (natural lake, reservoir, etc.). |
| `Grand_id` | int32:4 | GRanD database identifier (if the lake is a registered reservoir). |
| `Lake_area` | float:13.2 | Open water surface area (km²). |
| `Shore_len` | float:13.2 | Shoreline length (km). |
| `Shore_dev` | float:7.2 | Shoreline development index (dimensionless). |
| `Vol_total` | float:13.2 | Total lake/reservoir volume (km³). |
| `Vol_res` | float:13.2 | Managed reservoir volume component (km³). |
| `Vol_src` | int32:4 | Source authority for the volume estimate. |
| `Depth_avg` | float:7.1 | Mean depth (m). |
| `Dis_avg` | float:13.3 | Estimated mean annual outflow/discharge (m³/s). |
| `Res_time` | float:13.1 | Mean residence time (years). |
| `Elevation` | int32:4 | Lake surface elevation (m a.s.l.). |
| `Slope_100` | float:7.2 | Mean 100 m buffer slope (degrees). |
| `Wshd_area` | float:13.1 | Total watershed area feeding the lake (km²). |
| `Pour_long` | float:13.6 | Longitude of the modeled pour point (degrees). |
| `Pour_lat` | float:13.6 | Latitude of the modeled pour point (degrees). |


## HydroLAKES v1.0 – centroids

Data source: `/Users/snowfay/CF_calculate/data/HydroSHEDS data/HydroLAKES_points_v10_shp/HydroLAKES_points_v10_shp/HydroLAKES_points_v10.shp`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/HydroLAKES_points_v10_shp/HydroLAKES_TechDoc_v10.pdf`

### Layer: HydroLAKES_points_v10

- Driver: `ESRI Shapefile`
- Geometry type: `Point`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 1427688

| Field | Type | Meaning |
| --- | --- | --- |
| `Hylak_id` | int32:9 | Primary HydroLAKES identifier. |
| `Lake_name` | str:40 | Lake/reservoir name (if assigned). |
| `Country` | str:35 | Primary ISO-3 country code (may be multi-valued). |
| `Continent` | str:15 | Continent tag used by HydroLAKES. |
| `Poly_src` | str:10 | Source dataset for the polygon geometry. |
| `Lake_type` | int32:4 | HydroLAKES classification (natural lake, reservoir, etc.). |
| `Grand_id` | int32:4 | GRanD database identifier (if the lake is a registered reservoir). |
| `Lake_area` | float:13.2 | Open water surface area (km²). |
| `Shore_len` | float:13.2 | Shoreline length (km). |
| `Shore_dev` | float:7.2 | Shoreline development index (dimensionless). |
| `Vol_total` | float:13.2 | Total lake/reservoir volume (km³). |
| `Vol_res` | float:13.2 | Managed reservoir volume component (km³). |
| `Vol_src` | int32:4 | Source authority for the volume estimate. |
| `Depth_avg` | float:7.1 | Mean depth (m). |
| `Dis_avg` | float:13.3 | Estimated mean annual outflow/discharge (m³/s). |
| `Res_time` | float:13.1 | Mean residence time (years). |
| `Elevation` | int32:4 | Lake surface elevation (m a.s.l.). |
| `Slope_100` | float:7.2 | Mean 100 m buffer slope (degrees). |
| `Wshd_area` | float:13.1 | Total watershed area feeding the lake (km²). |
| `Pour_long` | float:13.6 | Longitude of the modeled pour point (degrees). |
| `Pour_lat` | float:13.6 | Latitude of the modeled pour point (degrees). |


## HydroBASINS level 10 lake basins

Data source: `/Users/snowfay/CF_calculate/data/HydroSHEDS data/hybas_lake_as_lev10_v1c/hybas_lake_as_lev10_v1c.shp`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/hybas_lake_as_lev10_v1c/HydroBASINS_TechDoc_v1c.pdf`

### Layer: hybas_lake_as_lev10_v1c

- Driver: `ESRI Shapefile`
- Geometry type: `Polygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 160518

| Field | Type | Meaning |
| --- | --- | --- |
| `HYBAS_ID` | int:11 | Permanent HydroBASINS polygon identifier at the dataset's level. |
| `NEXT_DOWN` | int:11 | HYRIV_ID of the immediate downstream reach (0 = ocean outlet). |
| `NEXT_SINK` | int:11 | HYBAS_ID of the downstream sink (endorheic target). |
| `MAIN_BAS` | int:11 | Identifier of the encompassing main basin (Pfafstetter coding). |
| `DIST_SINK` | float:10.1 | Flow distance (km) from the basin outlet to its terminal sink. |
| `DIST_MAIN` | float:10.1 | Flow distance (km) from the basin outlet to the main river mouth. |
| `SUB_AREA` | float:10.1 | Area (km²) of the polygon between nested HydroBASINS levels. |
| `UP_AREA` | float:10.1 | Total upstream area (km²) draining through the polygon outlet. |
| `PFAF_ID` | int:11 | Pfafstetter hierarchical basin code. |
| `SIDE` | str:6 | Pfafstetter side code (left/right). |
| `LAKE` | int32:6 | HydroLAKES (Hylak_id) identifier for lake polygons matched to the basin. |
| `ENDO` | int32:6 | See accompanying technical documentation for semantic details. |
| `COAST` | int32:6 | 1 if the basin drains directly to the ocean. |
| `ORDER` | int32:6 | Topological order/index used for sorting HydroBASINS polygons. |
| `SORT` | int:11 | Pre-calculated sort key for topological traversals. |


## HydroBASINS level 10 pour points

Data source: `/Users/snowfay/CF_calculate/data/HydroSHEDS data/hybas_pour_lev10_v1_shp/hybas_pour_lev10_v1.shp`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/hybas_pour_lev10_v1_shp/HydroBASINS_PourPoint_TechDoc_v1.pdf`

### Layer: hybas_pour_lev10_v1

- Driver: `ESRI Shapefile`
- Geometry type: `Point`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 5182169

| Field | Type | Meaning |
| --- | --- | --- |
| `HYBAS_ID` | float:19.11 | Permanent HydroBASINS polygon identifier at the dataset's level. |


## RiverATLAS v1.0 (global reaches)

Data source: `/Users/snowfay/CF_calculate/data/HydroSHEDS data/RiverATLAS_Data_v10.gdb/RiverATLAS_v10.gdb`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/RiverATLAS_Data_v10.gdb/RiverATLAS_Catalog_v10.pdf`
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/RiverATLAS_Data_v10.gdb/HydroATLAS_TechDoc_v10.pdf`

### Layer: RiverATLAS_v10

- Driver: `OpenFileGDB`
- Geometry type: `MultiLineString`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 8477883

| Field | Type | Meaning |
| --- | --- | --- |
| `HYRIV_ID` | int32 | Permanent HydroRIVERS/HydroATLAS river reach identifier. |
| `NEXT_DOWN` | int32 | HYRIV_ID of the immediate downstream reach (0 = ocean outlet). |
| `MAIN_RIV` | int32 | Identifier for the main river stem that the reach belongs to. |
| `ENDORHEIC` | int16 | 1 if the reach drains to an inland sink, 0 otherwise. |
| `ORD_STRA` | int16 | Strahler stream order of the reach. |
| `ORD_CLAS` | int16 | HydroSHEDS level-based stream order. |
| `ORD_FLOW` | int16 | Shreve (flow-based) stream order. |
| `HYBAS_L12` | float | Identifier of the intersecting HydroBASINS level-12 polygon. |
| `run_mm_cyr` | int16 | Runoff depth (mm/yr) computed from WaterGAP 2.2 climatology for HydroATLAS v1.0 (Table 4).; units: mm; local catchment aggregate; long-term annual mean |
| `inu_pc_cmn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; local catchment aggregate; minimum of long-term monthly climatology |
| `inu_pc_umn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; minimum of long-term monthly climatology |
| `inu_pc_cmx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; local catchment aggregate; maximum of long-term monthly climatology |
| `inu_pc_umx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; maximum of long-term monthly climatology |
| `inu_pc_clt` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; local catchment aggregate; latest available snapshot (~2010 baseline) |
| `inu_pc_ult` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; latest available snapshot (~2010 baseline) |
| `lka_pc_cse` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `lka_pc_use` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `lkv_mc_usu` | int32 | Combined natural lake and reservoir volume (10^6 m³) sourced from HydroLAKES/GRanD per HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `rev_mc_usu` | int32 | Managed reservoir storage volume (10^6 m³) derived from GRanD v1.3, summarized as in HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `dor_pc_pva` | int16 | Degree of regulation (%) = upstream reservoir storage / mean annual discharge (Lehner et al., 2014); HydroATLAS v1.0 Table 5.; units: percent of the referenced area; pour-point statistic (network outlet) |
| `gwt_cm_cav` | int16 | Depth to groundwater table (cm) from Fan et al. 2013 global product, averaged within each reporting unit (HydroATLAS v1.0 Table 6).; units: centimeters; local catchment aggregate; area-weighted average |
| `ele_mt_cav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; local catchment aggregate; area-weighted average |
| `ele_mt_uav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; entire upstream area aggregate; area-weighted average |
| `ele_mt_cmn` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; local catchment aggregate; minimum of long-term monthly climatology |
| `ele_mt_cmx` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; local catchment aggregate; maximum of long-term monthly climatology |
| `slp_dg_cav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees; local catchment aggregate; area-weighted average |
| `slp_dg_uav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees; entire upstream area aggregate; area-weighted average |
| `sgr_dk_rav` | int16 | Average stream gradient (m/km) computed along HydroRIVERS centerlines (HydroATLAS v1.0 Table 4).; units: m/km (slope or gradient); reach-length weighted statistic; area-weighted average |
| `clz_cl_cmj` | int16 | Categorical codes; decode via sheet 'clz_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cls_cl_cmj` | int16 | Categorical codes; decode via sheet 'cls_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tmp_dc_cyr` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; long-term annual mean |
| `tmp_dc_uyr` | int16 | Near-surface air temperature; units: °C; entire upstream area aggregate; long-term annual mean |
| `tmp_dc_cmn` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; minimum of long-term monthly climatology |
| `tmp_dc_cmx` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; maximum of long-term monthly climatology |
| `tmp_dc_c01` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for January |
| `tmp_dc_c02` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for February |
| `tmp_dc_c03` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for March |
| `tmp_dc_c04` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for April |
| `tmp_dc_c05` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for May |
| `tmp_dc_c06` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for June |
| `tmp_dc_c07` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for July |
| `tmp_dc_c08` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for August |
| `tmp_dc_c09` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; value circa 2009 |
| `tmp_dc_c10` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for October |
| `tmp_dc_c11` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for November |
| `tmp_dc_c12` | int16 | Near-surface air temperature; units: °C; local catchment aggregate; climatological mean for December |
| `pre_mm_cyr` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; long-term annual mean |
| `pre_mm_uyr` | int16 | Precipitation accumulation; units: mm; entire upstream area aggregate; long-term annual mean |
| `pre_mm_c01` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for January |
| `pre_mm_c02` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for February |
| `pre_mm_c03` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for March |
| `pre_mm_c04` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for April |
| `pre_mm_c05` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for May |
| `pre_mm_c06` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for June |
| `pre_mm_c07` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for July |
| `pre_mm_c08` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for August |
| `pre_mm_c09` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; value circa 2009 |
| `pre_mm_c10` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for October |
| `pre_mm_c11` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for November |
| `pre_mm_c12` | int16 | Precipitation accumulation; units: mm; local catchment aggregate; climatological mean for December |
| `pet_mm_cyr` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; long-term annual mean |
| `pet_mm_uyr` | int16 | Potential evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `pet_mm_c01` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for January |
| `pet_mm_c02` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for February |
| `pet_mm_c03` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for March |
| `pet_mm_c04` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for April |
| `pet_mm_c05` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for May |
| `pet_mm_c06` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for June |
| `pet_mm_c07` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for July |
| `pet_mm_c08` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for August |
| `pet_mm_c09` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; value circa 2009 |
| `pet_mm_c10` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for October |
| `pet_mm_c11` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for November |
| `pet_mm_c12` | int16 | Potential evapotranspiration; units: mm; local catchment aggregate; climatological mean for December |
| `aet_mm_cyr` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; long-term annual mean |
| `aet_mm_uyr` | int16 | Actual evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `aet_mm_c01` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for January |
| `aet_mm_c02` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for February |
| `aet_mm_c03` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for March |
| `aet_mm_c04` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for April |
| `aet_mm_c05` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for May |
| `aet_mm_c06` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for June |
| `aet_mm_c07` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for July |
| `aet_mm_c08` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for August |
| `aet_mm_c09` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; value circa 2009 |
| `aet_mm_c10` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for October |
| `aet_mm_c11` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for November |
| `aet_mm_c12` | int16 | Actual evapotranspiration; units: mm; local catchment aggregate; climatological mean for December |
| `ari_ix_cav` | int16 | units: dimensionless index; local catchment aggregate; area-weighted average |
| `ari_ix_uav` | int16 | units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `cmi_ix_cyr` | int16 | units: dimensionless index; local catchment aggregate; long-term annual mean |
| `cmi_ix_uyr` | int16 | units: dimensionless index; entire upstream area aggregate; long-term annual mean |
| `cmi_ix_c01` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for January |
| `cmi_ix_c02` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for February |
| `cmi_ix_c03` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for March |
| `cmi_ix_c04` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for April |
| `cmi_ix_c05` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for May |
| `cmi_ix_c06` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for June |
| `cmi_ix_c07` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for July |
| `cmi_ix_c08` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for August |
| `cmi_ix_c09` | int16 | units: dimensionless index; local catchment aggregate; value circa 2009 |
| `cmi_ix_c10` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for October |
| `cmi_ix_c11` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for November |
| `cmi_ix_c12` | int16 | units: dimensionless index; local catchment aggregate; climatological mean for December |
| `snw_pc_cyr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; long-term annual mean |
| `snw_pc_uyr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `snw_pc_cmx` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; maximum of long-term monthly climatology |
| `snw_pc_c01` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for January |
| `snw_pc_c02` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for February |
| `snw_pc_c03` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for March |
| `snw_pc_c04` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for April |
| `snw_pc_c05` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for May |
| `snw_pc_c06` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for June |
| `snw_pc_c07` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for July |
| `snw_pc_c08` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for August |
| `snw_pc_c09` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; value circa 2009 |
| `snw_pc_c10` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for October |
| `snw_pc_c11` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for November |
| `snw_pc_c12` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; local catchment aggregate; climatological mean for December |
| `glc_cl_cmj` | int16 | Categorical codes; decode via sheet 'glc_cl' in HydroATLAS_v10_Legends.xlsx. |
| `glc_pc_c01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for January |
| `glc_pc_c02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for February |
| `glc_pc_c03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for March |
| `glc_pc_c04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for April |
| `glc_pc_c05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for May |
| `glc_pc_c06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for June |
| `glc_pc_c07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for July |
| `glc_pc_c08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for August |
| `glc_pc_c09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; value circa 2009 |
| `glc_pc_c10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for October |
| `glc_pc_c11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for November |
| `glc_pc_c12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for December |
| `glc_pc_c13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 13 (see legend workbook) |
| `glc_pc_c14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 14 (see legend workbook) |
| `glc_pc_c15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 15 (see legend workbook) |
| `glc_pc_c16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 16 (see legend workbook) |
| `glc_pc_c17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 17 (see legend workbook) |
| `glc_pc_c18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 18 (see legend workbook) |
| `glc_pc_c19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 19 (see legend workbook) |
| `glc_pc_c20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 20 (see legend workbook) |
| `glc_pc_c21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 21 (see legend workbook) |
| `glc_pc_c22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 22 (see legend workbook) |
| `glc_pc_u01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `glc_pc_u02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `glc_pc_u03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `glc_pc_u04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `glc_pc_u05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `glc_pc_u06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `glc_pc_u07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `glc_pc_u08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `glc_pc_u09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `glc_pc_u10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `glc_pc_u11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `glc_pc_u12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `glc_pc_u13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `glc_pc_u14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `glc_pc_u15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `glc_pc_u16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 16 (see legend workbook) |
| `glc_pc_u17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 17 (see legend workbook) |
| `glc_pc_u18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 18 (see legend workbook) |
| `glc_pc_u19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 19 (see legend workbook) |
| `glc_pc_u20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 20 (see legend workbook) |
| `glc_pc_u21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 21 (see legend workbook) |
| `glc_pc_u22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 22 (see legend workbook) |
| `pnv_cl_cmj` | int16 | Categorical codes; decode via sheet 'pnv_cl' in HydroATLAS_v10_Legends.xlsx. |
| `pnv_pc_c01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for January |
| `pnv_pc_c02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for February |
| `pnv_pc_c03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for March |
| `pnv_pc_c04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for April |
| `pnv_pc_c05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for May |
| `pnv_pc_c06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for June |
| `pnv_pc_c07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for July |
| `pnv_pc_c08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for August |
| `pnv_pc_c09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; value circa 2009 |
| `pnv_pc_c10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for October |
| `pnv_pc_c11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for November |
| `pnv_pc_c12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for December |
| `pnv_pc_c13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 13 (see legend workbook) |
| `pnv_pc_c14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 14 (see legend workbook) |
| `pnv_pc_c15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; classification bin 15 (see legend workbook) |
| `pnv_pc_u01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `pnv_pc_u02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `pnv_pc_u03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `pnv_pc_u04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `pnv_pc_u05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `pnv_pc_u06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `pnv_pc_u07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `pnv_pc_u08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `pnv_pc_u09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `pnv_pc_u10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `pnv_pc_u11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `pnv_pc_u12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `pnv_pc_u13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `pnv_pc_u14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `pnv_pc_u15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `wet_cl_cmj` | int16 | Categorical codes; decode via sheet 'wet_cl' in HydroATLAS_v10_Legends.xlsx. |
| `wet_pc_cg1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; GLWD class group 1 (permanent wetlands) |
| `wet_pc_ug1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 1 (permanent wetlands) |
| `wet_pc_cg2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; GLWD class group 2 (seasonal wetlands) |
| `wet_pc_ug2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 2 (seasonal wetlands) |
| `wet_pc_c01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for January |
| `wet_pc_c02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for February |
| `wet_pc_c03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for March |
| `wet_pc_c04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for April |
| `wet_pc_c05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for May |
| `wet_pc_c06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for June |
| `wet_pc_c07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for July |
| `wet_pc_c08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for August |
| `wet_pc_c09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; value circa 2009 |
| `wet_pc_u01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `wet_pc_u02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `wet_pc_u03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `wet_pc_u04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `wet_pc_u05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `wet_pc_u06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `wet_pc_u07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `wet_pc_u08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `wet_pc_u09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `for_pc_cse` | int16 | Tree/forest cover share; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `for_pc_use` | int16 | Tree/forest cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `crp_pc_cse` | int16 | Cropland share; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `crp_pc_use` | int16 | Cropland share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pst_pc_cse` | int16 | Pasture share; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `pst_pc_use` | int16 | Pasture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ire_pc_cse` | int16 | Irrigated area share; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `ire_pc_use` | int16 | Irrigated area share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `gla_pc_cse` | int16 | Glacier cover share; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `gla_pc_use` | int16 | Glacier cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `prm_pc_cse` | int16 | Permanent water share; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `prm_pc_use` | int16 | Permanent water share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pac_pc_cse` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `pac_pc_use` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `tbi_cl_cmj` | int16 | Categorical codes; decode via sheet 'tbi_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tec_cl_cmj` | int16 | Categorical codes; decode via sheet 'tec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fmh_cl_cmj` | int16 | Categorical codes; decode via sheet 'fmh_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fec_cl_cmj` | int16 | Categorical codes; decode via sheet 'fec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cly_pc_cav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; area-weighted average |
| `cly_pc_uav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `slt_pc_cav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; area-weighted average |
| `slt_pc_uav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `snd_pc_cav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; area-weighted average |
| `snd_pc_uav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `soc_th_cav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare; local catchment aggregate; area-weighted average |
| `soc_th_uav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare; entire upstream area aggregate; area-weighted average |
| `swc_pc_cyr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; long-term annual mean |
| `swc_pc_uyr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `swc_pc_c01` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for January |
| `swc_pc_c02` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for February |
| `swc_pc_c03` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for March |
| `swc_pc_c04` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for April |
| `swc_pc_c05` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for May |
| `swc_pc_c06` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for June |
| `swc_pc_c07` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for July |
| `swc_pc_c08` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for August |
| `swc_pc_c09` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; value circa 2009 |
| `swc_pc_c10` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for October |
| `swc_pc_c11` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for November |
| `swc_pc_c12` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; local catchment aggregate; climatological mean for December |
| `lit_cl_cmj` | int16 | Categorical codes; decode via sheet 'lit_cl' in HydroATLAS_v10_Legends.xlsx. |
| `kar_pc_cse` | int16 | Karst proportion; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `kar_pc_use` | int16 | Karst proportion; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ero_kh_cav` | int32 | Soil erosion rate; local catchment aggregate; area-weighted average |
| `ero_kh_uav` | int32 | Soil erosion rate; entire upstream area aggregate; area-weighted average |
| `urb_pc_cse` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area; local catchment aggregate; fractional share/extent |
| `urb_pc_use` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `nli_ix_cav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index; local catchment aggregate; area-weighted average |
| `nli_ix_uav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `rdd_mk_cav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7.; local catchment aggregate; area-weighted average |
| `rdd_mk_uav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7.; entire upstream area aggregate; area-weighted average |
| `hft_ix_c93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; local catchment aggregate; value circa 1993 |
| `hft_ix_u93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 1993 |
| `hft_ix_c09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; local catchment aggregate; value circa 2009 |
| `hft_ix_u09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 2009 |
| `gad_id_cmj` | int16 | Administrative identifier (GAUL / GADM cross-walk); local catchment aggregate; dominant (majority) class ID |
| `gdp_ud_cav` | int32 | Gross domestic product per capita (constant 2011 PPP USD) from World Bank/SEDAC grids aggregated as in HydroATLAS v1.0 Table 7.; units: US dollars (constant PPP, per capita); local catchment aggregate; area-weighted average |
| `hdi_ix_cav` | int16 | UNDP Human Development Index (2013) averaged over each reporting unit (HydroATLAS v1.0 Table 7).; units: dimensionless index; local catchment aggregate; area-weighted average |
| `Shape_Length` | float | Geometry perimeter/length reported by the data source CRS. |


## BasinATLAS v1.0 (HydroBASINS derived attributes)

Data source: `/Users/snowfay/CF_calculate/data/HydroSHEDS data/BasinATLAS_Data_v10.gdb/BasinATLAS_v10.gdb`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/BasinATLAS_Data_v10.gdb/BasinATLAS_Catalog_v10.pdf`
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/BasinATLAS_Data_v10.gdb/HydroATLAS_TechDoc_v10.pdf`

### Layer: BasinATLAS_v10_lev01

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 10

| Field | Type | Meaning |
| --- | --- | --- |
| `HYBAS_ID` | float | Permanent HydroBASINS polygon identifier at the dataset's level. |
| `NEXT_DOWN` | float | HYRIV_ID of the immediate downstream reach (0 = ocean outlet). |
| `NEXT_SINK` | float | HYBAS_ID of the downstream sink (endorheic target). |
| `MAIN_BAS` | float | Identifier of the encompassing main basin (Pfafstetter coding). |
| `DIST_SINK` | float | Flow distance (km) from the basin outlet to its terminal sink. |
| `DIST_MAIN` | float | Flow distance (km) from the basin outlet to the main river mouth. |
| `SUB_AREA` | float | Area (km²) of the polygon between nested HydroBASINS levels. |
| `UP_AREA` | float | Total upstream area (km²) draining through the polygon outlet. |
| `PFAF_ID` | int32 | Pfafstetter hierarchical basin code. |
| `ENDO` | int32 | See accompanying technical documentation for semantic details. |
| `COAST` | int32 | 1 if the basin drains directly to the ocean. |
| `ORDER_` | int32 | See accompanying technical documentation for semantic details. |
| `SORT` | float | Pre-calculated sort key for topological traversals. |
| `run_mm_syr` | int16 | Runoff depth (mm/yr) computed from WaterGAP 2.2 climatology for HydroATLAS v1.0 (Table 4).; units: mm; HydroBASINS polygon aggregate; long-term annual mean |
| `inu_pc_smn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; HydroBASINS polygon aggregate; minimum of long-term monthly climatology |
| `inu_pc_umn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; minimum of long-term monthly climatology |
| `inu_pc_smx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; HydroBASINS polygon aggregate; maximum of long-term monthly climatology |
| `inu_pc_umx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; maximum of long-term monthly climatology |
| `inu_pc_slt` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; HydroBASINS polygon aggregate; latest available snapshot (~2010 baseline) |
| `inu_pc_ult` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; latest available snapshot (~2010 baseline) |
| `lka_pc_sse` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `lka_pc_use` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `lkv_mc_usu` | int32 | Combined natural lake and reservoir volume (10^6 m³) sourced from HydroLAKES/GRanD per HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `rev_mc_usu` | int32 | Managed reservoir storage volume (10^6 m³) derived from GRanD v1.3, summarized as in HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `dor_pc_pva` | int16 | Degree of regulation (%) = upstream reservoir storage / mean annual discharge (Lehner et al., 2014); HydroATLAS v1.0 Table 5.; units: percent of the referenced area; pour-point statistic (network outlet) |
| `gwt_cm_sav` | int16 | Depth to groundwater table (cm) from Fan et al. 2013 global product, averaged within each reporting unit (HydroATLAS v1.0 Table 6).; units: centimeters; HydroBASINS polygon aggregate; area-weighted average |
| `ele_mt_sav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; HydroBASINS polygon aggregate; area-weighted average |
| `ele_mt_uav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; entire upstream area aggregate; area-weighted average |
| `ele_mt_smn` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; HydroBASINS polygon aggregate; minimum of long-term monthly climatology |
| `ele_mt_smx` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; HydroBASINS polygon aggregate; maximum of long-term monthly climatology |
| `slp_dg_sav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees; HydroBASINS polygon aggregate; area-weighted average |
| `slp_dg_uav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees; entire upstream area aggregate; area-weighted average |
| `sgr_dk_sav` | int16 | Average stream gradient (m/km) computed along HydroRIVERS centerlines (HydroATLAS v1.0 Table 4).; units: m/km (slope or gradient); HydroBASINS polygon aggregate; area-weighted average |
| `clz_cl_smj` | int16 | Categorical codes; decode via sheet 'clz_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cls_cl_smj` | int16 | Categorical codes; decode via sheet 'cls_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tmp_dc_syr` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; long-term annual mean |
| `tmp_dc_uyr` | int16 | Near-surface air temperature; units: °C; entire upstream area aggregate; long-term annual mean |
| `tmp_dc_smn` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; minimum of long-term monthly climatology |
| `tmp_dc_smx` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; maximum of long-term monthly climatology |
| `tmp_dc_s01` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for January |
| `tmp_dc_s02` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for February |
| `tmp_dc_s03` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for March |
| `tmp_dc_s04` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for April |
| `tmp_dc_s05` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for May |
| `tmp_dc_s06` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for June |
| `tmp_dc_s07` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for July |
| `tmp_dc_s08` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for August |
| `tmp_dc_s09` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; value circa 2009 |
| `tmp_dc_s10` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for October |
| `tmp_dc_s11` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for November |
| `tmp_dc_s12` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for December |
| `pre_mm_syr` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; long-term annual mean |
| `pre_mm_uyr` | int16 | Precipitation accumulation; units: mm; entire upstream area aggregate; long-term annual mean |
| `pre_mm_s01` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for January |
| `pre_mm_s02` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for February |
| `pre_mm_s03` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for March |
| `pre_mm_s04` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for April |
| `pre_mm_s05` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for May |
| `pre_mm_s06` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for June |
| `pre_mm_s07` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for July |
| `pre_mm_s08` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for August |
| `pre_mm_s09` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; value circa 2009 |
| `pre_mm_s10` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for October |
| `pre_mm_s11` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for November |
| `pre_mm_s12` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for December |
| `pet_mm_syr` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; long-term annual mean |
| `pet_mm_uyr` | int16 | Potential evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `pet_mm_s01` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for January |
| `pet_mm_s02` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for February |
| `pet_mm_s03` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for March |
| `pet_mm_s04` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for April |
| `pet_mm_s05` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for May |
| `pet_mm_s06` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for June |
| `pet_mm_s07` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for July |
| `pet_mm_s08` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for August |
| `pet_mm_s09` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; value circa 2009 |
| `pet_mm_s10` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for October |
| `pet_mm_s11` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for November |
| `pet_mm_s12` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for December |
| `aet_mm_syr` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; long-term annual mean |
| `aet_mm_uyr` | int16 | Actual evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `aet_mm_s01` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for January |
| `aet_mm_s02` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for February |
| `aet_mm_s03` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for March |
| `aet_mm_s04` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for April |
| `aet_mm_s05` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for May |
| `aet_mm_s06` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for June |
| `aet_mm_s07` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for July |
| `aet_mm_s08` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for August |
| `aet_mm_s09` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; value circa 2009 |
| `aet_mm_s10` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for October |
| `aet_mm_s11` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for November |
| `aet_mm_s12` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for December |
| `ari_ix_sav` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; area-weighted average |
| `ari_ix_uav` | int16 | units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `cmi_ix_syr` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; long-term annual mean |
| `cmi_ix_uyr` | int16 | units: dimensionless index; entire upstream area aggregate; long-term annual mean |
| `cmi_ix_s01` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for January |
| `cmi_ix_s02` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for February |
| `cmi_ix_s03` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for March |
| `cmi_ix_s04` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for April |
| `cmi_ix_s05` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for May |
| `cmi_ix_s06` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for June |
| `cmi_ix_s07` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for July |
| `cmi_ix_s08` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for August |
| `cmi_ix_s09` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; value circa 2009 |
| `cmi_ix_s10` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for October |
| `cmi_ix_s11` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for November |
| `cmi_ix_s12` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for December |
| `snw_pc_syr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; long-term annual mean |
| `snw_pc_uyr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `snw_pc_smx` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; maximum of long-term monthly climatology |
| `snw_pc_s01` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `snw_pc_s02` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `snw_pc_s03` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `snw_pc_s04` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `snw_pc_s05` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `snw_pc_s06` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `snw_pc_s07` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `snw_pc_s08` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `snw_pc_s09` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `snw_pc_s10` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for October |
| `snw_pc_s11` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for November |
| `snw_pc_s12` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for December |
| `glc_cl_smj` | int16 | Categorical codes; decode via sheet 'glc_cl' in HydroATLAS_v10_Legends.xlsx. |
| `glc_pc_s01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `glc_pc_s02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `glc_pc_s03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `glc_pc_s04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `glc_pc_s05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `glc_pc_s06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `glc_pc_s07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `glc_pc_s08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `glc_pc_s09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `glc_pc_s10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for October |
| `glc_pc_s11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for November |
| `glc_pc_s12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for December |
| `glc_pc_s13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 13 (see legend workbook) |
| `glc_pc_s14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 14 (see legend workbook) |
| `glc_pc_s15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 15 (see legend workbook) |
| `glc_pc_s16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 16 (see legend workbook) |
| `glc_pc_s17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 17 (see legend workbook) |
| `glc_pc_s18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 18 (see legend workbook) |
| `glc_pc_s19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 19 (see legend workbook) |
| `glc_pc_s20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 20 (see legend workbook) |
| `glc_pc_s21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 21 (see legend workbook) |
| `glc_pc_s22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 22 (see legend workbook) |
| `glc_pc_u01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `glc_pc_u02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `glc_pc_u03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `glc_pc_u04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `glc_pc_u05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `glc_pc_u06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `glc_pc_u07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `glc_pc_u08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `glc_pc_u09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `glc_pc_u10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `glc_pc_u11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `glc_pc_u12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `glc_pc_u13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `glc_pc_u14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `glc_pc_u15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `glc_pc_u16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 16 (see legend workbook) |
| `glc_pc_u17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 17 (see legend workbook) |
| `glc_pc_u18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 18 (see legend workbook) |
| `glc_pc_u19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 19 (see legend workbook) |
| `glc_pc_u20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 20 (see legend workbook) |
| `glc_pc_u21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 21 (see legend workbook) |
| `glc_pc_u22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 22 (see legend workbook) |
| `pnv_cl_smj` | int16 | Categorical codes; decode via sheet 'pnv_cl' in HydroATLAS_v10_Legends.xlsx. |
| `pnv_pc_s01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `pnv_pc_s02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `pnv_pc_s03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `pnv_pc_s04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `pnv_pc_s05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `pnv_pc_s06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `pnv_pc_s07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `pnv_pc_s08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `pnv_pc_s09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `pnv_pc_s10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for October |
| `pnv_pc_s11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for November |
| `pnv_pc_s12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for December |
| `pnv_pc_s13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 13 (see legend workbook) |
| `pnv_pc_s14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 14 (see legend workbook) |
| `pnv_pc_s15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 15 (see legend workbook) |
| `pnv_pc_u01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `pnv_pc_u02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `pnv_pc_u03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `pnv_pc_u04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `pnv_pc_u05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `pnv_pc_u06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `pnv_pc_u07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `pnv_pc_u08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `pnv_pc_u09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `pnv_pc_u10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `pnv_pc_u11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `pnv_pc_u12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `pnv_pc_u13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `pnv_pc_u14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `pnv_pc_u15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `wet_cl_smj` | int16 | Categorical codes; decode via sheet 'wet_cl' in HydroATLAS_v10_Legends.xlsx. |
| `wet_pc_sg1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; GLWD class group 1 (permanent wetlands) |
| `wet_pc_ug1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 1 (permanent wetlands) |
| `wet_pc_sg2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; GLWD class group 2 (seasonal wetlands) |
| `wet_pc_ug2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 2 (seasonal wetlands) |
| `wet_pc_s01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `wet_pc_s02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `wet_pc_s03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `wet_pc_s04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `wet_pc_s05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `wet_pc_s06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `wet_pc_s07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `wet_pc_s08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `wet_pc_s09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `wet_pc_u01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `wet_pc_u02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `wet_pc_u03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `wet_pc_u04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `wet_pc_u05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `wet_pc_u06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `wet_pc_u07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `wet_pc_u08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `wet_pc_u09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `for_pc_sse` | int16 | Tree/forest cover share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `for_pc_use` | int16 | Tree/forest cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `crp_pc_sse` | int16 | Cropland share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `crp_pc_use` | int16 | Cropland share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pst_pc_sse` | int16 | Pasture share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `pst_pc_use` | int16 | Pasture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ire_pc_sse` | int16 | Irrigated area share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `ire_pc_use` | int16 | Irrigated area share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `gla_pc_sse` | int16 | Glacier cover share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `gla_pc_use` | int16 | Glacier cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `prm_pc_sse` | int16 | Permanent water share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `prm_pc_use` | int16 | Permanent water share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pac_pc_sse` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `pac_pc_use` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `tbi_cl_smj` | int16 | Categorical codes; decode via sheet 'tbi_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tec_cl_smj` | int16 | Categorical codes; decode via sheet 'tec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fmh_cl_smj` | int16 | Categorical codes; decode via sheet 'fmh_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fec_cl_smj` | int16 | Categorical codes; decode via sheet 'fec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cly_pc_sav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; area-weighted average |
| `cly_pc_uav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `slt_pc_sav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; area-weighted average |
| `slt_pc_uav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `snd_pc_sav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; area-weighted average |
| `snd_pc_uav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `soc_th_sav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare; HydroBASINS polygon aggregate; area-weighted average |
| `soc_th_uav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare; entire upstream area aggregate; area-weighted average |
| `swc_pc_syr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; long-term annual mean |
| `swc_pc_uyr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `swc_pc_s01` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `swc_pc_s02` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `swc_pc_s03` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `swc_pc_s04` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `swc_pc_s05` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `swc_pc_s06` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `swc_pc_s07` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `swc_pc_s08` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `swc_pc_s09` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `swc_pc_s10` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for October |
| `swc_pc_s11` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for November |
| `swc_pc_s12` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for December |
| `lit_cl_smj` | int16 | Categorical codes; decode via sheet 'lit_cl' in HydroATLAS_v10_Legends.xlsx. |
| `kar_pc_sse` | int16 | Karst proportion; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `kar_pc_use` | int16 | Karst proportion; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ero_kh_sav` | int32 | Soil erosion rate; HydroBASINS polygon aggregate; area-weighted average |
| `ero_kh_uav` | int32 | Soil erosion rate; entire upstream area aggregate; area-weighted average |
| `urb_pc_sse` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `urb_pc_use` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `nli_ix_sav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index; HydroBASINS polygon aggregate; area-weighted average |
| `nli_ix_uav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `rdd_mk_sav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7.; HydroBASINS polygon aggregate; area-weighted average |
| `rdd_mk_uav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7.; entire upstream area aggregate; area-weighted average |
| `hft_ix_s93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; HydroBASINS polygon aggregate; value circa 1993 |
| `hft_ix_u93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 1993 |
| `hft_ix_s09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; HydroBASINS polygon aggregate; value circa 2009 |
| `hft_ix_u09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 2009 |
| `gad_id_smj` | int16 | Administrative identifier (GAUL / GADM cross-walk); HydroBASINS polygon aggregate; dominant (majority) class ID |
| `gdp_ud_sav` | int32 | Gross domestic product per capita (constant 2011 PPP USD) from World Bank/SEDAC grids aggregated as in HydroATLAS v1.0 Table 7.; units: US dollars (constant PPP, per capita); HydroBASINS polygon aggregate; area-weighted average |
| `hdi_ix_sav` | int16 | UNDP Human Development Index (2013) averaged over each reporting unit (HydroATLAS v1.0 Table 7).; units: dimensionless index; HydroBASINS polygon aggregate; area-weighted average |
| `Shape_Length` | float | Geometry perimeter/length reported by the data source CRS. |
| `Shape_Area` | float | Geometry area reported by the data source CRS. |

### Layer: BasinATLAS_v10_lev02

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 62

Shares schema with a previously listed layer; see the matching layer above for field definitions.

### Layer: BasinATLAS_v10_lev03

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 292

Shares schema with a previously listed layer; see the matching layer above for field definitions.

### Layer: BasinATLAS_v10_lev04

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 1342

Shares schema with a previously listed layer; see the matching layer above for field definitions.

### Layer: BasinATLAS_v10_lev05

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 4734

Shares schema with a previously listed layer; see the matching layer above for field definitions.

### Layer: BasinATLAS_v10_lev06

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 16397

Shares schema with a previously listed layer; see the matching layer above for field definitions.

### Layer: BasinATLAS_v10_lev07

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 57646

Shares schema with a previously listed layer; see the matching layer above for field definitions.

### Layer: BasinATLAS_v10_lev08

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 190675

Shares schema with a previously listed layer; see the matching layer above for field definitions.

### Layer: BasinATLAS_v10_lev09

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 508190

Shares schema with a previously listed layer; see the matching layer above for field definitions.

### Layer: BasinATLAS_v10_lev10

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 941012

| Field | Type | Meaning |
| --- | --- | --- |
| `HYBAS_ID` | float | Permanent HydroBASINS polygon identifier at the dataset's level. |
| `NEXT_DOWN` | float | HYRIV_ID of the immediate downstream reach (0 = ocean outlet). |
| `NEXT_SINK` | float | HYBAS_ID of the downstream sink (endorheic target). |
| `MAIN_BAS` | float | Identifier of the encompassing main basin (Pfafstetter coding). |
| `DIST_SINK` | float | Flow distance (km) from the basin outlet to its terminal sink. |
| `DIST_MAIN` | float | Flow distance (km) from the basin outlet to the main river mouth. |
| `SUB_AREA` | float | Area (km²) of the polygon between nested HydroBASINS levels. |
| `UP_AREA` | float | Total upstream area (km²) draining through the polygon outlet. |
| `PFAF_ID` | float | Pfafstetter hierarchical basin code. |
| `ENDO` | int32 | See accompanying technical documentation for semantic details. |
| `COAST` | int32 | 1 if the basin drains directly to the ocean. |
| `ORDER_` | int32 | See accompanying technical documentation for semantic details. |
| `SORT` | float | Pre-calculated sort key for topological traversals. |
| `run_mm_syr` | int16 | Runoff depth (mm/yr) computed from WaterGAP 2.2 climatology for HydroATLAS v1.0 (Table 4).; units: mm; HydroBASINS polygon aggregate; long-term annual mean |
| `inu_pc_smn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; HydroBASINS polygon aggregate; minimum of long-term monthly climatology |
| `inu_pc_umn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; minimum of long-term monthly climatology |
| `inu_pc_smx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; HydroBASINS polygon aggregate; maximum of long-term monthly climatology |
| `inu_pc_umx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; maximum of long-term monthly climatology |
| `inu_pc_slt` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; HydroBASINS polygon aggregate; latest available snapshot (~2010 baseline) |
| `inu_pc_ult` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; latest available snapshot (~2010 baseline) |
| `lka_pc_sse` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `lka_pc_use` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `lkv_mc_usu` | int32 | Combined natural lake and reservoir volume (10^6 m³) sourced from HydroLAKES/GRanD per HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `rev_mc_usu` | int32 | Managed reservoir storage volume (10^6 m³) derived from GRanD v1.3, summarized as in HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `dor_pc_pva` | int16 | Degree of regulation (%) = upstream reservoir storage / mean annual discharge (Lehner et al., 2014); HydroATLAS v1.0 Table 5.; units: percent of the referenced area; pour-point statistic (network outlet) |
| `gwt_cm_sav` | int16 | Depth to groundwater table (cm) from Fan et al. 2013 global product, averaged within each reporting unit (HydroATLAS v1.0 Table 6).; units: centimeters; HydroBASINS polygon aggregate; area-weighted average |
| `ele_mt_sav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; HydroBASINS polygon aggregate; area-weighted average |
| `ele_mt_uav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; entire upstream area aggregate; area-weighted average |
| `ele_mt_smn` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; HydroBASINS polygon aggregate; minimum of long-term monthly climatology |
| `ele_mt_smx` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; HydroBASINS polygon aggregate; maximum of long-term monthly climatology |
| `slp_dg_sav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees; HydroBASINS polygon aggregate; area-weighted average |
| `slp_dg_uav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees; entire upstream area aggregate; area-weighted average |
| `sgr_dk_sav` | int16 | Average stream gradient (m/km) computed along HydroRIVERS centerlines (HydroATLAS v1.0 Table 4).; units: m/km (slope or gradient); HydroBASINS polygon aggregate; area-weighted average |
| `clz_cl_smj` | int16 | Categorical codes; decode via sheet 'clz_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cls_cl_smj` | int16 | Categorical codes; decode via sheet 'cls_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tmp_dc_syr` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; long-term annual mean |
| `tmp_dc_uyr` | int16 | Near-surface air temperature; units: °C; entire upstream area aggregate; long-term annual mean |
| `tmp_dc_smn` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; minimum of long-term monthly climatology |
| `tmp_dc_smx` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; maximum of long-term monthly climatology |
| `tmp_dc_s01` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for January |
| `tmp_dc_s02` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for February |
| `tmp_dc_s03` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for March |
| `tmp_dc_s04` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for April |
| `tmp_dc_s05` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for May |
| `tmp_dc_s06` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for June |
| `tmp_dc_s07` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for July |
| `tmp_dc_s08` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for August |
| `tmp_dc_s09` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; value circa 2009 |
| `tmp_dc_s10` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for October |
| `tmp_dc_s11` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for November |
| `tmp_dc_s12` | int16 | Near-surface air temperature; units: °C; HydroBASINS polygon aggregate; climatological mean for December |
| `pre_mm_syr` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; long-term annual mean |
| `pre_mm_uyr` | int16 | Precipitation accumulation; units: mm; entire upstream area aggregate; long-term annual mean |
| `pre_mm_s01` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for January |
| `pre_mm_s02` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for February |
| `pre_mm_s03` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for March |
| `pre_mm_s04` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for April |
| `pre_mm_s05` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for May |
| `pre_mm_s06` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for June |
| `pre_mm_s07` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for July |
| `pre_mm_s08` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for August |
| `pre_mm_s09` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; value circa 2009 |
| `pre_mm_s10` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for October |
| `pre_mm_s11` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for November |
| `pre_mm_s12` | int16 | Precipitation accumulation; units: mm; HydroBASINS polygon aggregate; climatological mean for December |
| `pet_mm_syr` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; long-term annual mean |
| `pet_mm_uyr` | int16 | Potential evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `pet_mm_s01` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for January |
| `pet_mm_s02` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for February |
| `pet_mm_s03` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for March |
| `pet_mm_s04` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for April |
| `pet_mm_s05` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for May |
| `pet_mm_s06` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for June |
| `pet_mm_s07` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for July |
| `pet_mm_s08` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for August |
| `pet_mm_s09` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; value circa 2009 |
| `pet_mm_s10` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for October |
| `pet_mm_s11` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for November |
| `pet_mm_s12` | int16 | Potential evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for December |
| `aet_mm_syr` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; long-term annual mean |
| `aet_mm_uyr` | int16 | Actual evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `aet_mm_s01` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for January |
| `aet_mm_s02` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for February |
| `aet_mm_s03` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for March |
| `aet_mm_s04` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for April |
| `aet_mm_s05` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for May |
| `aet_mm_s06` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for June |
| `aet_mm_s07` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for July |
| `aet_mm_s08` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for August |
| `aet_mm_s09` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; value circa 2009 |
| `aet_mm_s10` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for October |
| `aet_mm_s11` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for November |
| `aet_mm_s12` | int16 | Actual evapotranspiration; units: mm; HydroBASINS polygon aggregate; climatological mean for December |
| `ari_ix_sav` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; area-weighted average |
| `ari_ix_uav` | int16 | units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `cmi_ix_syr` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; long-term annual mean |
| `cmi_ix_uyr` | int16 | units: dimensionless index; entire upstream area aggregate; long-term annual mean |
| `cmi_ix_s01` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for January |
| `cmi_ix_s02` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for February |
| `cmi_ix_s03` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for March |
| `cmi_ix_s04` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for April |
| `cmi_ix_s05` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for May |
| `cmi_ix_s06` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for June |
| `cmi_ix_s07` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for July |
| `cmi_ix_s08` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for August |
| `cmi_ix_s09` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; value circa 2009 |
| `cmi_ix_s10` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for October |
| `cmi_ix_s11` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for November |
| `cmi_ix_s12` | int16 | units: dimensionless index; HydroBASINS polygon aggregate; climatological mean for December |
| `snw_pc_syr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; long-term annual mean |
| `snw_pc_uyr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `snw_pc_smx` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; maximum of long-term monthly climatology |
| `snw_pc_s01` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `snw_pc_s02` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `snw_pc_s03` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `snw_pc_s04` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `snw_pc_s05` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `snw_pc_s06` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `snw_pc_s07` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `snw_pc_s08` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `snw_pc_s09` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `snw_pc_s10` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for October |
| `snw_pc_s11` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for November |
| `snw_pc_s12` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for December |
| `glc_cl_smj` | int16 | Categorical codes; decode via sheet 'glc_cl' in HydroATLAS_v10_Legends.xlsx. |
| `glc_pc_s01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `glc_pc_s02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `glc_pc_s03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `glc_pc_s04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `glc_pc_s05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `glc_pc_s06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `glc_pc_s07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `glc_pc_s08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `glc_pc_s09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `glc_pc_s10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for October |
| `glc_pc_s11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for November |
| `glc_pc_s12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for December |
| `glc_pc_s13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 13 (see legend workbook) |
| `glc_pc_s14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 14 (see legend workbook) |
| `glc_pc_s15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 15 (see legend workbook) |
| `glc_pc_s16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 16 (see legend workbook) |
| `glc_pc_s17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 17 (see legend workbook) |
| `glc_pc_s18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 18 (see legend workbook) |
| `glc_pc_s19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 19 (see legend workbook) |
| `glc_pc_s20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 20 (see legend workbook) |
| `glc_pc_s21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 21 (see legend workbook) |
| `glc_pc_s22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 22 (see legend workbook) |
| `glc_pc_u01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `glc_pc_u02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `glc_pc_u03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `glc_pc_u04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `glc_pc_u05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `glc_pc_u06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `glc_pc_u07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `glc_pc_u08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `glc_pc_u09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `glc_pc_u10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `glc_pc_u11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `glc_pc_u12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `glc_pc_u13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `glc_pc_u14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `glc_pc_u15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `glc_pc_u16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 16 (see legend workbook) |
| `glc_pc_u17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 17 (see legend workbook) |
| `glc_pc_u18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 18 (see legend workbook) |
| `glc_pc_u19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 19 (see legend workbook) |
| `glc_pc_u20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 20 (see legend workbook) |
| `glc_pc_u21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 21 (see legend workbook) |
| `glc_pc_u22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 22 (see legend workbook) |
| `pnv_cl_smj` | int16 | Categorical codes; decode via sheet 'pnv_cl' in HydroATLAS_v10_Legends.xlsx. |
| `pnv_pc_s01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `pnv_pc_s02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `pnv_pc_s03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `pnv_pc_s04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `pnv_pc_s05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `pnv_pc_s06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `pnv_pc_s07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `pnv_pc_s08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `pnv_pc_s09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `pnv_pc_s10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for October |
| `pnv_pc_s11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for November |
| `pnv_pc_s12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for December |
| `pnv_pc_s13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 13 (see legend workbook) |
| `pnv_pc_s14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 14 (see legend workbook) |
| `pnv_pc_s15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; classification bin 15 (see legend workbook) |
| `pnv_pc_u01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `pnv_pc_u02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `pnv_pc_u03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `pnv_pc_u04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `pnv_pc_u05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `pnv_pc_u06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `pnv_pc_u07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `pnv_pc_u08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `pnv_pc_u09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `pnv_pc_u10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `pnv_pc_u11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `pnv_pc_u12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `pnv_pc_u13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `pnv_pc_u14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `pnv_pc_u15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `wet_cl_smj` | int16 | Categorical codes; decode via sheet 'wet_cl' in HydroATLAS_v10_Legends.xlsx. |
| `wet_pc_sg1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; GLWD class group 1 (permanent wetlands) |
| `wet_pc_ug1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 1 (permanent wetlands) |
| `wet_pc_sg2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; GLWD class group 2 (seasonal wetlands) |
| `wet_pc_ug2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 2 (seasonal wetlands) |
| `wet_pc_s01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `wet_pc_s02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `wet_pc_s03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `wet_pc_s04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `wet_pc_s05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `wet_pc_s06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `wet_pc_s07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `wet_pc_s08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `wet_pc_s09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `wet_pc_u01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `wet_pc_u02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `wet_pc_u03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `wet_pc_u04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `wet_pc_u05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `wet_pc_u06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `wet_pc_u07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `wet_pc_u08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `wet_pc_u09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `for_pc_sse` | int16 | Tree/forest cover share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `for_pc_use` | int16 | Tree/forest cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `crp_pc_sse` | int16 | Cropland share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `crp_pc_use` | int16 | Cropland share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pst_pc_sse` | int16 | Pasture share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `pst_pc_use` | int16 | Pasture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ire_pc_sse` | int16 | Irrigated area share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `ire_pc_use` | int16 | Irrigated area share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `gla_pc_sse` | int16 | Glacier cover share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `gla_pc_use` | int16 | Glacier cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `prm_pc_sse` | int16 | Permanent water share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `prm_pc_use` | int16 | Permanent water share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pac_pc_sse` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `pac_pc_use` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `tbi_cl_smj` | int16 | Categorical codes; decode via sheet 'tbi_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tec_cl_smj` | int16 | Categorical codes; decode via sheet 'tec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fmh_cl_smj` | int16 | Categorical codes; decode via sheet 'fmh_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fec_cl_smj` | int16 | Categorical codes; decode via sheet 'fec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cly_pc_sav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; area-weighted average |
| `cly_pc_uav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `slt_pc_sav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; area-weighted average |
| `slt_pc_uav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `snd_pc_sav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; area-weighted average |
| `snd_pc_uav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `soc_th_sav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare; HydroBASINS polygon aggregate; area-weighted average |
| `soc_th_uav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare; entire upstream area aggregate; area-weighted average |
| `swc_pc_syr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; long-term annual mean |
| `swc_pc_uyr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `swc_pc_s01` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for January |
| `swc_pc_s02` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for February |
| `swc_pc_s03` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for March |
| `swc_pc_s04` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for April |
| `swc_pc_s05` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for May |
| `swc_pc_s06` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for June |
| `swc_pc_s07` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for July |
| `swc_pc_s08` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for August |
| `swc_pc_s09` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; value circa 2009 |
| `swc_pc_s10` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for October |
| `swc_pc_s11` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for November |
| `swc_pc_s12` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; HydroBASINS polygon aggregate; climatological mean for December |
| `lit_cl_smj` | int16 | Categorical codes; decode via sheet 'lit_cl' in HydroATLAS_v10_Legends.xlsx. |
| `kar_pc_sse` | int16 | Karst proportion; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `kar_pc_use` | int16 | Karst proportion; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ero_kh_sav` | int32 | Soil erosion rate; HydroBASINS polygon aggregate; area-weighted average |
| `ero_kh_uav` | int32 | Soil erosion rate; entire upstream area aggregate; area-weighted average |
| `urb_pc_sse` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area; HydroBASINS polygon aggregate; fractional share/extent |
| `urb_pc_use` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `nli_ix_sav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index; HydroBASINS polygon aggregate; area-weighted average |
| `nli_ix_uav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `rdd_mk_sav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7.; HydroBASINS polygon aggregate; area-weighted average |
| `rdd_mk_uav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7.; entire upstream area aggregate; area-weighted average |
| `hft_ix_s93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; HydroBASINS polygon aggregate; value circa 1993 |
| `hft_ix_u93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 1993 |
| `hft_ix_s09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; HydroBASINS polygon aggregate; value circa 2009 |
| `hft_ix_u09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 2009 |
| `gad_id_smj` | int16 | Administrative identifier (GAUL / GADM cross-walk); HydroBASINS polygon aggregate; dominant (majority) class ID |
| `gdp_ud_sav` | int32 | Gross domestic product per capita (constant 2011 PPP USD) from World Bank/SEDAC grids aggregated as in HydroATLAS v1.0 Table 7.; units: US dollars (constant PPP, per capita); HydroBASINS polygon aggregate; area-weighted average |
| `hdi_ix_sav` | int16 | UNDP Human Development Index (2013) averaged over each reporting unit (HydroATLAS v1.0 Table 7).; units: dimensionless index; HydroBASINS polygon aggregate; area-weighted average |
| `Shape_Length` | float | Geometry perimeter/length reported by the data source CRS. |
| `Shape_Area` | float | Geometry area reported by the data source CRS. |

### Layer: BasinATLAS_v10_lev11

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 1031785

Shares schema with a previously listed layer; see the matching layer above for field definitions.

### Layer: BasinATLAS_v10_lev12

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 1034083

Shares schema with a previously listed layer; see the matching layer above for field definitions.


## LakeATLAS v1.0

Data source: `/Users/snowfay/CF_calculate/data/HydroSHEDS data/LakeATLAS_Data_v10.gdb/LakeATLAS_v10.gdb`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/LakeATLAS_Data_v10.gdb/LakeATLAS_Catalog_v10.pdf`
- `/Users/snowfay/CF_calculate/data/HydroSHEDS data/LakeATLAS_Data_v10.gdb/HydroATLAS_TechDoc_v10_1.pdf`

### Layer: LakeATLAS_v10_pol

- Driver: `OpenFileGDB`
- Geometry type: `MultiPolygon`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 1427688

| Field | Type | Meaning |
| --- | --- | --- |
| `Hylak_id` | int32 | Primary HydroLAKES identifier. |
| `Lake_name` | str:40 | Lake/reservoir name (if assigned). |
| `Country` | str:35 | Primary ISO-3 country code (may be multi-valued). |
| `Continent` | str:15 | Continent tag used by HydroLAKES. |
| `Poly_src` | str:10 | Source dataset for the polygon geometry. |
| `Lake_type` | int16 | HydroLAKES classification (natural lake, reservoir, etc.). |
| `Grand_id` | int16 | GRanD database identifier (if the lake is a registered reservoir). |
| `Vol_src` | int16 | Source authority for the volume estimate. |
| `Elevation` | int16 | Lake surface elevation (m a.s.l.). |
| `Pour_long` | float | Longitude of the modeled pour point (degrees). |
| `Pour_lat` | float | Latitude of the modeled pour point (degrees). |
| `HYBAS_L12` | float | Identifier of the intersecting HydroBASINS level-12 polygon. |
| `HYRIV_RCH` | int32 | See accompanying technical documentation for semantic details. |
| `HYRIV_CAT` | int32 | See accompanying technical documentation for semantic details. |
| `run_mm_vyr` | int16 | Runoff depth (mm/yr) computed from WaterGAP 2.2 climatology for HydroATLAS v1.0 (Table 4).; units: mm |
| `inu_pc_vmn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area |
| `inu_pc_umn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; minimum of long-term monthly climatology |
| `inu_pc_vmx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area |
| `inu_pc_umx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; maximum of long-term monthly climatology |
| `inu_pc_vlt` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area |
| `inu_pc_ult` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; latest available snapshot (~2010 baseline) |
| `lka_pc_vse` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area |
| `lka_pc_use` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `lkv_mc_usu` | int32 | Combined natural lake and reservoir volume (10^6 m³) sourced from HydroLAKES/GRanD per HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `rev_mc_usu` | int32 | Managed reservoir storage volume (10^6 m³) derived from GRanD v1.3, summarized as in HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `dor_pc_pva` | int16 | Degree of regulation (%) = upstream reservoir storage / mean annual discharge (Lehner et al., 2014); HydroATLAS v1.0 Table 5.; units: percent of the referenced area; pour-point statistic (network outlet) |
| `gwt_cm_vav` | int16 | Depth to groundwater table (cm) from Fan et al. 2013 global product, averaged within each reporting unit (HydroATLAS v1.0 Table 6).; units: centimeters |
| `ele_mt_lav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters |
| `ele_mt_uav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; entire upstream area aggregate; area-weighted average |
| `ele_mt_lmn` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters |
| `ele_mt_vmx` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters |
| `slp_dg_vav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees |
| `slp_dg_uav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees; entire upstream area aggregate; area-weighted average |
| `sgr_dk_vav` | int16 | Average stream gradient (m/km) computed along HydroRIVERS centerlines (HydroATLAS v1.0 Table 4).; units: m/km (slope or gradient) |
| `clz_cl_lmj` | int16 | Categorical codes; decode via sheet 'clz_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cls_cl_lmj` | int16 | Categorical codes; decode via sheet 'cls_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tmp_dc_lyr` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_uyr` | int16 | Near-surface air temperature; units: °C; entire upstream area aggregate; long-term annual mean |
| `tmp_dc_lmn` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_lmx` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l01` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l02` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l03` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l04` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l05` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l06` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l07` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l08` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l09` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l10` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l11` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l12` | int16 | Near-surface air temperature; units: °C |
| `pre_mm_lyr` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_uyr` | int16 | Precipitation accumulation; units: mm; entire upstream area aggregate; long-term annual mean |
| `pre_mm_l01` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l02` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l03` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l04` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l05` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l06` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l07` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l08` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l09` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l10` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l11` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l12` | int16 | Precipitation accumulation; units: mm |
| `pet_mm_lyr` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_uyr` | int16 | Potential evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `pet_mm_l01` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l02` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l03` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l04` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l05` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l06` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l07` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l08` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l09` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l10` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l11` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l12` | int16 | Potential evapotranspiration; units: mm |
| `aet_mm_vyr` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_uyr` | int16 | Actual evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `aet_mm_v01` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v02` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v03` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v04` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v05` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v06` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v07` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v08` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v09` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v10` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v11` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v12` | int16 | Actual evapotranspiration; units: mm |
| `ari_ix_lav` | int16 | units: dimensionless index |
| `ari_ix_uav` | int16 | units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `cmi_ix_lyr` | int16 | units: dimensionless index |
| `cmi_ix_uyr` | int16 | units: dimensionless index; entire upstream area aggregate; long-term annual mean |
| `cmi_ix_l01` | int16 | units: dimensionless index |
| `cmi_ix_l02` | int16 | units: dimensionless index |
| `cmi_ix_l03` | int16 | units: dimensionless index |
| `cmi_ix_l04` | int16 | units: dimensionless index |
| `cmi_ix_l05` | int16 | units: dimensionless index |
| `cmi_ix_l06` | int16 | units: dimensionless index |
| `cmi_ix_l07` | int16 | units: dimensionless index |
| `cmi_ix_l08` | int16 | units: dimensionless index |
| `cmi_ix_l09` | int16 | units: dimensionless index |
| `cmi_ix_l10` | int16 | units: dimensionless index |
| `cmi_ix_l11` | int16 | units: dimensionless index |
| `cmi_ix_l12` | int16 | units: dimensionless index |
| `snw_pc_vyr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_uyr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `snw_pc_vmx` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v01` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v02` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v03` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v04` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v05` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v06` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v07` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v08` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v09` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v10` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v11` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v12` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `glc_cl_vmj` | int16 | Categorical codes; decode via sheet 'glc_cl' in HydroATLAS_v10_Legends.xlsx. |
| `glc_pc_v01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_u01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `glc_pc_u02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `glc_pc_u03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `glc_pc_u04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `glc_pc_u05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `glc_pc_u06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `glc_pc_u07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `glc_pc_u08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `glc_pc_u09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `glc_pc_u10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `glc_pc_u11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `glc_pc_u12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `glc_pc_u13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `glc_pc_u14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `glc_pc_u15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `glc_pc_u16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 16 (see legend workbook) |
| `glc_pc_u17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 17 (see legend workbook) |
| `glc_pc_u18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 18 (see legend workbook) |
| `glc_pc_u19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 19 (see legend workbook) |
| `glc_pc_u20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 20 (see legend workbook) |
| `glc_pc_u21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 21 (see legend workbook) |
| `glc_pc_u22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 22 (see legend workbook) |
| `pnv_cl_vmj` | int16 | Categorical codes; decode via sheet 'pnv_cl' in HydroATLAS_v10_Legends.xlsx. |
| `pnv_pc_v01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_u01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `pnv_pc_u02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `pnv_pc_u03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `pnv_pc_u04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `pnv_pc_u05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `pnv_pc_u06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `pnv_pc_u07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `pnv_pc_u08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `pnv_pc_u09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `pnv_pc_u10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `pnv_pc_u11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `pnv_pc_u12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `pnv_pc_u13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `pnv_pc_u14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `pnv_pc_u15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `wet_cl_vmj` | int16 | Categorical codes; decode via sheet 'wet_cl' in HydroATLAS_v10_Legends.xlsx. |
| `wet_pc_vg1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_ug1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 1 (permanent wetlands) |
| `wet_pc_vg2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_ug2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 2 (seasonal wetlands) |
| `wet_pc_v01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_u01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `wet_pc_u02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `wet_pc_u03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `wet_pc_u04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `wet_pc_u05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `wet_pc_u06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `wet_pc_u07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `wet_pc_u08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `wet_pc_u09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `for_pc_vse` | int16 | Tree/forest cover share; units: percent of the referenced area |
| `for_pc_use` | int16 | Tree/forest cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `crp_pc_vse` | int16 | Cropland share; units: percent of the referenced area |
| `crp_pc_use` | int16 | Cropland share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pst_pc_vse` | int16 | Pasture share; units: percent of the referenced area |
| `pst_pc_use` | int16 | Pasture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ire_pc_vse` | int16 | Irrigated area share; units: percent of the referenced area |
| `ire_pc_use` | int16 | Irrigated area share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `gla_pc_vse` | int16 | Glacier cover share; units: percent of the referenced area |
| `gla_pc_use` | int16 | Glacier cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `prm_pc_vse` | int16 | Permanent water share; units: percent of the referenced area |
| `prm_pc_use` | int16 | Permanent water share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pac_pc_lse` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area |
| `pac_pc_use` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `tbi_cl_lmj` | int16 | Categorical codes; decode via sheet 'tbi_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tec_cl_lmj` | int16 | Categorical codes; decode via sheet 'tec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fmh_cl_lmj` | int16 | Categorical codes; decode via sheet 'fmh_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fec_cl_lmj` | int16 | Categorical codes; decode via sheet 'fec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cly_pc_vav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `cly_pc_uav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `slt_pc_vav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `slt_pc_uav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `snd_pc_vav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `snd_pc_uav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `soc_th_vav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare |
| `soc_th_uav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare; entire upstream area aggregate; area-weighted average |
| `swc_pc_vyr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_uyr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `swc_pc_v01` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v02` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v03` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v04` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v05` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v06` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v07` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v08` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v09` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v10` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v11` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v12` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `lit_cl_vmj` | int16 | Categorical codes; decode via sheet 'lit_cl' in HydroATLAS_v10_Legends.xlsx. |
| `kar_pc_vse` | int16 | Karst proportion; units: percent of the referenced area |
| `kar_pc_use` | int16 | Karst proportion; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ero_kh_vav` | int32 | Soil erosion rate |
| `ero_kh_uav` | int32 | Soil erosion rate; entire upstream area aggregate; area-weighted average |
| `urb_pc_vse` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area |
| `urb_pc_use` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `nli_ix_vav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index |
| `nli_ix_uav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `rdd_mk_vav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7. |
| `rdd_mk_uav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7.; entire upstream area aggregate; area-weighted average |
| `hft_ix_v93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index |
| `hft_ix_u93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 1993 |
| `hft_ix_v09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index |
| `hft_ix_u09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 2009 |
| `gad_id_lmj` | int16 | Administrative identifier (GAUL / GADM cross-walk) |
| `gdp_ud_vav` | int32 | Gross domestic product per capita (constant 2011 PPP USD) from World Bank/SEDAC grids aggregated as in HydroATLAS v1.0 Table 7.; units: US dollars (constant PPP, per capita) |
| `hdi_ix_vav` | int16 | UNDP Human Development Index (2013) averaged over each reporting unit (HydroATLAS v1.0 Table 7).; units: dimensionless index |
| `Shape_Length` | float | Geometry perimeter/length reported by the data source CRS. |
| `Shape_Area` | float | Geometry area reported by the data source CRS. |

### Layer: LakeATLAS_v10_pnt

- Driver: `OpenFileGDB`
- Geometry type: `Point`
- CRS: `GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]`
- Feature count: 1427688

| Field | Type | Meaning |
| --- | --- | --- |
| `Hylak_id` | int32 | Primary HydroLAKES identifier. |
| `Lake_name` | str:40 | Lake/reservoir name (if assigned). |
| `Country` | str:35 | Primary ISO-3 country code (may be multi-valued). |
| `Continent` | str:15 | Continent tag used by HydroLAKES. |
| `Poly_src` | str:10 | Source dataset for the polygon geometry. |
| `Lake_type` | int16 | HydroLAKES classification (natural lake, reservoir, etc.). |
| `Grand_id` | int16 | GRanD database identifier (if the lake is a registered reservoir). |
| `Vol_src` | int16 | Source authority for the volume estimate. |
| `Elevation` | int16 | Lake surface elevation (m a.s.l.). |
| `Pour_long` | float | Longitude of the modeled pour point (degrees). |
| `Pour_lat` | float | Latitude of the modeled pour point (degrees). |
| `HYBAS_L12` | float | Identifier of the intersecting HydroBASINS level-12 polygon. |
| `HYRIV_RCH` | int32 | See accompanying technical documentation for semantic details. |
| `HYRIV_CAT` | int32 | See accompanying technical documentation for semantic details. |
| `run_mm_vyr` | int16 | Runoff depth (mm/yr) computed from WaterGAP 2.2 climatology for HydroATLAS v1.0 (Table 4).; units: mm |
| `inu_pc_vmn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area |
| `inu_pc_umn` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; minimum of long-term monthly climatology |
| `inu_pc_vmx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area |
| `inu_pc_umx` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; maximum of long-term monthly climatology |
| `inu_pc_vlt` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area |
| `inu_pc_ult` | int16 | Floodplain inundation fraction (%) combining bankfull channel and seasonal flood extent following HydroATLAS v1.0 Table 5 (Lehner et al., 2019).; units: percent of the referenced area; entire upstream area aggregate; latest available snapshot (~2010 baseline) |
| `lka_pc_vse` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area |
| `lka_pc_use` | int16 | Share of the reporting unit covered by lakes and reservoirs (%) from GLWD classes 1–11 (HydroATLAS v1.0 Table 5).; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `lkv_mc_usu` | int32 | Combined natural lake and reservoir volume (10^6 m³) sourced from HydroLAKES/GRanD per HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `rev_mc_usu` | int32 | Managed reservoir storage volume (10^6 m³) derived from GRanD v1.3, summarized as in HydroATLAS v1.0 Table 5.; units: million cubic meters; entire upstream area aggregate; total sum/extent |
| `dor_pc_pva` | int16 | Degree of regulation (%) = upstream reservoir storage / mean annual discharge (Lehner et al., 2014); HydroATLAS v1.0 Table 5.; units: percent of the referenced area; pour-point statistic (network outlet) |
| `gwt_cm_vav` | int16 | Depth to groundwater table (cm) from Fan et al. 2013 global product, averaged within each reporting unit (HydroATLAS v1.0 Table 6).; units: centimeters |
| `ele_mt_lav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters |
| `ele_mt_uav` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters; entire upstream area aggregate; area-weighted average |
| `ele_mt_lmn` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters |
| `ele_mt_vmx` | int16 | Mean surface elevation (m) based on GMTED2010 at 7.5 arc-second resolution (HydroATLAS v1.0 Table 3).; units: meters |
| `slp_dg_vav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees |
| `slp_dg_uav` | int16 | Mean surface slope (degrees) calculated from GMTED2010 DEM derivatives (HydroATLAS v1.0 Table 3).; units: degrees; entire upstream area aggregate; area-weighted average |
| `sgr_dk_vav` | int16 | Average stream gradient (m/km) computed along HydroRIVERS centerlines (HydroATLAS v1.0 Table 4).; units: m/km (slope or gradient) |
| `clz_cl_lmj` | int16 | Categorical codes; decode via sheet 'clz_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cls_cl_lmj` | int16 | Categorical codes; decode via sheet 'cls_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tmp_dc_lyr` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_uyr` | int16 | Near-surface air temperature; units: °C; entire upstream area aggregate; long-term annual mean |
| `tmp_dc_lmn` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_lmx` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l01` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l02` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l03` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l04` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l05` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l06` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l07` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l08` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l09` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l10` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l11` | int16 | Near-surface air temperature; units: °C |
| `tmp_dc_l12` | int16 | Near-surface air temperature; units: °C |
| `pre_mm_lyr` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_uyr` | int16 | Precipitation accumulation; units: mm; entire upstream area aggregate; long-term annual mean |
| `pre_mm_l01` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l02` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l03` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l04` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l05` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l06` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l07` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l08` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l09` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l10` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l11` | int16 | Precipitation accumulation; units: mm |
| `pre_mm_l12` | int16 | Precipitation accumulation; units: mm |
| `pet_mm_lyr` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_uyr` | int16 | Potential evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `pet_mm_l01` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l02` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l03` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l04` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l05` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l06` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l07` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l08` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l09` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l10` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l11` | int16 | Potential evapotranspiration; units: mm |
| `pet_mm_l12` | int16 | Potential evapotranspiration; units: mm |
| `aet_mm_vyr` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_uyr` | int16 | Actual evapotranspiration; units: mm; entire upstream area aggregate; long-term annual mean |
| `aet_mm_v01` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v02` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v03` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v04` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v05` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v06` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v07` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v08` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v09` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v10` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v11` | int16 | Actual evapotranspiration; units: mm |
| `aet_mm_v12` | int16 | Actual evapotranspiration; units: mm |
| `ari_ix_lav` | int16 | units: dimensionless index |
| `ari_ix_uav` | int16 | units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `cmi_ix_lyr` | int16 | units: dimensionless index |
| `cmi_ix_uyr` | int16 | units: dimensionless index; entire upstream area aggregate; long-term annual mean |
| `cmi_ix_l01` | int16 | units: dimensionless index |
| `cmi_ix_l02` | int16 | units: dimensionless index |
| `cmi_ix_l03` | int16 | units: dimensionless index |
| `cmi_ix_l04` | int16 | units: dimensionless index |
| `cmi_ix_l05` | int16 | units: dimensionless index |
| `cmi_ix_l06` | int16 | units: dimensionless index |
| `cmi_ix_l07` | int16 | units: dimensionless index |
| `cmi_ix_l08` | int16 | units: dimensionless index |
| `cmi_ix_l09` | int16 | units: dimensionless index |
| `cmi_ix_l10` | int16 | units: dimensionless index |
| `cmi_ix_l11` | int16 | units: dimensionless index |
| `cmi_ix_l12` | int16 | units: dimensionless index |
| `snw_pc_vyr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_uyr` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `snw_pc_vmx` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v01` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v02` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v03` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v04` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v05` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v06` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v07` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v08` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v09` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v10` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v11` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `snw_pc_v12` | int16 | Fraction of time with snow cover (%) from MODIS MOD10A1 climatology aggregated as in HydroATLAS v1.0 Table 2.; units: percent of the referenced area |
| `glc_cl_vmj` | int16 | Categorical codes; decode via sheet 'glc_cl' in HydroATLAS_v10_Legends.xlsx. |
| `glc_pc_v01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_v22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `glc_pc_u01` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `glc_pc_u02` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `glc_pc_u03` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `glc_pc_u04` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `glc_pc_u05` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `glc_pc_u06` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `glc_pc_u07` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `glc_pc_u08` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `glc_pc_u09` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `glc_pc_u10` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `glc_pc_u11` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `glc_pc_u12` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `glc_pc_u13` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `glc_pc_u14` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `glc_pc_u15` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `glc_pc_u16` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 16 (see legend workbook) |
| `glc_pc_u17` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 17 (see legend workbook) |
| `glc_pc_u18` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 18 (see legend workbook) |
| `glc_pc_u19` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 19 (see legend workbook) |
| `glc_pc_u20` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 20 (see legend workbook) |
| `glc_pc_u21` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 21 (see legend workbook) |
| `glc_pc_u22` | int16 | GLC2000 land-cover class fractions (%) describing the reporting unit (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 22 (see legend workbook) |
| `pnv_cl_vmj` | int16 | Categorical codes; decode via sheet 'pnv_cl' in HydroATLAS_v10_Legends.xlsx. |
| `pnv_pc_v01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_v15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `pnv_pc_u01` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `pnv_pc_u02` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `pnv_pc_u03` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `pnv_pc_u04` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `pnv_pc_u05` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `pnv_pc_u06` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `pnv_pc_u07` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `pnv_pc_u08` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `pnv_pc_u09` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `pnv_pc_u10` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for October |
| `pnv_pc_u11` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for November |
| `pnv_pc_u12` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for December |
| `pnv_pc_u13` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 13 (see legend workbook) |
| `pnv_pc_u14` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 14 (see legend workbook) |
| `pnv_pc_u15` | int16 | Potential natural vegetation class fractions from EarthStat (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; classification bin 15 (see legend workbook) |
| `wet_cl_vmj` | int16 | Categorical codes; decode via sheet 'wet_cl' in HydroATLAS_v10_Legends.xlsx. |
| `wet_pc_vg1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_ug1` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 1 (permanent wetlands) |
| `wet_pc_vg2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_ug2` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; GLWD class group 2 (seasonal wetlands) |
| `wet_pc_v01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_v09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `wet_pc_u01` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for January |
| `wet_pc_u02` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for February |
| `wet_pc_u03` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for March |
| `wet_pc_u04` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for April |
| `wet_pc_u05` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for May |
| `wet_pc_u06` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for June |
| `wet_pc_u07` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for July |
| `wet_pc_u08` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; climatological mean for August |
| `wet_pc_u09` | int16 | Wetland class fractions (%) based on GLWD classes (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; value circa 2009 |
| `for_pc_vse` | int16 | Tree/forest cover share; units: percent of the referenced area |
| `for_pc_use` | int16 | Tree/forest cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `crp_pc_vse` | int16 | Cropland share; units: percent of the referenced area |
| `crp_pc_use` | int16 | Cropland share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pst_pc_vse` | int16 | Pasture share; units: percent of the referenced area |
| `pst_pc_use` | int16 | Pasture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ire_pc_vse` | int16 | Irrigated area share; units: percent of the referenced area |
| `ire_pc_use` | int16 | Irrigated area share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `gla_pc_vse` | int16 | Glacier cover share; units: percent of the referenced area |
| `gla_pc_use` | int16 | Glacier cover share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `prm_pc_vse` | int16 | Permanent water share; units: percent of the referenced area |
| `prm_pc_use` | int16 | Permanent water share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `pac_pc_lse` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area |
| `pac_pc_use` | int16 | Rainfed/paddy agriculture share; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `tbi_cl_lmj` | int16 | Categorical codes; decode via sheet 'tbi_cl' in HydroATLAS_v10_Legends.xlsx. |
| `tec_cl_lmj` | int16 | Categorical codes; decode via sheet 'tec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fmh_cl_lmj` | int16 | Categorical codes; decode via sheet 'fmh_cl' in HydroATLAS_v10_Legends.xlsx. |
| `fec_cl_lmj` | int16 | Categorical codes; decode via sheet 'fec_cl' in HydroATLAS_v10_Legends.xlsx. |
| `cly_pc_vav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `cly_pc_uav` | int16 | Topsoil clay fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `slt_pc_vav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `slt_pc_uav` | int16 | Topsoil silt fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `snd_pc_vav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `snd_pc_uav` | int16 | Topsoil sand fraction (%) from SoilGrids (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; area-weighted average |
| `soc_th_vav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare |
| `soc_th_uav` | int16 | Soil organic carbon stock (t/ha) from ISRIC SoilGrids aggregated by HydroATLAS (Table 6).; units: tonnes per hectare; entire upstream area aggregate; area-weighted average |
| `swc_pc_vyr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_uyr` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area; entire upstream area aggregate; long-term annual mean |
| `swc_pc_v01` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v02` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v03` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v04` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v05` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v06` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v07` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v08` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v09` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v10` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v11` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `swc_pc_v12` | int16 | Volumetric soil-water content (%) from GLDAS/Noah climatology (HydroATLAS v1.0 Table 6).; units: percent of the referenced area |
| `lit_cl_vmj` | int16 | Categorical codes; decode via sheet 'lit_cl' in HydroATLAS_v10_Legends.xlsx. |
| `kar_pc_vse` | int16 | Karst proportion; units: percent of the referenced area |
| `kar_pc_use` | int16 | Karst proportion; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `ero_kh_vav` | int32 | Soil erosion rate |
| `ero_kh_uav` | int32 | Soil erosion rate; entire upstream area aggregate; area-weighted average |
| `urb_pc_vse` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area |
| `urb_pc_use` | int16 | Urban land fraction (%) from GlobCover 2009 resampled for HydroATLAS v1.0 Table 7.; units: percent of the referenced area; entire upstream area aggregate; fractional share/extent |
| `nli_ix_vav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index |
| `nli_ix_uav` | int16 | Nighttime lights index from VIIRS/DMSP stable lights (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; area-weighted average |
| `rdd_mk_vav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7. |
| `rdd_mk_uav` | int32 | Road density (km per 100 km²) from gROADS v1 aggregated by HydroATLAS v1.0 Table 7.; entire upstream area aggregate; area-weighted average |
| `hft_ix_v93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index |
| `hft_ix_u93` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 1993 |
| `hft_ix_v09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index |
| `hft_ix_u09` | int16 | Human Footprint Index (dimensionless, 1993 or 2009) from Venter et al. 2016 (HydroATLAS v1.0 Table 7).; units: dimensionless index; entire upstream area aggregate; value circa 2009 |
| `gad_id_lmj` | int16 | Administrative identifier (GAUL / GADM cross-walk) |
| `gdp_ud_vav` | int32 | Gross domestic product per capita (constant 2011 PPP USD) from World Bank/SEDAC grids aggregated as in HydroATLAS v1.0 Table 7.; units: US dollars (constant PPP, per capita) |
| `hdi_ix_vav` | int16 | UNDP Human Development Index (2013) averaged over each reporting unit (HydroATLAS v1.0 Table 7).; units: dimensionless index |


## HSWUD domestic water use (monthly, 1965–2022)

Data source: `/Users/snowfay/CF_calculate/data/water use data/27610524/HSWUD_dom.nc`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/water use data/27610524/state.md`

### Layer: HSWUD_dom

- Driver: `NetCDF`

Additional info:
- Dimensions: time=696, lat=355, lon=615

| Field | Type | Meaning |
| --- | --- | --- |
| `dom` | float64 dims=(time, lat, lon) | Monthly domestic water use withdrawals (10^8 m³) from HSWUD dataset.; China monthly domestic water use; units: 10^8 cubic meters |


## HSWUD electricity sector water use

Data source: `/Users/snowfay/CF_calculate/data/water use data/27610524/HSWUD_ele.nc`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/water use data/27610524/state.md`

### Layer: HSWUD_ele

- Driver: `NetCDF`

Additional info:
- Dimensions: time=696, lat=355, lon=615

| Field | Type | Meaning |
| --- | --- | --- |
| `ele` | float64 dims=(time, lat, lon) | Monthly thermoelectric water withdrawals (10^8 m³) from HSWUD dataset. |


## HSWUD irrigation water use

Data source: `/Users/snowfay/CF_calculate/data/water use data/27610524/HSWUD_irr_.nc`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/water use data/27610524/state.md`

### Layer: HSWUD_irr_

- Driver: `NetCDF`

Additional info:
- Dimensions: time=696, lat=355, lon=615

| Field | Type | Meaning |
| --- | --- | --- |
| `irr` | float64 dims=(time, lat, lon) | Monthly irrigation water withdrawals (10^8 m³) from HSWUD dataset.; Monthly china irrigation water use; units: 10^8 cubic meters |


## HSWUD manufacturing water use

Data source: `/Users/snowfay/CF_calculate/data/water use data/27610524/HSWUD_manu.nc`

Supporting docs:
- `/Users/snowfay/CF_calculate/data/water use data/27610524/state.md`

### Layer: HSWUD_manu

- Driver: `NetCDF`

Additional info:
- Dimensions: time=696, lat=355, lon=615

| Field | Type | Meaning |
| --- | --- | --- |
| `manu` | float64 dims=(time, lat, lon) | Monthly manufacturing water use withdrawals (10^8 m³) from HSWUD dataset.; China monthly manufacture water use; units: 10^8 cubic meters |

