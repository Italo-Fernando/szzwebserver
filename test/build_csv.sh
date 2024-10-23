FILENAME="szz_experiments.csv"

echo "experimento,variante,req.por.seg,tempo_resposta,tempo_download,tempo_total" > "$FILENAME"

x_num=1
for variant in "B_SZZ" "R_SZZ"; do
    for rate in 1 20; do
        for run in $(seq 1 30); do  
            m_dir="./$variant/rate_$rate"
            tempo_resposta=$(grep -i meanrestime "${m_dir}/report_${variant}_rate_${rate}_run_${run}_stats.json" | head -n 1 | awk '{print $3}'| tr -d ',')
            tempo_download=$(cat "${m_dir}/download_${variant}_rate_${rate}_run_${run}.txt")
            tempo_total=$(cat "${m_dir}/totaltime_${variant}_rate_${rate}_run_${run}.txt")
            echo "$x_num,$variant,$rate,$tempo_resposta,$tempo_download,$tempo_total" >> "$FILENAME"
            x_num=$(($x_num+1))
        done
    done
done