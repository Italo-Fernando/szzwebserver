curl -X 'POST' \
  'http:127.0.0.1:5000/szz/find_bug_commits/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "szz_variant": "B_SZZ",
  "repository_url": "url",
  "bugfix_commit_hash": [
    "123"
  ]
}'