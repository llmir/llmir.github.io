"""Academic CV page shared by the English and Chinese builds."""

from itertools import groupby


def render(zh, profile, papers, patents, thesis, header, footer, a, e, author_line, author_credit, venue_metric):
    L = lambda en, cn: cn if zh else en
    idx = L('publications.html', 'publications-zh.html')
    by_id = {paper['id']: paper for paper in papers}

    def work(key, label):
        return a(f'{idx}#{key}', label, 'cv-index-link') + a(by_id[key]['url'], label, 'cv-print-link')

    def topic(title, body, references=()):
        links = f'<p class="cv-topic-links">{" · ".join(references)}</p>' if references else ''
        return f'<section class="cv-topic"><h4>{e(title)}</h4><p>{e(body)}</p>{links}</section>'

    def role(org, title, dates, body):
        return f'''<article class="cv-entry">
<div class="cv-entry-head"><h3>{org}</h3><span>{e(dates)}</span></div>
<p class="cv-role">{e(title)}</p>{body}</article>'''

    name = L('Li Lin', '林立')
    institution = L('CATL Hong Kong Research Institute (HKRI)', '宁德时代香港研究院（HKRI）')
    position = L('Senior AI Engineer', '高级 AI 工程师')
    university = L('The University of Hong Kong', '香港大学')
    degree = L('PhD in Electrical and Electronic Engineering', '电子与电气工程博士')
    current = role(e(institution), position, L('Nov 2025 – Present', '2025.11 至今'), ''.join((
        topic(
            L('Recursive Self-Improvement (RSI) and Automated Agent Harness Optimization', '递归自我改进（RSI）与 Agent Harness 自动优化'),
            L('I study how execution traces can inform automated harness revisions. I use controlled evaluations across successive revisions to measure cross-task transfer, regression, and whether improvements are sustained across iterations.',
              '研究如何利用执行轨迹自动修订智能体的执行框架，并通过多轮对照评测衡量改进能否持续积累、迁移到新任务，以及能否保留已有能力。')),
        topic(
            L('Multi-Agent AutoResearch Frameworks', '多智能体自主科研框架（Multi-Agent AutoResearch）'),
            L('I develop multi-agent frameworks that coordinate hypothesis development, experimental design, and independent verification for materials research. Applications include machine-learned force fields, materials property prediction, and screening.',
              '开发协同提出假设、设计实验和独立核验结果的多智能体科研框架，应用于机器学习力场、材料性质预测与筛选等方向。')),
        topic(
            L('Multimodal, generalizable AI for battery characterization', '面向电池表征的可泛化多模态 AI'),
            L('I develop advanced signal processing and multimodal AI methods for ultrasonic measurements, scanning electron microscopy (SEM), and other characterization modalities. I study how representations of battery state and microstructure generalize across cells, instruments, and measurement conditions.',
              '针对超声信号、扫描电子显微镜（SEM）图像等互补测量，开发先进信号处理与多模态 AI 方法，研究电池状态与材料微结构表征在不同电芯、仪器及采集条件下的泛化。')),
    )))
    doctoral = role(
        e(university),
        L('Doctoral Researcher, OMEGA Lab · Joint PhD training with SUSTech MedICAL Lab',
          '博士研究人员 · OMEGA Lab · 与南方科技大学 MedICAL Lab 联合培养'),
        L('Sep 2021 – Sep 2025', '2021.09–2025.09'),
        ''.join((
            topic(
                L('Data- and annotation-efficient learning', '数据与标注高效学习'),
                L('I studied how to recover dense segmentation from sparse, noisy supervision. YoloCurvSeg separates the synthesis of curvilinear anatomy from the reconstruction of real image backgrounds and uses contrastive learning to combine them. Its single-skeleton setting used 0.03–1.40% of the fully annotated pixels across four benchmarks. ProCNS uses prototype calibration and region-level noise suppression to limit the accumulation of pseudo-label errors during training.',
                  '研究如何从稀疏、含噪的监督中学习像素级分割。YoloCurvSeg 将曲线状解剖结构的合成与真实影像背景的重建分开，再利用对比学习将二者结合。在四个基准数据集上，单骨架方案使用的标注像素仅占完整标注的 0.03%–1.40%。ProCNS 通过原型校准与区域级噪声抑制，减少训练中伪标签误差的累积。'),
                (work('yolocurvseg', 'YoloCurvSeg'), work('procns', 'ProCNS'), work('lfsynthseg', 'LF-SynthSeg'))),
            topic(
                L('Cross-domain generalization and adaptation', '跨域泛化与自适应'),
                L('My work separates shifts in the input distribution from changes in what a site annotates. AADG searches for augmentation policies that improve generalization to unseen imaging domains. UniOCTSeg++ uses hierarchical prompts and bidirectional consistency to share supervision across annotation granularities. On its external OCT test sets, training with 30% labeled data plus unlabeled scans yielded a Dice score of 86.26%, versus 86.83% with full supervision. I have also worked on parameter-efficient adaptation for high-resolution imaging.',
                  '以设备与成像协议引起的输入分布偏移，以及不同中心的标注粒度差异为切入点。AADG 自动搜索数据增强策略，以提高模型在未见成像域中的泛化能力。UniOCTSeg++ 通过层级提示和双向一致性整合不同标注粒度的监督。在外部 OCT 测试中，采用 30% 标注数据和其余未标注影像时，Dice 为 86.26%，全监督结果为 86.83%。研究还涵盖高分辨率医学影像的参数高效适配。'),
                (work('scholar-2', 'AADG'), work('unioctsegplus', 'UniOCTSeg++'), work('scholar-41', 'Fusion Side Tuning'))),
            topic(
                L('Personalized federated learning across data silos', '数据孤岛下的个性化联邦学习'),
                L('I developed federated methods for institutions whose scans and weak labels follow different distributions. FedICRA learns site-aware representations and adapts the aggregation of segmentation heads. FedLPPA adds prompts for each site’s data distribution and annotation sparsity, together with a dual decoder and parameter-wise aggregation. Its evaluation covered four segmentation tasks across fundus imaging, OCTA, endoscopy and MRI.',
                  '面向跨机构的影像分布与弱标注差异，研究原始数据留在各机构时的协同训练。FedICRA 学习与中心相关的表征，并自适应聚合分割头。FedLPPA 用不同类型的提示建模各中心的数据分布与标注稀疏性，同时采用双解码器与逐参数聚合，在眼底照片、OCTA、内窥镜和 MRI 的四类分割任务上进行了评估。'),
                (work('fedlppa', 'FedLPPA'), work('fedicra', 'FedICRA'), a(thesis, L('Doctoral thesis', '博士论文')))),
            topic(
                L('Multimodal foundation models for medical image analysis', '面向医学影像分析的多模态基础模型'),
                L('I work on reusable medical image representations from unlabeled scans, paired reports and complementary imaging sequences. Uni4Eye++ uses entropy-guided masking and modality-specific reconstruction heads to pretrain jointly on 2D and 3D scans. PRIOR aligns images and reports at global and local levels and evaluates transfer on five downstream tasks. In brain MRI, MF-MCM learns cross-sequence complementarity to support lesion segmentation when annotations or modalities are missing.',
                  '从未标注影像、配对报告与互补成像序列中学习可迁移表征。Uni4Eye++ 用图像熵引导掩码，通过模态特定的重建头在二维和三维影像上开展联合预训练。PRIOR 在全局与局部层面对齐影像和报告，并在五项下游任务上评估迁移表现。MF-MCM 利用脑部 MRI 序列之间的互补信息，支持标注有限或序列缺失时的病灶分割。'),
                (work('uni4eyeplus', 'Uni4Eye++'), work('prior', 'PRIOR'), work('mfmcm', 'MF-MCM'))),
            topic(
                L('Image analysis in clinical workflows', '影像分析与临床工作流程'),
                L('SynLiTS combines phase-conditioned synthesis with context-aware fusion for imperfectly aligned liver CT. MEFN estimates uncertainty before combining PET and CT evidence. FOCUS adapts a vision foundation model to analyze OCT slices and aggregates their predictions for patient-level diagnosis. The study evaluated the diagnostic workflow at four external centers.',
                  'SynLiTS 结合期相条件合成和上下文感知融合，从配准不完全的多期肝脏 CT 中学习。MEFN 先估计各模态的不确定性，再融合 PET 与 CT 提供的证据。FOCUS 适配视觉基础模型分析 OCT 切片，将切片预测汇总为患者级诊断，并在四家外部中心评估该流程。'),
                (work('synlits', 'SynLiTS'), work('mefn', 'MEFN'), work('focus', 'FOCUS'))),
        )),
    )
    early = role(
        e(L('Southern University of Science and Technology', '南方科技大学')),
        L('Visiting Student and Research Assistant, MedICAL Lab', '访问学生与研究助理 · MedICAL Lab'),
        L('Jul 2019 – Aug 2021', '2019.07–2021.08'),
        f'''<p class="cv-entry-text">{L(
            'I worked on medical image segmentation, lesion detection with coarse annotations and dataset development. I was the first author of the SUSTech–SYSU dataset paper in Scientific Data.',
            '从事医学图像分割、粗标注病灶检测与数据集建设，并以第一作者在 Scientific Data 发表 SUSTech–SYSU 数据集。')}</p>
<p class="cv-topic-links">{work('sustech-sysu','SUSTech–SYSU')+' · '+work('bsdanet','BSDA-Net')}</p>''',
    )

    advisors = a('https://hub.hku.hk/cris/rp/rp00189', L('Kenneth K. Y. Wong', '黄建业')) + L(' and ', '、') + a(
        'https://hub.hku.hk/cris/rp/rp00131', L('Edmund Y. M. Lam', '林彦民'))
    schools = ''.join((
        role(e(university), degree, L('Sep 2021 – Sep 2025', '2021.09–2025.09'),
             f'<p class="cv-entry-text">{L("Advisors","博士导师")} {advisors}</p><p>{a(thesis, L("Towards federated and annotation-efficient deep learning for medical image analysis", "面向医学影像分析的联邦学习与标注高效深度学习"))}</p>'),
        role(e(L('Sun Yat-sen University', '中山大学')),
             L('MS in Information and Communication Engineering', '信息与通信工程硕士'),
             L('Sep 2018 – Jun 2021', '2018.09–2021.06'),
             f'<p class="cv-entry-text">{L("Outstanding Thesis nomination (top 5%)","优秀毕业论文提名（前 5%）")}</p>'),
        role(e(L('South China Normal University', '华南师范大学')),
             L('BEng in Communication Engineering', '通信工程学士'),
             L('Sep 2014 – Jun 2018', '2014.09–2018.06'),
             f'<p class="cv-entry-text">{L("Outstanding Thesis","优秀毕业论文")}</p>'),
    ))

    patent_list = []
    for kind, group in groupby(patents, key=lambda x: x['kind']):
        title = L('Granted Inventions', '授权发明专利') if kind == 'grant' else L('Published Applications', '已公开发明专利申请')
        terms = {'SUSTech': L('SUSTech', '南方科技大学'), 'SYSU': L('Sun Yat-sen University', '中山大学')}
        rows = ''.join(
            f'<li><span class="cv-list-meta"><time>{row["year"]}</time> {a(row.get("sourceZh",row["source"]) if zh else row["source"],row["number"])}</span>'
            f'<div>{e(row["titleZh" if zh else "title"])}<small>{terms[row["assignee"]]}</small></div></li>' for row in group
        )
        patent_list.append(f'<h3 class="cv-subheading">{title}</h3><ul class="cv-list cv-patents">{rows}</ul>')

    awards = (
        ('2024', L('Shenzhen AI Science and Technology Progress Award', '深圳人工智能科技进步奖'),
         L('Team contributor, AI cloud platform for ophthalmic diagnosis', '“爱眼云”人工智能诊断云平台团队成员'),
         'https://saai.net.cn/wp-content/uploads/2025/03/2024%E5%B9%B4%E5%BA%A6%E7%AC%AC%E5%9B%9B%E5%B1%8A%E2%80%9C%E6%B7%B1%E5%9C%B3%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%E5%A5%96%E2%80%9D%E8%8E%B7%E5%A5%96%E5%90%8D%E5%8D%95.pdf'),
        ('2023', L('Representative Algorithm in Medical AI, China', '中国医学人工智能代表性算法'),
         L('YoloCurvSeg, joint recipient with Xiaoying Tang', 'YoloCurvSeg，与唐晓颖共同入选'),
         'https://zj.people.com.cn/n2/2023/1223/c186327-40689790.html'),
        ('2021', L('MICCAI Student Travel Award', 'MICCAI 学生差旅奖'), '', ''),
        ('2021–2025', L('HKU Postgraduate Scholarship', '香港大学研究生奖学金'), '', ''),
    )
    award_html = ''.join(
        f'<li><time>{date}</time><div>{a(url,label) if url else e(label)}{f"<small>{e(note)}</small>" if note else ""}</div></li>'
        for date, label, note, url in awards
    )
    resources = (
        (L('Dataset', '数据集'), 'SUSTech–SYSU', by_id['sustech-sysu'].get('data') or by_id['sustech-sysu']['url'],
         L('Fundus images and expert annotations for lesion detection and grading', '用于病灶检测和分级的眼底影像与专家标注')),
        (L('Code', '代码'), 'FedLPPA', by_id['fedlppa']['code'],
         L('Personalized federated segmentation under heterogeneous weak supervision', '异构弱监督下的个性化联邦分割')),
        (L('Code', '代码'), 'YoloCurvSeg', by_id['yolocurvseg']['code'],
         L('Data synthesis and segmentation from sparse skeleton labels', '稀疏骨架标注下的数据合成与分割')),
        (L('Code', '代码'), 'PRIOR', by_id['prior']['code'],
         L('Joint visual and language pretraining with medical images and reports', '医学影像与报告的视觉语言联合预训练')),
    )
    resources_html = ''.join(
        f'<li><span>{e(kind)}</span><div>{a(url,label)}<small>{e(note)}</small></div></li>'
        for kind, label, url, note in resources
    )

    preprint = L('Preprint', '预印本')

    def edition(row):
        return f' <span class="status">{preprint}</span>' if row['status'] == 'preprint' else ''

    def citations(rows):
        return ''.join(
            f'<li><div>{work(row["id"],row["title"])}'
            f'<small>{author_line(row,zh)}{author_credit(row,zh)} · {e(row["venue"])}{venue_metric(row["venue"])}'
            f'{edition(row)}</small></div></li>'
            for row in rows
        )

    bibliography = []
    for published_year, group in groupby(papers, key=lambda row: row['year']):
        rows = list(group)
        bibliography.append(
            f'<details class="cv-bib"><summary><time>{published_year}</time><span>{len(rows)} {L("publications","篇")}</span></summary><ol>{citations(rows)}</ol></details>'
        )
    nav = (
        ('experience', L('Research Experience', '研究经历')), ('education', L('Education', '教育背景')),
        ('bibliography', L('Publications', '学术论文')), ('patents', L('Patents', '专利')),
        ('resources', L('Open Research', '开放成果')), ('honors', L('Recognition', '学术荣誉')),
    )
    sections = {key: title for key, title in nav}
    local_nav = ''.join(a('#'+key, title) for key, title in nav)
    full_index = a(idx, L('Search all publications →', '搜索全部论文 →'))
    return header(zh, 'cv') + f'''<main id="main" class="academic-cv">
<section class="cv-masthead" aria-labelledby="cv-name"><div class="container">
<div class="cv-identity">
<div><p class="cv-kicker">{L('Academic CV', '学术简历')}</p>
<h1 id="cv-name">{name} <span lang="{L('zh-CN','en')}">{L('林立','Li Lin')}</span></h1>
<p class="cv-affiliation">{e(position)} · {e(institution)}</p></div>
<div class="cv-links">
{a(profile["scholar"],"Google Scholar")}{a(profile["github"],"GitHub")}{a(profile["orcid"],"ORCID")}
{a("mailto:"+profile["primaryEmail"],L("Email","邮箱"),"cv-index-link")}
{a("mailto:"+profile["primaryEmail"],profile["primaryEmail"],"cv-print-link")}
<button class="cv-print" type="button" data-print-cv hidden>{L("Print / Save PDF","打印 / 保存 PDF")}</button>
</div>
</div></div></section>
<div class="container cv-layout">
<aside class="cv-sidebar"><nav class="cv-nav" aria-label="{L('CV sections','简历目录')}">{local_nav}</nav></aside>
<div class="cv-content">
<section class="cv-section" aria-labelledby="experience"><h2 id="experience">{sections['experience']}</h2>{current}{doctoral}{early}</section>
<section class="cv-section" aria-labelledby="education"><h2 id="education">{sections['education']}</h2>{schools}</section>
<section class="cv-section" aria-labelledby="bibliography"><div class="section-title"><h2 id="bibliography">{sections['bibliography']}</h2>{full_index}</div>
{''.join(bibliography)}</section>
<section class="cv-section" aria-labelledby="patents"><h2 id="patents">{sections['patents']}</h2>{''.join(patent_list)}</section>
<section class="cv-section" aria-labelledby="resources"><h2 id="resources">{sections['resources']}</h2><ul class="cv-list">{resources_html}</ul></section>
<section class="cv-section" aria-labelledby="honors"><h2 id="honors">{sections['honors']}</h2><ul class="cv-list">{award_html}</ul></section>
</div></div></main>{footer(zh, track_visit=True)}'''
