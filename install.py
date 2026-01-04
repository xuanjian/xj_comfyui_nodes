#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XJ Nodes 安装脚本
用于安装ComfyUI自定义节点所需的依赖包
"""

import subprocess
import sys
import os

def install_package(package):
    """安装Python包"""
    try:
        # 首先尝试正常安装
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ 成功安装 {package}")
        return True
    except subprocess.CalledProcessError:
        try:
            # 如果失败，尝试使用--break-system-packages标志
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", package])
            print(f"✓ 成功安装 {package} (使用系统包覆盖)")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ 安装 {package} 失败: {e}")
            return False

def main():
    """主安装函数"""
    print("开始安装 XJ Nodes 依赖包...")
    print("=" * 50)
    
    # 需要安装的包列表
    required_packages = [
        "requests",
        "Pillow",
        "numpy",
        "torch",
        "torchvision"
    ]
    
    success_count = 0
    total_count = len(required_packages)
    
    for package in required_packages:
        print(f"正在安装 {package}...")
        if install_package(package):
            success_count += 1
        print()
    
    print("=" * 50)
    print(f"安装完成: {success_count}/{total_count} 个包安装成功")
    
    if success_count == total_count:
        print("✓ 所有依赖包安装成功！")
        print("\n接下来请按照以下步骤完成安装:")
        print("1. 将 xj_nodes 文件夹复制到 ComfyUI 的 custom_nodes 目录")
        print("2. 重启 ComfyUI")
        print("3. 在节点菜单中查找 'XJ Nodes' 分类")
    else:
        print("⚠ 部分依赖包安装失败，请手动安装失败的包")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())