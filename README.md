# utae avatar 官网与说明书

官网：https://avatar.utae.cn/  
说明书：https://avatar.utae.cn/docs/

独立主仓库：`D:\claude\utae-avatar-document`。不修改桌面控制台源码。

## 编辑与构建

每篇说明书在 `docs/` 中单独维护，首页在 `site/home.html`，样式在 `site/site.css`。

```powershell
npm ci --ignore-scripts --no-audit --no-fund
npm run build
npm run check
```

构建输出到忽略跟踪的 `dist/`。构建脚本自动采用 BELOW NORMAL 优先级，单进程完成 Markdown 编译；不启动原生编译或图形界面。

文章顺序由 `scripts/build.mjs` 的 pages 列表控制；新增文章时同步更新索引篇和检查中的文章数。Markdown 使用相对 `.md` 链接，编译器转换为正式站点路径。搜索完全在浏览器本地执行。

## 部署

使用独立 GitHub 仓库的 Pages 工作流。`main` 更新后自动构建、验证并部署 `dist/`，入口固定为 `/` 与 `/docs/`。GitHub Pages 自定义域名设为 `avatar.utae.cn`，DNS CNAME 指向 `itorr.github.io`，证书就绪后强制 HTTPS。

未获明确发布要求时只提交，不推送。本次初建的推送用于已授权的官网发布。

## 内容与素材

功能依据和核对范围见 `maintenance/content-sources.md`。不将准备中入口、旧版本桥接能力、测试包或未核验下载链接当作已上线功能。产品与模型资源版权各归其权利方。

网站复用控制台 logo、粉色语义配色和寒蝉全圆体；字体许可证在 `site/assets/ChillRound-LICENSE.txt`。未使用未经许可的模型图片。维护时按用户要求禁止 GUI 自动化及自动截图；页面布局仅做源码与静态检查，未做浏览器视觉验收。

字体以 WOFF2 发布（保留完整字符集）；格式转换版已更名为 Utae Web Round，原始字体保留在 maintenance/fonts，许可证保持不变。重新转换可在装有 fontTools 和 Brotli 的 Windows Python 环境运行 `python scripts/font.py`，不属于每次文档构建的必要步骤。
