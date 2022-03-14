#!/bin/bash

start=2021-01-28
end=2021-02-01
while ! [[ "$start" > "$end" ]]; do
    next=$(date -d "$start + 1 day" +%F)
    echo $start $next
    start=$next
done
