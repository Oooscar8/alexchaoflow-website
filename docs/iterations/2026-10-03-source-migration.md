# 2026-10-03：网站源码独立维护

网站职责迁入 alexchaoflow-website：site/ 直接维护个人首页、见山和未来产品官网，scripts/ 与 tests/ 维护网站检查，docs/ 维护网站设计和发布记录。App 仓库只保留 App 开发职责及官网发布同步检查。

旧网页移动到 site/，不再维护第二份 dist。旧的 11 个静态资源中，10 个原字节不变；见山首页只新增“版本记录”页脚链接。新增 1.0.0（构建 2）prepared 说明和 releases.json，没有新增公开下载。

Pages 切换为 Actions：PR 仅检查；main 检查成功后只上传 site/，CI 写入真实部署提交。根 CNAME 保留，正式域名和 URL 路径不变。迁移上线状态与实际测试见[报告](../reports/2026-10-03-source-migration.md)。

每次 App 版本发布都需要先更新官网，再通过 App 仓库官网同步门禁；[同步协议](../APP_RELEASE_SYNC.md)说明字段与操作顺序。
