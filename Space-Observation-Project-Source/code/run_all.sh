#!/bin/bash
# Chạy pipeline cho toàn bộ danh sách hành tinh trong data/targets.txt (tuần tự), log vào logs/
cd "$(dirname "$0")" && source ../.venv/bin/activate
mkdir -p ../logs
while IFS= read -r name <&3; do
  [ -z "$name" ] && continue
  slug=$(echo "$name" | tr -c 'A-Za-z0-9\n' '_' | sed -E 's/_+/_/g; s/^_//; s/_$//')
  echo "=== $name"
  if python 04_measure_planet.py "$name" --sectors 4 > "../logs/$slug.log" 2>&1 < /dev/null; then echo "ok   $name"; else echo "FAIL $name (xem logs/$slug.log)"; fi
done 3< ../data/targets.txt
