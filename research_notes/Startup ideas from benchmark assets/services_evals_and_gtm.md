# Services, Evals and Consulting Business Models for a Technical Solo Founder, plus Solo-Founder GTM Evidence (as of Sept 2026)

Context: Ken Wu (UWaterloo CS, soon an MTS at Mercor) has an "autonomous research loop" (AI coding agents plus a protocol with held-out gates and leak checks). It took about ten public ML/data benchmarks to or near SOTA (RelBench, TGB, MAPF tracker, Loghub, Pollock CSV, WCXB, opendataloader-bench, a spelling benchmark). These notes assess whether that can be sold, and how solo technical founders get first revenue.

Research date: 2026-09-27. Search and fetch results were used. Where a figure comes from an aggregator (Sacra, Latka, Tracxn, SEO blogs), I flag it.

---

## Q1. Market for AI evals, benchmark construction and RL environments: players, pricing, what labs pay

### Takeaway
There is real money in this market, but it goes to scale suppliers. Mercor, Surge and Scale each have gross revenue in the billions or high hundreds of millions, and labs sign six- to seven-figure quarterly contracts. Per-task prices ($200–$2,000, occasionally $20k) and Prime Intellect's open bounties ($100–$5k) set the price for a solo builder. The eval tooling layer (Braintrust, Galileo, Arize and others) is a crowded, VC-funded SaaS category priced at $100–$250/month entry tiers. Custom evals and RL environments are also exactly Mercor's own line of business.

### Cited Findings
**RL-environment pricing (primary: Epoch AI, Jan 12 2026)**
- Per-task costs are most commonly $200–$2,000, with rare outliers up to $20,000 for complex software-engineering tasks — [Epoch AI, "An FAQ on RL Environments" (Jan 2026)](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Website replicas ("UI gyms") cost about $20,000 each, and complex product clones (e.g. a Slack clone) about $300,000 — [Epoch AI](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Contracts typically run six to seven figures per quarter, with $300k–$500k examples. Exclusive deals cost about 4–5x non-exclusive ones — [Epoch AI](https://epoch.ai/gradient-updates/state-of-rl-envs); also summarised in [Analytics India Mag](https://analyticsindiamag.com/ai-news-updates/complex-reinforcement-learning-tasks-can-cost-up-to-20000-each-epochai-report)
- Anthropic reportedly discussed spending more than $1B in a single year on RL environments (reported Sept 2025) — [Epoch AI](https://epoch.ai/gradient-updates/state-of-rl-envs)
- What buyers value, in order of emphasis: (1) robustness against reward hacking, (2) difficulty calibration (at least 2–3% pass rate, i.e. at least one success per 64–128 rollouts), (3) task diversity, (4) verifiability ("high reward must mean the task was actually solved") — [Epoch AI](https://epoch.ai/gradient-updates/state-of-rl-envs)
- Signs of quality and commoditisation problems: interviewees reported "a large amount of useless bad environments" (buggy website clones). The binding constraint is QC and managing task creators, not finding talent. Math tasks are "easy to create but don't transfer as well" and may shrink. Growth areas are enterprise workflows (spreadsheets, CRM, expense reports) and long-horizon agentic coding. "Benchmark creators and heavy tool users outperform AI researchers at task design" — [Epoch AI](https://epoch.ai/gradient-updates/state-of-rl-envs)

**Player landscape**
- The 2026 players fall into three groups: (a) human-data companies that added environments (Scale AI, Surge AI, Mercor, Turing, Centific); (b) environment-native startups (Mechanize, Fleet AI, HUD, Veris AI, Plato, Bespoke Labs); (c) open ecosystems (Prime Intellect) — [Troveo, "RL Environment Companies in 2026"](https://www.troveo.ai/resources/rl-environment-companies) (vendor-authored landscape; treat as directional). Longer lists exist at [AlignList Top 40](https://alignlist.com/guides/top-40-rl-environments-startups-and-companies), [YC RL company directory](https://www.ycombinator.com/companies/industry/Reinforcement%20Learning) and [Wing VC analysis](https://www.wing.vc/content/who-will-win-the-rl-environment-market--and-why)
- **Prime Intellect Environments Hub:** a community hub with bounties. Open-access tasks pay $100–$500, and application-only tasks pay $1,000–$5,000+. Prime Intellect is committing "hundreds of thousands of dollars" in grants, and it crowdsourced 400+ environments in 2 months through bounties plus an RL residency with 500+ applicants — [Prime Intellect blog, "Scaling Our Open-Source Environments Program"](https://www.primeintellect.ai/blog/scaling-environments-program); [Environments Hub launch post](https://www.primeintellect.ai/blog/environments)
- **Mercor:** had $2B annualized gross revenue in June 2026, up from $760M at end-2025, and $614M gross revenue in H1 2026. Contractors receive 60–70% of the top line, implying H1 2026 net revenue of about $180–250M — [Sacra (aggregator estimate)](https://sacra.com/c/mercor/). Mercor bought Sepal AI (Feb 2026) and Deeptune (July 2026) to build out RL environments — [RL List vendor profile (aggregator)](https://www.rl-list.com/vendors/mercor). Mercor reached a $10B valuation in late 2025 and sells domain-specific environments for coding, healthcare and law — [HeroHunt (aggregator)](https://www.herohunt.ai/blog/hiring-rl-environment-engineers-2026-labs-guide/)
- Mercor's own blog (June 30 2025) says "evals are the new PRD". It sells APEX benchmarks (APEX-Agents, APEX-Accounting, APEX-SWE), off-the-shelf data and custom human data to both AI labs and enterprises, and says it pioneered "environment generation using autograders" — [Mercor, "Welcome to the Era of Evals"](https://www.mercor.com/blog/welcome-to-the-era-of-evals/)
- **Surge AI:** reportedly $1B+ revenue in 2024 and about a $1.4B run-rate by late 2025 — [Sacra](https://sacra.com/c/surge-ai/); [Latka (low reliability)](https://getlatka.com/companies/surgehq.ai)
- **Scale AI:** $870M revenue in 2024. Meta bought a 49% non-voting stake for $14.3B in June 2025, which benefited Surge as a neutral alternative. SEAL builds benchmarks such as Humanity's Last Exam and MultiChallenge and runs the SEAL leaderboards — [Wikipedia: Scale AI](https://en.wikipedia.org/wiki/Scale_AI); [Contrary Research on Surge](https://research.contrary.com/company/surge-ai)

**Eval tooling SaaS (a different business: selling a platform, not the evals)**
- **Braintrust:** $80M Series B in Feb 2026 led by ICONIQ (a16z, Greylock, Elad Gil participating), about $121M raised in total. Pricing is a free tier (1 GB, 10K scores/month), Pro at $249/month, and custom Enterprise — [Voiceflow explainer](https://www.voiceflow.com/blog/what-is-braintrust); [Tracxn](https://tracxn.com/d/companies/braintrust/__oa36ci6gZZRhWulUAavDKOZLtVKKCXdoLz0NSTi-HOw)
- **Galileo:** Free tier, Pro at $100/month billed yearly, and Enterprise — [Respan comparison](https://www.respan.ai/market-map/compare/braintrust-vs-galileo-ai)
- Named alternatives in 2026 are LangSmith, Arize AX/Phoenix, Langfuse, Galileo, Confident AI, Patronus AI and W&B Weave — [Atlan](https://atlan.com/know/ai-agent/ai-agent-evals/braintrust-alternatives/). Atlan also claims a May 2026 Braintrust AWS breach exposed customer API keys. I have not verified this against a primary source.

### Inferences
- **Selling RL environments or evals to labs directly** is a real market, but labs buy through established vendors that can supply volume, QC and security reviews. A solo founder's realistic entry points are (a) Prime Intellect bounties ($100–$5k each, which prove capability publicly), (b) subcontracting to or through a vendor, or (c) a narrow niche that needs his specific skills. His loop's "held-out gates and leak checks" line up well with buyers' top priority: anti-reward-hacking and verifiability. That is a genuine differentiator for *environment QA/hardening* specifically.
- **The Mercor conflict is severe for this model.** Mercor's core, growing business is exactly "custom evals + RL environments for labs and enterprises" (the APEX line, plus the Sepal and Deeptune acquisitions). As a Mercor employee, Ken selling evals or environments to labs would compete directly with his employer (see Q4).
- **Eval-platform SaaS** is crowded and well funded (Braintrust at $121M raised, plus about 8 named competitors). It is not a solo-founder wedge.

### Gaps
- I did not verify pricing or revenue for Patronus AI, Arize, Vals AI, METR or Epoch AI in this pass. METR and Epoch are primarily non-profit or research organisations and are not direct commercial comparables.
- Mechanize's revenue and pricing are not public in the sources found.
- The per-environment prices are Epoch interview-based figures from Jan 2026. More recent 2026 price points for enterprise-workflow environments were not found.

---

## Q2. Autonomous ML / AI-scientist companies: traction and whether "benchmark SOTA via agents" is commoditised

### Takeaway
"Agent climbs an ML benchmark" is now a heavily funded and heavily published category. Top MLE-bench agents earn Kaggle medals on 65–80% of competitions, and Weco (AIDE) sells exactly "give us code + eval + metric, we optimise it". As a capability, Ken's loop is not unique. What differentiates it is *rigour*: held-out gates and leak checks, plus a public track record on about ten niche benchmarks.

### Cited Findings
- **MLE-bench (Kaggle-style ML engineering):** MLEvolve reports #1 with a 65.3% medal rate on a 12-hour budget. Famou-Agent 2.0 and PiEvolve report 80.3%, and CAIR MARS+ 78.8%, on 24-hour budgets — [MLEvolve GitHub](https://github.com/InternScience/MLEvolve); related 2026 papers include [ScienceFlow (arXiv 2608.14354)](https://arxiv.org/pdf/2608.14354) and [EurekAgent (arXiv 2606.13662)](https://arxiv.org/pdf/2606.13662). These are self-reported leaderboard claims.
- **Weco AI:** raised an $8M seed (July 30 2025, led by Golden Ventures, with BoxGroup, Founder Collective, Scott Belsky and others). Its agent "takes a piece of code, an evaluation command, and a metric… and autonomously runs experiment after experiment". AIDE is open source (aideml) and does tree search over code. Weco has a public beta and an "Aiden" autonomous ML engineer early-access page. Weco also claims AIDE² found a better autoresearch harness in 8 days, including "a layered system against reward hacking" — [Weco seed announcement](https://www.weco.ai/blog/seed-announcement); [Weco public beta](https://www.weco.ai/blog/beyond-trial-and-error-ml-engineering); [AIDE² post](https://www.weco.ai/blog/first-evidence-of-recursive-self-improvement); [aideml GitHub](https://github.com/WecoAI/aideml); [try.weco.ai](https://try.weco.ai/)
- **Intology (Zochi):** calls itself an "Artificial Scientist". It has papers in ICLR 2025 workshops, and a paper accepted to the ACL main proceedings — [Intology blog](https://www.intology.ai/blog/zochi-acl); [Zochi GitHub](https://github.com/IntologyAI/Zochi)
- **Periodic Labs:** raised a $300M seed (Sept 2025) at a $1.3B post-money valuation, led by a16z, with the founders Liam Fedus (ex-OpenAI) and Ekin Dogus Cubuk. Bloomberg (Mar 2026) reported talks at about a $7B valuation, and Forbes (May 2026) reported a $500M raise — [TechCrunch](https://techcrunch.com/2025/09/30/former-openai-and-deepmind-researchers-raise-whopping-300m-seed-to-automate-science/); [Bloomberg](https://www.bloomberg.com/news/articles/2026-03-25/ai-science-startup-periodic-labs-is-in-deal-talks-at-about-7-billion-valuation); [Forbes](https://www.forbes.com/sites/iainmartin/2026/05/07/former-openai-researcher-to-raise-500-million-for-ai-science-startup/)
- **FutureHouse → Edison Scientific:** raised a $70M seed at a $250M valuation (Dec 2025) and launched the Kosmos AI scientist — [Bloomberg](https://www.bloomberg.com/news/articles/2025-12-18/ai-startup-edison-raises-70-million-to-speed-up-scientific-research); [FutureHouse announcement](https://www.futurehouse.org/research-announcements/announcing-edison-scientific)
- **Kumo AI** (relational deep learning; the RelBench authors' company): raised $36.5M in total (Series B $18M, Sequoia, 2022). SiliconANGLE reported Nvidia acquired it in June 2026 — [SiliconANGLE, June 3 2026](https://siliconangle.com/2026/06/03/nvidia-snaps-kumo-ai-predictive-ai-startup-known-extreme-accuracy/); [BusinessWire 2022](https://www.businesswire.com/news/home/20220927005002/en/Predictive-AI-Startup-Kumo-Raises-$18-Million-in-Series-B-Funding-Led-By-Sequoia-Capital-Will-Broadly-Roll-Out-First-Version-of-Its-Product-on-October-16). This matters because RelBench is one of Ken's benchmarks: the main commercial player there is now inside Nvidia.

### Inferences
- "Autonomous ML engineer for your Kaggle-style problem" is **commoditised or crowded at the product level**. Weco sells it directly, open-source agents (AIDE, MLEvolve) are free, and frontier coding agents do much of it out of the box. A solo founder cannot outspend Weco, Periodic ($300M+) or Edison ($70M).
- **Services** remain viable, because clients pay for outcomes and trust, not for the agent. A "we took N public benchmarks to SOTA, with audited held-out discipline" portfolio is a credible sales asset for an applied-ML sprint. Leaderboard gains on niche benchmarks are weak evidence of client ROI unless they are framed as "your metric, your data, a leak-checked improvement".
- Rigour and anti-leak methodology is an under-supplied niche. Weco itself is building anti-reward-hacking layers, which confirms demand. Ken could sell "eval integrity audits", i.e. checking whether a team's reported gains survive held-out and leak checks. That is more distinctive than "we climb benchmarks".

### Gaps
- Sakana AI Scientist's commercial traction, Julius AI and Hex Magic pricing and usage were not verified in this pass.
- No public revenue figures were found for Weco or Intology.
- Kumo's acquisition price was not found.

---

## Q3. Consulting rates: freelance, boutique, productised sprints, fractional

### Takeaway
Credible senior freelance ML rates in the US and Canada run about $150–$250/hour (Toptal tier). Productised AI sprints are commonly advertised at $8k–$35k for 2–3 weeks, with $15k–$25k the most common point. Most of the productised-pricing sources are marketing blogs, so treat them as directional.

### Cited Findings
- Toptal ML engineers average $150–$250/hour (pre-vetted "top 3%"). General Toptal rates run $60–$150+/hour, with senior AI specialists at $200+. Clients pay a $500 deposit and a $79/month subscription. Toptal says the freelancer keeps their set rate — [Toptal ML page (Sept 2026)](https://www.toptal.com/developers/machine-learning); [HireInSouth on Toptal cost](https://www.hireinsouth.com/post/how-much-does-toptal-cost); [goLance rate guide](https://golance.com/hiring/best-freelance-machine-learning-engineers-hourly-rate)
- Productised examples: MLDeep lists $15,000 for a 2-week AI Stack Audit, and NetAesthetics a 2-week deep dive at $25,000. AIDOLS publishes a Sprint ($15–25k, 2–3 weeks), Build ($75–150k, 90 days) and Scale ($25k/month) — [AIDOLS pricing page](https://aidolsgroup.com/en/pricing/); [ConsultKit blog](https://www.consultkit.ai/blog/how-to-productize-ai-consulting-services)
- AI consultant benchmarks: $150–$500/hour, or $1,500–$25,000 per productised project. Readiness assessments run $5–15k (2–3 departments), $15–35k (full operations) and $35–75k+ (multi-division) — [Treetop Growth Strategy](https://treetopgrowthstrategy.com/ai-consultant-cost); [AuditYNow](https://auditynow.com/blog/ai-audit-pricing)
- Fixed-scope sprints are priced at $8k–$35k flat, and the sprint's job is to "deliver one undeniable result quickly" that opens retained work. Paid audits ($2.5k–$15k) convert to five- and six-figure implementation work far better than free audits — [Dojo Labs](https://dojolabs.co/blog/ai-consulting-pricing-models/); [DEMG](https://demg.ai/blog/ai-marketing-diagnostic-package-agencies/) (vendor marketing; directional only)

### Inferences
- A plausible ladder for Ken: a paid "benchmark/eval diagnostic" at about $5–10k (1 week: build a leak-checked held-out harness on the client's problem and report the baseline and headroom), then an "applied ML sprint" at about $15–30k (2–3 weeks, metric-targeted), then a retainer. At about $200/hour equivalent, 10 hours a week of moonlighting would bring in roughly $8k/month, capped by time and employment constraints.
- His loop's cost advantage (agents do most of the iteration) lets him fixed-price aggressively while keeping margin. The durable edge is methodology plus a public portfolio, not labour.

### Gaps
- I did not retrieve Upwork top-tier ML rate data or a named boutique ML firm's published rate card (e.g. a Canadian ML boutique). Fractional ML-lead monthly retainers were only found in marketing blogs, as the AIDOLS $25k/month example.

---

## Q4. Conflict of interest and employment constraints (general, not legal advice)

### Takeaway
The legal default is more favourable in Ontario (no statute; the inventor owns an invention absent contract terms or a hired-to-invent role), and California Labor Code §2870 protects unrelated work done on your own time. But both are overridden or limited by the actual employment contract. Crucially, §2870 excludes inventions that relate to the employer's current or prospective business. Evals, RL environments and expert-data services sit squarely inside Mercor's business, so that model is the highest-risk option while he is employed.

### Cited Findings
- **California §2870:** an employer cannot claim IP that is unrelated to its current or prospective business *and* developed outside work without employer resources. §2872 requires employers to give notice of the §2870 carve-out in assignment agreements — [Mondaq guide](https://www.mondaq.com/unitedstates/trade-secrets/1778072/california-labor-code-2870-employee-invention-ownership-guide); [Cohen IP](https://patentlawip.com/blog/california-labor-code-2870-employee-invention-ownership/)
- Practical advice: read the moonlighting policy before incorporating, and if pre-approval is required, get it *in writing* first. Courts have ruled against founders who had the right facts but no contemporaneous evidence (personal devices, time logs) — [Mondaq](https://www.mondaq.com/unitedstates/trade-secrets/1778072/california-labor-code-2870-employee-invention-ownership-guide); [Wilson Sonsini FAQ](https://ecvc.wsgr.com/faq/formation/when-to-start/im-currently-employed-can-i-work-on-my-startup); [Promise Legal PIIA guide](https://blog.promise.legal/employer-ip-invention-assignment-startup-founders/)
- **Ontario/Canada:** no §2870-style statute. Under *Comstock Canada v. Electec* (1991), an employee not hired to invent kept an invention made on his own time, even though he did the work on company premises, the employer knew of his side business and there was no contractual restriction. The default is that "the inventor keeps the benefit", unless the contract says otherwise or the character of the employment implies otherwise — [CanLII Connects commentary](https://canliiconnects.org/en/commentaries/28950); [vLex: Comstock v. Electec](https://ca.vlex.com/vid/comstock-can-v-electec-680957029)
- Mercor's business explicitly includes evals and benchmarks for AI labs and enterprises (the APEX suite) and RL environments (Sepal and Deeptune acquisitions) — [Mercor blog](https://www.mercor.com/blog/welcome-to-the-era-of-evals/); [RL List](https://www.rl-list.com/vendors/mercor)

### Inferences
- The operative document is Ken's Mercor PIIA / offer letter. The statute matters less than the contract, and it matters most for work that "relates to the employer's business". US startups typically add a non-solicit of customers, a duty of loyalty and outside-activity approval clauses.
- Business-model risk ranking while he is employed at Mercor:
  - **Highest risk:** custom evals, benchmark construction or RL environments sold to AI labs. This competes directly and overlaps Mercor's customers.
  - **Medium risk:** eval-integrity or leak-audit services to enterprises. This is adjacent to Mercor's enterprise evals.
  - **Lower risk:** applied-ML sprints on a client's own tabular or log/document problems, and open-source tools unrelated to training data. Even these need written approval if the contract requires it.
- The existing benchmark work predates employment. He should document provenance now (repo dates, personal hardware) and list it as prior inventions in the PIIA, which most PIIAs allow.
- If he works for Mercor from California, §2870 applies. If he works remotely from Ontario, his contract's governing law and Ontario common law apply. This is a question for a lawyer, not these notes.

### Gaps
- Mercor's actual PIIA and moonlighting terms are not public, and I did not find them.
- Mercor's governing-law clause and Ken's work location are not known.

---

## Q5. Solo-founder GTM: how technical solo founders get the first 10 customers and first revenue

### Takeaway
The best-documented paths are open-source or content-led. A free, useful artefact (a repo, a model, a blog post) earns attention on HN or GitHub, and a hosted or commercial tier monetises it. The first revenue is typically tiny ($64 MRR at Plausible) and slow, and growth compounds from public writing. Solo founders are now about 36% of new startups but raise disproportionately little VC, which favours revenue-first or bootstrapped paths.

### Cited Findings
- **Solo-founder base rates (Carta):** the share of new startups with a solo founder rose from 23.7% (2019) to 36.3% (H1 2025). Solo-led companies were 30% of 2024 foundings but received only 14.7% of priced-round cash. Solo founders were 35% of 2024 incorporations but only 17% of 2024-launched companies that closed a VC round that year — [Carta Solo Founders Report 2025](https://carta.com/data/solo-founders-report/)
- **Plausible (open-source SaaS, bootstrapped):** 60 beta users converted into their first paying subscribers at $64 MRR. It grew from $400 to $10k MRR in nine months, then reached $500k ARR ten months later. A single blog post (Apr 8 2020) hit HN and was read by 50k+ people within days. It reached $1M ARR with a team of four, and later about $3.1M ARR (2024), still bootstrapped — [Plausible: bootstrapping to $500k ARR](https://plausible.io/blog/bootstrapping-saas); [Plausible: $1M ARR open-source SaaS](https://plausible.io/blog/open-source-saas); [OperatorBook (secondary)](https://www.operatorbook.dev/stories/plausible-analytics-revenue-1m-arr-against-google)
- **Pieter Levels:** about $3M/year across solo products. Photo AI at about $138k/month (Nov 2025) is about 70% of income — [Nomadic Blueprint (secondary; Levels posts his revenue publicly on X)](https://nomadicblueprint.com/case-studies/pieter-levels); [FastSaaS](https://www.fast-saas.com/blog/pieter-levels-success-story/). Figures are self-reported and relayed by secondary sites.
- **Datalab (Marker/Surya/Chandra), Vik Paruchuri:** founded June 2024 in Brooklyn. The path ran open-source OCR and PDF tools with large adoption, then a hosted API and commercial licensing: the tools are free for research, personal use and startups under $2M in funding or revenue, with licences for commercial customers. It raised $3.5M (Pebblebed, Factorial), and paying customers reportedly include Anthropic — [Forkable profile](https://www.forkable.io/p/datalab-develops-small-ai-models); [Datalab About](https://www.datalab.to/about); [IDP-Software vendor page](https://idp-software.com/vendors/datalab/). This is the closest analogue to Ken's opendataloader-bench and "folio" PDF-parsing work. The licence model (free under $2M revenue) is a direct template.
- **Firecrawl:** spun out of Mendable (a managed RAG platform whose customers included Coinbase, Snap and MongoDB) after the team kept hitting the web-data pain point. Launched as open source (AGPL-3.0 core, MIT SDKs) in April 2024 and gained about 8k GitHub stars within months. It launched on YC Launch and later raised a Series A alongside /v2 — [YC Launch post](https://www.ycombinator.com/launches/LTf-firecrawl-open-source-crawling-and-scraping-for-ai-ready-web-data); [Firecrawl v1 launch-week post](https://www.firecrawl.dev/blog/launch-week-i-day-4-introducing-firecrawl-v1); [Firecrawl Series A post](https://www.firecrawl.dev/blog/firecrawl-v2-series-a-announcement)
- Productised-consulting ladder evidence: paid audits convert to implementation work at higher rates than free audits, and a sprint's job is "one undeniable result" that leads to retained work — [Dojo Labs](https://dojolabs.co/blog/ai-consulting-pricing-models/) (directional)

### Inferences
- Ken already has the "open-source artefact" half of the playbook: about ten SOTA or near-SOTA repos (folio, streetwise, tremor, marrow and others). Each is a potential Show HN, and benchmark-maintainer PRs and leaderboard entries are free distribution into exactly the teams that care about that problem (document parsing, log parsing, CSV dialect detection, address parsing).
- The strongest-evidence path for him looks like Datalab or Firecrawl, not "research loop as a service". Pick the one or two repos with the clearest commercial pain (PDF-to-structured parsing is proven by Datalab, Unstructured and Reducto; log parsing is another). Ship a hosted API and a commercial licence (free under an $X revenue threshold), then launch on HN. Use sprint consulting on that same problem domain to fund it and find the first 10 customers.
- The first 10 customers will most likely come from (a) people who star, open issues on or fork the repos, (b) benchmark maintainers and their users, and (c) warm network (UWaterloo, Mercor colleagues are off-limits for competing work). Expect first revenue to be small; Plausible started at $64 MRR.

### Gaps
- There is no systematic dataset (e.g. Stripe Atlas or Indie Hackers aggregate) on the median time to first 10 customers for technical solo founders. The evidence is case studies, with survivorship bias.
- No public ARR was found for Firecrawl or Datalab.

---

## Q6. Grants and non-dilutive funding for a Canadian / Waterloo founder

### Takeaway
The main options are SR&ED, NRC IRAP, Velocity and equity programmes. SR&ED is the largest source of non-dilutive money for a Canadian-controlled private corporation (CCPC) doing R&D: from 2026 it is a 35% refundable credit on up to $6M of spend. NRC IRAP funds incorporated SMEs, including up to $30k to hire young graduates. Velocity's grant programmes ($5k/$25k) are UW-linked, and the separate Velocity Fund writes $25k scout and $100k–$1M core equity cheques. YC and CDL are equity or mentorship programmes, not grants.

### Cited Findings
- **SR&ED:** Bill C-15 (Royal Assent Mar 26 2026) doubled the enhanced 35% refundable ITC expenditure limit from $3M to $6M, for tax years beginning on or after Dec 16 2024. That gives up to about $2.1M/year in refundable federal ITCs for eligible CCPCs. The limit phases out between $15M and $75M of taxable capital, and capital expenditures are eligible again — [BDO Canada](https://www.bdo.ca/insights/sr-ed-program-enhancements-and-updates-draft-legislation-released); [Welch LLP](https://welchllp.com/insights/knowledge/2026-changes-in-sred-largest-expansion-in-decades/); [ClearWealth](https://clearwealth.tax/blog/sred-expenditure-limit-2026-ccpc/)
- **NRC IRAP:** helps Canadian SMEs turn innovations into market-ready products — [NRC financial support page](https://nrc.canada.ca/en/support-technology-innovation/financial-support-technology-innovation). The IRAP Youth Employment Program provides up to $30,000 to hire a post-secondary graduate (aged 15–30) for 6–12 months. It is for incorporated, for-profit SMEs with 500 or fewer FTEs — [NRC: funding to hire young graduates](https://nrc.canada.ca/en/support-technology-innovation/nrc-irap-funding-hire-young-graduates); [hellodarwin summary](https://hellodarwin.com/business-aid/programs/industrial-research-assistance-program-irap-youth-employment-program)
- **Velocity (UWaterloo):** the Velocity grant programmes give about $390k a year in equity-free funding through "Velocity Fund $25K" and "Velocity Fund $5K" pitch programmes — [UWaterloo News](https://uwaterloo.ca/news/velocity-building-momentum-waterloo-startups). Separately, the spun-out Velocity Fund (a pre-seed VC) writes $25K scout cheques and $100K–$1M core cheques, promises a decision in two weeks, completed a $10M first close, and says it is the second most active pre-seed fund in Canada per CVCA 2025 — [velocity.fund](https://velocity.fund/); [BetaKit on Fund II $14M initial close](https://betakit.com/university-of-waterloo-backed-velocity-fund-ii-holds-14-million-initial-close/). **Stale or conflicting data flag:** the $390k/year grant figure comes from an older UW news article, and the fund-size figures differ between sources ($10M vs $14M initial close). Check the current terms directly.

### Inferences
- SR&ED only benefits a CCPC that performs eligible R&D, so it requires incorporating in Canada and paying Canadian salaries or contractors. It is highly relevant if Ken's "research loop" work is systematic experimental development, which it arguably is. SR&ED is paid after the fact, so it does not fund the first months.
- IRAP normally requires an incorporated company and an Industrial Technology Advisor (ITA) relationship, so it is more useful after incorporation and some traction.
- If Ken relocates to the US for Mercor, a Canadian CCPC may still be possible, but residency and control rules matter. That is a question for an accountant.

### Gaps
- Current (2026) Velocity grant amounts, cadence and eligibility (e.g. whether alumni are eligible) could not be confirmed from primary pages.
- Creative Destruction Lab terms and current YC deal terms were not fetched in this pass. From general knowledge, YC's standard deal is $500k and CDL is equity-free mentorship, but neither was verified here.
- NRC IRAP's core R&D project contribution amounts for early-stage firms were not confirmed from a primary source.
