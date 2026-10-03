# 见山 App 与官网的版本同步

每次见山 App 新版本准备 TestFlight 或正式上架，必须同步更新官网。网页内容只在本仓库修改；App 仓库维护自己的产品实现、发布资料以及官网同步门禁结果。

## 公开协议

`site/jianshan/releases.json` 使用 schema_version 1、app_id `com.oooscar8.AssetTrack`。releases 中每条记录包含字符串 version、build、state、updated_at、notes_url、notes_sha256、app_store_url、testflight_url。每个 marketing version 只保留一条当前 build/state 记录，避免同一说明页指向相互矛盾的分发状态。

| state | 真实状态 | 下载字段 |
| --- | --- | --- |
| prepared | 准备版本，尚未公开分发 | app_store_url 与 testflight_url 均为 null |
| testflight | 已具备相应 TestFlight 分发 | app_store_url 为 null；testflight_url 可为 null（非公开测试），或真实 Apple 邀请地址 |
| published | 已在 App Store 正式上架 | app_store_url 为真实 App Store 地址；testflight_url 为 null |

更新说明地址为 `https://alexchaoflow.com/jianshan/releases/<version>/`，页面文件是该目录的 index.html，notes_sha256 对应页面原始字节。GitHub release、归档成功、签名或上传成功均不能单独证明 App Store 已发布。公开 URL 格式检查也不能证明安装可用，发布时必须核实实际 Apple 状态。

当前记录为 1.0.0、build 2、prepared。未来状态变更更新该版本唯一记录及说明页，旧阶段保留在 Git 历史。说明页必须有可见数据块标记 data-release-version、data-release-build、data-release-state，正文同时显示版本、构建和“准备中 / 测试中 / 已发布”的对应状态。每次更新说明先修改网页，再重新计算 notes_sha256，最后运行 scripts/update_manifest.py。

## 每次版本发布的步骤

1. 在 App 仓库确定 version/build 与真实分发状态，完成对应 App 测试和发布资料。
2. 在本仓库新建分支，更新功能介绍、合成截图、隐私政策、使用支持及下载状态。逐项审阅；未变化的内容在版本说明中注明沿用，不机械改日期。
3. 增加或更新版本说明，更新 releases.json、notes_sha256、首页版本入口和 DEPLOYMENT.json；完成本地及浏览器检查。
4. 合并推送，待 Pages 完成后读取 deployment.json，并验证线上页面、releases.json 和更新说明内容。
5. 在 App 仓库记录固定的网站源码提交及相应版本信息，执行 App 仓库文档指定的官网同步检查。其检查会确认公开提交中的版本记录/说明与线上字节一致，并记录当前部署提交。
6. 同步检查通过后继续相应 App 发布步骤。Apple 实际分发状态改变时，及时再次更新网站状态与真实下载链接，并再次验证。

App 仓库控制自身发布门禁，网站仓库不持有 App 私有仓库访问令牌，也不调用 Apple 发布。当前采用明确的双仓发布检查；不存在通过 App 推送自动生成产品说明的流程。
