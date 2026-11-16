"""Biography, news, experience, and peer review on the bilingual homepage."""

from html import escape
from itertools import groupby
import re


def intro(zh, profile, cv_url):
    L = lambda en, cn: cn if zh else en
    profiles = (
        ('cv', cv_url, L('Academic CV', '学术简历')),
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
    if profile.get('wechatQr'):
        links += f'<a href="{escape(profile["wechatQr"])}" data-wechat><svg class="profile-icon" aria-hidden="true" viewBox="0 0 24 24"><use href="assets/profile-icons.svg#wechat"></use></svg>{L("WeChat", "微信")}</a>'
    emails = ' <span aria-hidden="true">·</span> '.join(
        f'<a href="mailto:{escape(address)}">{escape(address)}</a>'
        for address in (profile['primaryEmail'], profile['secondaryEmail'])
    )
    return f'''<section id="About" class="intro-band" aria-labelledby="name">
<div class="container intro-grid">
<a class="portrait-frame" href="{escape(profile['portraitLarge'])}" data-figure data-portrait data-caption="{L('Li Lin', '林立')}"
aria-label="{L('Enlarge portrait of Li Lin', '放大查看林立的照片')}" aria-haspopup="dialog"><img class="portrait"
src="{escape(profile['portrait'])}" width="408" height="491" alt="{L('Li Lin', '林立的照片')}" fetchpriority="high"></a>
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


def wechat_dialog(zh, profile):
    if not profile.get('wechatQr'):
        return ''
    title = '微信' if zh else 'WeChat'
    close = '关闭' if zh else 'Close'
    instruction = ('请用微信扫描二维码，添加时简要介绍自己并注明来意。' if zh else
                   'Scan in WeChat and include a brief introduction and the reason for reaching out in your friend request.')
    return f'''<dialog class="wechat-dialog" id="wechat-dialog" aria-labelledby="wechat-title">
<div class="dialog-bar"><h2 id="wechat-title">{title}</h2><form method="dialog"><button autofocus>{close} <span aria-hidden="true">×</span></button></form></div>
<div class="wechat-body"><img src="{escape(profile['wechatQr'])}" width="884" height="884" alt="{'微信二维码' if zh else 'WeChat contact QR code'}" loading="lazy" decoding="async"><p>{instruction}</p></div>
</dialog>'''


def biography(zh, thesis_url, profile, sidebar):
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
    email = f'<a href="mailto:{escape(profile["primaryEmail"])}">{L("email me", "给我发邮件")}</a>'
    collab = L(
        f'For collaborations in Agentic AI, recursive self-improvement (RSI), AI for Science, AI for Healthcare, computer vision, multimodal AI, or related areas, feel free to {email}',
        f'欢迎在智能体 AI、递归自我改进（RSI）、科学智能、医疗人工智能、计算机视觉、多模态 AI 等方向开展合作。您可以{email}',
    )
    if qr := profile.get('wechatQr'):
        wechat = f'<a href="{escape(qr)}" data-wechat aria-haspopup="dialog">{L("connect on WeChat", "微信")}</a>'
        collab += L(
            f' or {wechat}. In your WeChat request, please briefly introduce yourself and mention what you’d like to discuss.',
            f'，也可以通过{wechat}联系我。添加微信时，请在好友验证信息中简要介绍自己并注明来意。',
        )
    else:
        collab += L('.', '。')
    return f'''<section class="container section bio-section" aria-labelledby="Biography">
<h2 id="Biography">{L('Biography', '个人简介')}</h2>
<div class="biography-layout">{sidebar}
<div class="bio"><p>{current}</p>{directions(current_methods)}
<p>{healthcare}</p>{directions(methods)}<p class="bio-collaboration">{collab}</p></div></div></section>'''


def news(zh, affiliation_url, thesis_url, cv_url, papers):
    L = lambda en, cn: cn if zh else en
    dataset = next(paper['data'] for paper in papers if paper['id'] == 'sustech-sysu')
    code = {paper['id']: paper['code'] for paper in papers if paper.get('code')}
    related = {
        '#eyegraph': (
            (code['eyegraph'], L('Code', '代码')),
            (f'{code["eyegraph"]}/blob/main/img/online_demo.mp4', L('Demo video', '演示视频')),
        ),
        '#unioctsegplus': ((code['unioctsegplus'], L('Code and data guide', '代码与数据说明')),),
        '#mfmcm': ((code['mfmcm'], L('Training code', '训练代码')),),
        '#scholar-57': ((f'{code["scholar-57"]}/tree/main/evaluation', L('Evaluation code', '评测代码')),),
        '#mirage': ((code['mirage'], L('Training code', '训练代码')),),
        '#animerplus': (('https://animerplus.github.io/', L('Project page', '项目页')),),
        '#lumos': (('#scholar-61', L('TOF-MRA study', 'TOF-MRA 论文')), ('#scholar-62', 'DAPS')),
        '#scholar-52': (('#scholar-53', 'SMNet'),),
        '#yolocurvseg': (
            (code['yolocurvseg'], L('Code and data', '代码与数据')),
            (L('https://www.sustech.edu.cn/en/faculties/tangxiaoying.html',
               'https://www.sustech.edu.cn/zh/faculties/tangxiaoying.html'), L('Recognition', '奖项资料')),
        ),
        '#scholar-7': (('#scholar-6', L('Lesion-aware learning paper', '病灶感知学习论文')),),
        '#sustech-sysu': ((dataset, L('Download dataset', '下载数据集')),),
    }
    for project in ('unioctseg', 'mefn', 'animer', 'procns', 'fedlppa', 'lfsynthseg',
                    'uni4eyeplus', 'fedicra', 'prior', 'scholar-2', 'bsdanet'):
        related[f'#{project}'] = ((code[project], L('Code', '代码')),)

    recent = (
        ('2026-10', '#eyegraph', 'EyeGraph',
         ' uses a medical knowledge graph to guide retinal image report generation. Published online in IEEE TMI.',
         ' 将医学知识图谱推理引入眼底影像报告生成，已在 IEEE TMI 在线发表。'),
        ('2026-09', '#unioctsegplus', 'UniOCTSeg++',
         ' uses hierarchical prompts to share supervision across annotation granularities. Published in IEEE TMI.',
         ' 通过层级提示整合不同标注粒度的监督信息，发表于 IEEE TMI。'),
        ('2026-09', '#mfmcm', 'MF-MCM',
         ' uses complementary masks for MRI pretraining and tests transfer with missing sequences. Published in Information Fusion.',
         ' 用跨序列互补掩码进行脑部 MRI 预训练，并研究缺失序列时的迁移表现，发表于 Information Fusion。'),
        ('2026-08', '#focus', 'FOCUS',
         ' evaluates a foundation-model workflow for 3D OCT diagnosis across four external centers. Published in npj Digital Medicine.',
         ' 构建基于基础模型的三维 OCT 诊断流程，并在四家外部中心进行评估，发表于 npj Digital Medicine。'),
        ('2026-08', '#scholar-57', 'DRAgent',
         ' preprint evaluates multi-agent treatment planning for diabetic retinopathy with guideline checks and clinician review.',
         ' 预印本研究多专科智能体如何协作规划糖尿病视网膜病变的治疗方案，采用指南核查与医生评审。'),
        ('2026-06', '#synlits', 'SynLiTS',
         ' combines phase-conditioned synthesis with feature fusion for unaligned liver CT. Published in IEEE TMI.',
         ' 结合期相条件合成与特征融合，从配准不完全的多期肝脏 CT 中学习，发表于 IEEE TMI。'),
        ('2026-06', 'https://huggingface.co/datasets/Hal1010/HROCT-Bench', 'HROCT-Bench',
         ' updated six open retinal OCT subsets for evaluating segmentation across annotation granularities.',
         ' 更新 6 个公开的视网膜 OCT 子集，支持跨标注粒度的分割评测。'),
    )

    earlier = (
        ('2026-04', '#lumos', 'LUMOS',
         ' uses reliability-weighted pseudo-labels to share supervision across OCT annotation levels. Two other papers at IEEE ISBI study synthetic training data for TOF-MRA vessel segmentation and anatomy-guided PET attenuation correction.',
         ' 按可靠性对伪标签加权，在不同 OCT 标注层级之间传递监督。同届 IEEE ISBI 另有两项工作，分别研究基于合成数据的 TOF-MRA 血管分割和解剖先验引导的 PET 衰减校正。'),
        ('2026-03', '#mirage', 'MIRAGE',
         ' uses optimal transport and adaptive gradient balancing to reduce the effects of mismatched reports and false negatives in medical image–text pretraining. The study evaluates transfer on six tasks and appeared in Medical Image Analysis.',
         ' 利用最优传输与自适应梯度平衡，降低医学图文预训练中报告错配和假负样本的干扰。在六项任务上评估迁移表现，发表于 Medical Image Analysis。'),
        ('2026-03', '#animerplus', 'AniMer+',
         ' extends single-image 3D reconstruction to quadrupedal mammals and birds with shared Transformer layers and taxon-specific experts. Evaluation includes out-of-domain animals. Published in IEEE TPAMI.',
         ' 以共享 Transformer 层和面向不同分类群的专家模块，将单图三维重建扩展至四足哺乳动物和鸟类，并评估域外泛化表现。发表于 IEEE TPAMI。'),
        ('2025-11', affiliation_url, 'CATL HKRI',
         ' · Joined as a Senior AI Engineer. My work spans agent evaluation and self-improvement, autonomous research frameworks for materials, and multimodal battery characterization.',
         ' · 加入宁德时代香港研究院，担任高级 AI 工程师，研究智能体评测与自我改进、面向材料的自主科研框架，以及多模态电池表征。'),
        ('2025-09', thesis_url, L('PhD at the University of Hong Kong', '香港大学博士'),
         ' · Completed my PhD in Electrical and Electronic Engineering with joint training at SUSTech. My thesis studies efficient learning from sparse annotations and personalized federated learning across medical imaging sites.',
         ' · 获香港大学电子与电气工程博士学位，由港大与南科大联合培养。博士论文研究稀疏标注下的高效学习，以及跨机构医学影像的个性化联邦学习。'),
        ('2025-09', '#unioctseg', 'UniOCTSeg',
         ' combines hierarchical prompts with progressive consistency training to integrate six retinal-layer labeling schemes in one model. Evaluated on eight OCT datasets and published at MICCAI.',
         ' 结合层级提示与渐进一致性训练，用一个模型整合六种视网膜层标注粒度。在八个 OCT 数据集上评估，发表于 MICCAI。'),
        ('2025-08', '#mefn', 'MEFN',
         ' calibrates uncertainty in PET and CT separately before fusing voxel-level evidence. Evaluated for both tumor delineation and uncertainty on AutoPET and HECKTOR. Published in Knowledge-Based Systems.',
         ' 分别估计 PET 与 CT 的不确定性后，再融合体素级证据。在 AutoPET 和 HECKTOR 上评估肿瘤分割与不确定性估计，发表于 Knowledge-Based Systems。'),
        ('2025-06', '#animer', 'AniMer',
         ' uses family-level supervision to learn 3D pose and shape across quadrupeds. Its CtrlAni3D training data pair synthetic images with aligned mesh annotations. Published at CVPR.',
         ' 利用科级分类信息学习不同四足动物的三维姿态与形状，并构建合成图像与三维网格精确对应的 CtrlAni3D 训练数据。发表于 CVPR。'),
        ('2025-04', '#procns', 'ProCNS',
         ' calibrates feature prototypes as training progresses and suppresses unreliable pseudo-labels to limit error accumulation under sparse supervision. Published in IEEE JBHI.',
         ' 随训练逐步校准特征原型，抑制不可靠伪标签，缓解稀疏监督下伪标签误差的累积。发表于 IEEE JBHI。'),
        ('2025-03', '#fedlppa', 'FedLPPA',
         ' uses personalized prompts and parameter-wise aggregation to account for differences in institutional data distributions and weak annotation protocols. Evaluated across four segmentation tasks and published in IEEE TMI.',
         ' 通过个性化提示与逐参数聚合，适应机构间的影像分布与弱标注差异。在四项分割任务上评估，发表于 IEEE TMI。'),
        ('2025-02', '#lfsynthseg', 'LF-SynthSeg',
         ' uses healthy tissue anatomy and intensity to synthesize tumor training pairs, enabling brain tumor segmentation without manually drawn tumor masks. Published in IEEE JBHI.',
         ' 利用健康脑组织的解剖与强度信息合成肿瘤训练样本，在无需人工肿瘤掩码的条件下训练分割模型。发表于 IEEE JBHI。'),
        ('2024-12', '#scholar-52', 'MMCM',
         ' learns cross-sequence MRI representations through complementary masks. A second study, SMNet, combines cross-contrast alignment with arbitrary-scale isotropic reconstruction. Both appeared at IEEE BIBM.',
         ' 通过互补掩码学习 MRI 跨序列表征。同期的 SMNet 将跨对比度配准与任意倍率各向同性重建结合。两项工作均发表于 IEEE BIBM。'),
        ('2024-07', '#uni4eyeplus', 'Uni4Eye++',
         ' extends masked pretraining across 2D ophthalmic images and 3D volumes, with reconstruction heads tailored to each modality. Published online in IEEE TMI.',
         ' 将掩码预训练扩展到二维眼科图像和三维体数据，并为不同模态设置相应的重建头。已在 IEEE TMI 在线发表。'),
        ('2024-07', '#scholar-31', 'JOINEDTrans',
         ' transfers a vascular spatial prior to joint optic disc and cup segmentation and foveal localization. The coarse-to-fine design was evaluated on three public datasets and published in Computers in Biology and Medicine.',
         ' 将视网膜血管的空间先验迁移到视盘、视杯分割与中心凹定位，采用由粗到细的结构在三个公开数据集上评估。发表于 Computers in Biology and Medicine。'),
        ('2024-03', '#scholar-68', 'pFedWSD',
         ' distills shared segmentation knowledge into personalized teachers using estimates of site similarity. The framework handles differences in both imaging distributions and sparse labels. Published in Journal of Image and Graphics.',
         ' 估计机构间相似性，将共享分割知识蒸馏至个性化教师模型，同时处理影像分布与稀疏标注的异质性。发表于《中国图象图形学报》。'),
        ('2023-12', '#yolocurvseg', 'YoloCurvSeg',
         ' constructs dense segmentation supervision from one noisy skeleton by combining synthesized anatomy with backgrounds from unlabeled images. Published in Medical Image Analysis and named a representative algorithm at the China Medical AI Conference.',
         ' 将合成解剖结构与无标注图像背景结合，仅用一条含噪骨架构建像素级分割监督。发表于 Medical Image Analysis，并入选中国医学人工智能大会代表性算法。'),
        ('2023-10', '#fedicra', 'FedICRA',
         ' learns site-aware representations and personalizes parameter aggregation across institutions with different imaging distributions and weak labels. Published in the MLMI workshop proceedings at MICCAI.',
         ' 学习机构特异表征并实施个性化参数聚合，适应跨机构的影像分布与弱标注差异。发表于 MICCAI 的 MLMI 工作坊论文集。'),
        ('2023-10', '#prior', 'PRIOR',
         ' aligns medical images and reports at global and local scales, using sentence prototypes to preserve clinically relevant language. Transfer was evaluated on five downstream tasks. Published at ICCV.',
         ' 在全局和局部尺度对齐影像与临床报告，以句子原型保留临床语义。迁移评测覆盖五项下游任务，发表于 ICCV。'),
        ('2022-12', '#scholar-2', 'AADG',
         ' searches for augmentation policies that expand the diversity of training domains in feature space. Evaluation tests transfer across unseen retinal datasets and imaging modalities. Published in IEEE TMI.',
         ' 在特征空间搜索能拓展训练域多样性的数据增强策略，评估对未见视网膜数据集与其他成像模态的迁移表现。发表于 IEEE TMI。'),
        ('2022-12', '#scholar-20', 'JOINED',
         ' uses pixel-to-landmark distances as auxiliary supervision, jointly locating the fovea and delineating the optic disc and cup. Published in the MIDL proceedings.',
         ' 以像素到解剖标志点的距离作为辅助监督，联合定位中心凹、分割视盘和视杯。发表于 MIDL 论文集。'),
        ('2022-09', '#scholar-27', 'DS³-Net',
         ' learns to synthesize contrast-enhanced T1 MRI from paired and unpaired scans. A difficulty map emphasizes regions that are harder to reconstruct. Published at MICCAI.',
         ' 联合利用配对与非配对扫描合成 T1 增强 MRI，由难度图引导模型关注更难重建的区域。发表于 MICCAI。'),
        ('2022-09', '#uni4eye', 'Uni4Eye',
         ' pretrains a shared Transformer on 2D ophthalmic images and 3D volumes by reconstructing masked intensities and gradients. Transfer was evaluated on six classification tasks. Published at MICCAI.',
         ' 通过重建掩码区域的强度与梯度，在二维眼科图像和三维体数据上联合预训练共享 Transformer。迁移评测覆盖六项分类任务，发表于 MICCAI。'),
        ('2021-09', '#bsdanet', 'BSDA-Net',
         ' uses boundary heatmaps and signed distance maps to represent the foveal avascular zone, sharing its geometry between delineation and classification. Published at MICCAI.',
         ' 以边界热图和符号距离图表征黄斑中心凹无血管区，将几何信息用于联合分割与分类。发表于 MICCAI。'),
        ('2021-09', '#scholar-7', 'I-SECRET',
         ' learns fundus image enhancement from synthetic degradations and unpaired clinical images. Another paper studies lesion-centered contrastive learning for retinopathy grading. Both appeared at MICCAI.',
         ' 从合成退化图像和非配对临床图像中学习眼底影像增强。同期工作以病灶为中心开展对比学习，用于视网膜病变分级。两项工作均发表于 MICCAI。'),
        ('2021-04', '#scholar-35', L('Corneal nerve segmentation', '角膜神经分割'),
         ' combines contrastive image synthesis with quality enhancement to address uneven illumination and imperfect labels in confocal microscopy. Published at IEEE ISBI.',
         ' 结合对比式图像合成与质量增强，应对共聚焦显微镜影像的光照不均与标注误差。发表于 IEEE ISBI。'),
        ('2021-03', '#scholar-25', 'BLU-GAN',
         ' uses bidirectional ConvLSTM units to combine features across scales for retinal vessel segmentation. The paper received the Best Paper Award at BenchCouncil FICC 2020 and appeared in the 2021 proceedings.',
         ' 用双向 ConvLSTM 融合跨尺度特征来分割视网膜血管，获 BenchCouncil FICC 2020 最佳论文奖，正式论文收录于 2021 年出版的论文集。'),
        ('2020-11', '#sustech-sysu', 'SUSTech–SYSU',
         ' released 1,219 fundus photographs with lesion and anatomical landmark annotations and diabetic retinopathy grades from three protocols. Published in Scientific Data.',
         ' 开放 1,219 张眼底照片，提供病灶、解剖标志点标注及三套糖尿病视网膜病变分级。发表于 Scientific Data。'),
        ('2020-04', '#scholar-11', L('Retinal hemorrhage detection', '眼底出血病灶检测'),
         ' refines coarse bounding-box annotations before training a label-smoothed detector for retinal hemorrhages. Published at IEEE ISBI.',
         ' 先校正粗略的病灶框标注，再以标签平滑训练眼底出血病灶检测模型。发表于 IEEE ISBI。'),
    )

    venue_names = ('IEEE TMI', 'Information Fusion', 'npj Digital Medicine', 'Medical Image Analysis',
                   'IEEE TPAMI', 'Knowledge-Based Systems', 'IEEE JBHI', 'IEEE BIBM',
                   'Computers in Biology and Medicine', 'Journal of Image and Graphics', '《中国图象图形学报》',
                   'MICCAI', 'MLMI', 'CVPR', 'ICCV', 'MIDL', 'IEEE ISBI', 'BenchCouncil FICC 2020',
                   'Scientific Data', 'China Medical AI Conference', '中国医学人工智能大会')
    venue_pattern = re.compile(r'(?<![A-Za-z])(' + '|'.join(map(re.escape, venue_names)) + r')(?![A-Za-z])')

    def timeline(items):
        rows = []
        for date, url, title, en, cn in items:
            summary = venue_pattern.sub(r'<strong>\1</strong>', escape(L(en, cn)))
            resources = ''.join(
                f' <span class="news-resource"><span aria-hidden="true">·</span> '
                f'<a href="{escape(link)}">{escape(label)}</a></span>'
                for link, label in related.get(url, ())
            )
            rows.append(
                f'<li><time datetime="{date}">{date.replace("-", ".")}</time>'
                f'<p><a href="{escape(url)}">{escape(title)}</a>{summary}{resources}</p></li>'
            )
        return f'<ul class="news-list">{"".join(rows)}</ul>'

    archive = ''.join(
        f'<h3 id="News-{year}">{year}</h3>{timeline(items)}'
        for year, items in groupby(earlier, key=lambda notice: notice[0][:4])
    )
    year_range = f'{earlier[-1][0][:4]}–{earlier[0][0][:4]}'
    return f'''<section class="container section news-section" aria-labelledby="News">
<div class="section-title"><h2 id="News">{L('News', '学术动态')}</h2>
<div><a href="{escape(cv_url)}#resources">{escape(L('Code & data', '开放成果'))} →</a></div></div>
{timeline(recent)}
<details class="news-archive" id="NewsArchive">
<summary>{L('Earlier updates', '往期动态')} <span>({year_range})</span></summary>
{archive}</details>
</section>'''


def experience(zh, cv_url):
    L = lambda en, cn: cn if zh else en
    items = (
        (('catl.svg', 'experience-catl', 190, 20), L('CATL Hong Kong Research Institute (HKRI)', '宁德时代香港研究院（HKRI）'),
         '', ((L('Senior AI Engineer', '高级 AI 工程师'), L('Nov 2025 – Present', '2025.11 至今')),)),
        (('hku-crest.svg', '', 40, 40), L('The University of Hong Kong', '香港大学'),
         'OMEGA Lab',
         ((L('PhD in Electrical and Electronic Engineering', '电子与电气工程博士'), L('Sep 2021 – Sep 2025', '2021.09–2025.09')),)),
        (('sustech.png', '', 190, 189), L('Southern University of Science and Technology', '南方科技大学'),
         'MedICAL Lab', (
             (L('Joint PhD training with HKU', '博士联合培养（香港大学）'), L('Sep 2021 – Sep 2025', '2021.09–2025.09')),
             (L('Visiting Student and Research Assistant', '访问学生及研究助理'), L('Jul 2019 – Aug 2021', '2019.07–2021.08')),
         )),
        (('sysu.png', '', 229, 229), L('Sun Yat-sen University', '中山大学'),
         '', ((L('MS in Information and Communication Engineering', '信息与通信工程硕士'), L('Sep 2018 – Jun 2021', '2018.09–2021.06')),)),
        (('scnu.png', '', 220, 241), L('South China Normal University', '华南师范大学'),
         '', ((L('BEng in Communication Engineering', '通信工程学士'), L('Sep 2014 – Jun 2018', '2014.09–2018.06')),)),
    )

    def entry(logo, org, lab, appointments):
        file, css, width, height = logo
        mark_class = f'experience-mark {css}'.rstrip()
        mark = (f'<span class="{mark_class}" aria-hidden="true">'
                f'<img src="assets/institutions/{escape(file)}" alt="" width="{width}" height="{height}" loading="lazy" decoding="async"></span>')
        affiliation = f'<p class="experience-lab">{escape(lab)}</p>' if lab else ''
        details = ''.join(
            f'<div class="experience-detail"><p>{escape(role)}</p>'
            f'<span class="experience-date">{escape(date)}</span></div>'
            for role, date in appointments
        )
        return f'<li>{mark}<div><h3>{escape(org)}</h3>{affiliation}{details}</div></li>'

    return f'''<section class="container section experience-section" aria-labelledby="Experience">
<div class="section-title"><h2 id="Experience">{L('Experience', '工作与教育经历')}</h2>
<div><a href="{escape(cv_url)}#experience">{L('Academic CV', '完整学术简历')} →</a></div></div>
<ul class="experience-list experience-with-marks">{''.join(entry(*item) for item in items)}</ul></section>'''


def peer_review(zh, review_venues, venue_metric, metrics):
    L = lambda en, cn: cn if zh else en
    groups = (
        ('journals', L('Journal Reviewer', '期刊审稿人')),
        ('conferences', L('Conference Reviewer', '会议审稿人')),
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
