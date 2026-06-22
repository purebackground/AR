# AR 冰箱贴 · MindAR 可复用模板

## 这是什么

基于 MindAR（自然特征跟踪）+ A-Frame 的 Web AR 模板项目。用户扫码打开网页、摄像头对准冰箱贴图案、3D 内容叠加在图案上方并随手机角度移动。全程浏览器、不装 App。

## 文件结构

```
ar-layers/
├── index.html          ← 主模板（改 3D 内容在里面）
├── targets.mind        ← 图像识别指纹（换图要重新生成）
├── server.py           ← HTTPS 本地测试服务器
├── 启动.bat            ← Windows 双击启动
├── requirements.txt    ← Python 依赖
├── README.md           ← 本文件
└── model/
    ├── README.md       ← 3D 模型目录说明
    └── scene.glb       ← 把 3D 模型放这里（可选）
```

## 快速启动

### 1. 安装依赖（首次）

```bash
pip install pyOpenSSL
```

### 2. 启动服务器

双击 `启动.bat`，或：

```bash
python server.py
```

### 3. 手机测试

```
手机连同一 WiFi → 浏览器打开 https://<屏幕上显示的IP>:4443
电脑全屏打开冰箱贴图案 → 手机摄像头对准图案 → AR 内容叠加显示
```

⚠️ 自签名证书 → 浏览器提示"不安全"→ 点「高级」→「继续访问」

---

## 🔁 换新项目（新图 + 新模型）

### 第 1 步：生成图像目标文件

```bash
# 浏览器打开
https://hiukim.github.io/mind-ar-js-doc/tools/compile

# 上传冰箱贴图案（高清正面照）→ 点 Start 编译 → 下载 targets.mind
# 替换本目录的 targets.mind
```

**图片要求**：高对比度、细节丰富、不对称。避免大面积纯色、反光、对称图案。

### 第 2 步：获取 3D 模型

`.glb` 格式（glTF 2.0 Binary），放到 `model/scene.glb`。

**获取方式**：
| 方式 | 工具 | 说明 |
|------|------|------|
| AI 生成 | [Meshy](https://meshy.ai) | 上传图片 → AI 生成 3D → 下载 .glb |
| 模型商店 | [Sketchfab](https://sketchfab.com) | 搜索 → 下载 .glb 格式 |
| 自己建模 | [Blender](https://blender.org) | 免费，导出 glTF 2.0 Binary |

**模型要求**：三角面 < 50,000，文件 < 5 MB。

### 第 3 步：修改 index.html

搜索 `🔄🔄🔄` 定位到 3D 内容区，替换里面的 `<a-gltf-model>` 和兜底立方体 `<a-box>`。

**调整参数**：

| 属性 | 说明 | 示例 |
|------|------|------|
| `position="X Y Z"` | 模型位置，Y 越大越高，Z 越大越靠近镜头 | `position="0 0.3 0"` |
| `scale="X Y Z"` | 缩放比例 | `scale="0.5 0.5 0.5"` |
| `rotation="X Y Z"` | 旋转角度 | `rotation="0 45 0"` |

修改后刷新手机页面即可看效果，无需重启服务器。

### 第 4 步：部署上线

整个文件夹上传到 HTTPS 服务器（必须 HTTPS，否则摄像头不工作）。

**推荐**：腾讯云 COS + CDN、阿里云 OSS、Vercel、GitHub Pages。

拿到网址后生成二维码印在包装上。

---

## 模板能力

### 已内置（index.html 开箱即用）

| 功能 | 说明 |
|------|------|
| 图像识别跟踪 | MindAR 自然特征匹配 |
| 3D 模型显示 | `.glb` 加载 + 位置/缩放控制 |
| 兜底立方体 | 无模型时自动显示彩色几何体 |
| 环境光 + 方向光 | 两盏灯保证模型每个面可见 |
| 底座 + 金环 | 装饰元素，帮助感知空间位置 |
| 粒子环绕 | 金色粒子增加氛围 |
| targetFound/Lost | 识别状态切换 UI 提示 |
| 全屏相机 | 固定 CSS 保证手机摄像头满屏 |
| iOS 兼容 | 启动按钮满足 Safari 手势要求 |

### CDN 依赖（无需本地安装）

| 依赖 | 版本 | 说明 |
|------|------|------|
| A-Frame | 1.5.0 | 3D 渲染框架 |
| MindAR | 1.2.5 | 图像识别 AR 引擎 |

---

## 技术架构

```
用户扫码 → HTTPS 网页
              ↓
    A-Frame 初始化 3D 场景
              ↓
    MindAR 加载 targets.mind（图像指纹）
              ↓
    摄像头逐帧扫描 → 特征点匹配 → PnP 姿态估计
              ↓
    识别到目标 → mindar-image-target 显示子元素
              ↓
    3D 模型 / 立方体叠加在图案上方
              ↓
    手机移动 → 相机位姿实时更新 → 模型跟随
```

---

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 手机无法连接 | 防火墙拦截 | 管理员 PowerShell: `netsh advfirewall firewall add rule name="AR-4443" dir=in action=allow protocol=TCP localport=4443` |
| 摄像头不启动 | 非 HTTPS | 点浏览器"高级"→"继续访问" |
| 3D 模型不显示 | 文件太大 / 路径不对 | 检查浏览器控制台，确认 `model/scene.glb` 存在 |
| 识别经常丢 | 图片特征不够 | 换对比度更高的图重新生成 targets.mind |
| 模型位置不对 | position/scale 需要调 | 修改 index.html 对应参数，刷新即可 |

---

## 针对 AI 智能体的操作指引

如果你是 AI 智能体，收到用户说"帮我做一个 AR 冰箱贴"时，按以下流程操作：

### 步骤 1：确认用户需求

问用户三件事：
1. 冰箱贴图案文件在哪里？
2. 要用什么 3D 内容？（现有 .glb / AI 生成 / 纯几何体）
3. 项目放在哪个目录？

### 步骤 2：复制模板

```bash
cp -r <本模板目录> <目标项目目录>
```

### 步骤 3：生成 targets.mind

用浏览器打开 MindAR 编译器上传用户图片，下载 targets.mind 替换。

### 步骤 4：处理 3D 内容

- 如果有 .glb 文件 → 复制到 `model/scene.glb`
- 如果需要 AI 生成 → 指导用户用 Meshy
- 如果没有模型 → 删除兜底立方体或用几何体拼场景

### 步骤 5：修改 index.html

- 改 `<title>`
- 调整模型 position/scale
- 替换或删除兜底立方体
- 调整灯光颜色匹配模型

### 步骤 6：验证

1. 启动 `python server.py`
2. 手机打开 HTTPS 地址测试
3. 确认识别 + 3D 内容显示正常

### 关键文件路径速查

| 要改的 | 文件 | 搜索关键词 |
|------|------|------|
| 3D 内容替换 | `index.html` | `🔄🔄🔄` |
| 模型位置 | `index.html` | `position="0 0.3 0"` |
| 图像指纹 | `targets.mind` | 重新生成 |
| 服务器端口 | `server.py` | `PORT = 4443` |
