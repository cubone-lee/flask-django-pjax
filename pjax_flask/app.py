from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)


ITEMS = {
    1: {
        'name': 'Item 1',
        'price': '1000',
        'currency': 'USD'
    },
    2: {
        'name': 'Item 2',
        'price': '2000',
        'currency': 'USD'
    },
    3: {
        'name': 'Item 3',
        'price': '3000',
        'currency': 'USD'
    },
    4: {
        'name': 'Item 4',
        'price': '4000',
        'currency': 'USD'
    },
    5: {
        'name': 'Item 5',
        'price': '5000',
        'currency': 'USD'
    }
}


@app.route('/')
def index():
    items = ITEMS
    if 'X-PJAX' in request.headers:
        return render_template('partial/list.html', items=items)
    return render_template('index.html', items=items)


@app.route('/item/<int:item_id>/')
def item(item_id):
    item = ITEMS[item_id]
    if 'X-PJAX' in request.headers:
        return render_template('partial/item.html', item=item)
    return render_template('detail.html', item=item)
