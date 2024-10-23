SERVER_HOST=10.0.22.245
for variant in "B_SZZ" "R_SZZ"; do
    for usercount in 1 20; do
        m_dir="./results/$variant/rate_$usercount"
        mkdir -p "$m_dir"
        for run in $(seq 1 30); do
            if test "$SERVER_HOST" != "localhost" ; then
                # Reset server
                ssh -i ~/labsuser.pem ubuntu@10.0.22.245 '~/szzwebserver/start.sh'
                ssh -i ~/labsuser.pem ubuntu@10.0.22.245 'docker ps -a --format="table {{.Names}}\t{{.Status}}"'
                sleep 2
            fi

            # Run experiment and extract statistics
            sh run_experiment.sh -r $run -c $usercount -v $variant -h $SERVER_HOST
            new_file_name="report_${variant}_rate_${usercount}_run_${run}_stats.json"
            report_dir="./reports_${variant}_rate_${usercount}_run_${run}"
            cp "$report_dir/statistics.json" "$m_dir/$new_file_name"
            rm -rf "$report_dir"

            # Extract data from server
            if test "$SERVER_HOST" != "localhost" ; then
                sleep 2
                total_filename="totaltime_${variant}_rate_${usercount}_run_${run}.txt"
                download_filename="download_${variant}_rate_${usercount}_run_${run}.txt"
                scp -i ~/labsuser.pem ubuntu@10.0.22.245:~/szzwebserver/test/measures/total_* "$m_dir/$total_filename"
                scp -i ~/labsuser.pem ubuntu@10.0.22.245:~/szzwebserver/test/measures/download_* "$m_dir/$download_filename"
            fi
        done
    done
done