# 公开支持邮箱维护

网站公开地址为 `support@alexchaoflow.com`，用于使用问题、建议及隐私相关请求。支持页、隐私政策和当前版本说明都提供对应 mailto 链接；用户点击后由自己的邮件客户端发信，网站没有新增表单或邮件发送后端。

## 最新收件证据（2026-10-03）

用户报告从不同于目标收件邮箱的另一个邮箱向 support 地址发信后已收到。当前收件状态为 receipt-confirmed-by-user，证据来源是用户确认；Agent 未独立查看收件箱或邮件头。详见[新的日期报告](reports/2026-10-03-support-email-receipt-user-report.md)。下方保留的是完成配置、尚未收到用户确认时的历史状态。

## 配置与验证状态

2026-10-03 已确认 Cloudflare Email Routing 目标地址通过验证、精确 support 规则 Active、catch-all Disabled。目标收件邮箱及账户资料只保留在服务配置中，不保存到网页或此公开仓库。

同日公开 DNS 查询在 Cloudflare 权威解析器和 8.8.8.8 一致：

| 类型 | 名称 | 公开配置 |
| --- | --- | --- |
| MX | @ | 优先级 19：route2.mx.cloudflare.net |
| MX | @ | 优先级 30：route1.mx.cloudflare.net |
| MX | @ | 优先级 89：route3.mx.cloudflare.net |
| TXT / SPF | @ | v=spf1 include:_spf.mx.cloudflare.net ~all |
| TXT / DKIM | cf2024-1._domainkey | 平台生成的公钥记录已存在 |

这些结果证明配置和 DNS 已生效，**尚未证明外部测试邮件已实际到达目标收件箱**。在完成测试前，记录状态为 configured-awaiting-receipt-test。网站公开联系方式不附加已验证收件或响应时效承诺。

## 真实收件验收

1. 经用户明确授权，从不同于目标收件地址的另一个邮箱发一封测试信到 support 地址；内容只包含无敏感信息的唯一测试标记。
2. 在目标邮箱查找该标记，检查正常收件箱和垃圾箱；不要将真实目标地址或邮件原始头提交公开仓库。
3. 仅记录时间、支持地址、是否收件、必要的去标识故障摘要。收到后再更新 end_to_end_receipt_verified；仅 DNS 成功或规则 Active 不应通过该项。
4. Email Routing 提供收件转发。从目标邮箱直接回复可能使用目标邮箱发件身份；如需以公开支持地址回复，应先单独配置并验证发信服务，不能把转发规则视作已经具备域名发信能力。

Cloudflare 官方说明：[配置及测试](https://developers.cloudflare.com/email-service/get-started/route-emails/) · [回复限制](https://developers.cloudflare.com/email-service/reference/postmaster/)。

## 后续修改

保持公开地址及其在支持页、隐私政策、版本说明中的一致性。变更邮件供应商时先验证新的收件链路，保留已有网站 A、www CNAME 和 GitHub TXT 验证记录。若仅修改网站联系方式或隐私说明，仍需刷新网站资源摘要、版本说明摘要及 App 仓库官网同步凭据。
