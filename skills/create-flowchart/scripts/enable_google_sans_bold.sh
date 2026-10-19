#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <rendered-svg>" >&2
  exit 2
fi

svg_path=$1

if [[ ! -f "$svg_path" ]]; then
  echo "SVG not found: $svg_path" >&2
  exit 2
fi

if ! rg -q '\.text-bold \{' "$svg_path"; then
  echo "No D2 bold-text class found in: $svg_path" >&2
  exit 1
fi

perl -0pi -e 's/(\.d2-([0-9]+) \.text-bold \{\s*)font-family: "[^"]+";/$1font-family: "d2-$2-font-regular";\n\tfont-weight: 700;\n\tfont-variation-settings: "wght" 700;/s' "$svg_path"

if ! rg -q 'font-variation-settings: "wght" 700' "$svg_path"; then
  echo "Could not apply Google Sans bold variation to: $svg_path" >&2
  exit 1
fi
