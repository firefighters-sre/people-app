#!/bin/bash
#600 = 10 min
#1800 = 30min
for i in {0..1800}
  do 
     curl -o /dev/null -s -w "%{http_code}\n" "concierge-app:8080/access" -H "Content-Type: application/json" -d @acess.json
     
     #curl -v $ACCESS_URL -H "Content-Type: application/json" -d @access.json
     
     echo "Current date: $(date +"%T")"
     echo '----------------------------'
     sleep 1
 done