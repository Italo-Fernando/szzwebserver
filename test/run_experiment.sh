cd $(dirname "$0")
HOST=localhost
RUN=0
USER_COUNT=1
VARIANT="B_SZZ"
while getopts "r:h:c:v:" opt
do
   case "$opt" in
      r ) RUN="$OPTARG" ;;
      h ) HOST="$OPTARG" ;;
      c ) USER_COUNT="$OPTARG" ;;
      v ) VARIANT="$OPTARG" ;;
      ? ) echo "option not found";; 
   esac
done

jmeter -n -t ./SzzWebServer.jmx -l ./reports_${VARIANT}_rate_${USER_COUNT}_run_${RUN}/samples.csv -e -o ./reports_${VARIANT}_rate_${USER_COUNT}_run_${RUN}/ -q ./jmeter.properties \
-Jhost=${HOST} -Jusercount=${USER_COUNT} -Jszzvariant=${VARIANT}
