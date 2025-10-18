// API基础配置
const API_BASE_URL = 'http://localhost:8000'; // FastAPI后端地址

// API请求封装函数
function apiRequest(endpoint, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
        try {
            const url = `${API_BASE_URL}${endpoint}`;
            const xhr = new XMLHttpRequest();
            
            xhr.open(method, url, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            
            // 添加认证token
            const token = localStorage.getItem('authToken');
            if (token) {
                xhr.setRequestHeader('Authorization', `Bearer ${token}`);
            }
            
            xhr.onload = function() {
                if (xhr.status >= 200 && xhr.status < 300) {
                    const responseData = JSON.parse(xhr.responseText);
                    resolve(responseData);
                } else {
                    try {
                        const errorData = JSON.parse(xhr.responseText);
                        reject(new Error(errorData.detail || '请求失败'));
                    } catch (e) {
                        reject(new Error('请求失败'));
                    }
                }
            };
            
            xhr.onerror = function() {
                reject(new Error('网络错误'));
            };
            
            // 添加请求数据
            if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
                xhr.send(JSON.stringify(data));
            } else {
                xhr.send();
            }
        } catch (error) {
            console.error('API请求错误:', error);
            reject(error);
        }
    });
}

// 用户认证相关API
const authAPI = {
    // 用户登录
    login: function(phone, password) {
        return apiRequest('/api/auth/login', 'POST', { phone, password });
    },

    // 用户注册
    register: function(userData) {
        return apiRequest('/api/auth/register', 'POST', userData);
    },

    // 获取当前用户信息
    getCurrentUser: function() {
        return apiRequest('/api/auth/me');
    },

    // 用户登出
    logout: function() {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userInfo');
    }
};

// 商品相关API
const productAPI = {
    // 获取商品列表
    getProducts: function(params = {}) {
        const queryString = Object.keys(params)
            .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
            .join('&');
        const endpoint = `/api/products${queryString ? `?${queryString}` : ''}`;
        return apiRequest(endpoint);
    },

    // 获取单个商品
    getProductById: function(id) {
        return apiRequest(`/api/products/${id}`);
    },

    // 创建商品
    createProduct: function(productData) {
        return apiRequest('/api/products', 'POST', productData);
    },

    // 更新商品
    updateProduct: function(id, productData) {
        return apiRequest(`/api/products/${id}`, 'PUT', productData);
    },

    // 删除商品
    deleteProduct: function(id) {
        return apiRequest(`/api/products/${id}`, 'DELETE');
    }
};

// 订单相关API
const orderAPI = {
    // 获取订单列表
    getOrders: function(params = {}) {
        const queryString = Object.keys(params)
            .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`)
            .join('&');
        const endpoint = `/api/orders${queryString ? `?${queryString}` : ''}`;
        return apiRequest(endpoint);
    },

    // 获取单个订单
    getOrderById: function(id) {
        return apiRequest(`/api/orders/${id}`);
    },

    // 创建订单
    createOrder: function(orderData) {
        return apiRequest('/api/orders', 'POST', orderData);
    },

    // 更新订单状态
    updateOrderStatus: function(id, status) {
        return apiRequest(`/api/orders/${id}/status`, 'PATCH', { status });
    },

    // 删除订单
    deleteOrder: function(id) {
        return apiRequest(`/api/orders/${id}`, 'DELETE');
    }
};

// 分类相关API
const categoryAPI = {
    // 获取分类列表
    getCategories: function() {
        return apiRequest('/api/categories');
    }
};

// 通用工具函数
const utils = {
    // 显示错误消息
    showError: function(message) {
        const errorElement = document.getElementById('error-message');
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            
            // 3秒后自动隐藏错误消息
            setTimeout(function() {
                errorElement.style.display = 'none';
            }, 3000);
        }
    },

    // 显示加载状态
    showLoading: function(element) {
        if (element) {
            element.innerHTML = '<div class="loading"></div>';
        }
    },

    // 显示空状态
    showEmptyState: function(element, message = '暂无数据') {
        if (element) {
            element.innerHTML = '
                <div class="empty-state">
                    <i class="fa fa-folder-open-o"></i>
                    <p>' + message + '</p>
                </div>
            ';
        }
    },

    // 格式化日期时间
    formatDateTime: function(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');
        
        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
    },

    // 格式化货币
    formatCurrency: function(amount) {
        if (amount === null || amount === undefined) return '¥0.00';
        return '¥' + Number(amount).toFixed(2);
    },

    // 检查用户是否已登录
    isLoggedIn: function() {
        return !!localStorage.getItem('authToken');
    },

    // 获取存储的用户信息
    getUserInfo: function() {
        const userInfo = localStorage.getItem('userInfo');
        return userInfo ? JSON.parse(userInfo) : null;
    },

    // 存储用户信息
    saveUserInfo: function(userInfo) {
        localStorage.setItem('userInfo', JSON.stringify(userInfo));
    }
};