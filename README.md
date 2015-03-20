# ASExtractor
自动文档摘要

＃　日志

0.0317　计划：尝试中文摘要提取，限制字数，基本框架实现

	结果：Success,下一步尝试摘要评估

1.0318 由于中文文摘数据库不成熟，尝试将cnki的论文pdf,caj处理为数据集(pdf2txt)，进行摘要结果评估

	结果：Failure，由于论文期刊格式不一样，无法准确提取出原文已有摘要，pdf2txt原文信息部分丢失。

2.0319　Bug: SentenceExtraction.train()若用不同的source,结果会有较大差异，最好用'all_filters'

3.0320　计划：了解／尝试英文摘要，文章句子比例提取
