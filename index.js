<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>주식 데이터 검색</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f9;
        }
        .container {
            text-align: center;
            padding: 20px;
            background: #fff;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
        }
        h1 {
            margin-bottom: 20px;
            color: #333;
        }
        label {
            display: block;
            margin-bottom: 10px;
            font-weight: bold;
            color: #555;
        }
        input {
            padding: 10px;
            font-size: 16px;
            width: 100%;
            max-width: 300px;
            margin-bottom: 20px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            color: #fff;
            background-color: #007BFF;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .example {
            margin-top: 10px;
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>주식 데이터를 검색하세요</h1>
        <form action="/stock" method="POST">
            <label for="symbol">종목 코드 입력:</label>
            <input type="text" id="symbol" name="symbol" placeholder="예: TSLA, AAPL, 005930.KQ" required>
            <button type="submit">검색</button>
        </form>
        <div class="example">
            <p>예시: TSLA (Tesla), AAPL (Apple), 005930.KQ (삼성전자)</p>
        </div>
    </div>
</body>
</html>
