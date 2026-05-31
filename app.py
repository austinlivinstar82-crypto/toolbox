from flask import Flask, render_template, request
from datetime import datetime
import random
import traceback

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Safely get all form data
        company = request.form.get('company', '').strip() or 'Your Company'
        client = request.form.get('client', '').strip() or 'Client Name'
        invoice_num = request.form.get('invoice_num', '').strip() or f'INV-{random.randint(1000,9999)}'
        date_str = request.form.get('date', '').strip() or datetime.now().strftime('%Y-%m-%d')
        due_date = request.form.get('due_date', '').strip()
        notes = request.form.get('notes', '').strip()
        
        # Tax rate
        tax_rate_raw = request.form.get('tax_rate', '0').strip()
        try:
            tax_rate = float(tax_rate_raw) if tax_rate_raw else 0.0
        except:
            tax_rate = 0.0
        
        # Build items list
        items = []
        subtotal = 0.0
        
        descs = request.form.getlist('desc[]')
        qtys = request.form.getlist('qty[]')
        rates = request.form.getlist('rate[]')
        
        for i in range(len(descs)):
            desc = descs[i].strip() if i < len(descs) else ''
            if not desc:
                continue
            
            qty_raw = qtys[i].strip() if i < len(qtys) else '1'
            rate_raw = rates[i].strip() if i < len(rates) else '0'
            
            try:
                qty = float(qty_raw) if qty_raw else 1.0
            except:
                qty = 1.0
            
            try:
                rate = float(rate_raw) if rate_raw else 0.0
            except:
                rate = 0.0
            
            total = qty * rate
            subtotal += total
            
            items.append({
                'desc': desc,
                'qty': qty,
                'rate': rate,
                'total': total
            })
        
        # If no valid items, add a placeholder so template doesn't break
        if not items:
            items.append({'desc': 'Service', 'qty': 1, 'rate': 0, 'total': 0})
        
        tax = subtotal * (tax_rate / 100.0)
        grand_total = subtotal + tax
        
        data = {
            'company': company,
            'client': client,
            'invoice_num': invoice_num,
            'date': date_str,
            'due_date': due_date,
            'items': items,
            'tax_rate': tax_rate,
            'tax': tax,
            'subtotal': subtotal,
            'grand_total': grand_total,
            'notes': notes
        }
        
        return render_template('invoice.html', data=data)
        
    except Exception as e:
        # Show the actual error on screen so we can debug
        error_details = traceback.format_exc()
        return f"<h1>Debug Error</h1><pre>{error_details}</pre><br><a href='/'>Go Back</a>", 500

if __name__ == '__main__':
    app.run(debug=True)