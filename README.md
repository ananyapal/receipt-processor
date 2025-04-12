Fetch Rewards Receipt Processor Challenge

This project is a simple Flask-based web API that processes shopping receipts and calculates reward points based on a set of rules.

It was created as a solution to the Fetch Rewards Receipt Processor Challenge.

Features:

- Accepts receipts via a POST API.
- Calculates points based on specific rules.
- Returns total points when queried via GET API.
- Stores data in memory (no database needed).

How to Run:

1. Install dependencies

pip install flask

2. Run the application

python main.py

The server will be available at: http://127.0.0.1:5000/

API Endpoints:

1. POST /receipts/process  
Accepts a JSON receipt and returns a unique receipt ID.

Example request:

curl -X POST http://127.0.0.1:5000/receipts/process -H "Content-Type: application/json" -d "{\"retailer\": \"Target\", \"purchaseDate\": \"2022-01-01\", \"purchaseTime\": \"13:01\", \"items\": [{\"shortDescription\": \"Mountain Dew 12PK\", \"price\": \"6.49\"}, {\"shortDescription\": \"Emils Cheese Pizza\", \"price\": \"12.25\"}], \"total\": \"35.35\"}"

Example response:

{ "id": "your-unique-id" }

2. GET /receipts/{id}/points  
Returns the number of points awarded for a specific receipt.

Example request:

curl http://127.0.0.1:5000/receipts/your-unique-id/points

Example response:

{ "points": 28 }

Scoring Rules:

1. 1 point for every alphanumeric character in the retailer name  
2. 50 points if the total is a round dollar amount with no cents  
3. 25 points if the total is a multiple of 0.25  
4. 5 points for every two items on the receipt  
5. If the trimmed length of the item description is a multiple of 3, multiply the item price by 0.2 and round up to the nearest integer  
6. 6 points if the day in the purchase date is odd  
7. 10 points if the time of purchase is after 2:00pm and before 4:00pm  

Project Structure:

- main.py (Flask app with endpoints and logic)  
- README.md (This file)  
- requirements.txt (Optional: list of dependencies)

Notes:

- All data is stored in memory and will reset when the server is restarted.  
- This implementation is beginner-friendly and designed for basic backend development practice.
