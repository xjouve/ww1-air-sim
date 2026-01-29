#!/usr/bin/env python3
"""
Convertit les fichiers Frontlines.txt (format CFS3) en GeoJSON.

Format d'entrée (CFS3 Frontlines.txt):
<FrontLine>
  <Point Lat="N51*7'36.4800" Lon="E2*44'34.11600"/>
  ...
</FrontLine>

Format de sortie (GeoJSON):
{
  "type": "Feature",
  "properties": { "period": "1917" },
  "geometry": {
    "type": "LineString",
    "coordinates": [[lon, lat], ...]
  }
}
"""

import re
import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
FRONTLINES_DIR = PROJECT_ROOT / "src" / "frontlines"


def parse_dms(dms_str):
    """
    Parse une coordonnée DMS (Degrees Minutes Seconds) vers décimal.
    Format: N51*7'36.4800" ou E2*44'34.11600"
    """
    # Pattern: direction + degrés * minutes ' secondes "
    pattern = r'([NSEW])(\d+)\*(\d+)\'([\d.]+)"?'
    match = re.match(pattern, dms_str)

    if not match:
        raise ValueError(f"Cannot parse DMS: {dms_str}")

    direction, degrees, minutes, seconds = match.groups()

    decimal = float(degrees) + float(minutes) / 60 + float(seconds) / 3600

    if direction in ('S', 'W'):
        decimal = -decimal

    return decimal


def parse_frontline_txt(filepath):
    """
    Parse un fichier Frontlines.txt et retourne une liste de coordonnées [lon, lat].
    """
    coordinates = []

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Trouver tous les points
    point_pattern = r'<Point\s+Lat="([^"]+)"\s+Lon="([^"]+)"'
    matches = re.findall(point_pattern, content)

    for lat_dms, lon_dms in matches:
        try:
            lat = parse_dms(lat_dms)
            lon = parse_dms(lon_dms)
            coordinates.append([lon, lat])  # GeoJSON: [longitude, latitude]
        except ValueError as e:
            print(f"  Warning: {e}")

    return coordinates


def convert_to_geojson(coordinates, period):
    """
    Convertit une liste de coordonnées en GeoJSON Feature.
    """
    return {
        "type": "Feature",
        "properties": {
            "period": period,
            "description": f"Front line position for period {period}"
        },
        "geometry": {
            "type": "LineString",
            "coordinates": coordinates
        }
    }


def main():
    print("=" * 60)
    print("Frontlines CFS3 -> GeoJSON Converter")
    print("=" * 60)

    if not FRONTLINES_DIR.exists():
        print(f"Error: {FRONTLINES_DIR} not found")
        return

    converted = 0

    for period_dir in sorted(FRONTLINES_DIR.iterdir()):
        if not period_dir.is_dir():
            continue

        frontline_txt = period_dir / "Frontlines.txt"
        if not frontline_txt.exists():
            continue

        period = period_dir.name
        print(f"\nProcessing: {period}")

        # Parse le fichier CFS3
        coordinates = parse_frontline_txt(frontline_txt)
        print(f"  Points found: {len(coordinates)}")

        if len(coordinates) < 2:
            print(f"  Skipping: not enough points")
            continue

        # Convertir en GeoJSON
        geojson = convert_to_geojson(coordinates, period)

        # Écrire le fichier GeoJSON
        output_file = period_dir / f"frontline_{period.replace('+', '_plus_')}.geojson"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, indent=2)

        print(f"  Output: {output_file.name}")
        converted += 1

    print(f"\n{'=' * 60}")
    print(f"Converted {converted} frontline files to GeoJSON")
    print("=" * 60)


if __name__ == "__main__":
    main()
