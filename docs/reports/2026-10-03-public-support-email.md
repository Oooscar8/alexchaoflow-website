# 2026-10-03：公开支持邮箱页面验证

用户已授权公开 support@alexchaoflow.com。支持页、隐私政策和当前版本说明增加可见邮件链接，清理当前文档中“联系方式待补齐”的描述。App 仍为 1.0.0（构建 3）prepared，下载 URL 为空。

## 本地实际检查

- 5 个 HTML 页面、74 个本地引用、13 个网页资源摘要和公开版本状态检查通过；13 个既有测试通过，JavaScript 语法及 git diff --check 通过。
- 三个页面的 mailto 均精确匹配 support@alexchaoflow.com，链接文字包含同一公开地址；site/ 中未发现任何 Gmail 收件地址。
- 修改限于支持页、隐私页、当前版本说明及版本 JSON；其余 9 个网页资源摘要保持不变。历史准备阶段和 HTTP 检查报告未覆盖。
- 首次写入尝试因 stdin 编码错误在解析时失败，未修改源码；上述验收来自改用明确编码后对实际新内容的运行。
- 新增主动发送邮件时的信息处理说明，未改变 App 账本功能。App 仓库需同步审阅联系渠道和刷新固定网站提交 / notes_sha256。
- 原始本地摘要见[本地证据](2026-10-03-public-support-email-local.json)。

## 邮件验证范围

Cloudflare 控制台已确认目标地址验证、精确 support 规则 Active、catch-all Disabled。此处只记录公开支持地址，私有目标邮箱不进入仓库。公开权威 DNS 与 8.8.8.8 已一致查到 MX/SPF/DKIM，详见[配置](../SUPPORT_CONTACT.md)。

**尚未执行并确认外部测试邮件实际收件。** 配置成功、DNS 生效、网页上线与真正收到邮件是不同验收项，不能互相替代。

## 本地准备阶段的部署边界

本地阶段已通过，待正式部署后追加实际 Actions 提交、HTTPS 资源与跳转结果。网页浏览器验收本轮尚未执行；不得将先前构建的视觉验收写成本次已验证。

## 已部署与线上 HTTP 结果

官网内容提交 `8c5e0cac94d3d31fad3f5d0eba85aa18da41608c` 已由 [Pages Actions 37127404041](https://github.com/Oooscar8/alexchaoflow-website/actions/runs/37127404041) 成功发布，正常 TLS 获取 deployment.json 也返回同一提交。网站公开联系方式已部署，但两次完整 HTTP 运行均遇到超时，**本轮尚未达到单次完整 29/29 验收**。

- [首次完整检查](2026-10-03-public-support-email-production-first.json)：26/29。expenses.png、根域 HTTP 跳转和隐私页 HTTP 请求在 25 秒限制内超时。该次支持页、隐私页、版本说明的直接 HTTPS 请求成功且内容摘要匹配。
- [同条件完整复查](2026-10-03-public-support-email-production-recheck.json)：27/29。assets.png 只接收 142873/225685 字节，支持页直接 HTTPS 只接收 2289/5362 字节；两者均 HTTP 200、TLS 校验 0，但 curl 退出 28、正文摘要不完整，仍按失败处理。其余 27 项通过。
- 两轮保持正常系统 DNS、环境默认代理、TLS 校验、25 秒超时、完整内容摘要条件；没有解析覆盖、跳过 TLS 或合并不同轮次伪称全部通过。两个原始报告逐字节保留。
- 当前证据能确认 Pages 部署和新页面在成功请求中提供正确内容；间歇网络超时的原因尚未定位，不能据此承诺访问稳定性。
- 此次仅补文档证据，不修改网页资源。本轮仍未新增浏览器验收，仍未执行外部测试邮件的真实收件验收。
