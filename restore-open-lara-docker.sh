#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 /path/to/open-lara-docker-browser.tar.gz" >&2
    exit 2
fi

archive="$1"

echo "This restores to /mnt/storage1/docker-compose/open-lara."
echo "It can overwrite an existing deployment. Review the archive first:"
echo "  tar -tzf \"$archive\" | head"
echo
echo "Restore command:"
echo "  tar --acls --xattrs --numeric-owner -xzf \"$archive\" -C /"
