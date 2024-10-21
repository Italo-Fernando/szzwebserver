ssh -i ~/labsuser.pem ubuntu@10.0.22.245 '~/szzwebserver/start.sh'
ssh -i ~/labsuser.pem ubuntu@10.0.22.245 'docker ps -a --format="table {{.Names}}\t{{.Status}}"'
