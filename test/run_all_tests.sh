SERVER_HOST=10.0.22.245
for variant in "B_SZZ" "R_SZZ"; do
    for usercount in 1 20; do
        m_dir="./results/$variant/rate_$usercount"
        mkdir -p "$m_dir"
        for run in $(seq 1 30); do
            if test "$SERVER_HOST" != "localhost" ; then
                sh reset_server.sh
            fi
            sh run_experiment.sh -r $run -c $usercount -v $variant -h $SERVER_HOST
            new_file_name="report_${VARIANT}_rate_${USER_COUNT}_run_${RUN}_stats.json"
            cp "./reports_${VARIANT}_rate_${USER_COUNT}_run_${RUN}/statistics.json" "$m_dir/$new_file_name"
        done
    done
done