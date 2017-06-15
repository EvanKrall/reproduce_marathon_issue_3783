#!/bin/bash
$*
ret=$?
docker-compose stop -t 60
sleep 30s
docker-compose logs &
exit $ret
