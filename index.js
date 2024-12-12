const express = require("express");
const axios = require("axios");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

// EJS 템플릿 엔진 설정
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

// 정적 파일 서비스 (CSS, 이미지 등)
app.use(express.static(path.join(__dirname, "public")));

// 라우트: 홈 페이지
app.get("/", (req, res) => {
  res.render("index", { title: "Dynamic HTML App" });
});

// 라우트: 주식 데이터
app.get("/stock", async (req, res) => {
  const symbol = req.query.symbol || "AAPL"; // 기본값은 애플 주식
  try {
    const response = await axios.get(
      `https://query1.finance.yahoo.com/v7/finance/quote?symbols=${symbol}`
    );

    const stockData = response.data.quoteResponse.result[0];
    res.render("stock", { stock: stockData });
  } catch (error) {
    console.error(error);
    res.render("stock", { stock: null });
  }
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
