# ZELUX 公共协议基线

本目录是独立 `zelux-protocol` 仓库建立前的过渡契约源，当前版本为 `1.1.0`。

- `schemas/hello.schema.json`：服务端握手；
- `schemas/driver-manifest.schema.json`：驱动包清单；
- `examples/`：合法消息示例；
- Python 协商实现位于 `software/zeluxd/protocol.py`。

规则：新增字段必须可选；删除、改名、改变类型或单位必须提升协议 Major。
完成独立拆仓后，本目录迁移至 `zelux-protocol`，Studio 和 Agent 改为依赖其发布产物。

