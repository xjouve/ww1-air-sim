# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WW1 Air Simulation — a World War I combat flight simulator mod for CFS3 (Combat Flight Simulator 3), focused on the Western Front. The project prioritizes historical and geographic realism: precise village locations, roads, waterways, day-by-day frontline evolution based on unit war diaries (JMO), and historically accurate mission types per nation.

Maintained by Xavier Jouve. GitHub: `xjouve/ww1-air-sim`.

## Repository Structure

```
ww1-air-sim/
├── src/                    # Source data (versioned, editable)
│   ├── elevation/          # SRTM .hgt files
│   ├── hydrography/        # Waterways (OSM + historical corrections)
│   ├── landcover/          # Land classification (Corine/OSM)
│   ├── infrastructure/     # Villages, roads, railways, airfields
│   ├── frontlines/         # Front line snapshots by date (GeoJSON)
│   └── campaigns/          # Missions, aces, squadrons, targets
│
├── tools/                  # Build tools
│   ├── cfstmap/            # Terrain compiler (cfsTmap, SCASM, sclink)
│   ├── landclass/          # Landcover converter (tiff2lcf)
│   ├── water/              # Hydrography processor
│   └── scripts/            # Python build scripts
│
├── build/                  # Compiled outputs (generated, gitignored)
│   ├── terrain/            # BGL mesh files
│   ├── landcover/          # LCF files by period
│   ├── hydrography/        # Water BGL
│   ├── maps/               # DDS map backgrounds
│   └── campaign/           # CFS3-formatted campaign data
│
├── dist/                   # Distribution packages
├── sim/                    # Simulation configuration
│   ├── simulation.xml      # AI/combat parameters (v0.4)
│   ├── pilotconstants.xml  # Pilot skills, vision, G-tolerance
│   └── aircraft/           # Aircraft configs (.xdp)
│
├── docs/                   # Documentation
│   ├── architecture/       # Architecture docs
│   ├── historical/         # WWI doctrine documents (French)
│   └── tutorials/          # Theater creation tutorials
│
├── config.yaml             # Centralized build configuration
└── archive/                # Old WOFF-XJ structure (reference)
```

## Configuration

All build parameters are centralized in `config.yaml`:
- Terrain resolution and quality
- Landcover source (Corine vs 2GIS)
- Periods to generate (1914, 1915, ..., 1918+9)
- Historical corrections (flood zones, removed modern features)
- Active nations and campaign settings

## Build System

```bash
# Build everything
python tools/scripts/build_all.py

# Build specific layers
python tools/scripts/build_all.py --layer=terrain,landcover

# Build specific periods
python tools/scripts/build_all.py --periods=1917,1918

# Build with quality setting
python tools/scripts/build_all.py --quality=high
```

## Key Tools

| Tool | Location | Purpose |
|------|----------|---------|
| cfsTmap.exe | tools/cfstmap/ | Terrain mesh editor (GUI) |
| scasm.exe | tools/cfstmap/ | SCASM scenery compiler |
| sclink.exe | tools/cfstmap/ | BGL linker |
| tiff2lcf | tools/landclass/ | TIFF → LCF converter |
| water.exe | tools/water/ | Hydrography processor |
| build_all.py | tools/scripts/ | Master build script |

## Data Formats

### Source formats
| Format | Description |
|--------|-------------|
| .hgt | SRTM elevation data |
| .shp/.dbf/.shx | ESRI Shapefiles (GIS) |
| .geojson | Frontlines, corrections |

### CFS3 output formats
| Format | Layer | Description |
|--------|-------|-------------|
| .msh | Terrain | Mesh tiles in zip archives |
| .cel | Water | Hydrography cells + index |
| .lcf | Landcover | Land classification |
| .bgl | Scenery | 3D objects (buildings, roads) |
| .xdp | Aircraft | Configuration (XML) |

## Simulation Configuration (v0.4)

The `sim/simulation.xml` file controls AI combat behavior. Key v0.4 changes for historical realism:
- `fightThreshold=5`: AI requires significant advantage to engage (rare combats)
- `withdrawThreshold=3`: AI breaks off quickly (brief engagements)
- `soloWt=-5`: No lone pursuit (formation cohesion)
- `Vrille` as default substitute: Failed maneuvers → defensive spin
- `SHOOTING_RANGE=75m`: Point-blank fire doctrine

## Historical Corrections

The project includes historical corrections not found in modern GIS data:
- **Removed**: Post-1918 lakes (e.g., Lac de l'Ailette north of Chemin des Dames)
- **Added**: 1914 Yser flood zone (Belgian/French defensive flooding)
- **Frontlines**: Day-by-day evolution from JMO (Journaux des Marches et Opérations)

## Layer Architecture

```
Campaign (missions, targets, aces)     ← src/campaigns/
         ↓
Frontlines (by date)                   ← src/frontlines/
         ↓
Infrastructure (villages, roads)       ← src/infrastructure/
         ↓
Maps (visual background)               ← build/maps/
         ↓
Hydrography (waterways)                ← src/hydrography/
         ↓
Landcover (forests, fields)            ← src/landcover/
         ↓
Terrain (elevation mesh)               ← src/elevation/
```

## Legacy Structure

The old scattered mod structure (WOFF - XJ0 through XJ5) is preserved in `archive/` for reference. The new unified architecture eliminates redundancy and provides reproducible builds.
