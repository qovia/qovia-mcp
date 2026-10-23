#!/bin/sh
# Check your key (not charged), then search Xiaohongshu (RedNote) notes.
#   QOVIA_API_KEY=sk-qovia-... sh quickstart.sh
set -e
curl -s https://api.qovia.ai/v1/account -H "Authorization: Bearer $QOVIA_API_KEY"
echo
curl -s "https://api.qovia.ai/v1/raw/xiaohongshu/search?keyword=coffee&sort=latest" \
  -H "Authorization: Bearer $QOVIA_API_KEY"
echo
