# 内容核对记录

核对日期：2026-10-23。参考仓库 `D:\claude_project\utae-live2d-studio`，只读检查，未修改。

| 说明书主题 | 核对来源 |
| --- | --- |
| 产品定位 | README.md |
| 模型管理 | web2-ui/pages/skins/index.mjs |
| 控制台与矫正 | web2-ui/pages/home/index.mjs、components/home-controls/index.mjs |
| 来源、帧率、平滑、启动 | web2-ui/components/settings-summary/index.mjs |
| 语音、物理与画质 | web2-ui/components/settings-controls/index.mjs |
| 输出与截图 | web2-ui/components/output-controls/index.mjs |
| 转换、绑定、手动迁移 | docs/261023-独立绑定与手动迁移.md、web2-ui/AGENTS.md |
| 开发方、英文声明 | web/license-content.mjs |
| 配色与字体 | web2-ui/styles/themes.less、web2-ui/assets |

明确未宣传：准备中的添加到直播姬、没有在当前设置页挂载的录制组件、已移除的 VTS/OSF 桥接、未经核验的下载包和 iPhone 安装链接、最低配置和性能数字。迁移文档所述导入绑定入口未在 web2-ui 找到，公开文章明确注明新版控制台暂未提供入口。

文档对软件的功能说明来自现有源码；本任务没有启动桌面程序进行功能实测。网站自身完成构建与链接检查，未使用浏览器自动化或截图。

## 2026-10-24 官网改版

按用户确认，将产品定位改为“超高性能的 Live2D 虚拟形象动捕工具”。首页右侧使用大尺寸产品图标，配色延续桌面控制台；不新增未经实测的性能数字。网站提供粉、紫、蓝、绿四种配色，使用原生 radio，状态通过 data-theme 表达。说明书与首页统一字号层级、色块和圆角规则。继续禁止 GUI 自动化与截图，未做浏览器视觉验收。
