#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行测试脚本
用于执行所有自动化测试并生成覆盖率报告
"""

import os
import sys
import subprocess
import time

def run_command(command, cwd=None):
    """执行命令并返回结果"""
    print(f"执行命令: {' '.join(command)}")
    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        end_time = time.time()
        print(f"命令执行成功，用时: {end_time - start_time:.2f}秒")
        print("输出:")
        print(result.stdout)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        end_time = time.time()
        print(f"命令执行失败，用时: {end_time - start_time:.2f}秒")
        print("错误输出:")
        print(e.stderr)
        return False, e.stderr

def install_dependencies():
    """安装测试依赖"""
    print("\n=== 安装测试依赖 ===")
    # 在Windows上使用python -m pip来避免路径问题
    success, _ = run_command(["python", "-m", "pip", "install", "-r", "requirements.txt"])
    return success

def run_unit_tests():
    """运行单元测试"""
    print("\n=== 运行单元测试 ===")
    # 在Windows上使用python -m pytest来避免路径问题
    return run_command(["python", "-m", "pytest", "-v"])

def run_tests_with_coverage():
    """运行测试并生成覆盖率报告"""
    print("\n=== 运行测试并生成覆盖率报告 ===")
    # 在Windows上使用python -m pytest来避免路径问题
    return run_command(["python", "-m", "pytest", "--cov=.", "--cov-report=term-missing", "--cov-report=html"])

def run_specific_test(test_file):
    """运行特定的测试文件"""
    print(f"\n=== 运行特定测试: {test_file} ===")
    # 在Windows上使用python -m pytest来避免路径问题
    return run_command(["python", "-m", "pytest", "-v", test_file])

def main():
    """主函数"""
    print("=== 订单管理系统 (FastAPI) 自动化测试 ===")
    print(f"当前工作目录: {os.getcwd()}")
    
    # 安装依赖
    if not install_dependencies():
        print("依赖安装失败，退出测试")
        sys.exit(1)
    
    # 默认运行所有测试（非交互式环境）
    print("\n默认运行所有测试...")
    success, _ = run_unit_tests()
    
    if success:
        print("\n=== 测试运行成功 ===")
        if choice == "2":
            print("覆盖率报告已生成在 htmlcov/ 目录下")
            print("可以通过打开 htmlcov/index.html 查看详细的覆盖率报告")
        sys.exit(0)
    else:
        print("\n=== 测试运行失败 ===")
        sys.exit(1)

if __name__ == "__main__":
    main()