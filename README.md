# ZELUX 公共协议基线

本目录是独立 `zelux-protocol` 仓库建立前的过渡契约源，当前版本为 `1.1.0`。

- `schemas/hello.schema.json`：服务端握手；
- `schemas/driver-manifest.schema.json`：驱动包清单；
- `schemas/firmware-manifest.schema.json`：外设固件包清单；
- `examples/`：合法消息示例；
- Python 协商实现位于 `software/zeluxd/protocol.py`。

规则：新增字段必须可选；删除、改名、改变类型或单位必须提升协议 Major。
完成独立拆仓后，本目录迁移至 `zelux-protocol`，Studio 和 Agent 改为依赖其发布产物。

`.zdp` 是 ZIP 容器，根目录必须包含 `manifest.json` 以及清单声明的单个驱动产物。
正式设备只接受由 `drivers/trusted_keys/<key_id>.pem` 中 Ed25519 公钥验证通过的包；
开发模式可以暂存未受信包，但暂存不代表加载，未注册可执行实现的驱动不能被选择。

`.zfw` 同样是 ZIP 容器，包含 `manifest.json` 和单个固件镜像。当前实现只允许验证、
暂存和执行升级前置检查；在具体驱动实现 Bootloader、校验、恢复和回滚接口之前，
`write_enabled` 始终为 `false`。
