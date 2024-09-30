curl -X 'GET' \
  "http://127.0.0.1:5000/szz/bug_commits/$1" \
  -H 'accept: application/json'

echo 'request_id='$1