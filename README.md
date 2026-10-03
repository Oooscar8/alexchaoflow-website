# AlexChaoFlow 网站

这是 AlexChaoFlow 个人网站，以及见山和未来其他 App 官网的唯一网页源码仓库。网站使用静态 HTML、CSS、JavaScript 和图片，没有运行时后端或数据库。

正式入口：[个人首页](https://alexchaoflow.com/) · [见山官网](https://alexchaoflow.com/jianshan/) · [隐私政策](https://alexchaoflow.com/jianshan/privacy/) · [使用支持](https://alexchaoflow.com/jianshan/support/)。见山当前官网记录为 1.0.0（构建 3）准备版本，新增 App 内使用支持入口；仍在准备上架，尚无公开 App 下载或公开支持联系方式。

## 开发入口

| 内容 | 位置 |
| --- | --- |
| 个人首页 | [site/index.html](site/index.html) |
| 见山官网 | [site/jianshan/index.html](site/jianshan/index.html) |
| 版本公开状态 | [site/jianshan/releases.json](site/jianshan/releases.json) · [1.0.0 说明](site/jianshan/releases/1.0.0/index.html) |
| 网站架构与职责 | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| 本地验证、浏览器检查与线上验证 | [docs/TESTING.md](docs/TESTING.md) |
| 发布、域名与故障排查 | [DEPLOYMENT.md](DEPLOYMENT.md) |
| App 版本与官网同步 | [docs/APP_RELEASE_SYNC.md](docs/APP_RELEASE_SYNC.md) |
| 当前网页文件摘要 | [DEPLOYMENT.json](DEPLOYMENT.json) |
| 迭代记录 | [docs/iterations/README.md](docs/iterations/README.md) |
| 测试报告 | [docs/reports/README.md](docs/reports/README.md) |
| 历史来源记录 | [docs/history/README.md](docs/history/README.md) |
| 维护者与 Agents 规则 | [AGENTS.md](AGENTS.md) |

## 本机开发

本地仓库为 `~/my/alexchaoflow-website`。从最新 `main` 新建工作分支，直接编辑 `site/`；不再从 App 仓库复制网页，也不生成并提交第二份 `dist/`。

```bash
python3 -m http.server 4173 --bind 127.0.0.1 --directory site
```

打开 `http://127.0.0.1:4173/` 或 `/jianshan/`。修改并审阅网页后运行：

```bash
python3 scripts/update_manifest.py
python3 scripts/check_site.py
python3 -m unittest discover -s tests -v
node --check site/jianshan/site.js
```

GitHub Actions 对 PR 执行检查；`main` 推送或在 `main` 手动运行后，仅将 `site/` 发布至 GitHub Pages。Cloudflare 管理域名与 DNS，网页流量以 DNS only 方式直接到 GitHub Pages。

[AssetTrack-iOS](https://github.com/Oooscar8/AssetTrack-iOS) 是私有 App 仓库，负责 iOS 源码、App 测试、产品架构、调试和 App 版本记录。每次准备 TestFlight 或正式发布见山新版本，必须先更新本仓库相应页面和版本记录，再通过 App 仓库的官网同步检查；具体步骤见[同步协议](docs/APP_RELEASE_SYNC.md)。
