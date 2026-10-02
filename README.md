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

GitHub Pages 发布 `main` 分支根目录，`.nojekyll` 保证直接提供静态文件。目标自定义地址为 `https://alexchaoflow.com/jianshan/`。域名已注册并完成 GitHub 所有权验证与 Pages 绑定，仓库保留 GitHub 生成的 CNAME。网站 DNS、HTTPS 与公开访问验证待完成。旧 GitHub Pages 官网地址已 301 跳转至 `http://alexchaoflow.com/jianshan/`，当前处于切换配置中，不能把旧地址当作独立备用入口或将目标 HTTPS 地址宣称为已上线。

App 尚未在 App Store 发布，页面不提供虚假的下载链接。支持联系方式将在公开发行前补齐。
