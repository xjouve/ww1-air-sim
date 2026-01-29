# Architecture du projet WW1 Air Simulation

## Vue d'ensemble

Ce projet est une simulation de combat aérien de la Première Guerre mondiale sur le front de l'Ouest, basée sur le moteur CFS3 (Combat Flight Simulator 3). L'objectif est d'atteindre un niveau de réalisme historique et géographique maximal.

## Structure du dépôt

```
ww1-air-sim/
├── src/                    # Données sources (versionnées)
├── tools/                  # Outils de compilation
├── build/                  # Sorties compilées (générées)
├── dist/                   # Packages distribuables
├── sim/                    # Configuration simulation
├── docs/                   # Documentation
├── archive/                # Anciens mods (référence)
└── config.yaml             # Configuration centralisée
```

## Couches de données (Layers)

Le système utilise une architecture en couches superposées :

```
┌─────────────────────────────────────────┐
│  Campagne (missions, cibles, as)        │  ← src/campaigns/
├─────────────────────────────────────────┤
│  Lignes de front (par date)             │  ← src/frontlines/
├─────────────────────────────────────────┤
│  Infrastructure (villages, routes, aérodromes) │  ← src/infrastructure/
├─────────────────────────────────────────┤
│  Cartes (fond de carte visuel)          │  ← build/maps/
├─────────────────────────────────────────┤
│  Hydrographie (cours d'eau, lacs)       │  ← src/hydrography/
├─────────────────────────────────────────┤
│  Landcover (forêts, champs, urbain)     │  ← src/landcover/
├─────────────────────────────────────────┤
│  Terrain (élévation)                    │  ← src/elevation/
└─────────────────────────────────────────┘
```

## Sources de données

### Élévation (Terrain)
- **Source** : SRTM GL1 (Shuttle Radar Topography Mission)
- **Résolution** : 1 arc-seconde (~30m)
- **Format source** : `.hgt` (Height files)
- **Couverture** : N47-N51, E001-E006 (Belgique, Nord de la France, Alsace)

### Hydrographie
- **Source principale** : OpenStreetMap (waterways)
- **Corrections historiques** :
  - Suppression des lacs/réservoirs post-1918 (ex: Lac de l'Ailette)
  - Ajout des zones d'inondation de 1914 (Yser)
- **Format** : GeoJSON, Shapefiles

### Landcover (Classification terrain)
- **Sources** :
  - Corine Land Cover (CLC) - classification européenne standardisée
  - OpenStreetMap landuse
- **Périodes** : 11 périodes distinctes (1914 à 1918+9)
- **Format sortie** : `.lcf` (CFS3 Landcover File)

### Infrastructure
- **Villages/Villes** : OSM places + corrections historiques
- **Routes** : OSM roads (primaires et secondaires)
- **Chemins de fer** : OSM railways
- **Aérodromes** : Positions historiques issues des JMO

### Lignes de front
- **Source** : Reconstitution manuelle à partir des JMO (Journaux des Marches et Opérations)
- **Format** : GeoJSON avec dates ISO
- **Granularité** : Jour par jour pour les périodes de mouvement, snapshots espacés pour les périodes statiques

## Pipeline de compilation

```
src/elevation/*.hgt
       │
       ▼ [cfsTmap + SCASM]
build/terrain/*.bgl
       │
       ▼
src/landcover/* + landclasses.xml
       │
       ▼ [tiff2lcf]
build/landcover/*/*.lcf
       │
       ▼
src/hydrography/*.shp
       │
       ▼ [water.exe + shorelines.exe]
build/hydrography/*.bgl
       │
       ▼
src/campaigns/* + src/frontlines/*
       │
       ▼ [build_campaign.py]
build/campaign/*
       │
       ▼ [packaging]
dist/*.zip
```

## Configuration

Le fichier `config.yaml` à la racine centralise tous les paramètres :

- Résolution et qualité du terrain
- Source du landcover (Corine vs 2GIS)
- Périodes à générer
- Corrections historiques à appliquer
- Nations actives dans la campagne
- Chemins des outils

## Formats CFS3

| Extension | Description | Outil de génération |
|-----------|-------------|---------------------|
| `.bgl` | Binary scenery (terrain, hydrographie) | SCASM/sclink |
| `.lcf` | Landcover classification | tiff2lcf |
| `.dds` | Textures (cartes, eau) | Conversion image |
| `.xdp` | Configuration avion (XML) | Manuel |
| `.xml` | Configuration simulation | Manuel |

## Principes de conception

### 1. Séparation source/compilé
Les données sources (`src/`) sont versionnées et éditables. Les sorties compilées (`build/`) sont régénérables à tout moment.

### 2. Configuration centralisée
Un seul fichier `config.yaml` contrôle toutes les options de build. Pas de duplication de variantes (fini les 8 versions de terrain).

### 3. Historicité maximale
- Lignes de front datées au jour près
- Corrections hydrographiques (pas de lacs modernes)
- Aérodromes positionnés selon les archives
- Types de missions fidèles à la doctrine de chaque nation

### 4. Reproductibilité
Les scripts Python dans `tools/scripts/` permettent de régénérer tout le contenu depuis les sources.

## Migration depuis l'ancienne structure

L'ancienne structure (WOFF - XJ0/XJ1/.../XJ5) est préservée dans `archive/` pour référence. La correspondance :

| Ancien | Nouveau |
|--------|---------|
| WOFF - XJ0 - Terrain | build/terrain/ |
| WOFF - XJ1 - Landcover | build/landcover/ |
| WOFF - XJ2 - Map | build/maps/ |
| WOFF - XJ3 - Water | build/hydrography/ |
| WOFF - XJ4 - Global layer | build/campaign/ |
| WOFF - XJ5 - France Campaign | src/campaigns/ |
