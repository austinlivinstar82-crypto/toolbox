from flask import Flask, render_template, request
from datetime import datetime
import random

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = {
            'company': request.form.get('company', 'Your Company') or 'Your Company',
            'client': request.form.get('client', 'Client Name') or 'Client Name',
            'invoice_num': request.form.get('invoice_num') or f'INV-{random.randint(1000,9999)}',
            'date': request.form.get('date') or datetime.now().strftime('%Y-%m-%d'),
            'due_date': request.form.get('due_date', ''),
            'items': [],
            'tax_rate': 0.0,
            'notes': request.form.get('notes', ''),
        }
        
        # Safely parse tax rate
        try:
            data['tax_rate'] = float(request.form.get('tax_rate', 0) or 0)
        except (ValueError, TypeError):
            data['tax_rate'] = 0.0
        
        descriptions = request.form.getlist('desc[]')
        quantities = request.form.getlist('qty[]')
        rates = request.form.getlist('rate[]')
        
        subtotal = 0
        
        for i in range(len(descriptions)):
            desc = descriptions[i].strip() if i < len(descriptions) else ''
            if not desc:
                continue
                
            try:
                qty = float(quantities[i]) if i < len(quantities) and quantities[i] else 1
            except (ValueError, TypeError):
                qty = 1
                
            try:
                rate = float(rates[i]) if i < len(rates) and rates[i] else 0
            except (ValueError, TypeError):
                rate = 0
            
            total = qty * rate
            subtotal += total
            
            data['items'].append({
                'desc': desc,
                'qty': qty,
                'rate': rate,
                'total': total
            })
        
        # If no items were valid, add a blank one so template doesn't break
        if not data['items']:
            data['items'].append({
                'desc': 'Service',
                'qty': 1,
                'rate': 0,
                'total': 0
            })
        
        tax = subtotal * (data['tax_rate'] / 100)
        grand_total = subtotal + tax
        
        data['subtotal'] = subtotal
        data['tax'] = tax
        data['grand_total'] = grand_total
        
        return render_template('invoice.html', data=data)
        
    except Exception as e:
        # If anything breaks, show a simple error page instead of crashing
        return f"<h1>Something went wrong</h1><p>{str(e)}</p><a href='/'>Go Back</a>", 500

if __name__ == '__main__':
    app.run(debug=True)