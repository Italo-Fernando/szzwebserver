curl -X 'POST' \
  'http://127.0.0.1:5000/szz/fix_commits' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "szz_variant": "R_SZZ",
  "repository_url": "https://github.com/SimpleServer/SimpleServer",
  "fix_commit_hash": [
    "8b16295318cd85c55b04e962479de1c6532a6759"
  ]
}'