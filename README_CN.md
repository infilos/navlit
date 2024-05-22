## Navlit

简单轻量易用的导航服务。

### 主要功能

- 访客(无需登录)：
  - 访问导航服务首页，浏览并点击站点卡片以访问目标站点。
  - 访问导航服务提交页，编辑提交站点卡片申请，稍后由管理员完成审核。
- 操作员：
  - **以访客身份访问导航登录页，注册或登录成为操作员。**
  - 访问导航服务首页，浏览并点击站点卡片以访问目标站点。
  - **访问导航服务首页，浏览并收藏喜欢的站点，该站点将会被划入“收藏”分类并作为收个分类展示在首页。**
    - 可以在收藏页点击取消收藏，之后该站点将会被展示在原有分类中。
  - **访问导航服务管理页，可以创建站点卡片，然后编辑、激活/冻结、删除、预览由自己创建的站点卡片。**
    - 由操作员创建的站点卡片无需由管理员审核，仅需操作员自己管理即可。
- 管理员：
  - 系统首次启动时将会自动初始化一名管理员角色的用户，可以通过命令或数据库修改管理员密码。
  - 站点卡片管理页，管理所有站点卡片，支持编辑、激活/冻结、删除、预览。
  - 站点卡片审核页，审核由访客提交的站点卡片申请，通过或拒绝。
  - 用户管理页，管理所有用户，支持重置密码、删除或提升为管理员。
  - 操作员注册审核页，审核操作员用户注册申请，通过或拒绝。
- 趋势统计：
  - 所有用户均可浏览导航站点的趋势统计数据。
  - 分类总数、站点总数、累计历史访问量、本月访问量、本周访问量、本日访问量、用户量(包括访客)。
  - 月度站点访问曲线
  - 周度站点访问曲线
  - 日度站点访问曲线
  - TOP10 访问站点
  - TOP10 收藏站点
  - TOP10 访问用户