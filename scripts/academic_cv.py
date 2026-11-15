"""Academic CV page shared by the English and Chinese builds."""

from itertools import groupby


def render(zh, profile, papers, patents, thesis, header, footer, a, e, author_line, author_credit, venue_metric, idx):
    L = lambda en, cn: cn if zh else en
    by_id = {paper['id']: paper for paper in papers}

    def work(key, label):
        return a(f'{idx}#{key}', label, 'cv-index-link') + a(by_id[key]['url'], label, 'cv-print-link')

    short_venues = {
        'IEEE Transactions on Medical Imaging': 'IEEE TMI',
        'IEEE Journal of Biomedical and Health Informatics': 'IEEE JBHI',
        'IEEE Transactions on Pattern Analysis and Machine Intelligence': 'IEEE TPAMI',
        'Medical Image Analysis': 'MedIA',
        'Computers in Biology and Medicine': 'CIBM',
        'Knowledge-Based Systems': 'KBS',
        'BenchCouncil FICC 2020': L('FICC 2020, proc.', 'FICC 2020，论文集'),
        'MLMI 2025 at MICCAI': L('MLMI at MICCAI 2025, proc.', 'MICCAI 2025 MLMI，论文集'),
    }

    def example(key, label):
        paper = by_id[key]
        venue = short_venues.get(paper['venue'], paper.get(L('venue', 'venueZh'), paper['venue']))
        details = [f'{venue} {paper["year"]}']
        if paper['status'] == 'preprint':
            details.append(L('preprint', '预印本'))
        if award := paper.get(L('award', 'awardZh')):
            details.append(award)
        detail = L(', ', '，').join(details)
        return work(key, L(f'{label} ({detail})', f'{label}（{detail}）'))

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
            f'<p class="cv-entry-text">{L("My research in medical imaging and computer vision spans my doctorate and subsequent collaborations.", "我的医学影像与计算机视觉研究从博士阶段延续至后续合作。")}</p>',
            topic(
                L('Data- and annotation-efficient learning', '数据与标注高效学习'),
                L('I develop methods that learn from scarce, incomplete, or noisy supervision and imbalanced data. This work combines anatomy-guided synthesis, prototype-based pseudo-label calibration, and semi-supervised adaptation to make better use of unlabeled scans and underrepresented cases.',
                  '面向标注有限、不完整、含噪及数据分布不均衡等问题，研究解剖先验引导的数据合成、基于原型的伪标签校准与半监督适配，提升模型利用未标注影像和低频病例的能力。'),
                (example('scholar-59', 'TailBoost'), example('scholar-61', L('Annotation-Free TOF-MRA Segmentation', '无标注 TOF-MRA 分割')),
                 example('procns', 'ProCNS'), example('lfsynthseg', 'LF-SynthSeg'), example('scholar-17', 'ASLSeg'), example('yolocurvseg', 'YoloCurvSeg'))),
            topic(
                L('Cross-domain generalization and adaptation', '跨域泛化与自适应'),
                L('I study how imaging models transfer across acquisition domains and annotation protocols. My work includes learned augmentation for unseen domains, complementary teachers for adaptation to multiple unlabeled targets, and anatomy-aware prompting for supervision at different levels of detail.',
                  '研究医学影像模型如何应对采集域和标注规范的变化，包括面向未见域的增强策略学习、面向多个未标注目标域的互补教师适配，以及跨标注粒度的解剖感知提示学习。'),
                (example('unioctsegplus', 'UniOCTSeg++'), example('unioctseg', 'UniOCTSeg'), example('lumos', 'LUMOS'),
                 example('scholar-33', 'RVms'), example('scholar-2', 'AADG'))),
            topic(
                L('Personalized federated learning across data silos', '数据孤岛下的个性化联邦学习'),
                L('I developed personalized federated learning methods for institutions with heterogeneous imaging distributions and weak annotations. Site-aware representation learning, shared and local prompts, and adaptive aggregation or distillation let institutions share knowledge while retaining models suited to their own data.',
                  '面向影像分布与弱标注形式各异的医疗机构，研究个性化联邦学习。通过中心感知表征、共享与本地提示、自适应聚合及蒸馏，在跨机构共享知识的同时保留模型对本地数据的适配能力。'),
                (example('fedlppa', 'FedLPPA'), example('scholar-68', 'pFedWSD'), example('fedicra', 'FedICRA'),
                 a(thesis, L('Doctoral thesis (HKU 2025)', '博士论文（香港大学 2025）')))),
            topic(
                L('Multimodal representation learning and foundation models', '多模态表征学习与基础模型'),
                L('I study transferable representations through masked modeling of 2D and 3D scans, complementary MRI pretraining, and image–report alignment. Related work addresses noisy image–text correspondence and grounds medical vision–language reasoning in clinical knowledge graphs.',
                  '研究二维与三维影像掩码建模、互补 MRI 序列预训练与影像–报告对齐，以学习可跨任务迁移的表征。相关工作进一步处理影像与文本的含噪配对，并利用临床知识图谱支持医学视觉语言推理。'),
                (example('eyegraph', 'EyeGraph'), example('mfmcm', 'MF-MCM'), example('scholar-52', 'MMCM'),
                 example('mirage', 'MIRAGE'), example('uni4eyeplus', 'Uni4Eye++'), example('uni4eye', 'Uni4Eye'), example('prior', 'PRIOR'))),
            topic(
                L('Image synthesis and reconstruction', '影像合成与重建'),
                L('I work on recovering or synthesizing complementary information when acquisitions differ in contrast, resolution, or spatial alignment. Applications include cross-contrast MRI reconstruction, diffusion synthesis for unaligned multiphase CT, and anatomy-guided CT synthesis for PET attenuation correction.',
                  '针对成像对比度、分辨率和空间对齐状态的差异，研究如何恢复或合成互补影像信息，涵盖跨对比度 MRI 重建、配准不完全的多期 CT 扩散合成，以及用于 PET 衰减校正的解剖先验引导 CT 合成。'),
                (example('synlits', 'SynLiTS'), example('scholar-62', 'DAPS'), example('diff4mmlits', 'Diff4MMLiTS'),
                 example('scholar-53', 'SMNet'), example('scholar-27', 'DS³-Net'))),
            topic(
                L('Clinical image analysis and decision support', '临床影像分析与决策支持'),
                L('I contribute to methods that turn imaging evidence into quantitative findings and patient-level assessments. This work spans anatomy-aware measurements, uncertainty-aware PET/CT fusion, 3D OCT diagnosis, and the evaluation of multidisciplinary agents for treatment planning.',
                  '研究如何从影像证据提取定量信息并支持患者级评估，涵盖解剖先验引导的定量分析、考虑不确定性的 PET/CT 融合、三维 OCT 诊断，以及面向治疗方案制定的多学科智能体评测。'),
                (example('focus', 'FOCUS'), example('scholar-57', 'DRAgent'), example('mefn', 'MEFN'),
                 example('scholar-64', L('Non-perfusion Segmentation', '无灌注区分割')), example('scholar-31', 'JOINEDTrans'))),
            topic(
                L('3D computer vision', '三维计算机视觉'),
                L('I also contribute to family-aware models for reconstructing animal pose and shape from single images. This work combines shared representations with family-level supervision to transfer across species.',
                  '参与研究面向动物姿态与形状的单图三维重建，利用动物科级监督组织共享表征，提升跨物种迁移能力。'),
                (example('animerplus', 'AniMer+'), example('animer', 'AniMer'))),
        )),
    )
    early_works = ' · '.join((
        example('bsdanet', 'BSDA-Net'), example('scholar-35', L('Corneal Nerve Segmentation', '角膜神经分割')),
        example('scholar-23', 'EPC-GAN'), example('scholar-25', 'BLU-GAN'),
        example('sustech-sysu', 'SUSTech–SYSU'), example('scholar-11', L('Hemorrhage Detection', '出血病灶检测')),
    ))
    early = role(
        e(L('Southern University of Science and Technology', '南方科技大学')),
        L('Visiting Student and Research Assistant, MedICAL Lab', '访问学生与研究助理 · MedICAL Lab'),
        L('Jul 2019 – Aug 2021', '2019.07–2021.08'),
        f'''<p class="cv-entry-text">{L(
            'I studied lesion detection from coarse annotations, anatomical segmentation, and contrastive image synthesis and enhancement. I was the first-listed author of the SUSTech–SYSU dataset paper in Scientific Data. BSDA-Net first appeared as a preprint during this appointment and was subsequently published at MICCAI 2021.',
            '研究粗标注病灶检测、解剖结构分割，以及基于对比学习的影像合成与增强。以第一作者在 Scientific Data 发表 SUSTech–SYSU 数据集研究。BSDA-Net 于任内发布预印本，后发表于 MICCAI 2021。')}</p>
<p class="cv-topic-links">{early_works}</p>''',
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
        ('2020', by_id['scholar-25'][L('award','awardZh')], 'BLU-GAN · BenchCouncil FICC 2020', ''),
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
            f'<li><div>{work(row["id"],row[L("title","titleZh")])}'
            f'<small>{author_line(row,zh)}{author_credit(row,zh)} · {e(row.get(L("venue","venueZh"),row["venue"]))}{venue_metric(row["venue"])}'
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
    return header + f'''<main id="main" class="academic-cv">
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
