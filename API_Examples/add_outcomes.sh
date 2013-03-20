#!/bin/bash
# This is a 
token="<access_token>"
# Update date (with the id)
#data='{"can_edit":true,"id":3299,"title":"Add Assignments to a Canvas Course","points_possible":5,"description":"","ratings":[{"points":5,"description":"Exceeds Expectations"},{"points":3,"description":"Meets Expectations"},{"points":0,"description":"Does Not Meet Expectations"}],"context_type":"Account","context_id":82726,"mastery_points":3,"url":"/api/v1/outcomes/3299"}'
data='{"can_edit":true,"title":"Add Assignments to a Canvas Course","points_possible":5,"description":"","ratings":[{"points":5,"description":"Exceeds Expectations"},{"points":3,"description":"Meets Expectations"},{"points":0,"description":"Does Not Meet Expectations"}],"context_type":"Account","context_id":82726,"mastery_points":3}'

# get the default account outcome group
curl -H "Authorization: Bearer $token" "https://cwt.instructure.com/api/v1/accounts/82726/root_outcome_group"

curl -X POST -H "Authorization: Bearer $token" -H "Content-Type: application/json" "https://cwt.instructure.com/api/v1/accounts/82726/outcome_groups/3755/outcomes"
