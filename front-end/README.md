# 订单管理系统 - 前端演示

这是一个简单的前端演示页面，用于展示与FastAPI后端的交互功能。本前端采用纯HTML、CSS和JavaScript实现，无需额外构建工具，可直接在浏览器中运行。

## 项目结构

```
front-end/
├── css/                  # CSS样式文件
│   └── style.css         # 主样式文件
├── js/                   # JavaScript文件
│   ├── api.js            # API交互封装
│   └── app.js            # 主应用逻辑
├── images/               # 图片资源目录
├── index.html            # 主页面
└── README.md             # 本说明文件
```

## 功能特性

- 用户登录/登出
- 显示用户信息
- 获取并展示商品列表
- 获取并展示订单列表
- 响应式设计，适配不同屏幕尺寸
- 现代化UI设计

## 使用方法

1. 确保FastAPI后端服务已启动（默认监听在http://localhost:8000）
2. 直接在浏览器中打开 `index.html` 文件即可访问前端页面
3. 使用系统中的用户账号进行登录（手机号码和密码）
4. 登录成功后，可以查看用户信息、获取商品列表和订单列表

## API配置

前端默认连接的后端API地址为：`http://localhost:8000`

如果您的FastAPI后端运行在不同的地址或端口，请修改 `js/api.js` 文件中的 `API_BASE_URL` 常量：

```javascript
// 修改为您的后端API地址
const API_BASE_URL = 'http://your-backend-url:port';
```

## 主要API端点

前端与以下API端点进行交互：

- **用户认证**
  - `POST /api/auth/login` - 用户登录
  - `GET /api/auth/me` - 获取当前用户信息

- **商品管理**
  - `GET /api/products` - 获取商品列表

- **订单管理**
  - `GET /api/orders` - 获取订单列表

## 注意事项

1. 本前端仅作为演示用途，提供基本的UI界面和API交互功能
2. 如果后端API结构有所不同，可能需要修改 `js/api.js` 中的API调用函数
3. 登录状态会保存在浏览器的localStorage中
4. 为了获得最佳体验，请确保后端服务正常运行

## 浏览器兼容性

支持以下主流浏览器的最新版本：
- Google Chrome
- Mozilla Firefox
- Apple Safari
- Microsoft Edge

## 许可证

保留所有权利。