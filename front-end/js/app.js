// 使用全局定义的API对象
// authAPI, productAPI, orderAPI, utils 已在api.js中全局定义

// DOM元素
const loginSection = document.getElementById('login-section');
const userInfoSection = document.getElementById('user-info-section');
const apiDemoSection = document.getElementById('api-demo-section');
const loginForm = document.getElementById('login-form');
const userInfoElement = document.getElementById('user-info');
const logoutBtn = document.getElementById('logout-btn');
const getProductsBtn = document.getElementById('get-products-btn');
const productsResult = document.getElementById('products-result');
const getOrdersBtn = document.getElementById('get-orders-btn');
const ordersResult = document.getElementById('orders-result');

// 初始化应用
function initApp() {
    // 检查用户登录状态
    if (utils.isLoggedIn()) {
        showLoggedInState();
    } else {
        showLoggedOutState();
    }

    // 绑定事件监听器
    bindEventListeners();
}

// 显示登录状态
function showLoggedInState() {
    loginSection.style.display = 'none';
    userInfoSection.style.display = 'block';
    apiDemoSection.style.display = 'block';
    
    // 获取并显示用户信息
    loadUserInfo();
}

// 显示未登录状态
function showLoggedOutState() {
    loginSection.style.display = 'block';
    userInfoSection.style.display = 'none';
    apiDemoSection.style.display = 'none';
    
    // 清空用户信息
    userInfoElement.innerHTML = '';
}

// 加载用户信息
function loadUserInfo() {
    userInfoElement.innerHTML = '<div class="loading"></div>';
    
    // 尝试从API获取用户信息
    authAPI.getCurrentUser()
        .then(function(userData) {
            utils.saveUserInfo(userData);
            displayUserInfo(userData);
        })
        .catch(function(error) {
            console.error('加载用户信息失败:', error);
            
            // 如果API调用失败，尝试使用本地存储的用户信息
            const storedUserInfo = utils.getUserInfo();
            if (storedUserInfo) {
                displayUserInfo(storedUserInfo);
            } else {
                userInfoElement.innerHTML = '<p class="error-text">无法加载用户信息</p>';
                // 可能需要重新登录
                setTimeout(function() {
                    authAPI.logout();
                    showLoggedOutState();
                }, 2000);
            }
        });
}

// 显示用户信息
function displayUserInfo(userData) {
    userInfoElement.innerHTML = `
        <p><strong>用户ID:</strong> ${userData.id || 'N/A'}</p>
        <p><strong>用户名:</strong> ${userData.username || userData.name || 'N/A'}</p>
        <p><strong>手机号码:</strong> ${userData.phone || 'N/A'}</p>
        <p><strong>邮箱:</strong> ${userData.email || '未设置'}</p>
        <p><strong>注册时间:</strong> ${utils.formatDateTime(userData.created_at)}</p>
    `;
}

// 处理登录
function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    // 显示加载状态
    const submitBtn = loginForm.querySelector('button[type="submit"]');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<div class="loading" style="width: 20px; height: 20px; margin: 0 auto;"></div>';
    
    // 调用登录API
    authAPI.login(username, password)
        .then(function(response) {
            // 保存认证信息 - 后端返回access_token而非token
            if (response.access_token) {
                localStorage.setItem('authToken', response.access_token);
                console.log('登录成功，已保存token');
                
                // 登录成功后直接显示登录状态，showLoggedInState会自动调用loadUserInfo获取用户信息
                showLoggedInState();
                
                // 清空表单
                loginForm.reset();
            } else {
                throw new Error('未收到有效认证令牌');
            }
        })
        .catch(function(error) {
            console.error('登录失败:', error);
            utils.showError(error.message || '登录失败，请检查账号密码');
        })
        .finally(function() {
            // 恢复按钮状态
            submitBtn.disabled = false;
            submitBtn.innerHTML = '登录';
        });
}

// 处理登出
function handleLogout() {
    authAPI.logout();
    showLoggedOutState();
}

// 加载商品列表
function loadProducts() {
    utils.showLoading(productsResult);
    
    productAPI.getProducts()
        .then(function(products) {
            if (!products || products.length === 0) {
                utils.showEmptyState(productsResult, '暂无商品数据');
                return;
            }
            
            // 显示商品列表
            productsResult.innerHTML = '';
            for (let i = 0; i < products.length; i++) {
                const product = products[i];
                const productElement = document.createElement('div');
                productElement.className = 'result-item';
                productElement.innerHTML = 
                    '<h4>' + (product.name || '商品名称') + '</h4>' +
                    '<p><strong>价格:</strong> ' + utils.formatCurrency(product.price) + '</p>' +
                    '<p><strong>库存:</strong> ' + (product.stock || 0) + '</p>' +
                    '<p><strong>描述:</strong> ' + (product.description || '暂无描述') + '</p>';
                productsResult.appendChild(productElement);
            }
        })
        .catch(function(error) {
            utils.showError(error.message || '获取商品列表失败');
            utils.showEmptyState(productsResult, '获取商品列表失败');
        });
}

// 加载订单列表
function loadOrders() {
    utils.showLoading(ordersResult);
    
    orderAPI.getOrders()
        .then(function(orders) {
            if (!orders || orders.length === 0) {
                utils.showEmptyState(ordersResult, '暂无订单数据');
                return;
            }
            
            // 显示订单列表
            ordersResult.innerHTML = '';
            for (let i = 0; i < orders.length; i++) {
                const order = orders[i];
                const orderElement = document.createElement('div');
                orderElement.className = 'result-item';
                orderElement.innerHTML = 
                    '<h4>订单 #' + (order.id || 'N/A') + '</h4>' +
                    '<p><strong>总金额:</strong> ' + utils.formatCurrency(order.total_amount) + '</p>' +
                    '<p><strong>状态:</strong> ' + getStatusText(order.status) + '</p>' +
                    '<p><strong>创建时间:</strong> ' + utils.formatDateTime(order.created_at) + '</p>';
                ordersResult.appendChild(orderElement);
            }
        })
        .catch(function(error) {
            utils.showError(error.message || '获取订单列表失败');
            utils.showEmptyState(ordersResult, '获取订单列表失败');
        });
}

// 获取订单状态文本
function getStatusText(status) {
    const statusMap = {
        'pending': '待处理',
        'processing': '处理中',
        'shipped': '已发货',
        'delivered': '已送达',
        'canceled': '已取消'
    };
    return statusMap[status] || status || '未知';
}

// 绑定事件监听器
function bindEventListeners() {
    // 登录表单提交
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    // 登出按钮点击
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
    
    // 获取商品按钮点击
    if (getProductsBtn) {
        getProductsBtn.addEventListener('click', loadProducts);
    }
    
    // 获取订单按钮点击
    if (getOrdersBtn) {
        getOrdersBtn.addEventListener('click', loadOrders);
    }
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', initApp);