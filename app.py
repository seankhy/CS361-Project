from flask import Flask, request, redirect, render_template, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from io import StringIO
import csv



app = Flask(__name__)

# Configuration for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)
    date = db.Column(db.DateTime, nullable=True)

@app.route('/')
def index():
    expenses = Expense.query.filter(Expense.deleted_at.is_(None)).all()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        note = request.form['note']
        # Get the date from the form
        date_str = request.form['date']
        # Convert the date string to a datetime object
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None

        new_expense = Expense(name=name, amount=amount, note=note, date=date)
        db.session.add(new_expense)
        db.session.commit()

        return redirect('/')
    return render_template('add.html')

# Route for soft delete - marking an expense as deleted without removing it from the database
@app.route('/soft_remove/<int:expense_id>', methods=['POST'])
def soft_remove_expense(expense_id):
    expense_to_remove = Expense.query.get_or_404(expense_id)
    expense_to_remove.deleted_at = datetime.utcnow()  # Set the time of deletion
    db.session.commit()
    return redirect(url_for('index'))

# Route for hard delete - actually removing the expense from the database
@app.route('/remove/<int:expense_id>', methods=['POST'])
def hard_remove_expense(expense_id):
    expense_to_remove = Expense.query.get_or_404(expense_id)
    db.session.delete(expense_to_remove)  # Actually delete the record
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/history')
def history():
    # Fetch expenses that have been added and not deleted
    recent_adds = Expense.query.filter(Expense.deleted_at.is_(None)).order_by(Expense.created_at.desc()).limit(10).all()
    # Fetch expenses that have been soft deleted but not hard deleted
    recent_deletes = Expense.query.filter(Expense.deleted_at.isnot(None)).order_by(Expense.deleted_at.desc()).limit(10).all()

    return render_template('history.html', recent_adds=recent_adds, recent_deletes=recent_deletes)

@app.route('/export')
def export_expenses():
    # Fetch expenses that haven't been soft-deleted
    expenses = Expense.query.filter(Expense.deleted_at.is_(None)).all()

    # Create a StringIO object to hold CSV data
    si = StringIO()
    cw = csv.writer(si)

    # Write expense amount data
    for expense in expenses:
        cw.writerow([expense.amount])

    # Set the output to return as a response
    output = si.getvalue()
    return Response(output, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=expenses_amount_only.csv"})





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)