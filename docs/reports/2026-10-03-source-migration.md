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
