import json
import os
from flask import Flask, render_template_string, request, redirect

app = Flask(__name__)

DATA_FILE = "expenses.json"

# File Handling Concept: Loading previous records from JSON file
def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return []

# File Handling Concept: Saving data permanently to disk
def save_expenses(expenses):
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

# --- HTML & CSS TEMPLATE ---
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Expense Tracker</title>
    <style>
        body { font-family: Arial, sans-serif; background: #fff5f5; text-align: center; margin-top: 40px; }
        .container { display: inline-block; padding: 30px; background: white; border-radius: 10px; box-shadow: 0px 0px 15px rgba(0,0,0,0.1); width: 450px; text-align: left; }
        h2, .total-box { text-align: center; }
        input, select, button { width: 100%; padding: 10px; margin: 8px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
        button { background-color: #dc3545; color: white; font-weight: bold; border: none; cursor: pointer; }
        button:hover { background-color: #bd2130; }
        .total-box { background: #f8d7da; padding: 15px; border-radius: 5px; font-size: 20px; font-weight: bold; color: #721c24; margin-bottom: 20px; }
        ul { list-style: none; padding: 0; max-height: 200px; overflow-y: auto; }
        li { background: #f9f9f9; padding: 10px; margin: 5px 0; border-radius: 4px; display: flex; justify-content: space-between; border-left: 5px solid #dc3545; }
    </style>
</head>
<body>

<div class="container">
    <h2>💰 Expense Tracker</h2>
    
    <div class="total-box">
        Total Amount: ${{ total_amount }}
    </div>

    <form method="POST" action="/add">
        <input type="text" name="title" placeholder="Expense Title (e.g., Groceries)" required>
        <input type="number" name="amount" step="any" placeholder="Amount ($)" required>
        
        <!-- Categories Concept -->
        <select name="category">
            <option value="Food">Food</option>
            <option value="Rent">Rent</option>
            <option value="Bills">Bills</option>
            <option value="Entertainment">Entertainment</option>
            <option value="Other">Other</option>
        </select>
        <button type="submit">Add Expense</button>
    </form>

    <h3>History:</h3>
    <ul>
        {% for expense in expenses %}
            <li>
                <span><strong>{{ expense.title }}</strong> ({{ expense.category }})</span>
                <span>${{ expense.amount }}</span>
            </li>
        {% endfor %}
    </ul>
</div>

</body>
</html>
"""

@app.route('/')
def home():
    expenses = load_expenses()
    # Calculate Total Amount Concept
    total_amount = sum(float(item['amount']) for item in expenses)
    return render_template_string(HTML, expenses=expenses, total_amount=total_amount)

@app.route('/add', methods=['POST'])
def add_expense():
    title = request.form.get('title')
    amount = request.form.get('amount')
    category = request.form.get('category')

    # Dictionaries Concept: Organizing data into a key-value structure
    new_expense = {
        "title": title,
        "amount": amount,
        "category": category
    }

    expenses = load_expenses()
    expenses.append(new_expense)
    save_expenses(expenses)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)