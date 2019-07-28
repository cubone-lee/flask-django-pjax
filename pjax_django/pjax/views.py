from django.shortcuts import render


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


def index(request):
    context = {'items': ITEMS}

    if 'X-Pjax' in request.headers:
        return render(request, 'partial/list.html', context)

    return render(request, 'index.html', context)


def item(request, item_id):
    items = ITEMS
    context = {
        'item_id': item_id,
        'item': items[item_id]
    }

    if 'X-Pjax' in request.headers:
        return render(request, 'partial/item.html', context)

    return render(request, 'detail.html', context)
