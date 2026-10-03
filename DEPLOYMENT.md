# 部署与更新

## 当前流程

网站唯一源码在本仓库 `site/`；直接维护 HTML、CSS、JavaScript 和图片，无构建复制或跨仓发布。修改后更新 `DEPLOYMENT.json` 摘要并完成 [测试](docs/TESTING.md)，合并、推送 main。

[pages.yml](.github/workflows/pages.yml) 对 PR 和主分支进行检查。只有 main 的 push 或 workflow_dispatch 能进入 deploy，部署任务需要检查成功，拥有最小的 contents:read、pages:write、id-token:write 权限。官方 Actions 顶层引用固定提交 SHA，升级时核对官方仓库版本并重新验证。

CI 上传目录仅为 site/，不是仓库根目录。根目录 CNAME、README、脚本、测试和开发文档不会作为网页 artifact 发布。site/.nojekyll 保留；CI 写入 site/deployment.json，内容为实际仓库和 github.sha，用于线上部署追溯，不提交 Git。访问该 JSON 可知正在服务的部署 commit。

GitHub 仓库 Settings → Pages 的 Build and deployment Source 必须为 **GitHub Actions**；这是从旧 main 根目录模式迁移时的一次性设置。自定义域名仍为 alexchaoflow.com，Enforce HTTPS 保持开启。只有实际完成线上测试，才能将迁移标记为已验证。

## 域名与 DNS

- 注册商与权威 DNS：Cloudflare；NS 为 hayes.ns.cloudflare.com、miki.ns.cloudflare.com。
- 根域 `@` 的四条 A：185.199.108.153、185.199.109.153、185.199.110.153、185.199.111.153。
- `www` CNAME：oooscar8.github.io。
- 网站五条记录保持 DNS only。TTL 为 Auto。
- 保留 GitHub 账户域名验证 TXT `_github-pages-challenge-Oooscar8`。
- GitHub Pages 域名绑定、证书与强制 HTTPS 管理网页访问；Cloudflare 不代理当前网页 HTTP 流量。

根 CNAME 内容为 alexchaoflow.com，保留它作为已验证绑定的维护记录。Actions 模式的域名来自 Pages 设置，不依靠把 CNAME 复制到 artifact。DNS 不填写 /jianshan/；网站目录决定路径。官方网站地址、www/HTTP/旧 GitHub 项目 URL 的跳转应在部署后验证。

## 故障定位与恢复

1. Actions check 失败：查看缺失引用、版本说明摘要、网页清单或 JS 错误；修复后重新提交，不跳过检查。
2. deploy 失败：核对 Pages 的 Actions 来源、github-pages environment 和日志。不要改 DNS 来修复脚本错误。
3. 工作流成功但网页不符：检查线上 deployment.json、资源摘要与测试 commit，等待部署传播后以新报告复查。
4. 域名或 HTTPS 失败：分别核对权威 DNS、系统解析、GitHub Pages 域名/证书状态。保留失败证据，不禁用 TLS 验证。
5. 确认需要恢复网页版本时，正常 revert 相关源码提交并经检查重新部署；不强推，不自动改回旧 Pages 发布模式，不修改独立博客。

初次迁移前状态见 [history](docs/history/README.md)。App 上架与网站发布独立；版本同步规则见 [APP_RELEASE_SYNC.md](docs/APP_RELEASE_SYNC.md)。

参考：[GitHub Pages 自定义工作流](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages) · [自定义域名](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site)。
