#!/bin/bash
$*
ret=$?
if [[ $ret -ne 0 ]]; then
  docker-compose stop
  docker-compose logs
fi
exit $ret
