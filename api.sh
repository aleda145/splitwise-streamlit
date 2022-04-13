#!/bin/bash
# Gets splitwise csv from API and saves to location, easily scheduled with crontab
curl -X "GET" \
  "https://secure.splitwise.com/api/v3.0/export_group/$SPLITWISE_GROUP.csv" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $SPLITWISE_TOKEN" \
  -o $SPLITWISE_CSV_LOCATION/splitwise.csv
