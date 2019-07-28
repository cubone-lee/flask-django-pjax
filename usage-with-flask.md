# Sử dụng pjax với Flask
### Vậy pjax là gì?
```
pjax = pushState + ajax 
```
[**pjax**](https://github.com/defunkt/jquery-pjax) là một jQuery plugin kết hợp giữa **pushState** và **ajax**  do [Chris Wanstrath](https://github.com/defunkt) founder của github phát triển.
Về **ajax** cho phép chúng ta thay đổi nội dung HTML, còn **pushState** thì cho phép thay đổi đường dẫn URL mà không cần phải reload lại trang.

Nếu đọc qua ở trên mà bạn chưa hiểu về pjax thì bạn có thể vào bất kì repository nào trên [github](github.com) để tham khảo. Khi bạn vào thư mục của bất kỳ repository nào, bạn có để ý trình duyệt của bạn không hề reload nhưng URL vẫn thay đổi chứ?

=> Bạn cũng có thể sử dụng ajax + pushState để làm nhưng sẽ mất thời gian hơn.

### Vậy khi nào nên sử dụng pjax?

- Khi bạn muốn viết ứng dụng quản lý source như github.
- Khi phân trang có thể bookmark.
- Khi viết chức năng search...

**NOTE:** Để có thể tiếp tục với nội dung ở dưới bạn cần phải có những kiến thức cơ bản sau
- Python + Flask
- Jinja2
- HTML + Javascript

### Sử dụng pjax với Flask
**B1.** Cài đặt Flask, dĩ nhiên rồi:

```
pip install Flask
```

**B2.** Tạo ứng dụng và thư mục ứng dụng Flask theo cấu trúc bên dưới:

```
pjax-flask
  app.py
```

**B3.** Chỉnh sửa tập tin **app.py** với nội dung:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'
```

**B4.** Chạy ứng dụng Flask

```
flask run
```

Kết quả

```
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

**B5.** Tắt ứng dụng đang chạy bằng **Control + C** trên MacOS và **CTRL+C** trên Windows.

**B6.** Tải pjax về máy 

```
curl -LO https://raw.github.com/defunkt/jquery-pjax/master/jquery.pjax.js
```

Hoặc truy cập đường dẫn ở dưới và lưu tất cả nội dung vào một tập tin tên là **query.pjax.js** hoặc tên tùy ý

```
https://raw.githubusercontent.com/defunkt/jquery-pjax/master/jquery.pjax.js
```

**B7.** Lần lượt tạo thư mục và tập tin như cấu trúc bên dưới:

```
pjax-flask
  - static
    - js
      - query.pjax.js
  app.py
```

**B8.** Xóa hết nội dung trong tập tin **app.py** và thay thế bằng nội dung sau:
```
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

# fake data
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
    """
    hiển thị danh sách tất cả items
    """
    items = ITEMS
    
    if 'X-PJAX' in request.headers:  # kiểm tra xem có pjax hay không
        return render_template('partial/list.html', items=items)
    return render_template('index.html', items=items)


@app.route('/item/<int:item_id>/')
def item(item_id):
    """
    hiển thị chi tiết item
    """
    item = ITEMS[item_id]
    if 'X-PJAX' in request.headers:  # kiểm tra xem có pjax hay không
        return render_template('partial/item.html', item=item)
    return render_template('detail.html', item=item)

```

**B9.** Lần lượt tạo thư mục và tập tin như cấu trúc bên dưới

```
pjax-flask
  - static
    - js
      - query.pjax.js
  - templates
    - partial
      - item.html
      - list.html
    index.html
    detail.html
  app.py
``` 

**NOTE**: mình sẽ comment giải thích trong từng tập tin.

- **index.html** với nội dung

```
<!doctype html>

<html lang="en">
<head>
    <meta charset="utf-8">
    <title>PJAX FLASK DEMO</title>
    
    <!-- Chèn jQuery bằng CDN của google -->
    <script src="//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    
    <!-- Chèn jquery-pjax đã tải ở trên -->
    <script type="text/javascript" src="{{ url_for('static', filename='js/jquery.pjax.js') }}"></script>
    
    <!-- Đây chỉ là css cho đẹp không cần quan tâm -->
    <style type="text/css">
        table {
          font-family: arial, sans-serif;
          border-collapse: collapse;
          width: 100%;
        }

        td, th {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
        }

        tr:nth-child(even) {
          background-color: #dddddd;
        }
    </style>
</head>

<body>
    <div id="pjax-container">
        {% include 'partial/list.html' %}
    </div>
    
    <!-- Sử dụng jquery-pjax -->
    <script type="text/javascript">
        if ($.support.pjax) {
            let options = {
                type: 'GET' // Bạn cũng có thể dụng POST
            };
            
            // a[data-pjax]: pjax sẽ hoạt động với tất cả thẻ a có attribute là data-pjax 
            // #pjax-container: pjax sẽ thay thế nội dung HTML thẻ div có id là pjax-container
            $(document).pjax('a[data-pjax]', '#pjax-container', options);
        }
    </script>
</body>
</html>
```

- **detail.html** với nội dung

```
<!doctype html>

<html lang="en">
<head>
    <meta charset="utf-8">
    <title>PJAX FLASK DEMO</title>
    <style>
        table {
          font-family: arial, sans-serif;
          border-collapse: collapse;
          width: 100%;
        }

        td, th {
          border: 1px solid #dddddd;
          text-align: left;
          padding: 8px;
        }

        tr:nth-child(even) {
          background-color: #dddddd;
        }
    </style>
</head>

<body>
    {% include 'partial/item.html' %}
</body>
</html>

```

- **item.html** với nội dung

```
<h2>
    {% if 'X-PJAX' in request.headers %}
        <a href="{{ url_for('index') }}" data-pjax="index">Back To List</a>
    {% else %}
        <a href="{{ url_for('index') }}">Back To List</a>
    {% endif %}
</h2>
<h2>ITEM {{ item_id }} DETAIL WITH PJAX</h2>
<table>
    <tr>
        <th>Name</th>
        <th>Price</th>
        <th>Currency</th>
    </tr>

    <tr>
        <td>{{ item.name }}</td>
        <td>{{ item.price }}</td>
        <td>{{ item.currency }}</td>
    </tr>
</table>
```

- **list.html** với nội dung

```
<h2>PJAX FLASK DEMO</h2>
<table>
    <tr>
        <th>Name</th>
        <th>Price</th>
        <th>Currency</th>
        <th>PJAX</th>
        <th>WITHOUT PJAX</th>
    </tr>
    {% for id, item in items.items() %}
        <tr>
            <td>{{ item.name }}</td>
            <td>{{ item.price }}</td>
            <td>{{ item.currency }}</td>
            <td>
                <!-- Thêm attribute data-pjax="detail" vào thẻ a để có thể sử dụng pjax -->
                <a href="{{ url_for('item', item_id=id) }}" data-pjax="detail">view</a>
            </td>
            <td>
                <a href="{{ url_for('item', item_id=id) }}">view</a>
            </td>
        </tr>
    {% endfor %}
</table>
```

**B10.** Chạy lại ứng dụng

```
flask run
```

```
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

Truy cập vào liên kết `http://127.0.0.1:5000/` bằng trình duyệt và xem kết quả

![alt text](images/pjax-flask-demo.gif)

### Tổng kết
Trong bài viết này mình đã hướng dẫn các bạn sử dụng pjax với Flask. Trong bài sau mình sẽ hướng dẫn sử dụng pjax với Django.

Cám ơn các bạn đã quan tâm.

Các bạn có thể xem đầy đủ source code tại [đây](https://github.com/cubone-lee/flask-django-pjax).

Lê Đức Trí.
