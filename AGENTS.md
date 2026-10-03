# 维护者与 Agents 指南

## 职责与维护入口

本仓库是 AlexChaoFlow 个人网站、见山及未来其他 App 官网的唯一网页源码维护入口，负责网站测试、架构、部署、迭代和测试报告。`site/` 是真实源码；无需复制到 App 仓库，也不要引入第二份提交到 Git 的构建产物。

私有 `Oooscar8/AssetTrack-iOS` 只负责见山 App 开发、测试、开发文档和发布门禁；两个 README 相互索引。用户已明确授权这一职责迁移，旧报告中的 `AssetTrack-iOS/Website` 仅表示历史来源，不是现行流程。

## 工作流程

1. 修改前检查 Git 状态，在 `~/my/alexchaoflow-website` 从最新 main 新建工作分支；保留无关用户改动，不强推。
2. 网页编辑在 `site/`，维护资料在 `docs/`，工具在 `scripts/`，测试在 `tests/`。
3. 审阅变化后运行 `scripts/update_manifest.py`，完成 `docs/TESTING.md` 中相应检查。哈希更新不能代替人工或浏览器验收。
4. 合回 main 并推送后，由 Actions 检查并只发布 site/。PR 仅检查，不获得部署权限。
5. 实际线上验证通过后记录报告；工作流成功、域名可解析、HTTPS 可访问、页面内容正确是不同证据，不相互代替。

## App 版本同步

每次 App 新版本准备 TestFlight 或公开发布，必须按 [APP_RELEASE_SYNC.md](docs/APP_RELEASE_SYNC.md) 更新官网功能、截图、隐私、支持和版本记录，随后通过 App 仓库同步门禁。状态必须符合实际分发情况；GitHub release 不代表 App Store 上架。首版当前为 prepared，下载 URL 为空。

## 发布与数据边界

这是公开仓库，只能保存已获授权公开的网页、合成演示截图、公开版本说明及维护资料。不得提交财务数据、真实财务截图、账号资料、令牌、私钥、签名产物或原始日志。

保留根目录已验证的 CNAME。域名绑定位于 GitHub Pages 设置，Actions 仅上传 site/，根 CNAME 作为维护记录保留。不要修改独立的 Oooscar8.github.io 博客仓库。Cloudflare DNS 仍指向 GitHub Pages，保持 DNS only 和 GitHub 验证 TXT。

`site/deployment.json` 是 CI 根据实际 Git 提交生成的公开部署证据，不提交、不手工编辑，也不属于静态源码哈希清单。其他新资源必须纳入清单。历史报告不覆盖；新验证采用新文件名。短暂网络失败应保留证据并复查，不自动回滚网站或放宽 TLS 验证。
