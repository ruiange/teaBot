import express from 'express';
import mainRouter from "./router/index.js";
import dotenv from 'dotenv';

// 加载环境变量
dotenv.config();

const app = express();

const PORT = process.env.PORT || 3000;

// 启用 JSON 解析中间件
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.use(mainRouter)

app.listen(PORT, () => {
    console.log(`Server is running on port http://127.0.0.1:${PORT}`);
});