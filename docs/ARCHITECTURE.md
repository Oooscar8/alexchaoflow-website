# 网站架构

## 仓库边界

`alexchaoflow-website` 统一维护个人品牌首页、见山和未来产品的官网；`AssetTrack-iOS` 维护见山 App。两者通过官网公开版本记录和 App 发布前检查衔接，不再共享可编辑网页副本。

```text
alexchaoflow-website/
  site/                    网页唯一源码，也是 Pages artifact 的目录
    index.html             alexchaoflow.com/
    jianshan/              alexchaoflow.com/jianshan/
      privacy/             隐私政策
      support/             支持说明
      releases.json        供 App 发布门禁读取的公开版本状态
      releases/1.0.0/      对用户公开的版本说明
  scripts/                 静态检查、文件摘要、线上验证
  tests/                   检查工具的正向与失败用例
  docs/                    网站架构、迭代、测试与历史资料
  .github/workflows/       检查与 Pages 发布
```

HTML 提供内容、CSS 提供样式、JavaScript 提供截图切换等交互。现阶段没有打包框架和生成式模板；直接维护浏览器可以读取的文件。新产品可在 `site/<product>/` 增加目录，并更新首页入口、测试和摘要，不需修改 DNS。

## 部署边界

PR 只检查。主分支推送后，Actions 再次检查，生成当前提交的 `deployment.json`，只上传 site/ artifact，经 GitHub Pages 提供 HTTPS。网站维护文档和测试工具保存在公开 GitHub 仓库，但不作为网页 artifact 发布。

Cloudflare 管理域名注册和权威 DNS。四条根域 A 记录与 www CNAME 使用 DNS only；GitHub Pages 管理实际静态文件传输、证书和强制 HTTPS。域名与 `/jianshan/` 路径不因仓库目录迁移改变。

## 版本证据

`DEPLOYMENT.json` 记录网站仓库与 site/、每个源码资源摘要及整份摘要的 SHA-256；避免记录“自身文件所在提交”造成自引用。线上 `deployment.json` 由 CI 写入真实部署 commit，验证报告另行记录测试时 commit、manifest/script 摘要和访问结果。

旧 App 仓库的源码 commit 只保留在 `historical_origin` 与 [history](history/README.md)，不再作为当前网站源码版本。官网公开版本说明由本仓库维护，App 仓库只记录公开同步依据及检查结果。
