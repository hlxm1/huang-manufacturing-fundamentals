# 机械制造技术基础 · 可溯源学习与工艺分析技能

基于黄健求主编《机械制造技术基础》第2版，按技术类、深入学习与实际工艺分析用途整理。覆盖9章，提供按需读取的知识技能、方法库、自编练习、来源页码与核验记录。

这是一套可重复调用的资料与分析流程；不表示模型已永久训练或记住整本教材。

## 成果导航

- [技能入口](skills/huang-manufacturing-fundamentals/SKILL.md)
- [九章学习路径](skills/huang-manufacturing-fundamentals/references/learning-path.md)
- [速查表](skills/huang-manufacturing-fundamentals/cheatsheet.md)、[方法库](skills/huang-manufacturing-fundamentals/patterns.md)、[术语表](skills/huang-manufacturing-fundamentals/glossary.md)
- [工艺分析模板](skills/huang-manufacturing-fundamentals/references/process-plan-template.md)
- [公式与图表核验](skills/huang-manufacturing-fundamentals/references/formula-audit.md)
- [来源索引](skills/huang-manufacturing-fundamentals/references/source-index.json)、[提取元数据](skills/huang-manufacturing-fundamentals/references/extraction-metadata.json)、[质量报告](skills/huang-manufacturing-fundamentals/references/quality-report.md)

## 安装与调用

将`skills/huang-manufacturing-fundamentals`整个目录复制到你的Codex个人技能目录，保留`SKILL.md`及全部子目录。默认位置为用户目录下的`.codex/skills/`；若设置了`CODEX_HOME`，使用该目录下的`skills/`。已在本次工作所在机器的个人技能目录安装。

在新会话中调用：

```text
$huang-manufacturing-fundamentals
按第7章方法审核这份工艺路线，解释定位基准、余量和关键检验点，并给原书页码。
```

其他示例：

- “从零讲第2章切削力与刀具寿命，给自编例子和练习。”
- “检查我的六点定位方案，列自由度和夹紧受力路径。”
- “用极值法计算这条装配游隙链，再比较调整方案。”

若当前会话尚未识别新技能，可在新会话点名调用，或直接读取本仓库技能入口。其他支持`SKILL.md`的代理可按自己的技能目录布局安装。

## 原书定位工具

索引查询仅需Python标准库，从仓库根目录运行：

```powershell
python skills/huang-manufacturing-fundamentals/scripts/source_lookup.py --chapter 7
python skills/huang-manufacturing-fundamentals/scripts/source_lookup.py --topic 定位
python skills/huang-manufacturing-fundamentals/scripts/source_lookup.py --page 228
```

返回的PDF页码以1开始计数。正文`PDF页=印刷页+10`仅适用于索引指定的324页扫描件，封面/目录等前置页不按此式转换。

可选：搜索用户本地OCR缓存，每页文件名`page-NNN.json`，至少包含`pdf_page`和`text`字段；不需要上传缓存。

```powershell
python skills/huang-manufacturing-fundamentals/scripts/source_lookup.py --search 尺寸链 --ocr ./local-ocr
```

可选：用用户自备原PDF渲染某页，需要PyMuPDF。输出会写入明确指定的位置：

```powershell
python -m pip install pymupdf
python skills/huang-manufacturing-fundamentals/scripts/source_lookup.py --page 228 --pdf ./source.pdf --render ./page-228.png
```

渲染前会检查原PDF页数及SHA-256，防止将本索引误用于另一文件。原PDF和缓存不在本仓库提供。

## 来源与范围

黄健求主编，楼应侯、朱从容副主编，机械工业出版社，第2版，2011年8月第1次印刷；ISBN978-7-111-34225-0。源PDF共324页，章节正文印刷p.1–310，参考文献p.311。

采用本地逐页OCR、分章检索与提炼，并抽查关键公式扫描页。OCR覆盖324页不等于所有文字/公式准确；核验范围和未核验项详见质量报告。现代制造数据与标准引用保留出版时代边界，具体生产参数应结合现行资料及实测能力。

本仓库发布独立整理的结构化知识、简短必要符号、分析方法和自编练习，不含原书PDF、整本OCR、页面图片或依赖包。原书著作权归其权利人；本仓库不授予原书的复制或传播权。未为教材及其衍生内容擅自附加开源许可。

转换工具：[book-to-skill](https://github.com/virgiliojr94/book-to-skill)；生成技能同时按skill-creator规范组织。
