#!/bin/bash

URL="http://localhost:5001/cleanup"
MAX_RETRIES=3
RETRY_COUNT=0

echo "🚀 ServiceNow Simulation Started..."

while [ $RETRY_COUNT -lt $MAX_RETRIES ]
do
    echo "Attempt $((RETRY_COUNT+1))..."

    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST $URL \
    -H "Content-Type: application/json" \
    -H "x-api-key: my-secret-key" \
    -d '{
      "incident": "INC12345",
      "server": "local"
    }')

    STATUS=$(echo "$RESPONSE" | tail -n 1)
    BODY=$(echo "$RESPONSE" | sed '$d')

    echo "Response Status: $STATUS"
    echo "Response Body:"
    echo "$BODY"

    if [ "$STATUS" -eq 200 ]; then
        echo "✅ Cleanup successful"
        exit 0
    else
        echo "⚠️ Retry needed..."
        RETRY_COUNT=$((RETRY_COUNT+1))
        sleep 2
    fi
done

echo "❌ Failed after $MAX_RETRIES attempts"
exit 1