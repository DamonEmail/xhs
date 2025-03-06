# 小红书高赞评论爬取器 (｡･ω･｡)ﾉ ♡

一个可爱的小红书笔记高赞评论采集工具 ٩(◕‿◕｡)۶

## ✨ 功能特点

- 🔍 支持按关键词搜索笔记
- 🌟 自动筛选高赞评论（默认点赞数 ≥200 或回复数 ≥80）
- 💬 支持收集主评论和子评论
- 💾 自动保存评论数据为 JSON 格式
- 🔒 支持设置代理
- ⚡ 智能控制请求频率
- 🎯 自动处理验证码和登录流程
- 📝 支持批量关键词处理
- 🚥 智能频率控制，避免被封

## 🚀 安装步骤

1. 克隆项目到本地 (づ｡◕‿‿◕｡)づ

```bash
git clone https://github.com/yourusername/redtalk.git
cd redtalk
```

2. 安装依赖 (ﾉ ◕ ヮ ◕)ﾉ\*:･ﾟ ✧

```bash
pip install -r requirements.txt
```

3. 安装 Playwright 浏览器 ⊂(◉‿◉)つ

```bash
playwright install chromium
```

## 🎮 使用方法

1. 修改关键词（在 RedTalk.py 的 main 函数中）：

```python
keywords = ["你的关键词1", "你的关键词2"]  # 在这里添加你想搜索的关键词
```

2. 运行程序：

```bash
python RedTalk.py
```

3. 程序会自动打开浏览器，请在浏览器中完成以下步骤 (●'◡'●)：

   - ✅ 完成验证码验证
   - 🔑 登录小红书账号
   - ↩️ 登录完成后按回车继续

4. 数据将保存在 `hot_comments` 目录下，按关键词分类存储 (｡♥‿♥｡)

## ⚙️ 配置说明

可以在 `RedTalk.py` 中修改以下参数 (◕ᴗ◕✿)：

```python
self.max_notes = 20            # 每个关键词最多收集的笔记数
self.max_comments_per_note = 50 # 每个笔记最多收集的评论数
self.hot_comment_min_likes = 200 # 评论最少点赞数
self.min_reply_count = 80      # 评论最少回复数
self.request_interval = (1, 2)  # 请求间隔范围(秒)
self.max_retries = 3           # 最大重试次数
```

## ⚠️ 注意事项

- 🔐 需要手动登录小红书账号
- 🌐 建议使用代理 IP 避免被限制
- 📜 遵守小红书的使用条款和规范
- 🐌 注意控制爬取频率，做个有礼貌的爬虫 (｡◕‿◕｡)
- 🎯 每个笔记最多获取 100 条评论（10 页）
- 🔄 程序会自动处理请求失败和重试
- 📊 数据实时保存，不用担心中断
- 🎨 支持评论中的图片链接获取

## 📊 数据格式

收集的数据将保存为 JSON 格式 (ﾉ ◕ ヮ ◕)ﾉ\*:･ﾟ ✧：

```json
{
  "note_id_1": {
    "title": "笔记标题",
    "crawl_time": "20240306_020000",
    "comments": [
      {
        "comment_id": "评论ID",
        "content": "评论内容",
        "like_count": 666,
        "reply_count": 88,
        "user_name": "用户昵称",
        "create_time": "1709683200000",
        "pictures": ["图片URL1", "图片URL2"]
      }
    ]
  }
}
```

## 📦 依赖

- 🐍 Python 3.7+
- 🌐 httpx>=0.24.0
- 🎭 playwright>=1.41.0
- ⚡ asyncio>=3.4.3
- 🔗 urllib3>=2.0.0

## 💝 最后

如果这个工具对你有帮助，欢迎给个 star ⭐️ (｡♥‿♥｡)

遇到问题或有建议都可以提 issue 哦～ (◕‿◕✿)

Happy Crawling! ٩(◕‿◕｡)۶

## 🎨 更新日志

### v1.0.0 (2024-03-06)

- 🎉 首次发布
- 🌟 支持高赞评论筛选
- 📝 支持多关键词批量处理
- 🔄 自动处理登录和验证码
- 💾 实时保存数据
