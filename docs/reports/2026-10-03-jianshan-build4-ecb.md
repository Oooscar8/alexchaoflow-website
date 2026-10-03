# 2026-10-03：见山构建 4 官网检查

本次同步 App 1.0.0（构建 4）的 ECB 单一来源参考汇率、换算方向和隐私说明，保持 prepared 状态，没有公开 App Store / TestFlight 下载。

## 来源与范围

已读取本机 App 的 FXService、SettingsView、PrivacyPolicyView 和工程构建号。请求固定为 `https://api.frankfurter.dev/v2/providers/ecb/rates?base=CNY&quotes=USD,HKD,EUR,SGD,GBP,JPY`，固定 User-Agent 为 `AssetTrack/1.0`。Frankfurter 提供 CNY 基准报价；App 解码时取倒数并保留 10 位小数，表示每单位外币对应的人民币。网站用与此一致的用户说明，不公开私有账号信息。

核对的公开来源：[Frankfurter 文档与隐私 FAQ](https://frankfurter.dev/) · [ECB 欧元参考汇率](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html)。网站将“不记录 IP / 请求 URL”明确归属于 Frankfurter 的公开说明，不承诺网络基础设施不处理任何请求信息。

## 本地实际检查

- 5 个 HTML 页面、74 个本地引用、13 个资源摘要与 1 条 prepared 版本记录检查通过；13 个既有网站工具测试通过，JS 语法和 git diff --check 通过。
- 当前说明页只有一个可见 1.0.0 / 4 / prepared 标记，正文显示“1.0.0 (4) · 准备中”，JSON 的 notes_sha256 与原始 HTML 字节一致。
- 首页、隐私页、支持页、版本说明及版本 JSON 共 5 个网页资源更新；其余 8 个网页资源摘要保持不变，合成图片、样式及交互脚本未修改。
- 支持、隐私、版本说明继续只公开 support@alexchaoflow.com；site/ 未发现任何 Gmail 地址。无 Apple 下载 URL。
- 新增[用户报告收件证据](2026-10-03-support-email-receipt-user-report.md)，明确没有独立查看收件箱。之前的未测试报告和 HTTP 26/29、27/29 结果原样保留。
- 本地检查摘要见[JSON 证据](2026-10-03-jianshan-build4-ecb-local.json)。

## 部署与验收边界

本地准备完成后再记录实际部署提交、Actions 结果及正常 DNS/TLS 访问证据。此前其他构建的结果不能代替本次验证。本轮尚未新增浏览器验收，也不把用户报告收件写成 Agent 独立验证。此网站报告不代替 App 测试或 Apple 审核结果。

## 实际部署与线上验证

官网内容提交 `a00648bdef03ea94475a7f603a9259b17380b85e` 已由 [Pages Actions 37128825031](https://github.com/Oooscar8/alexchaoflow-website/actions/runs/37128825031) 成功发布。正常 TLS 获取 deployment.json 返回相同提交。

[本轮完整 HTTP 检查](2026-10-03-jianshan-build4-production.json)为 **26/29**，没有达到单次完整通过：

- assets.png 返回 HTTP 200、TLS 验证 0，但在 25 秒内只下载 205726/225685 字节。
- 隐私页直接 HTTPS 返回 HTTP 200、TLS 验证 0，但只下载 1337/6448 字节。
- styles.css 请求 25 秒内收到 0 字节。
- 这三项均为 curl 退出 28，正文不完整或未取回，按失败保存；其余 26 项通过，包括 16 个跳转的最终网址和内容摘要。
- 保持正常系统 DNS、环境默认代理、TLS 验证、原 25 秒限时和完整正文摘要检查，没有使用地址覆盖或跨轮次拼接通过结论。原始 JSON 逐字节归档。
- Pages 成功与已获取的正确内容不能证明所有访问稳定；本轮 HTTP 状态为 deployed-partial-network-timeouts，间歇超时原因尚未定位。
- 本次证据收尾没有改变 site/ 字节、版本说明摘要或公开版本记录。仍没有新增浏览器验收；支持邮件的收件结论仍仅来自用户报告，未独立查看邮箱。
