# Django Ninja 文档多语种翻译与 Vercel 部署方案

## Context

django-ninja.cn 站点当前仅支持中文,流量下降。需参考同目录 mypydantic 项目,使用 `mkdocs-static-i18n` 插件实现多语种支持,并完成 Vercel 部署配置。

**目标**:
1. 支持 mypydantic 的全部 10 种语言:zh(默认)、en、ru、hi、id、de、nl、ko、ja、fr
2. 全量翻译全部 97 个英文页面
3. 其余语言提供 nav_translations(本地化导航),内容通过 `fallback_to_default: true` 回退到中文
4. 完善 Vercel 构建配置

**参考实现**: `/Users/yiqun/WebStromProjects/mypydantic/mkdocs.yml` L199-L289 (i18n 配置)

---

## Phase 1: 基础设施搭建

### 1.1 添加 i18n 插件依赖
- **文件**: [docs/requirements.txt](file:///Users/yiqun/WebStromProjects/django-ninja/docs/requirements.txt)
- 追加 `mkdocs-static-i18n==1.3.0`

### 1.2 重组文档为 folder-based 多语种结构
- 将 `docs/docs/` 下全部 97 个 md 文件及 12 个子目录移动到 `docs/docs/zh/`
- 使用 `git mv` 保留 git 历史
- 结构变化: `docs/docs/index.md` → `docs/docs/zh/index.md`,`docs/docs/tutorial/*` → `docs/docs/zh/tutorial/*`,以此类推
- 静态资源 `img/`、`extra.css`、`ads.txt` 等保持在 `docs/docs/` 根目录(非语言相关)
- `docs/src/`(代码示例)不动

---

## Phase 2: mkdocs.yml i18n 配置

### 2.1 添加 i18n 插件
- **文件**: [docs/mkdocs.yml](file:///Users/yiqun/WebStromProjects/django-ninja/docs/mkdocs.yml)
- 在 `plugins` 段添加 i18n 插件,参考 mypydantic 配置:

```yaml
plugins:
  - search
  - i18n:
      docs_structure: folder
      fallback_to_default: true
      reconfigure_material: true
      languages:
        - locale: zh
          default: true
          name: 简体中文
          build: true
        - locale: en
          name: English
          build: true
          site_name: "Django Ninja documentation (en)"
          site_description: "Django Ninja - Fast Django REST framework"
          nav_translations:  # 中文 → 英文,详见 2.2
            ...
        - locale: ru
          name: Russian
          build: true
          site_name: "Документация Django Ninja"
          nav_translations: ...
        # hi, id, de, nl, ko, ja, fr 同理
  - mkdocstrings:
      handlers:
        python:
          setup_commands:
            - from django.conf import settings
            - settings.configure()
```

### 2.2 nav_translations 编写
- 现有 nav 使用中文标签(如 "介绍"、"教程"、"解析输入"),需为每个非默认语言提供 `nav_translations`,将中文标签映射为目标语言
- 英文 nav_translations 示例: `介绍: Introduction`、`教程: Tutorial`、`解析输入: Parsing Input` 等
- 共约 60 个导航项 × 9 种语言,使用并行 agent 批量生成

---

## Phase 3: 全量英文翻译(97 个页面)

### 3.1 创建 en 文件夹结构
- 创建 `docs/docs/en/`,镜像 `docs/docs/zh/` 的目录结构

### 3.2 批量翻译执行策略
将 97 个文件按目录分批,使用并行 general-purpose agent 翻译(每批 8-12 个文件):

| 批次 | 目录 | 预估文件数 |
|------|------|-----------|
| 1 | 顶层文件 (index, motivation, contact, help, releases, whatsnew_v1) | 6 |
| 2 | tutorial/ | ~10 |
| 3 | guides/ (input/, response/) | ~18 |
| 4 | guides/ 其余 + reference/ | ~10 |
| 5 | django-ninja-jwt/ | 9 |
| 6 | django-ninja-extra/ | ~20 |
| 7 | django-ninja-crud/ + proposals/ | ~6 |
| 8 | coding-qa/ + online-tools/ + site-build/ + blog/ | ~18 |

**翻译规则**:
- 仅翻译中文正文为英文,代码块/命令/API 不翻译
- 保留所有 Markdown 格式、链接路径、Front matter
- 保留 `::: python.module` 等 mkdocstrings 指令原样
- 翻译质量:技术术语准确,符合英文技术文档习惯

---

## Phase 4: 其余语言 nav_translations

为 ru、hi、id、de、nl、ko、ja、fr 8 种语言编写 nav_translations(仅导航标签,约 60 项/语言)。内容页面通过 `fallback_to_default: true` 回退到中文。使用并行 agent 一次性生成。

---

## Phase 5: Vercel 部署配置

### 5.1 更新 vercel.json
- **文件**: [vercel.json](file:///Users/yiqun/WebStromProjects/django-ninja/vercel.json)
- 当前仅有 `installCommand`,需补全 build 配置:

```json
{
  "installCommand": "pip3 install --break-system-packages -r docs/requirements.txt",
  "buildCommand": "bash scripts/build-docs.sh",
  "outputDirectory": "docs/site"
}
```

### 5.2 验证 build-docs.sh 兼容性
- **文件**: [scripts/build-docs.sh](file:///Users/yiqun/WebStromProjects/django-ninja/scripts/build-docs.sh)
- 脚本流程: pip install → `cd docs && PYTHONPATH=../ python3 -m mkdocs build` → `python3 scripts/modify_sitemap.py`
- i18n 插件会自动为每种语言生成子站点(/en/、/ru/ 等),sitemap 应自动包含多语言 URL
- `modify_sitemap.py` 仅追加自定义 URL,不影响 i18n,无需改动

### 5.3 主题语言设置
- mkdocs.yml 中 `theme.language: zh` 保持为默认语言
- i18n 插件的 `reconfigure_material: true` 会自动配置语言切换器

---

## 验证方案

1. **本地构建测试**: 运行 `bash scripts/build-docs.sh`,确认无报错
2. **多语言路径检查**: 确认 `docs/site/zh/`、`docs/site/en/` 等路径已生成
3. **语言切换器**: 打开 `docs/site/index.html`,确认右上角有语言选择器
4. **fallback 验证**: 访问 `/en/` 下某未翻译页面,确认回退到中文内容但导航为英文
5. **sitemap 检查**: 查看 `docs/site/sitemap.xml`,确认包含多语言 URL
6. **Vercel 部署**: push 后在 Vercel 控制台确认构建成功,访问线上站点验证

---

## 关键文件清单

| 文件 | 操作 |
|------|------|
| [docs/requirements.txt](file:///Users/yiqun/WebStromProjects/django-ninja/docs/requirements.txt) | 添加 mkdocs-static-i18n |
| [docs/mkdocs.yml](file:///Users/yiqun/WebStromProjects/django-ninja/docs/mkdocs.yml) | 添加 i18n 插件配置 |
| [vercel.json](file:///Users/yiqun/WebStromProjects/django-ninja/vercel.json) | 补全 buildCommand 和 outputDirectory |
| docs/docs/zh/ (新建) | git mv 现有全部内容 |
| docs/docs/en/ (新建) | 全量翻译 97 个文件 |
| [scripts/build-docs.sh](file:///Users/yiqun/WebStromProjects/django-ninja/scripts/build-docs.sh) | 无需改动(已兼容) |
| [scripts/modify_sitemap.py](file:///Users/yiqun/WebStromProjects/django-ninja/scripts/modify_sitemap.py) | 无需改动 |
