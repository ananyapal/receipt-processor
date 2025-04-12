from flask import Flask, request, jsonify
import uuid
import re
import math

app = Flask(__name__)
receipts = {}  # Stores receipt data by receipt ID


# Helper function to calculate points based on rules
def calculate_points(receipt):
    points = 0

    # Rule 1: Alphanumeric characters in retailer name
    points += len(re.findall(r'[a-zA-Z0-9]', receipt.get("retailer", "")))

    # Rule 2: Round dollar amount
    try:
        total = float(receipt.get("total", 0))
        if total == int(total):
            points += 50

        # Rule 3: Multiple of 0.25
        if total % 0.25 == 0:
            points += 25
    except ValueError:
        pass

    # Rule 4: 5 points for every 2 items
    items = receipt.get("items", [])
    points += (len(items) // 2) * 5

    # Rule 5: Item description length
    for item in items:
        desc = item.get("shortDescription", "").strip()
        if len(desc) % 3 == 0:
            try:
                price = float(item.get("price", 0))
                points += math.ceil(price * 0.2)  # Math.ceil for rounding up
            except ValueError:
                pass

    # Rule 6: Purchase date is odd
    date = receipt.get("purchaseDate", "")
    if date:
        try:
            day = int(date.split("-")[2])
            if day % 2 == 1:
                points += 6
        except:
            pass

    # Rule 7: Purchase time between 2:00pm and 4:00pm
    time = receipt.get("purchaseTime", "")
    if time:
        try:
            hour, minute = map(int, time.split(":"))
            if hour == 14 or (hour == 15 and minute < 60):
                points += 10
        except:
            pass

    return points


@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.get_json()
    receipt_id = str(uuid.uuid4())
    receipts[receipt_id] = {
        "receipt": data,
        "points": calculate_points(data)
    }
    return jsonify({"id": receipt_id})


@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def get_points(receipt_id):
    data = receipts.get(receipt_id)
    if data:
        return jsonify({"points": data["points"]})
    return jsonify({"error": "Receipt not found"}), 404


if __name__ == '__main__':
    app.run(debug=True)