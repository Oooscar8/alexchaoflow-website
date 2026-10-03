# 2026-10-03：网站源码迁移检查

本报告记录仓库结构与本地检查；该阶段尚未宣布新的 Pages Actions 流程已上线。后续 CI、线上 HTTP 和浏览器验收由发布维护者记录，不能用旧域名验收代替。

## 改动范围

网页唯一源码迁到 site/。旧的 11 个资源逐一比较：10 个字节不变；见山首页只增加指向版本记录的页脚链接，去掉该链接后恢复原 SHA-256。新建 1.0.0（构建 2）prepared 说明页与 releases.json。根 CNAME 原字节不变。来源、摘要与比较明细见[本地证据 JSON](2026-10-03-source-migration-local.json)。

## 实际本地结果

- 5 个 HTML 页面、73 个本地引用、13 个资源摘要、1 条公开 prepared 记录检查通过。
- 13 个单元测试通过，覆盖本地引用失败、目录越界、符号链接、资源摘要漂移、准备版错误下载入口、版本说明摘要不符及单版本记录冲突等条件。
- JavaScript 语法、所有 Python AST 解析、工作流 YAML 解析和 git diff --check 通过。
- 线上验证脚本 --help 可用；现有报告路径返回退出码 2，旧字节保持不变；默认仍验证 TLS。
- 官方 Actions 顶层 SHA 从官方仓库标签读取并固定。PR 只检查，main 检查成功后才取得 Pages 部署权限，artifact 仅包含 site/。

本轮不改变 iOS App 行为，不运行 iOS 测试。本地文本/语法检查不能证明浏览器交互和真实公网部署成功。

## 线上验收

待实际迁移部署后补充：GitHub Actions run、Pages build_type、部署 commit、正式资源及跳转检查、五页浏览器和窄屏验收。待全部通过后更新 DEPLOYMENT.json 的 migration_status；保留此处本地阶段证据。


## 后续线上验收完成

- 先将 Pages build_type 从 legacy 改为 workflow，GET 确認 cname=alexchaoflow.com、https_enforced=true、所有权 verified；随后合并并推送网站提交 `9141b604aadbdaac585bdcfe6c8f822ee026d03f`。旧站点在新 artifact 部署前继续服务，Cloudflare 配置和域名未改动。
- [实际 Actions run](https://github.com/Oooscar8/alexchaoflow-website/actions/runs/37109513230) 的 check 与 deploy 均 success，部署完成于 2026-10-03T08:23:28Z。PR 的只检查分支通过代码审查，未为本次工作创建 PR。
- 正常系统解析与 TLS 验证下 **29/29**（13 资源 + 原四页 16 跳转）单次通过；源文件哈希与正式 HTTPS 地址匹配。见[原始验证 JSON](2026-10-03-source-migration-production.json)。没有将新版本页跳转计入原有16项。
- 正式站五页在 1280px 与 390px 检查标题、正文、图片与横向溢出；最终各页无破图、无待加载图片、无横向溢出。版本记录入口显示 1.0.0 (2) 准备中，FAQ 展开成功。初始图片/load 等待和根页导航有超时，随后实际加载完成；保留该观察，不写成所有导航首次都成功。见[浏览器摘要](2026-10-03-source-migration-browser.json)。临时视口已恢复。
- App 仓库的真实 prepared 版本核验通过；其报告在 App 仓库保存，未执行 TestFlight、App Store 发布或新 iOS 测试。
- 本次后续提交只补维护文档与证据，不改变 site/ 的网页字节；DEPLOYMENT.json 的源文件摘要保持可复查，CI 生成 deployment.json 记录每次实际部署提交。

后续证据提交前：11份 Markdown / 31个本地目标 / 0错误，source revision 与13资源摘要保持不变，diff检查通过。外部链接和标题锚点不属于文档检查范围。
