#!/usr/bin/env bash
set -euo pipefail

source_project="${1:-/mnt/storage1/openlara-project}"
destination="$(cd "$(dirname "$0")/.." && pwd)/game"

for required in \
    "$source_project/OpenLara/bin/OpenLara-fixed" \
    "$source_project/OpenLara/bin/DATA/TITLE.PHD" \
    "$source_project/OpenLara/bin/FMV/CORE.RPL"
do
    if [ ! -e "$required" ]; then
        printf 'Required local file not found: %s\n' "$required" >&2
        exit 1
    fi
done

install -d "$destination/DATA" "$destination/FMV" "$destination/audio/1"

install -m 0755 \
    "$source_project/OpenLara/bin/OpenLara-fixed" \
    "$destination/OpenLara"

cp -a "$source_project/OpenLara/bin/DATA/." "$destination/DATA/"
cp -a "$source_project/OpenLara/bin/FMV/." "$destination/FMV/"
cp -a "$source_project/OpenLara/bin/audio/1/." "$destination/audio/1/"

printf 'Imported legal local game files into: %s\n' "$destination"
