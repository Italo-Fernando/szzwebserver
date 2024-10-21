RESET_SERVER=${1:-false}
HOST=${2:-localhost}
sh clean_test_result.sh
for variant in "B_SZZ" "R_SZZ"; do
    for usercount in 1 20; do
        for run in $(seq 1 30); do
            if test "${RESET_SERVER}" = true; then
                sh reset_server.sh
            fi
            sh run_experiment.sh -r $run -c $usercount -v $variant -h $HOST
        done
    done
done