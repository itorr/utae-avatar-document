utae avatar · Steam 视觉物料
核对日期：2026-10-24

交付：18 张可编辑 SVG、18 张对应 PNG/JPG、1 个多尺寸 ICO。
打开 index.html 浏览完整索引。upload/ 是 Steam 静态图片；extras/ 是介绍与宣传图；svg/ 是源文件。
尚不能称为全部上架资料齐备：缺少至少 5 张合格真实产品截图。没有上传、发布或操作 Steam 后台。

必需静态物料（本包均已制作）
store-header          920×430 PNG
store-small           462×174 PNG
store-main            1232×706 PNG
store-vertical        748×896 PNG
library-capsule       600×900 PNG
library-header        920×430 PNG
library-hero          3840×1240 PNG，无字
library-logo          1280×300 PNG，透明背景（官方要求宽1280和/或高720）
shortcut-icon         512×512 PNG，附多尺寸 ICO；详细规范允许256或512
app-icon              184×184 JPG，不透明浅粉底，避免自动生成黑底

可选与条件适用
store-background      1438×810 PNG：低亮度商店背景
event-cover           800×450 PNG：创建活动/公告时需要；本包为无日期品牌介绍图
event-header          1920×622 PNG：活动/公告建议配图
promo-landscape       1920×1080 PNG：外部宣传图，不是商店截图
about-intro           1200×660 PNG：商店介绍主视觉
about-tracking/models/output 1200×400 PNG：商店介绍功能图
以上介绍图尺寸为设计尺寸，不是 Steam 强制尺寸。中文文案仅作为中文素材，不代表其他语种已本地化。
Bundle：当前没有捆绑包产品信息，不制造捆绑包素材。建立 Bundle 时除同套胶囊外另需 Bundle Header；正文规范707×232，而当前模板提供1414×464，实际建包时核对该上传槽。
macOS：仅在正式支持并提供 Mac 构建时需要 ICNS；当前未确认该平台，不暗示已经支持。
集换式卡牌、成就、点数商店、广播侧图、DLC、Demo 和限时覆盖图不属于本次基础上架必需项；没有对应功能/活动授权与内容，不虚构。
视频预告片需要真实录制与具体内容，本包不以静态图伪装视频。

文字与安全区域
所有基础商店/库胶囊仅出现产品名 utae avatar；主标语“让形象动起来。”不放入胶囊。
库 Hero 无字，Library Logo 独立透明。上传后建议将 Logo 放左下，避免挡住居中的图标。
官方库文档写中心860×380安全区；下载的3840×1240模板显示的绿色区域更大。本包保守按中心860×380（x1490–2350，y430–810）安排眼睛与腮红等识别细节，外围方块及白色轮廓允许随窗口裁切；不把模板与文字的差异说成一致。
官方活动 Header PSD 的绿色框约为x84–1835、y114–494。本包标题与图标置于框内；上下延展区域不放文字。该范围按模板合成图像读出，边缘像素可能相差1px。
普通胶囊规范未规定统一百分比安全边距；本包留出自定边距并单独排版，不将设计边距冒充官方要求。小胶囊已检查120×45与184×69缩小图，见review/small-capsule-proof.png。

SVG 可编辑性与字体
文字保留为 text，背景由独立 SVG 图形构成，产品图标是内嵌原始PNG图层；这是可编辑排版源文件，并非全矢量图标。
没有重绘或更换品牌图标。每张 SVG 内嵌图标与裁剪后的字体，无网络资源依赖。
字体源：maintenance/fonts/ChillRoundF.ttf，SIL OFL 1.1，许可附于assets/ChillRound-LICENSE.txt。
裁剪字体已按保留字体名称要求改名UtaeSteamRound。完整原字体也随包提供；部分编辑器不支持SVG内嵌字体，可安装完整字体使用回退族名。
PNG导出时临时将字形转路径进行确定性渲染，因此不依赖操作系统安装字体；源SVG仍为可编辑文字。
Steam使用位图上传，不要把SVG当作Steam上传格式。胶囊/背景提供PNG，App Icon严格为JPG，Library Logo透明PNG，快捷图标PNG/ICO。
修改源SVG后可在支持SVG的编辑器按原始像素尺寸导出。generate.py重新生成时会覆盖svg/中的手工编辑；若用脚本维护，请改generate.py。

真实截图缺口（至少5张，每张≥1920×1080，16:9）
1. 当前控制台与实际加载模型，体现日常操作。
2. 摄像头面捕连接及模型实时响应。
3. 模型表情编辑与实际预览。
4. 参数绑定/图层操作与实际结果。
5. 已运行的输出设置及对应实际模型画面。
请由用户在真实运行状态手动采集，使用允许用于商业宣传的模型/背景；不叠加营销文案，不拼贴示意图，不把同一张拆成五张。
当前仅找到旧版宣传拼图docs/marketing/utae-avatar-deck-light-jpg-2x/scr.jpg（1470×924，含旧界面、营销标注及其他产品），以及渲染调试图；它们不满足当前截图条件，未纳入上传文件。
未自动截图或操作GUI。需要真实截图与模型宣传授权后才能补齐该必需项。适龄标记须按真实内容审核。

功能与来源
定位和标语来自本次用户需求，不包含帧率成绩、占用数字、竞品比较等未核实性能数据。
功能文案核对docs/tracking.md、docs/models.md、docs/output.md：摄像头/兼容iPhone来源、矫正、平滑、麦克风嘴型辅助、表情编辑、动作快捷键、参数绑定、图层、Spout2、PNG与分层TIFF。
iPhone需兼容发送端；Spout2需接收端支持。准备中的“添加到直播姬”没有写入素材。
开发方从D:/claude_project/utae-live2d-studio/web/license-content.mjs核对为“沈阳神奇海螺传媒工作室”；不将开发方文字放进基础胶囊。
没有捏造商店URL、App ID、价格或发售日期。

官方核对来源
概览：https://partner.steamgames.com/doc/store/assets
商店尺寸/截图：https://partner.steamgames.com/doc/store/assets/standard
库资源/安全区：https://partner.steamgames.com/doc/store/assets/libraryassets
内容限制：https://partner.steamgames.com/doc/store/assets/rules
社区图标：https://partner.steamgames.com/doc/store/assets/community
活动：https://partner.steamgames.com/doc/store/assets/eventassets
官方页面链接的模板包：https://www.dropbox.com/scl/fo/cvkwbosmrimklcl9h0qko/AF5IPErKP-mQM_3YO1Dw2lA?dl=0&rlkey=b3ad0izykq367g4luasrinw9z
已下载并检查当前PSD合成图；模板原文件留在仓库work/steam-spec/，不作为品牌交付或提交到Git。

验证与再生成
Python 3 + Pillow + fontTools + Brotli + CairoSVG：python steam-assets/generate.py
纯图片处理，无产品编译、无GUI。manifest.json包含尺寸、用途、Alpha契约及SHA256。
正常PNG使用straight/unassociated alpha；半透明红色探针实际读取为RGBA(255,0,0,128)，未重复预乘。原PNG复制与内嵌保持真实编码，不把预乘像素伪标为straight。
review/validation.json记录尺寸和编码检查，review/contact-sheet.jpg为素材总览。
