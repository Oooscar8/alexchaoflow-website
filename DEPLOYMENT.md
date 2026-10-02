# 部署与更新

初始网页来源提交：`c0b533bd89c79a7dc6d4b80cd8b4e549ae13d86d`（私有 App 仓库的 `Website/`）。公开网页文件的 SHA-256 摘要见 [DEPLOYMENT.json](DEPLOYMENT.json)。

维护仓库运行 `python3 Website/build_site.py --output .build/github-pages-<本轮名称>`，将产物同步到本仓库根目录。同步时保留 `.git`、本仓库维护文档及已验证的 CNAME；检查差异、更新来源摘要、提交并推送。

GitHub Pages 使用 main 分支根目录发布。本次仅发布静态网页；没有后端、数据库、支付或自动收集表单。源 App 仓库保持私有。

初始本地验收：4 个 HTML 页面、57 个本地引用通过构建器检查；JavaScript 语法检查通过；浏览器检查截图切换、FAQ展开、隐私/支持导航，390px 宽度四页均无横向溢出。本轮没有修改或重跑 iOS App 测试。

2026-10-03 已确认域名 `alexchaoflow.com` 注册成功且 NS 委派 Cloudflare。GitHub TXT 所有权验证、网站 DNS、Pages 自定义域名绑定和 HTTPS 签发尚待完成；当前继续使用 GitHub Pages 默认地址。默认地址的部署与 HTTPS 状态不代表自定义域名已经验收。配置顺序与官方记录以 [GitHub 文档](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) 为准。DNS 中不填写 `/jianshan/`，该路径已经由本站目录提供。

初始迁移保留历史 Sites 站点，不自动删除旧站点或覆盖用户已有博客。公开支持联系方式与实际 App Store 链接仍待补齐。
