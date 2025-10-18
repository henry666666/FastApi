# 项目文档概览

本文档旨在为新接触项目的开发人员提供项目中所有文档的概览，帮助您快速了解项目结构和重要文档内容。

## 文档列表与描述

### 1. [README.md](README.md)
**项目主文档**，包含项目概述、快速开始指南、基本使用说明等核心信息。

### 2. [TEST_RESULTS_SUMMARY.md](TEST_RESULTS_SUMMARY.md)
**测试结果摘要**，记录了API测试的详细结果，包括11个测试用例的执行情况、问题诊断与修复过程、测试源数据等。

### 3. [CI_CD_PROCESS.md](CI_CD_PROCESS.md)
**CI/CD流程文档**，详细说明如何使用Docker Compose为FastAPI应用实现CI/CD流程，包括环境要求、服务组件、部署步骤等。

### 4. [SIMPLE_API_TESTING_PLAN.md](SIMPLE_API_TESTING_PLAN.md)
**简单API测试计划**，定义了项目API的基础测试策略、测试场景和测试方法。

### 5. [STABILITY_TESTING_PLAN.md](STABILITY_TESTING_PLAN.md)
**稳定性测试计划**，专注于系统稳定性和性能测试的策略和方法。

### 6. [API_RESPONSE_OPTIMIZATION.md](API_RESPONSE_OPTIMIZATION.md)
**API响应优化指南**，提供了优化API响应性能和质量的建议和方法。

### 7. [API_TESTING.md](API_TESTING.md)
**API测试详细文档**，包含API测试的完整方法、工具使用和最佳实践。

### 8. [MIGRATION_PROCESS.md](MIGRATION_PROCESS.md)
**数据库迁移流程**，描述了数据库结构变更和数据迁移的规范和步骤。

### 9. [PROJECT_MAPPING.md](PROJECT_MAPPING.md)
**项目映射文档**，展示了项目各组件之间的关系和模块映射。

### 10. [TASK.md](TASK.md)
**任务描述文档**，记录了项目的具体任务、要求和实现细节。

## 项目简介

这是一个基于FastAPI框架开发的订单管理系统后端服务，主要功能包括：
- 用户认证与授权（登录、注册、用户信息管理）
- 商家管理
- 商品管理
- 订单管理

项目采用了现代Python后端开发架构：
- **FastAPI** 作为Web框架
- **SQLAlchemy** 作为ORM
- **Docker** 用于容器化部署
- **PostgreSQL/SQLite** 作为数据库
- **JWT** 用于身份认证

## 推荐阅读顺序

对于新接触项目的开发人员，建议按以下顺序阅读文档：

1. 先阅读 [README.md](README.md) 了解项目基本情况
2. 查看 [TEST_RESULTS_SUMMARY.md](TEST_RESULTS_SUMMARY.md) 了解API功能和测试情况
3. 阅读 [CI_CD_PROCESS.md](CI_CD_PROCESS.md) 了解如何部署和运行项目
4. 根据需要深入阅读其他专业文档

## 快速开始

### 环境要求
- Docker Desktop (Windows/macOS) 或 Docker + Docker Compose (Linux)
- Python 3.11+（如直接在本地运行）

### 运行项目

使用Docker Compose运行项目：
```bash
# Windows系统
start_services.bat --build

# Linux/macOS系统
./start_services.sh --build
```

### 运行测试
```bash
# Windows系统
start_services.bat --test

# Linux/macOS系统
docker-compose run app python -m pytest
```

## 项目结构

主要目录结构：
- `app.py` - FastAPI应用入口
- `routers/` - API路由定义
- `service/` - 业务逻辑层
- `repository/` - 数据访问层
- `models.py` - 数据库模型定义
- `database.py` - 数据库连接配置
- `tests/` - 测试代码
- `utils/` - 工具函数

## 获取帮助

如果在使用项目过程中遇到问题，请查阅相关文档或联系项目维护人员。