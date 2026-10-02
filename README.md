# AlexChaoFlow 网站

AlexChaoFlow 产品主页与见山 iOS App 官网。静态 HTML、CSS 和 JavaScript，无运行时依赖。

## 入口索引

- [产品主页](index.html)
- [见山官网](jianshan/index.html)
- [隐私政策](jianshan/privacy/index.html)
- [使用支持](jianshan/support/index.html)
- [部署与更新说明](DEPLOYMENT.md)
- [来源提交与文件摘要](DEPLOYMENT.json)
- [维护者与 Agents 指南](AGENTS.md)

## 本机预览

在本仓库运行 `python3 -m http.server 4173 --bind 127.0.0.1`，打开 `http://127.0.0.1:4173/jianshan/`。

GitHub Pages 发布 `main` 分支根目录，`.nojekyll` 保证直接提供静态文件。默认访问地址为 https://oooscar8.github.io/alexchaoflow-website/jianshan/ 。目标自定义地址为 `https://alexchaoflow.com/jianshan/`，域名已注册并委派 Cloudflare；所有权验证、网站 DNS、Pages 绑定和 HTTPS 尚未完成，不能把目标地址当作已上线。

App 尚未在 App Store 发布，页面不提供虚假的下载链接。支持联系方式将在公开发行前补齐。
