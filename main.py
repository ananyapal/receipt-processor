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
    retailer = receipt.get("retailer", "")
    points += len(re.findall(r"[a-zA-Z0-9]", retailer))

    # Rule 2 & 3: Total is round or multiple of 0.25
    try:
        total = float(receipt.get("total", 0))
        if total.is_integer():
            points += 50
        if round(total % 0.25, 2) == 0:
            points += 25
    except (ValueError, TypeError):
        pass

    # Rule 4: 5 points for every 2 items
    items = receipt.get("items", [])
    points += (len(items) // 2) * 5

    # Rule 5: Item description length mod 3 → bonus
    for item in items:
        desc = item.get("shortDescription", "").strip()
        try:
            price = float(item.get("price", 0))
            if len(desc) % 3 == 0 and desc != "":
                points += math.ceil(price * 0.2)
        except (ValueError, TypeError):
            pass

    # Rule 6: Purchase day is odd
    date = receipt.get("purchaseDate", "")
    try:
        day = int(date.split("-")[2])
        if day % 2 == 1:
            points += 6
    except (IndexError, ValueError):
        pass

    # Rule 7: Time between 2:00pm and 4:00pm
    time = receipt.get("purchaseTime", "")
    try:
        hour, minute = map(int, time.split(":"))
        if hour == 14 or (hour == 15 and minute < 60):
            points += 10
    except (ValueError, IndexError):
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
    app.run(host="0.0.0.0", port=5000, debug=True)


