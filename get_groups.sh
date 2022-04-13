#!/bin/bash
# Examine which groups the user has access to
curl -X "GET" \
  "https://secure.splitwise.com/api/v3.0/get_groups/" \
  -H "accept: application/json" \
  -H "Authorization: Bearer $SPLITWISE_TOKEN" \
  | jq ".groups[] | .name, .id"
