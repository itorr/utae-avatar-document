# utae avatar API

本文对应 API v2，面向歌映直播、礼物互动和其他本机插件。

## 1. 快速选择

| 需求 | 使用方式 | 默认地址 |
| --- | --- | --- |
| 每帧读取模型最终参数，追求最低延迟 | Windows 只读共享内存 | `Local\UtaeLive2D.State.v2` |
| 控制模型、触发礼物效果、订阅状态 | 原生 WebSocket | `ws://127.0.0.1:48991/ws` |

端口默认是 `48991`，服务默认只用于本机回环地址。原生控制台的“设置 → API”可启停网络接口，输入 `1..65535` 的整数端口后点击“应用”立即生效并保存；关闭后仍可在原生控制台重新启用。切换端口会断开已有连接，调用方须使用新地址重新连接。端口占用或保存失败会提示错误并恢复原设置。

配置保存在 `config/app.json` 的 `api.enabled` 和 `api.port`；旧配置缺少 `enabled` 时默认启用。`app.getState` 的 `api` 同时提供 `enabled`（配置）、`running`（实际监听状态）和 `error`（启动失败原因）。开关控制 HTTP/WebSocket 服务，不关闭只读共享内存。监听设置只允许通过原生控制台的进程内调用修改；WebSocket 不接受 `app.updateApi`。

推荐做法：高频状态从共享内存读取，可靠控制使用 `/ws`。不要用 WebSocket 每帧轮询全部参数。

## 2. 原生 WebSocket 基础格式

请求：

```json
{"id":1,"method":"external.getState","params":{}}
```

成功响应：

```json
{"id":1,"ok":true,"result":{}}
```

失败响应：

```json
{"id":1,"ok":false,"error":{"code":"INVALID_PARAMS","message":"可读的错误说明"}}
```

| 字段 | 类型 | 必填 | 范围/默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `id` | 整数 | 建议 | 64 位整数；省略时按 `0` 处理 | 匹配请求和响应 |
| `method` | 字符串 | 是 | 无默认值 | 方法名 |
| `params` | 对象 | 否 | 默认 `{}` | 方法参数 |

单条消息最大 `16 MiB`。除订阅事件外，每个请求返回一次响应。

## 3. 最短可用示例

### 3.1 礼物砸头

```json
{
  "id": 1,
  "method": "effect.trigger",
  "params": {
    "preset": "flinch",
    "source": "gift",
    "side": "left",
    "intensity": 1.0,
    "durationMs": 480,
    "queue": true
  }
}
```

### 3.2 注入面捕输入

```json
{
  "id": 2,
  "method": "parameter.inject",
  "params": {
    "source": "song-live",
    "mode": "add",
    "priority": 50,
    "weight": 1.0,
    "ttlMs": 1000,
    "values": {"FaceAngleX": 8.0, "EyeOpenLeft": -0.4}
  }
}
```

### 3.3 订阅状态

```json
{
  "id": 3,
  "method": "state.subscribe",
  "params": {
    "topics": [
      {"name": "model.state", "maxHz": 15},
      {"name": "model.parameters", "maxHz": 30}
    ]
  }
}
```

### 3.4 方法速查

| 方法 | 用途 |
| --- | --- |
| `external.getState` | 查询模型、位置、运动、表情、动作和挂件 |
| `external.getParameters` | 查询最终 Live2D 参数 |
| `external.getInputs` | 查询面捕与外部混合后的输入 |
| `external.getControlStatus` | 查询注入来源和效果队列数量 |
| `state.subscribe` | 按频率订阅状态或最终参数 |
| `parameter.inject` | 注入一组输入参数 |
| `parameter.clearSource` | 清除一个来源的参数和效果 |
| `effect.trigger` | 触发礼物砸头等语义效果 |
| `model.move` | 立即或平滑移动模型 |

## 4. 原生 API 方法

### 4.1 `external.getState`

返回当前模型、位置、运动扩展、表情、动作和挂件状态。无参数。

| 主要返回字段 | 类型 | 范围/默认值 | 说明 |
| --- | --- | --- | --- |
| `frameId` | 无符号整数 | 从 `1` 递增；尚未发布时为 `0` | 渲染状态帧号 |
| `qpc` | 整数 | Windows QPC 计数 | 高精度时间戳 |
| `qpcFrequency` | 整数 | 每秒 QPC 计数 | 将 `qpc` 换算为秒 |
| `sharedMemory` | 字符串 | 默认 `Local\UtaeLive2D.State.v2` | 共享内存名称 |
| `model.loaded` | 布尔 | 默认 `false` | 模型是否加载完成 |
| `model.name/id/path` | 字符串 | 默认空字符串 | 模型信息 |
| `model.geometry` | 对象 | 见下文；无效时 `valid=false` | Cubism 原始几何及模型到输出坐标变换 |
| `transform` | 对象 | 见“坐标规则” | 保存的基础位置 |
| `effectiveTransform` | 对象 | 见“坐标规则” | 加上运动扩展后的实际位置 |
| `movement` | 对象 | 未启用时 `enabled=false` | 运动扩展配置和当前结果 |
| `render.width/height` | 整数 | 大于等于 `0` | 输出尺寸 |
| `trackingActive` | 布尔 | 默认 `false` | 面捕追踪是否活动 |
| `expressions/motions/items` | 数组 | 默认 `[]` | 表情、动作和挂件状态 |

`model.id` 在模型已加载时始终非空。Studio 使用自有模型档案的标识；缺失时底层模型加载器可对实际加载的 `.moc3` 内容计算 SHA-256，格式为 `sha256:<64 位小写十六进制>`。原生 JSON 与共享内存使用同一个 ID。

`model.geometry` 字段：

| 字段 | 说明 |
| --- | --- |
| `valid` | 几何是否可用；为 `false` 时不得使用其数值计算 |
| `space` | 固定 `output-height` |
| `pose` | 固定 `load`，表示加载姿态静态几何 |
| `canvas.widthPixels/heightPixels` | Cubism 原始画布像素宽高 |
| `canvas.originXPixels/originYPixels` | Cubism 原始画布原点像素 |
| `canvas.pixelsPerUnit` | Cubism 模型单位到画布像素的比例 |
| `drawableBounds.left/bottom/right/top` | 加载姿态 drawable 原始模型坐标边界 |
| `modelToScene` | `[m00,m01,m10,m11,tx,ty]`，原始模型单位到输出高度坐标 |

`modelToScene` 固定使用：

```text
x_scene = m00*x + m01*y + tx
y_scene = m10*x + m11*y + ty
```

两套坐标都为 X 向右、Y 向上；scene 中 `1.0` 等于输出画面高度。矩阵已包含 `.model3.json` layout 和 Studio 的 `fitScale_`，但不包含用户位置、缩放和旋转。

`movement` 字段：

| 字段 | 范围/默认值 | 说明 |
| --- | --- | --- |
| `enabled` | 默认 `false` | 是否启用模型运动扩展 |
| `x/y/z` | 模型配置值，默认 `0` | 三轴运动强度；API v2 不在这里限制范围 |
| `smoothingX/Y/Z` | 模型配置值，默认 `10` | 三轴平滑强度 |
| `inputX/Y/Z` | 实时数字，默认 `0` | 平滑后的 `FacePositionX/Y/Z` |
| `translationX/Y` | 实时数字，默认 `0` | 最终画面位移 |
| `distanceScale` | `0.1..10`，默认 `1` | Z 轴产生的距离缩放 |

### 4.2 `external.getParameters`

返回表情、动作、呼吸、物理和 Cubism `Update()` 完成后的最终参数。无参数。

```json
{
  "modelLoaded": true,
  "modelName": "MO",
  "modelID": "c224...",
  "parameters": [
    {"name":"ParamAngleX","value":3.2,"min":-30.0,"max":30.0,"defaultValue":0.0}
  ]
}
```

`min`、`max`、`defaultValue` 来自当前模型，没有统一固定范围。没有模型时 `parameters=[]`。

### 4.3 `external.getInputs`

返回混入外部来源后的面捕输入。无参数。每个输入包含 `name`、`value`、`min`、`max`、`defaultValue` 和 `addedBy`。

| 字段 | API v2 固定值 |
| --- | --- |
| `min` | `-1000000` |
| `max` | `1000000` |
| `defaultValue` | `0` |
| `addedBy` | `Utae Live2D Studio` |

### 4.4 `external.getControlStatus`

无参数。

| 返回字段 | 类型 | 说明 |
| --- | --- | --- |
| `sourceCount` | 整数 | 尚未过期的参数注入来源数 |
| `effectCount` | 整数 | 正在执行和等待执行的效果总数 |
| `queuedEffectCount` | 整数 | 尚未开始的排队效果数 |

### 4.5 `state.subscribe`

替换当前连接的订阅列表，不影响其他连接。

| 参数 | 类型 | 必填 | 范围/默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `topics` | 数组 | 否 | 默认 `[]` | 空数组取消全部订阅 |
| `topics[].name` | 字符串 | 是 | `model.state` 或 `model.parameters` | 主题名 |
| `topics[].maxHz` | 整数 | 否 | 默认 `30`；限制到 `1..60` | 此连接的最高推送频率 |

可以简写成 `"topics":["model.state"]`，此时 `maxHz=30`。

事件格式为 `{"event":"external.state","patch":{}}`。

| 主题 | 事件名 | `patch` 内容 |
| --- | --- | --- |
| `model.state` | `external.state` | 与 `external.getState` 相同 |
| `model.parameters` | `external.parameters` | 与 `external.getParameters` 相同 |

服务端只保留每个主题的最新待发送帧。慢客户端不会无限积压，也不会阻塞渲染线程。

成功结果为 `{"accepted":true,"snapshot":{...}}`，其中 `snapshot` 与 `external.getState` 相同。

### 4.6 `parameter.inject`

向面捕输入层注入参数。注入发生在参数映射、表情、动作和物理之前。

| 参数 | 类型 | 必填 | 范围/默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `source` | 字符串 | 否 | 默认 `native`；不能为空 | 来源；同名新数据覆盖旧数据 |
| `mode` | 字符串 | 否 | 默认 `set`；`set` 或 `add` | 混合方式 |
| `priority` | 整数 | 否 | 默认 `50`；限制到 `-1000..1000` | 从低到高混合 |
| `weight` | 数字 | 否 | 默认 `1.0`；限制到 `0..1` | 来源整体权重 |
| `ttlMs` | 整数 | 否 | 默认 `1000`；限制到 `1..60000` ms | 到期自动清除 |
| `values` | 对象或数组 | 否 | 默认 `{}` | 参数 ID 和数值 |
| 参数值 | 数字 | 是 | 有限数，`-1000000..1000000` | 越界拒绝整条请求 |

`values` 支持两种写法：

```json
{"FaceAngleX":8.0,"EyeOpenLeft":-0.4}
```

```json
[{"id":"FaceAngleX","value":8.0},{"id":"EyeOpenLeft","value":-0.4}]
```

混合公式：

- `add`：`当前值 += 注入值 × weight`
- `set`：`当前值 += (注入值 - 当前值) × weight`

同一个 `source` 再次调用会整体替换该来源的参数、模式、优先级、权重和 TTL。

成功结果与 `external.getControlStatus` 相同。

### 4.7 `parameter.clearSource`

清除指定来源的注入参数，以及该来源正在执行或排队的效果。

| 参数 | 类型 | 必填 | 范围/默认值 |
| --- | --- | --- | --- |
| `source` | 字符串 | 是 | 非空，无默认值 |

重复清除不存在的来源也返回成功。

成功结果为 `{"cleared":"来源名"}`。

### 4.8 `effect.trigger`

触发语义效果。当前只支持礼物砸头 `flinch`。

| 参数 | 类型 | 必填 | 范围/默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `preset` | 字符串 | 否 | 默认 `flinch`；仅 `flinch` | 效果类型 |
| `source` | 字符串 | 否 | 默认 `native-effect`；不能为空 | 来源和排队分组 |
| `side` | 字符串 | 否 | 默认 `right`；建议 `left/right` | 只有 `left` 按左侧处理，其他值按右侧 |
| `intensity` | 数字 | 否 | 默认 `1.0`；限制到 `0..4` | 强度 |
| `durationMs` | 整数 | 否 | 默认 `480`；限制到 `16..5000` ms | 单次时间 |
| `queue` | 布尔 | 否 | 默认 `false` | 是否等待同来源前一个效果结束 |

队列规则：

- `queue=false`：立即执行，替换同一 `source` 的所有旧效果。
- `queue=true`：排到同一 `source` 最后一个效果之后；不同来源可同时执行。
- API v2 不限制显式排队数量，调用方应自行限制直播高峰队列长度。

`flinch` 使用二次衰减包络。`intensity=1` 时峰值为：

| 输入参数 | 峰值变化 |
| --- | --- |
| `FaceAngleZ` | 左侧 `+19`，右侧 `-19` |
| `FaceAngleX` | `+17` |
| `FaceAngleY` | 左侧 `-10`，右侧 `+10` |
| `EyeOpenLeft` | `-0.8` |
| `EyeOpenRight` | `-0.8` |

实际最终参数变化还取决于模型参数映射、表情、动作和物理。

成功结果与 `external.getControlStatus` 相同，可直接看到新的效果总数和排队数。

### 4.9 `model.move`

在 Utae 原生坐标中移动主模型。

| 参数 | 类型 | 必填 | 范围/默认值 | 说明 |
| --- | --- | --- | --- | --- |
| `x` | 数字 | 否 | 无显式限制；绝对模式保持不变，相对模式默认 `0` | 水平位置或增量 |
| `y` | 数字 | 否 | 无显式限制；绝对模式保持不变，相对模式默认 `0` | 垂直位置或增量 |
| `scale` | 数字 | 否 | 绝对模式保持不变；相对模式默认 `0` | 缩放或增量；最终限制到 `0.1..20` |
| `rotation` | 数字 | 否 | 无显式限制；绝对模式保持不变，相对模式默认 `0` | 度或度增量 |
| `duration` | 数字 | 否 | 默认 `0`；限制到 `0..10` 秒 | `0` 为立即移动 |
| `relative` | 布尔 | 否 | 默认 `false` | 是否使用增量 |

坐标规则：

- `x=0,y=0` 是画面中心；`x` 向右为正，`y` 向下为正。
- 坐标以输出画面高度归一化；`y=0.5` 大约是中心到画面底边。
- `scale=1` 是基础大小。
- 动画使用平滑起止插值；新移动请求替换未完成的旧移动。

成功结果为 `{"accepted":true}`。该命令只改变运行时位置，不写入模型 `.uvtb`。

## 5. Windows 共享内存

共享内存适合每渲染帧读取。ABI 定义在 `src/runtime/ExternalState.h`。

### 5.1 标识与固定容量

| 项目 | 值 |
| --- | --- |
| 映射名 | `Local\UtaeLive2D.State.v2` |
| 魔数 | `UTAEL2D`，占 8 字节，末尾为 `0` |
| `abiVersion` | `2` |
| 参数/表情/动作 ID | 每个 `64` 字节 UTF-8 缓冲 |
| 模型名称 | `128` 字节 UTF-8 缓冲 |
| 模型 ID | `128` 字节 UTF-8 缓冲 |
| 最大输入数 | `512` |
| 最大最终参数数 | `2048` |
| 最大表情数 | `256` |
| 最大动作数 | `256` |
| 最大挂件数 | `256` |

超出容量的尾部数据不会写入共享内存；WebSocket JSON 查询不受固定数组容量限制。

### 5.2 安全读取

1. `OpenFileMappingW(FILE_MAP_READ, FALSE, L"Local\\UtaeLive2D.State.v2")`。
2. `MapViewOfFile(..., FILE_MAP_READ, ...)` 建立只读映射。
3. 校验 `magic`、`abiVersion` 和 `structSize`。
4. 读取 `sequence`；奇数表示正在写，需重试。
5. 读取数据后再次读取 `sequence`。
6. 只有前后相同且为偶数时，快照才有效；否则重试。
7. 仅当 `catalogGeneration` 变化时重读 ID、范围和默认值目录。

### 5.3 关键字段

| 字段 | 类型/范围 | 说明 |
| --- | --- | --- |
| `sequence` | 64 位整数；偶数稳定、奇数写入中 | 无锁一致性序号 |
| `frameId` | 64 位无符号整数 | 渲染帧号 |
| `qpc/qpcFrequency` | 64 位整数 | 高精度时间和频率 |
| `catalogGeneration` | 32 位无符号整数 | 目录变化代数 |
| `flags bit0/1/2/3` | `0/1` | 模型已加载/追踪活动/运动扩展启用/模型几何有效 |
| `modelCanvas[5]` | `float` 数组 | 画布宽、高、原点 X、原点 Y、`pixelsPerUnit` |
| `modelDrawableBounds[4]` | `float` 数组 | drawable 原始模型坐标 left、bottom、right、top |
| `modelToScene[6]` | `float` 数组 | m00、m01、m10、m11、tx、ty |
| `baseTransform[4]` | `x,y,scale,rotation` | 基础位置 |
| `effectiveTransform[4]` | `x,y,scale,rotation` | 实际渲染位置 |
| `reservedTransform[4]` | 保留槽，恒为零 | 保持 ABI v2 后续字段偏移不变，不提供第三方坐标 |
| `inputValues` | `float` 数组 | 输入目录对应值 |
| `mappedValues` | `float` 数组 | 映射阶段值，与最终参数目录对齐 |
| `finalValues` | `float` 数组 | 最终参数，与最终参数目录对齐 |
| `expressionActive/motionActive` | `0/1` 数组 | 表情和动作状态 |
| `items` | 固定结构数组 | ID、类型、ArtMesh 固定信息、位置、缩放、旋转、透明度 |

`parameterCatalog` 的 `minimum/maximum/defaultValue` 来自模型。API v2 的 `inputCatalog` 主要用于 ID；输入允许范围使用 `-1000000..1000000`。

## 6. 外部接入边界

仅提供原生 `/ws` 与共享内存接口。第三方应用兼容 WebSocket、报文外壳和坐标换算已移除。模型绑定文件的手动导入不提供网络协议兼容。

## 7. 错误和边界行为

| 情况 | 原生错误码 |
| --- | --- |
| JSON 无法解析 | `PARSE_ERROR` |
| 缺少或错误的 `method` | `INVALID_REQUEST` |
| 未知方法 | `METHOD_NOT_FOUND` |
| 参数类型、枚举或范围无效 | `INVALID_PARAMS` |
| 未知效果 | `UNKNOWN_EFFECT` |

文档写“限制到范围”的字段会自动限制；写“必须在范围内”的字段越界会拒绝请求。

## 8. 独立礼物测试程序

先启动 Studio 并加载模型：

```bat
礼物砸头测试.bat --queue --count 3 --side left
```

程序通过 `/ws` 触发效果，再从共享内存打印明显变化的最终 Live2D 参数。

| 参数 | 范围/默认值 | 说明 |
| --- | --- | --- |
| `--queue` | 默认关闭 | 开启排队 |
| `--count N` | 默认 `1`；限制到 `1..100` | 发送次数 |
| `--side left\|right` | 默认 `right` | 方向 |
| `--duration MS` | 默认 `480`；限制到 `16..5000` | 单次毫秒数 |
| `--port PORT` | 默认 `48991`；有效 TCP 端口为 `1..65535` | API 端口 |

未加载模型时仍可连接，但最终参数列表为空。
