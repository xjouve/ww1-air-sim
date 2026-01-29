# Source Data

This directory contains source data for building the WW1 Air Simulation scenery.

## Data Categories

### Committed to Git (text-based, lightweight)

| Directory | Description | Status |
|-----------|-------------|--------|
| `campaigns/` | Mission types, aces, targets | ✓ Committed |
| `frontlines/` | Front line positions by period (GeoJSON) | ✓ Committed |

### Not Committed (binary, download separately)

| Directory | Description | Size | Source |
|-----------|-------------|------|--------|
| `elevation/` | SRTM GL1 terrain elevation | ~264 MB | USGS EarthExplorer |
| `hydrography/` | Waterways, lakes, rivers | ~276 MB | OpenStreetMap + historical |
| `infrastructure/` | Villages, roads, railways | ~617 MB | OpenStreetMap |
| `landcover/` | Land use classification | ~546 MB | OpenStreetMap |

## Download Instructions

### 1. Elevation Data (SRTM)

**Source**: [USGS EarthExplorer](https://earthexplorer.usgs.gov/) or [OpenTopography](https://opentopography.org/)

**Tiles needed** (1 arc-second resolution):
- N47E001 through N47E008
- N48E001 through N48E008
- N49E001 through N49E008
- N50E001 through N50E008
- N51E001 through N51E008

**Coverage**: Belgium, Northern France, Western Germany (47°N-52°N, 1°E-9°E)

**Format**: `.hgt` or `.hgt.zip` files

**Destination**: `src/elevation/`

### 2. OpenStreetMap Data

**Source**: [Geofabrik](https://download.geofabrik.de/europe.html)

**Regions needed**:
- [Belgium](https://download.geofabrik.de/europe/belgium.html) - `.shp.zip`
- [Nord-Pas-de-Calais](https://download.geofabrik.de/europe/france/nord-pas-de-calais.html) - `.shp.zip`
- [Picardie](https://download.geofabrik.de/europe/france/picardie.html) - `.shp.zip`
- [Champagne-Ardenne](https://download.geofabrik.de/europe/france/champagne-ardenne.html) - `.shp.zip`
- [Lorraine](https://download.geofabrik.de/europe/france/lorraine.html) - `.shp.zip`
- [Alsace](https://download.geofabrik.de/europe/france/alsace.html) - `.shp.zip`

**Shapefiles to extract**:

| Shapefile | Category | Destination |
|-----------|----------|-------------|
| `gis_osm_waterways_free_1.*` | Hydrography | `src/hydrography/osm/{region}/` |
| `gis_osm_water_a_free_1.*` | Hydrography | `src/hydrography/osm/{region}/` |
| `gis_osm_landuse_a_free_1.*` | Landcover | `src/landcover/osm/{region}/` |
| `gis_osm_places_free_1.*` | Settlements | `src/infrastructure/settlements/{region}/` |
| `gis_osm_roads_free_1.*` | Roads | `src/infrastructure/roads/{region}/` |
| `gis_osm_railways_free_1.*` | Railways | `src/infrastructure/railways/{region}/` |

### 3. Historical Corrections

These files contain manual corrections not available in modern GIS data:

**Hydrography corrections** (`src/hydrography/historical/`):
- Remove post-1918 water features (e.g., Lac de l'Ailette)
- Add 1914 flood zones (e.g., Yser inundation)

**Source**: Manual digitization from historical maps and archives.

## Build Pipeline

Once source data is in place, run:

```bash
python tools/scripts/build_all.py
```

This will:
1. Process elevation data → `build/terrain/*.bgl`
2. Generate landcover → `build/landcover/*.lcf`
3. Process hydrography → `build/hydrography/*.bgl`
4. Compile campaign data → `build/campaign/*`

See `docs/architecture/README.md` for detailed pipeline documentation.
