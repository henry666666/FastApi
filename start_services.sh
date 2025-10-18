#!/bin/bash

# 显示帮助信息
show_help() {
    echo "使用说明：./start_services.sh [选项]"
    echo "选项："
    echo "  --build           构建Docker镜像后启动"
    echo "  --detach          后台模式启动服务"
    echo "  --stop            停止所有服务"
    echo "  --restart         重启所有服务"
    echo "  --logs            查看服务日志"
    echo "  --help            显示此帮助信息"
}

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "错误：Docker未安装，请先安装Docker。"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "错误：docker-compose未安装，请先安装docker-compose。"
    exit 1
fi

# 根据参数执行不同操作
while [[ $# -gt 0 ]]; do
    case $1 in
        --build)
            echo "正在构建Docker镜像..."
            docker-compose build
            shift
            ;;
        --detach)
            DETACH="-d"
            shift
            ;;
        --stop)
            echo "正在停止所有服务..."
            docker-compose down
            exit 0
            ;;
        --restart)
            echo "正在重启所有服务..."
            docker-compose down
            docker-compose up $DETACH
            exit 0
            ;;
        --logs)
            echo "查看服务日志..."
            docker-compose logs -f
            exit 0
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            show_help
            exit 1
            ;;
    esac
done

# 默认启动服务
echo "正在启动服务..."
docker-compose up $DETACH

if [ -z "$DETACH" ]; then
    echo ""
    echo "按 Ctrl+C 停止服务"
fi