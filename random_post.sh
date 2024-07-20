#!/bin/bash

while true
do
  # Create a variable 'a' with a random value between 3 and 5
  a=$((RANDOM % 10 + 1))

  # Loop 'a' times
  for ((i=1; i<=a; i++))
  do
    # Sleep for a random time between 0 and 5 seconds
    sleep $((RANDOM % 6))
    
    # Execute the curl command
    curl -X POST "http://localhost:7000/predict" -H "Content-Type: application/json" -d @input_data.json
  done
done

