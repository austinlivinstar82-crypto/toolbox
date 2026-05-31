cat > app.py << 'EOF'
from flask import Flask, render_template, request
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = {
        'company': request.form.get('company', 'Your Company'),
        'client': request.form.get('client', 'Client Name'),
        'invoice_num': request.form.get('invoice_num', f'INV-{random.randint(1000,9999)}'),
        'date': request.form.get('date', datetime.now().strftime('%Y-%m-%d')),
        'due_date': request.form.get('due_date', ''),
        'items': [],
        'tax_rate': float(request.form.get('tax_rate', 0)),
        'notes': request.form.get('notes', ''),
    }
    
    descriptions = request.form.getlist('desc[]')
    quantities = request.form.getlist('qty[]')
    rates = request.form.getlist('rate[]')
    
    subtotal = 0
    for i in range(len(descriptions)):
        if descriptions[i]:
            qty = float(quantities[i]) if i < len(quantities) else 1
            rate = float(rates[i]) if i < len(rates) else 0
            total = qty * rate
            subtotal += total
            data['items'].append({
                'desc': descriptions[i],
                'qty': qty,
                'rate': rate,
                'total': total
            })
    
    tax = subtotal * (data['tax_rate'] / 100)
    grand_total = subtotal + tax
    
    data['subtotal'] = subtotal
    data['tax'] = tax
    data['grand_total'] = grand_total
    
    return render_template('invoice.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
EOF