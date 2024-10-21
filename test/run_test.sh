RUN="${1:-0}"
jmeter -n -t ./SzzWebServer.jmx -l report_${RUN}.csv -e -o ./reports_${RUN}/ -q ./jmeter.properties