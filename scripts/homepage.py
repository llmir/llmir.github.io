"""Biography, news, experience, and peer review on the bilingual homepage."""

from html import escape


def intro(zh, profile):
    L = lambda en, cn: cn if zh else en
    profiles = (
        ('cv', L('cv.html', 'cv-zh.html'), L('Academic CV', '学术简历')),
        ('scholar', profile['scholar'], 'Google Scholar'),
        ('github', profile['github'], 'GitHub'),
        ('orcid', profile['orcid'], 'ORCID'),
        ('researchgate', profile['researchgate'], 'ResearchGate'),
        ('openreview', profile['openreview'], 'OpenReview'),
    )
    links = ''.join(
        f'<a href="{escape(url)}"><svg class="profile-icon" aria-hidden="true" viewBox="0 0 24 24">'
        f'<use href="assets/profile-icons.svg#{icon}"></use></svg>{escape(label)}</a>'
        for icon, url, label in profiles
    )
    emails = ' <span aria-hidden="true">·</span> '.join(
        f'<a href="mailto:{escape(address)}">{escape(address)}</a>'
        for address in (profile['primaryEmail'], profile['secondaryEmail'])
    )
    return f'''<section id="About" class="intro-band" aria-labelledby="name">
<div class="container intro-grid">
<img class="portrait" src="{escape(profile['portrait'])}" width="1300" height="1565"
alt="{L('Li Lin', '林立的照片')}" fetchpriority="high">
<div class="intro-text">
<div class="identity"><h1 id="name">{L('Li Lin', '林立')} <span class="alternate-name"
lang="{L('zh-CN', 'en')}">{L('林立', 'Li Lin')}</span></h1></div>
<p class="intro-role">{L('Senior AI Engineer', '高级 AI 工程师')}</p>
<div class="intro-affiliations">
<p class="affiliation">{L('CATL Hong Kong Research Institute (HKRI)', '宁德时代香港研究院（HKRI）')}</p>
<p class="intro-degree">{L('PhD, The University of Hong Kong', '香港大学博士')}</p>
</div>
<p class="email-line">{emails}</p>
<nav class="social-links" aria-label="{L('Academic profiles', '学术主页')}">{links}</nav>
<p class="intro-interests">{L('AI for Healthcare · AI for Science · Computer Vision · Agentic AI · Recursive Self-Improvement (RSI)', '医疗人工智能 · 科学智能 · 计算机视觉 · 智能体 AI · 递归自我改进（RSI）')}</p>
</div></div></section>'''


def biography(zh, thesis_url, email, sidebar):
    L = lambda en, cn: cn if zh else en
    thesis = f'<a href="{escape(thesis_url)}">{L("doctoral thesis", "博士论文")}</a>'
    current = L(
        'At CATL HKRI, my research spans <strong>Agentic AI</strong> and <strong>AI for Science</strong>. I study how agents improve through experience and how AI can advance materials discovery and battery characterization.',
        '我在宁德时代香港研究院（HKRI）从事<strong>智能体 AI（Agentic AI）</strong>和<strong>科学智能（AI for Science）</strong>研究，关注智能体如何从执行经验中不断改进，以及人工智能如何推进材料发现与电池表征。',
    )
    current_methods = L((
        '<strong>Recursive self-improvement (RSI) and automated agent harness optimization.</strong> I study how agents can turn recurring failures into lasting improvements. My work combines trace-guided harness optimization with multi-round evaluations of cross-task transfer and capability retention.',
        '<strong>Multi-agent AutoResearch frameworks.</strong> I study how agents can carry out iterative scientific inquiry, coordinating hypothesis development, experiment design, and independent verification so that results can refine subsequent hypotheses (machine-learned force fields, materials property prediction and screening, etc.).',
        '<strong>Multimodal, generalizable AI for battery characterization.</strong> I combine advanced signal processing and multimodal AI to characterize battery state and microstructure from complementary measurements, including ultrasound and scanning electron microscopy (SEM), across cells and acquisition conditions.',
    ), (
        '<strong>递归自我改进（RSI）与 Agent Harness 自动优化。</strong>利用执行轨迹诊断反复出现的失败，研究如何自动优化智能体的执行框架，并用多轮评测检验改进能否跨任务迁移、能否保留已有能力。',
        '<strong>多智能体自主科研框架（Multi-Agent AutoResearch）。</strong>研究如何组织多个智能体协同提出假设、设计实验和独立核验，并根据实验结果修正后续假设，应用于机器学习力场、材料性质预测与筛选等。',
        '<strong>面向电池表征的可泛化多模态 AI。</strong>结合先进信号处理与多模态学习，利用超声信号、扫描电子显微镜（SEM）图像等互补信息表征电池状态和材料微结构，研究模型在不同电芯和采集条件下的泛化。',
    ))
    healthcare = L(
        f'My interest in <strong>AI for Healthcare</strong> grew out of undergraduate research in biomedical engineering. I began working on medical imaging during my master’s studies and made it the focus of my PhD at the University of Hong Kong ({thesis}). I continue to develop learning methods that address challenges shared across <strong>medical image analysis</strong> tasks.',
        f'我的<strong>医疗人工智能（AI for Healthcare）</strong>研究起步于本科阶段的生物医学工程工作，硕士期间转向医学影像，并在香港大学博士期间深入开展（{thesis}）。我持续研究<strong>医学影像分析</strong>中可迁移至不同任务的学习方法。',
    )
    methods = L((
        '<strong>Data- and annotation-efficient learning.</strong> I study how to learn when expert labels are scarce and supervision is incomplete or imperfect, drawing on a range of approaches (self-supervised, weakly supervised, semi-supervised, active, and noise-robust learning, etc.).',
        '<strong>Generalizable AI and foundation models.</strong> I develop multimodal representations that can transfer across imaging protocols, institutions, and tasks, and study how domain generalization and efficient adaptation can support deployment in new settings.',
        '<strong>Personalized federated learning.</strong> I develop federated optimization and model personalization methods that learn across institutional data silos while accounting for differences in data distributions and supervision across sites.',
    ), (
        '<strong>数据与标注高效学习。</strong>面向样本有限、监督不完整且不完美的情形，研究自监督、弱监督、半监督、主动学习和噪声鲁棒学习等方法，降低模型对大规模专家标注的依赖。',
        '<strong>可泛化 AI 与基础模型。</strong>研究可跨成像协议、临床机构与任务迁移的多模态表征，利用域泛化与高效适配提升模型在新环境中的适用性。',
        '<strong>个性化联邦学习。</strong>面向机构间的数据孤岛，研究联邦优化与模型个性化，使各中心在保留原始数据的前提下协同学习，并适应各自的影像分布与标注条件。',
    ))
    def directions(items):
        return '<ul class="bio-methods">' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>'
    collab = L(
        f'If you’re interested in collaborating on Agentic AI, AI for Science, AI for Healthcare, computer vision, multimodal AI, or related topics, please <a href="mailto:{escape(email)}">feel free to email me</a>.',
        f'如果您有兴趣在智能体 AI、科学智能、医疗人工智能、计算机视觉或多模态 AI 等方向开展合作，欢迎<a href="mailto:{escape(email)}">给我发邮件</a>。',
    )
    return f'''<section class="container section bio-section" aria-labelledby="Biography">
<h2 id="Biography">{L('Biography', '个人简介')}</h2>
<div class="biography-layout">{sidebar}
<div class="bio"><p>{current}</p>{directions(current_methods)}
<p>{healthcare}</p>{directions(methods)}<p class="bio-collaboration">{collab}</p></div></div></section>'''


def news(zh, affiliation_url, thesis_url):
    L = lambda en, cn: cn if zh else en
    notices = (
        ('2026-10', '#eyegraph', 'EyeGraph',
         ' connects medical vision–language modeling with knowledge-graph reasoning. Published online in IEEE TMI.',
         ' 将知识图谱推理引入医学视觉语言模型，已在 IEEE TMI 在线发表。'),
        ('2026-09', '#unioctsegplus', 'UniOCTSeg++',
         ' uses hierarchical prompts to share supervision across annotation granularities. Published in IEEE TMI.',
         ' 通过层级提示整合不同标注粒度的监督信息，发表于 IEEE TMI。'),
        ('2026-09', '#mfmcm', 'MF-MCM',
         ' learns complementary representations across brain MRI sequences for segmentation with incomplete inputs. Published in Information Fusion.',
         ' 学习脑部 MRI 序列间的互补表征，在部分序列缺失时仍可进行分割，发表于 Information Fusion。'),
        ('2026-08', '#focus', 'FOCUS',
         ' evaluates a foundation-model workflow for 3D OCT diagnosis across four external centers. Published in npj Digital Medicine.',
         ' 构建基于基础模型的三维 OCT 诊断流程，并在四家外部中心进行评估，发表于 npj Digital Medicine。'),
        ('2026-08', '#scholar-57', 'DRAgent',
         ' preprint presents a multi-agent framework for diabetic retinopathy treatment planning and evaluates it with clinicians and clinical guidelines.',
         ' 预印本提出面向糖尿病视网膜病变治疗规划的多智能体框架，结合临床指南与医生评审进行评估。'),
        ('2026-06', '#synlits', 'SynLiTS',
         ' combines phase-conditioned synthesis with feature fusion for unaligned liver CT. Published in IEEE TMI.',
         ' 结合期相条件合成与特征融合，从配准不完全的多期肝脏 CT 中学习，发表于 IEEE TMI。'),
        ('2026-03', '#mirage', 'MIRAGE',
         ' studies how to reduce the effect of mismatched and semantically related pairs in medical image–text pretraining. Published in Medical Image Analysis.',
         ' 研究如何减轻图文错配及语义相近样本对医学图文预训练的干扰，发表于 Medical Image Analysis。'),
        ('2026-03', '#animerplus', 'AniMer+',
         ' extends family-aware pose and shape estimation to mammals and birds. Published in IEEE TPAMI.',
         ' 利用动物分类学信息进行姿态与形状估计，将模型扩展至哺乳类和鸟类，发表于 IEEE TPAMI。'),
        ('2025-11', affiliation_url, 'CATL HKRI',
         ' · Joined as a Senior AI Engineer, working on AI for Science and Agentic AI.',
         ' · 加入宁德时代香港研究院，担任高级 AI 工程师，从事科学智能与智能体 AI 研究。'),
        ('2025-09', thesis_url, L('PhD at the University of Hong Kong', '香港大学博士'),
         ' · Completed my PhD in Electrical and Electronic Engineering, with a thesis on federated and annotation-efficient learning.',
         ' · 获电子与电气工程博士学位，论文研究面向医学影像分析的联邦学习与标注高效学习。'),
        ('2025-09', '#unioctseg', 'UniOCTSeg',
         ' introduces hierarchical prompting for joint learning across retinal layer annotation protocols. Published at MICCAI.',
         ' 提出层级提示方法，在不同视网膜层标注规范下联合训练模型，发表于 MICCAI。'),
        ('2025-06', '#animer', 'AniMer',
         ' uses taxonomic structure for animal pose and shape estimation. Published at CVPR.',
         ' 利用动物分类学中的层级关系估计动物姿态与形状，发表于 CVPR。'),
        ('2025-03', '#fedlppa', 'FedLPPA',
         ' studies personalized federated segmentation under heterogeneous weak supervision. Published in IEEE TMI.',
         ' 研究各机构弱标注条件不一致时的个性化联邦分割，发表于 IEEE TMI。'),
        ('2023-12', 'https://doi.org/10.1016/j.media.2023.102937', 'YoloCurvSeg',
         ' constructs dense segmentation supervision from a single noisy skeleton annotation. Published in Medical Image Analysis.',
         ' 从一条含噪骨架标注构造像素级分割监督，发表于 Medical Image Analysis。'),
        ('2023-10', 'https://openaccess.thecvf.com/content/ICCV2023/html/Cheng_PRIOR_Prototype_Representation_Joint_Learning_from_Medical_Images_and_Reports_ICCV_2023_paper.html', 'PRIOR',
         ' learns transferable representations from paired medical images and clinical reports. Published at ICCV.',
         ' 从配对的医学影像与临床报告中学习可迁移表征，发表于 ICCV。'),
    )

    def timeline(items):
        content = ''.join(
            f'<li><time datetime="{date}">{date.replace("-", ".")}</time>'
            f'<p><a href="{escape(url)}">{escape(title)}</a>{escape(L(en, cn))}</p></li>'
            for date, url, title, en, cn in items
        )
        return f'<ul class="news-list">{content}</ul>'

    return f'''<section class="container section news-section" aria-labelledby="News">
<h2 id="News">{L('News', '学术动态')}</h2>{timeline(notices[:8])}
<details class="news-archive"><summary>{L('Earlier updates', '往期动态')}</summary>{timeline(notices[8:])}</details>
</section>'''


def experience(zh, cv_url):
    L = lambda en, cn: cn if zh else en
    items = (
        (L('CATL Hong Kong Research Institute (HKRI)', '宁德时代香港研究院（HKRI）'),
         '', ((L('Senior AI Engineer', '高级 AI 工程师'), L('Nov 2025 – Present', '2025.11 至今')),)),
        (L('The University of Hong Kong', '香港大学'),
         'OMEGA Lab',
         ((L('PhD in Electrical and Electronic Engineering', '电子与电气工程博士'), L('Sep 2021 – Sep 2025', '2021.09–2025.09')),)),
        (L('Southern University of Science and Technology', '南方科技大学'),
         'MedICAL Lab', (
             (L('Joint PhD training with HKU', '博士联合培养（香港大学）'), L('Sep 2021 – Sep 2025', '2021.09–2025.09')),
             (L('Visiting Student and Research Assistant', '访问学生及研究助理'), L('Jul 2019 – Aug 2021', '2019.07–2021.08')),
         )),
        (L('Sun Yat-sen University', '中山大学'),
         '', ((L('MS in Information and Communication Engineering', '信息与通信工程硕士'), L('Sep 2018 – Jun 2021', '2018.09–2021.06')),)),
        (L('South China Normal University', '华南师范大学'),
         '', ((L('BEng in Communication Engineering', '通信工程学士'), L('Sep 2014 – Jun 2018', '2014.09–2018.06')),)),
    )

    def entry(org, lab, appointments):
        affiliation = f'<p class="experience-lab">{escape(lab)}</p>' if lab else ''
        details = ''.join(
            f'<div class="experience-detail"><p>{escape(role)}</p>'
            f'<span class="experience-date">{escape(date)}</span></div>'
            for role, date in appointments
        )
        return f'<li><h3>{escape(org)}</h3>{affiliation}{details}</li>'

    return f'''<section class="container section experience-section" aria-labelledby="Experience">
<div class="section-title"><h2 id="Experience">{L('Experience', '工作与教育经历')}</h2>
<div><a href="{escape(cv_url)}#experience">{L('Academic CV', '完整学术简历')} →</a></div></div>
<ul class="experience-list">{''.join(entry(*item) for item in items)}</ul></section>'''


def peer_review(zh, review_venues, venue_metric, metrics):
    L = lambda en, cn: cn if zh else en
    groups = (
        ('journals', L('Journal peer review', '期刊审稿')),
        ('conferences', L('Conference peer review', '会议审稿')),
    )
    def metric_key(venue, conferences):
        if not venue.endswith(')'):
            return venue
        title, _, suffix = venue.rpartition(' (')
        return suffix.removesuffix(')') if conferences else title

    def metric_order(venue, conferences):
        label, *_ = metrics.get(metric_key(venue, conferences), ('',))
        if label.startswith('JIF '):
            return -float(label.removeprefix('JIF '))
        return {'CCF A': -3, 'CCF B': -2, 'CCF C': -1}.get(label, 0)

    def venue_rows(key):
        conferences = key == 'conferences'
        venues = sorted(review_venues[key], key=lambda name: metric_order(name, conferences))
        return ''.join(f'<li>{escape(name)}{venue_metric(metric_key(name, conferences))}</li>' for name in venues)

    entries = ''.join(
        f'<div><dt>{label}</dt><dd><ul>{venue_rows(key)}</ul></dd></div>'
        for key, label in groups
    )
    return f'''<section class="container section service-section" aria-labelledby="Service">
<h2 id="Service">{L('Academic Service', '学术服务')}</h2>
<dl class="service-list">{entries}</dl></section>'''
