Fetch Rewards Receipt Processor

This is a Flask-based API that processes receipts and calculates reward points based on defined rules.  
The project is a solution to the Fetch Rewards Receipt Processor Challenge:  
https://github.com/fetch-rewards/receipt-processor-challenge

Features:

- POST /receipts/process: Accepts a receipt and returns a unique ID  
- GET /receipts/<id>/points: Returns points awarded for a submitted receipt  
- In-memory receipt storage (no database required)  
- Implements all 7 reward rules outlined in the challenge  

How to Run Locally:

1. Install dependencies  
   pip install -r requirements.txt  

2. Start the server  
   python main.py  

The app will be available at:  
http://127.0.0.1:5000  

Example Requests:

Submit a receipt:

curl -X POST http://127.0.0.1:5000/receipts/process -H "Content-Type: application/json" -d "{\"retailer\": \"Target\", \"purchaseDate\": \"2022-01-01\", \"purchaseTime\": \"13:01\", \"items\": [{\"shortDescription\": \"Mountain Dew 12PK\", \"price\": \"6.49\"}, {\"shortDescription\": \"Emils Cheese Pizza\", \"price\": \"12.25\"}], \"total\": \"35.35\"}"

Get receipt points:

curl http://127.0.0.1:5000/receipts/<receipt-id>/points

Running with Docker (optional):

1. Build the Docker image  
   docker build -t receipt-processor .  

2. Run the container  
   docker run -p 5000:5000 receipt-processor  

Visit the app at:  
http://localhost:5000  

Files:

- main.py: Flask app and logic  
- requirements.txt: Project dependencies  
- Dockerfile: (optional) Container support  
