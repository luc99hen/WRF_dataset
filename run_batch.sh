#!/bin/bash

start=2021-01-08
end=2021-01-09
while ! [[ "$start" > "$end" ]]; do
    next=$(date -d "$start + 1 day" +%F)
    start_month=$(echo $start | cut -d'-' -f2)
    start_day=$(echo $start | cut -d'-' -f3)
    end_month=$(echo $next | cut -d'-' -f2)
    end_day=$(echo $next | cut -d'-' -f3)
    sudo docker run --user root -v /media/dl/resource/luc:/wrf/host --name "case_${start_month}_${start_day}" -e START_M=$start_month -e START_D=$start_day -e END_M=$end_month -e END_D=$end_day run_case
    start=$next
done
