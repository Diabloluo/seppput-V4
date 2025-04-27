
import json
import requests

# 标准 Serverless 入口函数
async def handler(request):
    if request.method == "POST":
        try:
            body = await request.body()
            data = json.loads(body)
            symbol = data.get("symbol", "").upper()
            if not symbol:
                return {"statusCode": 400, "body": json.dumps({"error": "股票代码不能为空"})}

            price = get_real_time_price(symbol)
            if price is None:
                return {"statusCode": 500, "body": json.dumps({"recommendation": "无法获取实时股价，请检查股票代码或稍后重试。"})}

            recommendation = recommend_sell_put(symbol, price)
            return {"statusCode": 200, "body": json.dumps({"recommendation": recommendation})}
        except Exception as e:
            return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    return {"statusCode": 200, "body": json.dumps({"message": "Sell Put 推荐小工具 Serverless API 正常运行 ✅"})}

# Sell Put 推荐逻辑（标普500、道指30支持版）
def recommend_sell_put(symbol: str, current_price: float) -> str:
    sp500_symbols = ["AAPL", "MSFT", "AMZN", "NVDA", "META", "GOOG", "GOOGL", "TSLA", "BRK.B", "UNH"]
    dow30_symbols = ["AAPL", "MSFT", "AXP", "BA", "CAT", "CVX", "DIS", "GS", "HD", "HON"]

    if symbol in sp500_symbols or symbol in dow30_symbols:
        return f"[{symbol}] 当前股价 {current_price} 美元，推荐Sell Put行权价为当前价的85%-90%。"
    else:
        return f"[{symbol}] 当前股价 {current_price} 美元，非成分股，推荐自定义保守Sell Put策略。"

# 调用 TwelveData 实时股价
def get_real_time_price(symbol: str) -> float:
    try:
        api_key = "daa15a0f598e4d1595e255110a357ede"  # 已内置你的API Key
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={api_key}"
        response = requests.get(url)
        data = response.json()
        if 'price' in data:
            return float(data['price'])
        else:
            return None
    except:
        return None
