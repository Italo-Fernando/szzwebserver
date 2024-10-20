curl -X 'POST' \
  'http://127.0.0.1:5000/szz/fix_commits' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "szz_variant": "R_SZZ",
  "repository_url": "https://github.com/gpac/gpac",
  "fix_commit_hash": [
    "588ce9b1dade5e7db703fb9af603184a09ae4494"
  ]
}'