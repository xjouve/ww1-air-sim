# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

WW1 Air Simulation content repository for "Wings Over Flanders Fields" (WOFF/OFF) — a World War I combat flight simulator. This is primarily a **data and content repository** (not a traditional software project) containing terrain meshes, landcover classifications, water layers, campaign maps, simulation configurations, and tooling for scenery creation.

Maintained by Xavier Jouve. GitHub: `xjouve/ww1-air-sim`.

## Repository Structure

The repository is organized into layered scenery packages (XJ series) and supporting tools:

- **`WOFF - XJ0 - Terrain`**: Elevation mesh data at various resolutions (1 arc-sec, 30 arc-sec) and quality tiers (hi, exhi, shi)
- **`WOFF - XJ1 - Landcover`**: Land classification layers (2GIS and Corine Land Cover variants)
- **`WOFF - XJ2 - Map`**: Campaign maps (B&W, Color, Etat Major historical; with/without frontlines)
- **`WOFF - XJ3 - Water`**: Regional water layers (Yser-Somme, Aisne-Velse, Meuse-Moselle, Bas-Haut-Rhin, Total)
- **`WOFF - XJ4 - Global layer`**: Integrated scenery layer combining all components with full campaign data (missions, aces, pilots, targets for 1914-1918 across Britain, Germany, France, USA)
- **`WOFF - XJ5 - France Campaign`**: France-specific campaign configuration

### Tools and Utilities

- **`cfstmap/`**: CfsTmap terrain editor — creates elevated mesh scenery from elevation data, compiles to BGL format via SCASM
  - `cfsTmap.exe` — terrain map editor (GUI)
  - `scasm.exe` — SCASM 2.39 scenery compiler (source → BGL)
  - `sclink.exe` — links multiple BGL files into a single BGL
- **`water/`**: Water feature processing from GIS shapefiles (`water.exe`, `shorelines.exe`)
- **`landclass/`**: Landcover classification tooling; uses `tiff2lcf` to convert TIFF raster data to LCF files using `landclasses.xml` definitions
- **`Map Simulator/`**: Windows WPF application (.NET 4.6.1) for interactive map visualization using GMap.NET, SQLite, and Entity Framework

### Data and Configuration

- **`Sim/OBDWW1 Over Flanders Fields/`**: Core simulation configs — `simulation.xml` (physics, damage, weapons) and `pilotconstants.xml` (pilot skills, vision, G-tolerance)
- **`Sim/.../aircraft/`**: Per-aircraft variant configs (e.g., `Alb_DVa_AC1`, `Fokker_DR1_AC2`)
- **`New_Theater/`**: Raw source data — SRTM elevation (.hgt.zip), DEM files, GIS shapefiles for Belgium/Picardy regions
- **`new-theater-kit/`**: Step-by-step tutorials (STEP 1-10.doc) for creating new simulation theaters
- **`docs/`**: French-language pilot tactics and operations guides (WWI-era doctrine)

## Key Tool Workflows

### Terrain Creation Pipeline
1. Source SRTM elevation data (`.hgt` files from `New_Theater/`)
2. Load into CfsTmap (`cfstmap/cfsTmap.exe`) to create terrain layouts
3. Compile via SCASM (`scasm.exe`) to produce BGL scenery files
4. Link multiple BGLs with `sclink.exe` (see `cfstmap/Arran/linkit.bat` for example)

### Landcover Generation
```
tiff2lcf <input.tif> <color-to-value.txt> <resolution> <size> landclasses.xml <output.lcf>
```
Example: `tiff2lcf test8RGBA.tif c2v.txt 1024000 1024 landclasses.xml test.lcf`

### Water Layer Processing
Uses `water/water.exe` and `water/shorelines.exe` with GIS shapefile inputs (`.shp/.dbf/.shx`).

## Data Formats

- **BGL**: Binary scenery format for Combat Flight Simulator engine
- **MTW**: Terrain map working files
- **LCF**: Landcover classification files
- **HGT**: SRTM elevation data (1 arc-second resolution)
- **SHP/DBF/SHX**: ESRI Shapefiles for geographic features
- **XML**: Simulation parameters, landcover class definitions, aircraft configs

## Architecture Notes

The scenery system uses a **layered composition model** — each XJ layer (0-5) is independently versioned and can be mixed. The layers stack: terrain mesh (XJ0) at the base, landcover (XJ1) on top, then water (XJ3), maps (XJ2), and the global integration layer (XJ4) ties everything together with campaign data. XJ5 adds region-specific campaign overrides.

Campaign data in XJ4 is organized by time period (1914-1918+) and nation, with separate configuration files for missions, pilot rosters, ace records, and ground targets per period.
