#!/usr/bin/env python3
"""
WW1 Air Simulation - Script de build principal

Usage:
    python build_all.py [--quality=high] [--periods=all] [--layer=terrain,landcover,water,campaign]

Ce script orchestre la génération de toutes les couches du simulateur
depuis les données sources vers les formats CFS3.
"""

import argparse
import yaml
import os
import sys
from pathlib import Path

# Racine du projet (2 niveaux au-dessus de ce script)
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONFIG_FILE = PROJECT_ROOT / "config.yaml"


def load_config():
    """Charge la configuration depuis config.yaml"""
    if not CONFIG_FILE.exists():
        print(f"Erreur: {CONFIG_FILE} introuvable")
        sys.exit(1)

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def build_terrain(config, quality=None):
    """
    Génère le mesh terrain depuis les fichiers SRTM.

    Pipeline:
    1. Charger les fichiers .hgt depuis src/elevation/
    2. Créer les layouts CfsTmap
    3. Compiler via Terrain SDK
    4. Sortie vers build/terrain/*.msh (mesh tiles)

    Format sortie: CFS3Europe_*.msh dans archives zip
    """
    print("\n=== BUILD TERRAIN ===")
    terrain_cfg = config['terrain']
    quality = quality or terrain_cfg['quality']

    src_dir = PROJECT_ROOT / terrain_cfg['source_dir']
    out_dir = PROJECT_ROOT / terrain_cfg['output_dir']

    print(f"  Source: {src_dir}")
    print(f"  Output: {out_dir}")
    print(f"  Quality: {quality}")
    print(f"  Resolution: {terrain_cfg['resolution']}")

    # TODO: Implémenter l'appel à cfsTmap et SCASM
    # cfstmap_exe = PROJECT_ROOT / config['tools']['cfstmap']
    # scasm_exe = PROJECT_ROOT / config['tools']['scasm']
    # sclink_exe = PROJECT_ROOT / config['tools']['sclink']

    print("  [TODO] Implémentation pipeline terrain")


def build_landcover(config, periods=None):
    """
    Génère les fichiers LCF depuis les données de classification.

    Pipeline:
    1. Charger les données Corine/2GIS/OSM depuis src/landcover/
    2. Appliquer les corrections historiques par période
    3. Convertir via tiff2lcf
    4. Sortie vers build/landcover/{period}/
    """
    print("\n=== BUILD LANDCOVER ===")
    lc_cfg = config['landcover']
    periods = periods or lc_cfg['periods']

    src_dir = PROJECT_ROOT / lc_cfg['source_dir']
    out_dir = PROJECT_ROOT / lc_cfg['output_dir']

    print(f"  Source: {src_dir}")
    print(f"  Output: {out_dir}")
    print(f"  Periods: {periods}")
    print(f"  Classification source: {lc_cfg['source']}")

    # TODO: Implémenter l'appel à tiff2lcf
    # tiff2lcf_exe = PROJECT_ROOT / config['tools']['tiff2lcf']

    print("  [TODO] Implémentation pipeline landcover")


def build_hydrography(config):
    """
    Génère l'hydrographie depuis les shapefiles.

    Pipeline:
    1. Charger OSM waterways depuis src/hydrography/osm/
    2. Appliquer corrections historiques (retraits lacs modernes, ajout inondations)
    3. Fusionner dans src/hydrography/merged/
    4. Convertir via water.exe
    5. Sortie vers build/hydrography/*.cel (cellules eau + cells.idx)

    Format sortie: hyp*.cel files avec cells.idx index
    """
    print("\n=== BUILD HYDROGRAPHY ===")
    hydro_cfg = config['hydrography']

    src_dir = PROJECT_ROOT / hydro_cfg['source_dir']
    out_dir = PROJECT_ROOT / hydro_cfg['output_dir']

    print(f"  Source: {src_dir}")
    print(f"  Output: {out_dir}")
    print(f"  Historical corrections: {hydro_cfg['include_historical_corrections']}")

    if hydro_cfg['include_historical_corrections']:
        print("  Flood zones:")
        for fz in hydro_cfg.get('flood_zones', []):
            print(f"    - {fz['name']} ({fz['start_date']} to {fz['end_date']})")
        print("  Modern features to remove:")
        for rm in hydro_cfg.get('remove_modern', []):
            print(f"    - {rm['name']}")

    # TODO: Implémenter l'appel à water.exe
    # water_exe = PROJECT_ROOT / config['tools']['water']

    print("  [TODO] Implémentation pipeline hydrography")


def build_frontlines(config, periods=None):
    """
    Génère les lignes de front pour chaque période CFS3.

    Pipeline:
    1. Charger les snapshots GeoJSON datés depuis src/frontlines/
    2. Pour chaque période de sortie, interpoler le front à la date médiane
    3. Convertir au format CFS3 (Frontlines.txt)
    4. Sortie vers build/campaign/frontlines/{period}/
    """
    print("\n=== BUILD FRONTLINES ===")
    fl_cfg = config['frontlines']
    periods = periods or fl_cfg['output_periods']

    src_dir = PROJECT_ROOT / fl_cfg['source_dir']
    out_dir = PROJECT_ROOT / fl_cfg['output_dir']

    print(f"  Source: {src_dir}")
    print(f"  Output: {out_dir}")
    print(f"  Interpolation: {fl_cfg['interpolation']}")
    print(f"  Output periods: {periods}")

    # TODO: Implémenter l'interpolation et conversion

    print("  [TODO] Implémentation pipeline frontlines")


def build_campaign(config):
    """
    Génère les données de campagne (missions, cibles, as).

    Pipeline:
    1. Charger les missions depuis src/campaigns/missions/
    2. Charger les cibles depuis src/campaigns/targets/
    3. Charger les as depuis src/campaigns/aces/
    4. Formater pour CFS3
    5. Sortie vers build/campaign/
    """
    print("\n=== BUILD CAMPAIGN ===")
    camp_cfg = config['campaigns']

    src_dir = PROJECT_ROOT / camp_cfg['source_dir']
    out_dir = PROJECT_ROOT / camp_cfg['output_dir']

    print(f"  Source: {src_dir}")
    print(f"  Output: {out_dir}")
    print(f"  Nations:")
    for nation in camp_cfg['nations']:
        status = "active" if nation['active'] else "inactive"
        start = nation.get('start_period', '1914')
        print(f"    - {nation['name']} ({nation['code']}) [{status}, from {start}]")

    # TODO: Implémenter la génération de campagne

    print("  [TODO] Implémentation pipeline campaign")


def build_maps(config):
    """
    Génère les cartes de fond (DDS).

    Pipeline:
    1. Générer/convertir les images de carte
    2. Convertir en DDS
    3. Sortie vers build/maps/{style}/
    """
    print("\n=== BUILD MAPS ===")
    maps_cfg = config['maps']

    out_dir = PROJECT_ROOT / maps_cfg['output_dir']

    print(f"  Output: {out_dir}")
    print(f"  Styles:")
    for style in maps_cfg['styles']:
        status = "active" if style['active'] else "inactive"
        print(f"    - {style['name']}: {style['description']} [{status}]")

    # TODO: Implémenter la génération de cartes

    print("  [TODO] Implémentation pipeline maps")


def main():
    parser = argparse.ArgumentParser(
        description="WW1 Air Simulation - Build system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python build_all.py                     # Build tout avec config par défaut
  python build_all.py --quality=medium    # Build terrain en qualité moyenne
  python build_all.py --layer=terrain     # Build uniquement le terrain
  python build_all.py --periods=1917,1918 # Build uniquement certaines périodes
        """
    )

    parser.add_argument('--quality', choices=['low', 'medium', 'high', 'extra-high', 'super-high'],
                        help="Qualité du terrain")
    parser.add_argument('--periods', type=str,
                        help="Périodes à générer (comma-separated, ou 'all')")
    parser.add_argument('--layer', type=str,
                        help="Couches à générer (comma-separated: terrain,landcover,water,frontlines,campaign,maps)")
    parser.add_argument('--dry-run', action='store_true',
                        help="Afficher les actions sans les exécuter")

    args = parser.parse_args()

    print("=" * 60)
    print("WW1 Air Simulation - Build System")
    print("=" * 60)

    config = load_config()
    print(f"\nProjet: {config['project']['name']} v{config['project']['version']}")
    print(f"Auteur: {config['project']['author']}")

    # Déterminer les couches à builder
    if args.layer:
        layers = [l.strip() for l in args.layer.split(',')]
    else:
        layers = ['terrain', 'landcover', 'water', 'frontlines', 'campaign', 'maps']

    # Déterminer les périodes
    periods = None
    if args.periods and args.periods != 'all':
        periods = [p.strip() for p in args.periods.split(',')]

    # Exécuter les builds
    if 'terrain' in layers:
        build_terrain(config, args.quality)

    if 'landcover' in layers:
        build_landcover(config, periods)

    if 'water' in layers:
        build_hydrography(config)

    if 'frontlines' in layers:
        build_frontlines(config, periods)

    if 'campaign' in layers:
        build_campaign(config)

    if 'maps' in layers:
        build_maps(config)

    print("\n" + "=" * 60)
    print("Build terminé (squelette - implémentation à compléter)")
    print("=" * 60)


if __name__ == "__main__":
    main()
