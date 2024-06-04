index_string = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>NRS</title> <!-- 直接设置自定义标题 -->
    {%metas%}
    <link rel="icon" type="image/x-icon" href="assets/icon.png"> 
    {%css%}
    {%favicon%}
    {%scripts%}
</head>
<body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
</body>
</html>
'''