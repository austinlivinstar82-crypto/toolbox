import os

os.makedirs('templates', exist_ok=True)

app_py = '''from flask import Flask, render_template, request
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
'''

requirements_txt = '''Flask==3.0.0
gunicorn==21.2.0
'''

index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Invoice Generator | Simple Invoice Maker Online</title>
    <meta name="description" content="Create professional invoices instantly. Free, simple invoice generator for freelancers and small businesses. No signup required.">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50 min-h-screen">
    <div class="max-w-3xl mx-auto bg-white rounded-xl shadow-lg p-6 md:p-8 mt-8">
        <h1 class="text-3xl font-bold text-gray-800 mb-2">Free Invoice Generator</h1>
        <p class="text-gray-600 mb-6">Create professional invoices in seconds. No signup. No watermark.</p>
        
        <form action="/generate" method="POST" class="space-y-4">
            <div class="grid md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Your Company</label>
                    <input type="text" name="company" placeholder="Your Business Name" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" required>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Client Name</label>
                    <input type="text" name="client" placeholder="Client Business Name" class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500" required>
                </div>
            </div>
            
            <div class="grid md:grid-cols-3 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Invoice #</label>
                    <input type="text" name="invoice_num" placeholder="INV-1001" class="w-full px-4 py-2 border rounded-lg">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Date</label>
                    <input type="date" name="date" class="w-full px-4 py-2 border rounded-lg">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Due Date</label>
                    <input type="date" name="due_date" class="w-full px-4 py-2 border rounded-lg">
                </div>
            </div>
            
            <div class="border-t pt-4">
                <h3 class="font-semibold text-gray-800 mb-3">Items</h3>
                <div id="items" class="space-y-2">
                    <div class="grid grid-cols-12 gap-2">
                        <div class="col-span-6">
                            <input type="text" name="desc[]" placeholder="Description" class="w-full px-3 py-2 border rounded" required>
                        </div>
                        <div class="col-span-2">
                            <input type="number" name="qty[]" placeholder="Qty" value="1" min="0" step="0.1" class="w-full px-3 py-2 border rounded" required>
                        </div>
                        <div class="col-span-3">
                            <input type="number" name="rate[]" placeholder="Rate ($)" min="0" step="0.01" class="w-full px-3 py-2 border rounded" required>
                        </div>
                        <div class="col-span-1 flex items-center">
                            <button type="button" onclick="addItem()" class="text-blue-600 text-xl font-bold">+</button>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="grid md:grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Tax Rate (%)</label>
                    <input type="number" name="tax_rate" value="0" min="0" max="100" step="0.01" class="w-full px-4 py-2 border rounded-lg">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-1">Notes</label>
                    <textarea name="notes" rows="2" placeholder="Payment terms, thank you note..." class="w-full px-4 py-2 border rounded-lg"></textarea>
                </div>
            </div>
            
            <button type="submit" class="w-full bg-blue-600 text-white font-bold py-3 rounded-lg hover:bg-blue-700 transition">
                Generate Invoice
            </button>
        </form>
    </div>

    <script>
        function addItem() {
            const container = document.getElementById('items');
            const div = document.createElement('div');
            div.className = 'grid grid-cols-12 gap-2';
            div.innerHTML = `
                <div class="col-span-6"><input type="text" name="desc[]" placeholder="Description" class="w-full px-3 py-2 border rounded" required></div>
                <div class="col-span-2"><input type="number" name="qty[]" placeholder="Qty" value="1" min="0" step="0.1" class="w-full px-3 py-2 border rounded" required></div>
                <div class="col-span-3"><input type="number" name="rate[]" placeholder="Rate ($)" min="0" step="0.01" class="w-full px-3 py-2 border rounded" required></div>
                <div class="col-span-1 flex items-center"><button type="button" onclick="this.parentElement.parentElement.remove()" class="text-red-600 text-xl font-bold">×</button></div>
            `;
            container.appendChild(div);
        }
    </script>
</body>
</html>
'''

invoice_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice - Free Invoice Generator</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @media print {
            .no-print { display: none !important; }
            body { background: white; }
            .invoice-box { box-shadow: none; border: none; }
        }
    </style>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="max-w-4xl mx-auto p-4 md:p-8">
        <div class="no-print flex justify-between items-center mb-6">
            <a href="/" class="text-blue-600 font-semibold">← Create New Invoice</a>
            <button onclick="window.print()" class="bg-green-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-green-700">
                Print / Save as PDF
            </button>
        </div>
        
        <div class="invoice-box bg-white p-8 md:p-12 shadow-lg rounded-lg">
            <div class="flex justify-between items-start mb-8">
                <div>
                    <h2 class="text-2xl font-bold text-gray-800">{{ data.company }}</h2>
                    <p class="text-gray-500 mt-1">Invoice</p>
                </div>
                <div class="text-right">
                    <p class="text-sm text-gray-500">Invoice #</p>
                    <p class="text-xl font-bold text-gray-800">{{ data.invoice_num }}</p>
                    <p class="text-sm text-gray-500 mt-2">Date: {{ data.date }}</p>
                    {% if data.due_date %}
                    <p class="text-sm text-gray-500">Due: {{ data.due_date }}</p>
                    {% endif %}
                </div>
            </div>
            
            <div class="mb-8">
                <p class="text-sm text-gray-500 uppercase tracking-wide font-semibold">Bill To</p>
                <p class="text-lg font-medium text-gray-800">{{ data.client }}</p>
            </div>
            
            <table class="w-full mb-8">
                <thead>
                    <tr class="border-b-2 border-gray-800">
                        <th class="text-left py-2 font-semibold">Description</th>
                        <th class="text-right py-2 font-semibold">Qty</th>
                        <th class="text-right py-2 font-semibold">Rate</th>
                        <th class="text-right py-2 font-semibold">Amount</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in data.items %}
                    <tr class="border-b border-gray-200">
                        <td class="py-3">{{ item.desc }}</td>
                        <td class="py-3 text-right">{{ item.qty }}</td>
                        <td class="py-3 text-right">${{ "%.2f"|format(item.rate) }}</td>
                        <td class="py-3 text-right font-medium">${{ "%.2f"|format(item.total) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <div class="flex justify-end">
                <div class="w-64 space-y-2">
                    <div class="flex justify-between text-gray-600">
                        <span>Subtotal</span>
                        <span>${{ "%.2f"|format(data.subtotal) }}</span>
                    </div>
                    {% if data.tax_rate > 0 %}
                    <div class="flex justify-between text-gray-600">
                        <span>Tax ({{ data.tax_rate }}%)</span>
                        <span>${{ "%.2f"|format(data.tax) }}</span>
                    </div>
                    {% endif %}
                    <div class="flex justify-between text-xl font-bold text-gray-800 border-t pt-2">
                        <span>Total</span>
                        <span>${{ "%.2f"|format(data.grand_total) }}</span>
                    </div>
                </div>
            </div>
            
            {% if data.notes %}
            <div class="mt-8 pt-4 border-t text-gray-600 text-sm">
                <p class="font-semibold mb-1">Notes:</p>
                <p>{{ data.notes }}</p>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

with open('requirements.txt', 'w', encoding='utf-8') as f:
    f.write(requirements_txt)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)

with open('templates/invoice.html', 'w', encoding='utf-8') as f:
    f.write(invoice_html)

print("All files fixed successfully!")