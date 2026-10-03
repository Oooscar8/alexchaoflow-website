# 网站测试

## 修改后检查

```bash
python3 scripts/update_manifest.py
python3 scripts/check_site.py
python3 -m unittest discover -s tests -v
node --check site/jianshan/site.js
```

先审阅源码变化，再更新摘要。`check_site.py` 检查 site/ 文件类型、拒绝符号链接和目录外引用、检查本地图片/样式/脚本/锚点、核对全部资源摘要和公开版本状态。检查器以原 App 仓库链接验证为基础迁入；无需构建复制步骤。`tests/` 验证真实失败条件：缺失文件、无效锚点、目录越界、符号链接、非网页文件及未记录/修改的资源。

JavaScript 语法检查不验证交互，链接检查不验证外部服务状态。摘要相同只证明字节相同，不证明文字真实或视觉正确。

## 浏览器验收

本地运行 `python3 -m http.server 4173 --bind 127.0.0.1 --directory site`。检查个人首页、见山首页、隐私、支持及版本说明：主导航和页脚、图片加载、桌面与 390px 窄屏布局、FAQ 展开、三张截图切换、版本入口。所有演示截图仅使用合成数据。

版本更新额外核对：功能介绍是否符合 App 实现；隐私与支持是否与本版一致；公开下载链接是否为已经实际可用的 Apple 地址。prepared 状态不得声称可安装。

## 线上验证

```bash
python3 scripts/verify_deployment.py \
  --website-commit "$(git rev-parse HEAD)" \
  --output .build/reports/https-new-run.json
```

脚本默认读取本仓库 `DEPLOYMENT.json`，验证清单中的 HTTPS 资源字节与四个主要页面的 HTTP、www、旧 GitHub Pages URL 跳转，记录 HTTP 状态、实际地址、TLS 结果与摘要。`--website-commit` 是该次测试对应的部署目标，由调用者确认；实际线上部署身份另以 `https://alexchaoflow.com/deployment.json` 核对。输出采用排他创建，不能覆盖旧报告。curl 禁用用户 curlrc，默认使用系统解析和环境代理，不关闭 TLS。

`--resolve HOST:PORT:PUBLIC_IP` 只用于标注清楚的公开入口诊断；此模式会禁用代理，不代表系统 DNS 已成功。应保留失败运行，再用新文件名复查。完整访问结果与浏览器验收都完成后，才在报告中宣布该版本线上验收通过。

CI 中部署成功不自动视作上述访问验收通过；不因瞬时 DNS 或连接失败自动回滚。网站变化无需重新运行 iOS 测试，App 本身变更仍遵循 App 仓库测试要求。

## 支持邮箱页面检查

公开支持地址应在支持页和隐私政策中同时可见且对应 mailto:support@alexchaoflow.com。检查网页不包含私有目标邮箱，当前版本说明的联系方式与页面一致。HTML 链接检查只能验证 mailto 配置形式，不能证明实际收件；邮件配置和端到端验证按[支持邮箱维护](SUPPORT_CONTACT.md)记录。
