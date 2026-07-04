#!/bin/bash
# ============================================================
#  NPFJ 构建脚本（macOS / Linux）
#  用法: bash build.sh
#  输出: NPFJ-交付包.zip（不含 node_modules 和源码）
# ============================================================
set -e

echo "📦 NPFJ 构建开始..."

# 1. 构建前端
echo "🔧 构建前端..."
cd frontend
npm install --silent
npm run build
cd ..

# 2. 检查 dist
if [ ! -d "frontend/dist" ]; then
    echo "❌ 前端构建失败"
    exit 1
fi

# 3. 打包交付物
echo "🗜️ 打包交付物..."
mkdir -p _dist
cp run.py _dist/
cp -r backend _dist/
cp -r frontend/dist _dist/frontend/dist
mkdir -p _dist/frontend
cp -r frontend/dist _dist/frontend/dist
cp -r docs _dist/

# 只保留必要的后端文件，排除 __pycache__
find _dist/backend -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# 生成 zip
cd _dist
zip -r ../NPFJ-交付包.zip ./*
cd ..
rm -rf _dist

echo "✅ 构建完成！交付包: NPFJ-交付包.zip"
