# ZELUX Protocol

Studio、Device Agent、驱动包和固件包之间的公共契约，当前版本见 `VERSION`。

- `schemas/hello.schema.json`：服务端握手；
- `schemas/driver-manifest.schema.json`：驱动包清单；
- `schemas/firmware-manifest.schema.json`：外设固件包清单；
- `schemas/robotd-imu.schema.json`：robotd 与设备管理层之间的 IMU 数据契约；
- `schemas/imu-management.schema.json`：Studio IMU 管理状态；命令见 `examples/imu-management-commands.json`。型号目录来自 robotctl，客户端不复制轴向定义；
- `schemas/fan-inventory.schema.json`：风扇实例清单；单/多风扇由 `instances` 数组表达，同一型号通过 `driver_id` 复用；
- `schemas/fan-socket.schema.json`：Device Agent 与 root 风扇服务的版本化 JSON 行协议；示例见 `examples/fan-socket-commands.json`；
- `schemas/fan-pwm-setup.schema.json`：Studio/Device Agent 的物理 PWM 引脚配置流程；逻辑 pin ID、逐引脚 readiness、预览、确认应用与重启状态，不接受任意路径或命令；
- `examples/`：合法消息示例；
- Python 协商实现位于 `software/zeluxd/protocol.py`。

规则：新增字段必须可选；删除、改名、改变类型或单位必须提升协议 Major。
提交前运行：`python tools/validate.py`。正式发布将从本仓库生成 TypeScript 和
Python SDK；其他仓库不得维护同名字段的另一套手写定义。

`.zdp` 是 ZIP 容器，根目录必须包含 `manifest.json` 以及清单声明的单个驱动产物。
正式设备只接受由 `drivers/trusted_keys/<key_id>.pem` 中 Ed25519 公钥验证通过的包；
开发模式可以暂存未受信包，但暂存不代表加载，未注册可执行实现的驱动不能被选择。

`.zfw` 同样是 ZIP 容器，包含 `manifest.json` 和单个固件镜像。当前实现只允许验证、
暂存和执行升级前置检查；在具体驱动实现 Bootloader、校验、恢复和回滚接口之前，
`write_enabled` 始终为 `false`。

IMU 型号管理契约新增于 1.3.0；1.4.0 对齐总线 IMU 多姿态机体对齐标定的交互语义。风扇实例与 socket 契约新增于 1.5.0。严格 Schema 验证使用 python -m pip install -r requirements-dev.txt 后执行 python tools/validate.py --schemas。基础无依赖校验仍可执行。型号目录/标称安装规则由 robotd 参数层提供，禁止在 Studio/Agent 维护另一份型号适配判断；标定输出的完整传感器→机体映射由 robotd 配置和运行身份回读。

风扇运行读数的新鲜度、操作结果未知与刷新失败语义见 `docs/fan-runtime-semantics.md`（API v1 向后兼容可选扩展）。

协议 1.6.0：新增只读 fan pwm_readiness 操作，并允许实例携带可选 pwm_pin 逻辑档案 ID。

协议 1.7.0：新增受限的 Studio PWM pin setup 命令/状态契约。具体 root helper 只接受已知 pin ID 和一次性预览 token；Studio 不直接写启动配置或发起远程重启。Agent 在实例创建、启用或启用态更新前需再次校验引脚 ready 和映射一致。
