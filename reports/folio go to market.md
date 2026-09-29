# folio Enterprise: go-to-market groundwork

*Prepared 29 September 2026. Every competitor price and licence term below was checked at the source on that date unless marked otherwise. This is groundwork for the "folio Enterprise" idea (rank 2 in [Startup ideas from benchmark assets](Startup%20ideas%20from%20benchmark%20assets.md)). It is not legal advice, and nothing here should be acted on before the Mercor preconditions in section 0 are met.*

## Bottom line

**The idea holds up, but it is narrower than the earlier report suggested.** A competitor now sells almost exactly the folio Enterprise pitch.

- **The buyer is real.** Some regulated finance teams are barred from cloud APIs, and they state it in public:
  - Finanz Informatik runs the Sparkassen AI platform "without cloud connectivity in its own data centres".
  - A National Bank of Canada RAG role requires "Canada-only data residency and no external calls".
  - Deutsche Bundesbank converts prospectuses with Docling and runs open-weight LLMs.

  Several on-prem AI vendors also need a fast, local parser to embed: Squirro, Zylon, Onyx, Nextcloud and Nuix.
- **folio's claimed edge has been matched.**
  - **Nutrient's PDF-to-Markdown.** Its *Standard* mode is free and unlimited at any company size, runs locally at 0.004 s/page and scores 0.89 overall on opendataloader-bench. Its *Vision* mode scores **0.93 overall, 0.94 on tables**, runs locally without a GPU and does OCR. Vision costs $299–2,990/yr at list prices ([Nutrient benchmark, updated 2026-09-28](https://www.nutrient.io/blog/pdf-extraction-benchmark-opendataloader-bench/), [pricing](https://www.nutrient.io/api/pricing/pdf-to-markdown/)). Those numbers are Nutrient's own, just as folio's 0.9235 is Ken's own harness run. **folio is not yet on the maintainers' leaderboard, and `foliopdf` is not yet on PyPI** (checked today). "Top of opendataloader-bench" cannot be used in outreach until the leaderboard PR lands, and even then Nutrient Vision claims a higher score.
  - **Docling.** Red Hat now ships hardened, supported Docling builds for regulated enterprises ([Red Hat Developer, 2026-06-30](https://developers.redhat.com/articles/2026/06/30/scale-document-ingestion-docling-and-ray-openshift-ai)).
- **What remains defensible.** folio is the only engine that combines five things:
  1. The highest self-reported score among text-layer, model-free engines: 0.9235 against Nutrient Standard's 0.89.
  2. Apache-2.0 source that a bank can audit line by line.
  3. Deterministic output with no model weights and **no telemetry**. Nutrient's licence says its SDK may send telemetry, and Vision "may require connectivity to verify entitlements".
  4. **OEM redistribution rights.** Nutrient's licence and Datalab's model licence both restrict these.
  5. About 29× Docling's CPU speed on this benchmark.

  So the sharpest wedge is **ISVs that ship on-prem AI into banks and law firms (OEM)**, plus **air-gapped teams that need auditable, dependency-free ingestion for born-digital PDFs**. It is not "the most accurate parser".

## 0. Preconditions (do these before any outreach)

1. **Mercor.** Get written outside-activity approval and a prior-inventions schedule, as in the earlier report's day 1–2 plan. Sales to law firms and investment banks carry an extra flag: Mercor's stated expansion thesis is that "investment banks, consulting firms, and law firms" are future enterprise customers ([Contrary Research](https://research.contrary.com/company/mercor); Sacra says the same). Under California Labor Code §2870's "prospective business" test those segments are the riskiest. Mercor also serves "all of the top five AI labs and six of the Magnificent Seven" (Contrary). Exclude all of them.
2. **Make the claim checkable.**
   - Publish `foliopdf` to PyPI.
   - Open the opendataloader-bench PR from `docs/SUBMISSION.md`.
   - Put the held-out table number (0.7135 against hybrid's 0.8935) on the README front page.
   - Ship `folio eval`, which scores folio, Docling, OpenDataLoader and Nutrient Standard on a buyer's own PDFs, offline.
3. **Canadian anti-spam law (CASL).** Cold commercial email to Canadian recipients is allowed only under implied consent. That means an address published conspicuously, with no "no solicitation" statement, and a message relevant to the recipient's role. Every message needs sender identification and an unsubscribe. Where that is unclear, use warm intros, public team channels or LinkedIn instead. The prospect list below deliberately holds **no personal contact details**.

## 1. Ideal customer profile

### Who buys

| Segment | Firm type and size | Buyer (economic) / champion (technical) | Why folio fits | Why it may not |
|---|---|---|---|---|
| **A. On-prem AI ISVs (OEM), highest priority** | 20–500-person vendors selling self-hosted or air-gapped RAG, search or eDiscovery into banks, governments and law firms (Squirro, Zylon, deepset, Onyx, Nextcloud, Nuix) | CTO or VP Engineering / engineer who owns the ingestion pipeline | They must ship a parser inside the customer's perimeter. Nutrient forbids OEM use without a separate deal ([licence §5](https://github.com/PSPDFKit/pdf-to-markdown)). Datalab's model licence forbids use by competitors and above a revenue threshold. Unstructured's hosted API cannot be called from an air gap. Apache-2.0 folio can be embedded freely, and the paid part is support, a hardened build and the table add-on | ISVs often default to free Docling. OEM deals are slow and small at first |
| **B. Regulated finance, direct** | Mid-market and large banks, cooperative-bank IT centres, pension and asset managers, fund administrators, central banks and regulators. Best fit is 1,000–50,000 staff with an internal AI platform team | Head of AI platform, CDO, or IT architecture lead / ML engineer on the RAG or "document intelligence" team | Born-digital PDFs dominate (filings, prospectuses, fund notices, policies). Policy bars external calls. GPU capacity inside the perimeter is scarce or queued. Model-risk rules (OSFI E-23 from 1 May 2027; SR 11-7) favour deterministic, explainable components | Incoming customer documents are often scans, where folio has **no OCR**. Tables are folio's weakest held-out metric. Procurement takes 3–9 months |
| **C. Legal, mostly via vendors** | Firms still on on-prem DMS or eDiscovery (iManage Work on-prem, Relativity Server, Nuix on-prem), plus in-house legal at regulated companies | Director of KM, innovation or litigation support / legal engineer | iManage says a "substantial number" of customers stay on-prem for data-protection or client reasons, while Ask iManage and its other AI features are cloud-only ([iManage AMA, 2026-01-14](https://imanage.com/resources/resource-center/blog/they-asked-we-answered-imanage-reddit-ama/); [Ask iManage](https://imanage.com/imanage-products/the-imanage-platform/ai/ask-imanage/)). Relativity aiR is not available on Server ([Relativity server policy](https://www.relativity.com/server-policy/); [agenticediscovery](https://agenticediscovery.com/vs-relativity-air/)) | Big law **buys** Harvey or Legora rather than building ([The Logic, 2026-08-19](https://thelogic.co/news/bay-street-law-partner-ai-roles/)). Law firms are Mercor's stated expansion segment. eDiscovery corpora are mostly email and scans |

**Not the ICP:**
- Insurers' claims operations and healthcare: they are scan-heavy.
- Anyone happy with a cloud API: Nutrient, Datalab and LlamaParse are cheaper to buy than a licence.
- AI labs, Mercor customers and competitors, and Reducto (a Mercor supplier).

### Trigger events to watch for

1. **A RAG or "document intelligence" project** leaves the pilot stage and meets a real corpus: millions of pages, and a CPU-only cluster inside the perimeter. Docling on CPU is the usual first attempt, and its GitHub issues show where that hurts:
   - an 8-K filing went from 18 s to 80 s on 2 vCPUs after an upgrade (docling #4174, Sept 2026, open when fetched);
   - a 5-page PDF took more than 15 minutes in docling-serve (#2635);
   - "Docling too slow on CPU machine" (#1101).

   RAGFlow users report DeepDoc parsing that pins 128 cores (#5711) and batch jobs stuck below 1% (#11142).
2. **An air-gap or data-residency mandate.** Examples:
   - Finanz Informatik's no-cloud AI platform;
   - Swiss FINMA-driven on-prem deployments, per [Squirro's case study](https://squirro.com/on-premises-enterprise-ai);
   - Luxembourg professional secrecy, which drove the CSSF onto the air-gapped Clarence cloud ([LuxConnect](https://www.luxconnect.lu/cssf-adopts-clarence/));
   - Canadian government data that must not be "above the Unclassified level" in CANChat ([SSC](https://www.canada.ca/en/shared-services/services/gc-ai/canchat.html)).
3. **A cloud-API compliance block.** A community user objected that uploaded documents "are getting sent over to Marker as opposed to a self-hosted Tika/Docling" ([Open WebUI discussion #14312](https://github.com/open-webui/open-webui/discussions/14312)). A firewall blocks Hugging Face model downloads (docling #904).
4. **Vendor AI that is cloud-only.** iManage AI features are cloud-only. Relativity Server customers can open new matters only until 31 Dec 2027. Nuix Discover GenAI went GA on SaaS on 4 Sept 2026, with on-prem promised for "next quarter" ([Nuix](https://www.nuix.com/whats-new-in-nuix-neo)).
5. **Model-risk deadlines.** OSFI Guideline E-23 takes effect on 1 May 2027 and brings generative and third-party models into inventory, validation and explainability ([OSFI](https://www.osfi-bsif.gc.ca/en/guidance/guidance-library/guideline-e-23-model-risk-management-2027)). A deterministic, rule-based parser is simpler to validate than a VLM. That argument is plausible, but no buyer has confirmed it yet.

### Budget-line evidence

- **Money is already spent on on-prem parsing:**
  - Datalab's Enterprise tier sells "on-prem VPC and air-gapped deployment" at custom prices ([Datalab pricing](https://www.datalab.to/pricing)). Its self-serve on-prem licence covers 1–3 instances, with extra instances "must be purchased" ([datalab-on-prem](https://github.com/datalab-to/datalab-on-prem)).
  - Reducto, LlamaParse and Unstructured all put VPC or on-prem only in their top tier (section 6).
  - Azure Document Intelligence disconnected containers cost 12× the monthly commitment per year, e.g. $8,640/yr for prebuilt at 100k pages/month. *That figure comes from the earlier report via DocuOCR and was not re-verified today.*
- **Funded teams:**
  - CPP Investments' AI & Emerging Tech lead role lists $163k–255k (New York range, posted 2026-09-26) ([posting mirror](https://freehire.me/jobs/lead-software-engineer-ai-emerging-tech-canada-pension-plan-investment-board-epxxapsn)).
  - Cooley advertises $220k–250k for a senior AI data engineer, and Kirkland & Ellis has committed $500M to a custom AI platform ([JD Journal, 2026-09-25](https://www.jdjournal.com/2026/09/25/law-firms-ai-talent/)).

  A $6–18k/yr ingestion licence is well under one engineer's cost.
- **Price ceiling pressure:** Nutrient Vision lists at $2,990/yr for 100k pages a month, and its Standard mode is free. folio can't charge for pages. It has to charge for OEM rights, air-gap packaging, support and audit artefacts.

## 2. Prospect list (28 organisations or teams)

Rules:
- Public information only.
- No personal names or contact details.
- AI labs, known Mercor customers and competitors, and Reducto are excluded.

Legend:
- **Fit:** H means born-digital documents, an explicit no-cloud rule and a build-not-buy team. M means two of those three. L means one.
- **Mercor:** "clear" means no known link. "flag" means it cannot be ruled out, with the reason given.

### A. On-prem AI ISVs (OEM or embed)

| # | Organisation / team | Public evidence of need | Fit | Mercor |
|---|---|---|---|---|
| 1 | **Squirro** (Zurich), enterprise GenAI platform | Deploys "entirely on-premises" for "a national financial institution… prohibited from using public cloud", "driven by… FINMA". Supports "fully air-gapped defense networks" ([Squirro](https://squirro.com/on-premises-enterprise-ai)). Built ECB Athena ([ECB](https://www.bankingsupervision.europa.eu/press/supervisory-newsletters/newsletter/2023/html/ssm.nl231115_2.en.html)) | H | flag: AI software vendor. No known link, but Mercor serves "AI app developers" |
| 2 | **Zylon** (makers of PrivateGPT) | "On-premise Private AI platform for regulated industries". Parsing, splitting and embedding "happen on the customer's hardware" ([Zylon](https://www.zylon.ai/), [private-gpt](https://github.com/zylon-ai/private-gpt)) | H | flag: as #1 |
| 3 | **deepset** (Haystack Enterprise) | Self-hosted and air-gapped options. IDP for "loan agreements, contracts, and regulatory filings" ([deepset FS](https://www.deepset.ai/industries/financial-services), [platform](https://www.deepset.ai/products-and-services/haystack-enterprise-platform)) | H/M | flag: as #1 |
| 4 | **Onyx** (open-source enterprise RAG) | Markets an "air-gappable" self-hosted deployment ([Onyx](https://onyx.app/insights/self-hosted-rag)), but file parsing goes through the Unstructured API client ([Unstructured × Onyx](https://unstructured.io/blog/using-danswer-with-unstructured)), which cannot be called from an air gap | H | flag: as #1 |
| 5 | **Nextcloud GmbH**, Context Chat | Admin manual: document parsing "is a CPU-bound task"; on CPU, 20 MB counts as a large file; LLMs can run "entirely on-premises" ([Nextcloud docs](https://docs.nextcloud.com/server/stable/admin_manual/ai/app_context_chat.html)) | H | clear |
| 6 | **Nuix**, Nuix Discover / Neo | GenAI (summaries, semantic search, AI chat) went GA on SaaS on 4 Sept 2026, with on-prem "next quarter". Supports BYO local LLMs ([Nuix](https://www.nuix.com/whats-new-in-nuix-neo), [on-prem](https://www.nuix.com/solutions/nuix-discover-on-premises)) | M: eDiscovery mixes email and scans | clear |
| 7 | **iManage**, on-prem Work product team | "A substantial number of our customers are still… constrained by local data protection requirements or client requirements", yet AI features are cloud-only ([AMA](https://imanage.com/resources/resource-center/blog/they-asked-we-answered-imanage-reddit-ama/)) | M: vendor strategy is cloud-first | clear |
| 8 | **InfiniFlow** (RAGFlow) | DeepDoc parsing hits CPU and memory limits: [#5711](https://github.com/infiniflow/ragflow/issues/5711) (128 cores near 100%), [#11142](https://github.com/infiniflow/ragflow/issues/11142) (2,000-file batch stuck below 1%), [#11822](https://github.com/infiniflow/ragflow/issues/11822) (OOM at 62 GB) | M: has its own parser | flag: as #1 |
| 9 | **Open WebUI** | Pluggable "content extraction engines" (Tika, Docling, Mistral OCR, Datalab Marker API, MinerU, external) ([docs](https://docs.openwebui.com/features/chat-conversations/rag/document-extraction/)). Users push back on sending documents to a hosted API ([#14312](https://github.com/open-webui/open-webui/discussions/14312)) | M: distribution rather than revenue | flag: as #1 |
| 10 | **LibreChat** | A built-in local `document_parser` for PDF, DOCX and XLSX; richer OCR strategies send files to provider APIs ([LibreChat OCR docs](https://www.librechat.ai/docs/features/ocr)), so a better *local* parser is a natural upgrade | M | flag: as #1 |
| 11 | **Clarence** (LuxConnect–Proximus), air-gapped sovereign cloud | "Europe's first… sovereign disconnected cloud". Pitched to Luxembourg banks, funds and insurers under professional secrecy. The CSSF was its first customer ([LuxConnect](https://www.luxconnect.lu/cssf-adopts-clarence/), [Clarence](https://clarence-cloud.com/en/solution/use-cases/)). Marketplace or channel play | M | **flag:** built with Google technology, and Google is a Mercor customer. Deal only with Clarence, never with Google |

### B. Regulated finance and financial regulators (direct)

| # | Organisation / team | Public evidence of need | Fit | Mercor |
|---|---|---|---|---|
| 12 | **Finanz Informatik** (Sparkassen IT), central AI platform | FI's CEO: the central AI platform "operates in FI's own data centres without cloud connectivity"; even EU hyperscaler clouds create dependency; "AI agents analyse incoming documents" ([Der Bank Blog, 2026-02-10](https://www.der-bank-blog.de/wie-ki-sparkassen-banking2026/digital-banking/37728230/)) | H on policy, M on documents: incoming customer paperwork is often scanned | clear |
| 13 | **National Bank of Canada**, GenAI search/RAG team (Montréal) | Senior data scientist role: RAG, "table and diagram extraction", PaddleOCR for scanned PDFs, "Canada-only data residency and no external calls" ([listing](https://www.simplyhired.ca/job/2-eHnLymG7ymeaiZlucmbLdF7N4yXsyKjzhoF5y19QAdpEmROVL1ww)). *Seen only in a search-engine snippet; the page returned 403 to our fetcher. Verify before citing to them.* | H | flag (low): bank with a capital-markets arm, next to Mercor's "investment banks" thesis |
| 14 | **Deutsche Bundesbank**, collateral-eligibility (prospectus) review | Converts prospectus PDFs to Markdown **with Docling**, runs open-weight LLMs (Llama 3.3 70B), and names "PDF extraction artifacts" and "advanced PDF parsing" as limitations ([arXiv 2606.27316, 2026-06-25](https://arxiv.org/abs/2606.27316)) | H: born-digital, bilingual prospectuses | clear |
| 15 | **CSSF** (Luxembourg regulator) | Runs AI pilots on "sensitive data" in the air-gapped Clarence cloud ([CSSF](https://www.cssf.lu/en/2024/12/the-cssf-adopts-clarence-to-develop-artificial-intelligence-with-full-sovereignty-a-major-breakthrough-for-the-financial-sector/)) | M: public procurement | clear |
| 16 | **ECB Banking Supervision**, Athena / suptech | Athena searches and extracts across "millions of… supervisory assessments and bank documents", built with Squirro on a GPU cluster ([ECB](https://www.bankingsupervision.europa.eu/press/supervisory-newsletters/newsletter/2023/html/ssm.nl231115_2.en.html)) | L direct (reach it via Squirro) | clear |
| 17 | **FINRA**, FILLIP internal LLM tool | An internal LLM tool used weekly by about 40% of staff for "document comparison", member-firm risk reviews, and fund and ETF analysis ([FINRA](https://www.finra.org/media-center/blog/advancing-finras-mission-with-ai-1028205)). Hosting is not disclosed | M | clear |
| 18 | **PSP Investments**, Floyd AI platform (Montréal) | Senior Applied AI Engineer: "retrieval across unstructured and structured data", Databricks, Azure/GCP ([posting mirror, 2026-07-29](https://freehire.me/jobs/senior-applied-ai-engineer-psp-investments-cp654qv7)). **Uses OpenAI, Gemini and Claude APIs, so cloud is allowed.** The pitch is cost and determinism, not air-gap | M/L | clear (a lab customer, not a Mercor customer) |
| 19 | **CPP Investments**, AI & Emerging Tech (Toronto) | Lead engineer role: "LLM pipelines, Agentic, MCP, Graph/RAG", AWS Bedrock ([posting mirror, 2026-09-26](https://freehire.me/jobs/lead-software-engineer-ai-emerging-tech-canada-pension-plan-investment-board-epxxapsn)) | L: cloud-first | clear |
| 20 | **Citco**, Document Intelligence | A proprietary AI platform extracts data from "thousands – and often tens of thousands" of fund documents per client (capital calls, credit agreements) ([Citco, 2024](https://www.citco.com/insights/first-ai-plus-human-platform-offers-fund-managers-high-accuracy-and-structured-data-from-fund-documents)) | M: may already be built | clear |
| 21 | **US SEC**, Division of Examinations and Corporate Finance | The 2024 AI inventory lists "Developed Parsing Logic for Filings" (in operation) and an "8-K Filing Solution" built "on existing enterprise data and analytics platforms… rather than procuring… SaaS" ([SEC inventory CSV](https://www.sec.gov/files/sec-2024-ai-use-case-inventory.csv)) | L: EDGAR is mostly HTML, and folio is PDF-only | clear |

### C. Legal and public-sector legal

| # | Organisation / team | Public evidence of need | Fit | Mercor |
|---|---|---|---|---|
| 22 | **HMCTS**, Common Platform AI RAG service | Open-source "Document Ingestion Rag Service"; ingestion currently uses **Azure Document Intelligence** ([hmcts/cp-ai-rag-service](https://github.com/hmcts/cp-ai-rag-service)) | L: cloud is permitted, so this is a cost pitch only | clear |
| 23 | **Cooley**, Cooley AI | Separate AI unit; 14 open roles, including a senior AI data engineer at $220k–250k ([JD Journal](https://www.jdjournal.com/2026/09/25/law-firms-ai-talent/)) | M | **flag:** large law firm, Mercor's stated expansion segment |
| 24 | **Kirkland & Ellis** | $500M commitment to a custom AI platform (same source) | M | **flag:** as #23 |
| 25 | **Fasken** | Hiring "AI enablement lawyers" and running 50% tech secondments, but partnered with Legora to build agents ([The Logic](https://thelogic.co/news/bay-street-law-partner-ai-roles/)) | L: buys rather than builds | **flag:** as #23 |
| 26 | **Osler**, AI workflow team | "AI workflow lawyer… designing and building AI agents" (same source) | L | **flag:** as #23 |
| 27 | **Gowling WLG**, AI, Innovation and Knowledge | Has a senior director of AI, innovation and knowledge, and a role rolling out automation tools (same source) | L | **flag:** as #23 |
| 28 | **Shared Services Canada**, GC AI / CANChat | CANChat is limited to Unclassified data; the Government of Canada is investing in Canadian-hosted LLMs ([SSC](https://www.canada.ca/en/shared-services/services/gc-ai/canchat.html), [SSC AI](https://www.canada.ca/en/shared-services/services/innovation/artificial-intelligence.html)). A Protected B tier would need ingestion inside the perimeter. The route in is PSPC's AI Source List ([CanadaBuys EN578-180001/B](https://canadabuys.canada.ca/en/tender-opportunities/tender-notice/pw-ee-017-34526); its listed closing date has passed, so check the current intake) | M | clear |

**Recommended order of attack:**
1. OEM prospects #1, #2, #4 and #5 first. One deal reaches many banks, and Apache-2.0 plus OEM rights is folio's clearest difference from Nutrient.
2. Then #12, #13 and #14, where the no-cloud rule is public and the documents are born-digital.
3. Treat the law firms (#23–27) as parked until the Mercor approval explicitly covers them.

### Segment signals from public issue trackers (not organisations)

These show the pain, but they were filed by individuals, so no people or employers are named. The right move is **not** to pitch in these threads. Answer only where folio directly fixes the reported problem, and disclose authorship.

| Signal | Link |
|---|---|
| Docling CPU-only conversion of a text-native 8-K went from 18 s to 80 s on 2 vCPUs after an upgrade; the reporter pinned an old version | [docling #4174](https://github.com/docling-project/docling/issues/4174) (Sept 2026) |
| docling-serve took more than 15 minutes to parse a 5-page PDF | [docling #2635](https://github.com/docling-project/docling/issues/2635) |
| "Docling too slow on CPU machine"; "How to make docling use less hardware" | [#1101](https://github.com/docling-project/docling/issues/1101), [#2877](https://github.com/docling-project/docling/issues/2877) |
| Behind a corporate firewall, models can't be downloaded; offline use | [docling #904](https://github.com/docling-project/docling/issues/904), [#232](https://github.com/docling-project/docling/issues/232), [docling-serve #69](https://github.com/docling-project/docling-serve/issues/69) |
| Marker on CPU makes the machine unresponsive | [marker #979](https://github.com/datalab-to/marker/issues/979) |
| Unstructured doesn't work offline | [unstructured #1080](https://github.com/Unstructured-IO/unstructured/issues/1080) (2023) |
| Relativity Server customers can't use aiR, and Server takes new matters only until 31 Dec 2027 | [Relativity](https://www.relativity.com/server-policy/) |

### Excluded or not pursued

- AI labs and big tech: OpenAI, Anthropic, Google/DeepMind, Meta, Microsoft, Amazon, Nvidia, xAI, Mistral, Cohere.
- H2O.ai: builds its own LLMs.
- Prem AI: trains its own models.
- AI-native finance and legal apps: Harvey, Legora, Hebbia, AlphaSense. They are plausibly Mercor-style buyers of expert data.
- Mercor competitors: Scale, Surge, Turing, Micro1, Invisible, Handshake, Labelbox, Andela.
- Reducto: a Mercor supplier and a competitor.
- Bulge-bracket investment banks, MBB consulting and the Big Four: Mercor's stated expansion targets.
- UK i.AI Redbox: sunset at the end of 2025 ([repo notice](https://github.com/i-dot-ai/redbox)).

## 3. Outreach templates

All three state the limits up front. Replace the `[…]` placeholders with evidence that is specific to the recipient. Never reuse a line from another prospect.

### 3a. Cold email (for OEM vendors; adapt for bank teams)

> **Subject:** Local PDF-to-Markdown for [Product]'s air-gapped installs, CPU-only, Apache-2.0
>
> Hi [team / first name if they published it for this purpose],
>
> [Product]'s docs say [specific public line, e.g. "parsing happens on the customer's hardware" / "air-gappable deployment"]. I build **folio**, an Apache-2.0 PDF-to-Markdown extractor that reads the PDF text layer with no models, no GPU and no network calls. On opendataloader-bench (200 real PDFs) it scored 0.92 overall at about 0.03 s/page on 4 CPU cores in my own harness run with the maintainers' scorer. Docling scored 0.88 at 0.76 s/page. I've submitted the result to the public leaderboard; it isn't verified by the maintainers yet.
>
> Where it's weak, so you don't have to find out yourself:
> - **No OCR.** Scanned or image-only pages produce nothing. folio flags them so you can send them to your existing OCR.
> - **Tables.** On the 40 documents I held out while tuning, the table score was 0.71 against 0.89 for the best open-source hybrid. Reading order and headings held up; tables did not.
> - Some commercial engines score higher on this benchmark with OCR enabled, at higher cost per page.
>
> If [Product] ships into banks or law firms that can't call a cloud parser, folio could sit in your ingestion step under Apache-2.0, with an optional paid pack (hardened container, table add-on, support SLA, redistribution terms).
>
> `pip install foliopdf && folio eval your_samples/` scores folio against Docling and OpenDataLoader on your own PDFs, entirely offline. Worth 20 minutes to compare on your hardest customer documents?
>
> [Name], [company, address]. Reply "no" and I won't write again. [Unsubscribe line for CASL/CAN-SPAM]

### 3b. GitHub Discussion / Show HN post

> **Show HN: folio: CPU-only PDF→Markdown at ~0.03 s/page, and where it loses**
>
> folio is a pure-Python PDF-to-Markdown extractor for **born-digital** PDFs. It reads pdfium's text layer and page geometry; there's no OCR, no layout model and no GPU, and the only dependency is pypdfium2. It's Apache-2.0.
>
> On opendataloader-bench (200 single-page real-world PDFs, scored with the upstream evaluator, unmodified) my run gets:
>
> | | Overall | Reading order | Table | Heading | s/page |
> |---|---|---|---|---|---|
> | folio (4-core Xeon) | 0.924 | 0.947 | 0.888 | 0.879 | 0.026 |
> | opendataloader-hybrid (stored, re-scored) | 0.907 | 0.934 | 0.928 | 0.821 | 0.463 |
> | docling (stored, re-scored) | 0.882 | 0.898 | 0.887 | 0.824 | 0.762 |
>
> The honest part:
> - I tuned on 160 documents and held out 40. On the held-out 40, folio is **below** opendataloader-hybrid overall (0.879 vs 0.897), and **tables are much worse** (0.71 vs 0.89).
> - The table detectors are geometric rules, and a table shape they haven't seen is simply missed.
> - Scanned PDFs produce nothing.
> - Nutrient reports 0.93 for its local Vision mode, which does OCR. It's proprietary and metered, but if you need scans or top table accuracy, compare it.
> - None of these numbers are maintainer-verified yet. The leaderboard PR is [link].
>
> Why it might still be useful: if you convert large volumes of text-native PDFs (filings, prospectuses, policies, contracts) on CPUs you already have, and especially if the documents can't leave your network, it's roughly 29× faster than Docling on this benchmark and deterministic (same bytes in, same Markdown out).
>
> `folio eval` compares folio with Docling and OpenDataLoader on your own PDFs, offline. The per-document diffs, experiment log and every rejected change are in the repo. I'd especially like examples where it breaks.

Etiquette: post once, reply to everything, and don't cross-post into competitors' issue trackers. The HN title should describe the project without superlatives.

### 3c. LinkedIn note

LinkedIn connection notes are short (about 200 characters on free accounts at last check; verify). Send the note to a public team member, never a scraped profile.

> Saw [Org]'s "[no external calls / no-cloud AI platform]" line. I built folio: CPU-only, offline PDF→Markdown, 0.03 s/page. No OCR, and tables are weaker. Would you compare it on your PDFs?

The follow-up message after they accept carries the same limits paragraph as the email.

## 4. Pricing page draft

### What Datalab does (verified 29 Sept 2026)

- **Code:** Marker's code is now **Apache-2.0**. Earlier versions were GPL, and the opendataloader-bench table still says GPL-3.0.
- **Model weights:** a modified OpenRAIL-M licence ([marker README](https://github.com/datalab-to/marker)).
- **The threshold is inconsistent across Datalab's own pages:**
  - Datalab's pricing page says the models are "free for research, personal projects, and startups with **under $2M** in funding or revenue" ([pricing](https://www.datalab.to/pricing)). The Chandra README says the same ($2M, "cannot be used competitively with our API").
  - The **Marker README and Marker's `MODEL_LICENSE` Attachment A say $5M.** The licence text restricts use if your organisation had "more than… $5,000,000 in gross revenue in the prior year" **or** "raised more than… $5,000,000 in total equity or debt funding". Clause 2(c) also bars any organisation offering a product that "competes with" Datalab.

  Folio should copy the structure and choose one number deliberately.
- **Paid tiers:** Team is $400/month with BAA/DPA available. Enterprise is custom, with on-prem VPC and air-gapped deployment. The self-serve on-prem licence allows 1–3 standalone instances ([datalab-on-prem](https://github.com/datalab-to/datalab-on-prem)).

**Structural difference.** folio's code is already Apache-2.0, and released versions can't be retro-gated. So the revenue-threshold clause can only apply to the **Enterprise pack**, which is closed-source add-ons and deliverables, and never to the core.

### Draft page

> # folio pricing
>
> **folio core is free and open source (Apache-2.0), forever.** CPU-only PDF→Markdown for born-digital PDFs. No OCR: image-only pages are detected and reported, not read.
>
> | | **Community** | **Team** | **Enterprise** | **OEM / Redistribution** |
> |---|---|---|---|---|
> | Price | $0 | **$6,000 / year** | **from $18,000 / year** | **from $15,000 / year** + per-customer fee |
> | Licence | Apache-2.0 core | Core + Enterprise pack, 1 production deployment (up to 64 vCPU) | Core + Enterprise pack, unlimited deployments within one corporate group | Right to embed the Enterprise pack in your product and ship it to your customers |
> | `folio eval` offline comparison CLI | ✓ | ✓ | ✓ | ✓ |
> | Table add-on (improved table detection) | | ✓ | ✓ | ✓ |
> | Signed container image, SBOM, reproducible builds | | ✓ | ✓ | ✓ |
> | Offline licence file: **no phone-home, no telemetry** | n/a (none in core) | ✓ | ✓ | ✓ |
> | Scan detection + routing hook to your OCR | | ✓ | ✓ | ✓ |
> | Audit log + determinism attestation (same input → byte-identical output) | | | ✓ | ✓ |
> | Model-risk documentation pack (method, tests, held-out results) for OSFI E-23 / SR 11-7 | | | ✓ | on request |
> | Annual accuracy review on up to 500 of your documents, run inside your network | | | ✓ | |
> | Support | GitHub issues | Email, 2 business days | Email + shared channel, 1 business day | Engineering channel |
> | IP indemnity | | | Capped at 12 months' fees | Negotiated |
>
> **Free Enterprise pack for small organisations and research.** The Enterprise pack is free for personal use, academic and non-commercial research, and organisations with **under US$2M in gross revenue in the prior 12 months *and* under US$2M in total equity or debt funding raised**. It is not available to organisations whose product competes with folio's paid offerings. Above either threshold, a Team, Enterprise or OEM licence is required for the Enterprise pack. The Apache-2.0 core is always free for everyone.
>
> **folio-on-your-documents diagnostic: $3,500 fixed.** We run `folio eval` on up to 200 of your PDFs inside your environment, against Docling, OpenDataLoader and your current tool, and deliver per-document scores and failure examples. The fee is credited in full against a first-year licence.
>
> **What folio does not do:** OCR, handwriting, images, formula recognition, or table accuracy at the level of the best VLM-based parsers. We will tell you if your documents need those.

**Pricing notes and open questions:**
- **These prices are hypotheses to test in the validation calls.** The anchors:
  - Datalab Team is $4,800/yr for the hosted API.
  - Nutrient Vision Pro is $2,990/yr for 100k pages a month.
  - Azure DI disconnected is about $8,640/yr at 100k pages a month (via the earlier report).
  - Datalab and Reducto on-prem are unpublished ("contact sales").
- A Team price near $6k sits above Nutrient's metered tier. That is only justified by OEM rights, air-gap packaging and support, because those are what the buyer is paying for.
- **Threshold choice.** $2M matches Datalab's current headline. $5M would match Marker's own licence text. Either way, apply it to revenue *and* funding, as Datalab does.
- **Indemnity.** For a solo founder it needs an incorporated entity, E&O/cyber insurance and a hard cap. Drop it from Team if insurance isn't in place.
- **No SOC 2.** Say so plainly. Self-hosted software with no telemetry reduces, but doesn't remove, vendor-risk questionnaires.
- **Open-core boundary.** If the table add-on is later upstreamed to the Apache core, the paid tiers lose their main feature. Decide the boundary once and write it into the README.

## 5. Validation plan

**Target:** 15 discovery calls within 30 days. Aim for 8 with OEM vendors and 7 with bank, regulator or legal teams. Plan on about 150 targeted touches, using the prospect list plus public-channel replies to the Show HN post.

### Ten discovery-call questions

1. Tell me about the last time a document-AI project was blocked or slowed by where documents were allowed to go. Who said no, and under which policy?
2. What's in the corpus?
   - The share that is text-native versus scanned or image-only.
   - The main document types.
   - Pages per month.
   - Languages.
3. What turns PDFs into text today (Docling, Unstructured OSS, Azure DI container, ABBYY, in-house), and what does it cost in compute, licences and engineer time?
4. Where the documents live, how many cores and GPUs can you actually get, and how long does it take to get more?
5. How do you judge parse quality today? Have you ever scored parsers on your own documents?
6. Which failure hurts most downstream: tables, reading order, headings or scanned pages? Show me one example.
7. What does a new component have to pass to reach production (security review, SBOM, no outbound traffic, model-risk validation under E-23 or SR 11-7), and how long did the last one take?
8. Whose budget pays for ingestion tooling, and have you paid for Datalab, Reducto, Unstructured, Azure DI containers or Nutrient before?
9. Suppose a parser was about 25× faster than Docling on CPU and comparable or better on text-native PDFs, but had no OCR and weaker tables. Where would it fit, and what would you do with the scanned pages?
10. *(For vendors.)* How do you ship a parser to customers today? Do licence terms such as no-OEM, revenue thresholds or telemetry ever block you? *(For end users.)* Would you pay $3,500 for a scored run on 200 of your documents inside your network, credited to a licence? If not, what would make it worth it?

### Signals that would kill the idea within 30 days

Decide on day 30. Any **two** of these kill folio Enterprise as a product. Keep folio as an open-source credibility asset and pivot to idea 1 (applied-ML sprints) or idea 4 (bookkeeper converter).

| # | Kill signal | Threshold |
|---|---|---|
| K1 | Nobody is feeling the pain | Fewer than 15 calls booked from about 150 targeted touches (under 10% conversion) |
| K2 | The fit conditions don't co-occur | Fewer than 4 of the first 15 calls have all three: a cloud-API block, **70% or more** born-digital pages, and a CPU or throughput problem |
| K3 | Free is good enough | More than half the qualified calls say Docling (possibly Red Hat-supported) or Nutrient Standard already meets their needs |
| K4 | folio isn't better on real documents | On the first 3 buyer sample sets, folio fails to beat Docling, OpenDataLoader and Nutrient Standard on at least 2 of 3 metrics, **or** trails the best on tables by more than 0.10 TEDS |
| K5 | No willingness to pay | Zero paid diagnostics or signed design-partner LOIs by day 30, **and** no OEM vendor willing to name a price |
| K6 | Procurement is out of reach | Two-thirds or more of interested buyers need SOC 2 Type II, insurance or a vendor size a solo founder can't reach within 6 months |
| K7 | Employer | Mercor or counsel declines, or limits the work to segments with no buyers. **This alone stops the effort.** |

**Signals to continue:**
- At least 2 paid diagnostics, or one OEM vendor asking for redistribution terms.
- At least 3 teams sending sample PDFs unprompted.
- folio wins K4 on at least 2 of 3 sample sets.

## 6. Competitive quick reference (verified 29 Sept 2026)

| Vendor | Price (list) | Self-host? | Note for folio |
|---|---|---|---|
| **Reducto** | Parse $10 per 1k pages on pay-as-you-go (Standard, $150 free credit). Growth and Enterprise are custom ([pricing](https://reducto.ai/pricing)) | **Enterprise tier only** (VPC and on-prem) | A Mercor supplier; never partner with or sell to it |
| **LlamaParse** (LlamaIndex) | $1.25 per 1k credits; parsing costs 1 / 3 / 10 / 45 credits per page for Fast / Cost-effective / Agentic / Agentic Plus, i.e. **$1.25–56.25 per 1k pages**. Plans are Free, Starter $50/mo, Pro $500/mo and Enterprise ([pricing](https://www.llamaindex.ai/pricing), [docs](https://developers.llamaindex.ai/llamaparse/general/pricing/)) | **Enterprise only**, as a private VPC or marketplace deployment. No air-gapped offering is stated | Cloud-first |
| **Unstructured** | 10k pages free, then **$0.015 per page**. Business plan is custom ([pricing](https://unstructured.io/pricing)) | Business plan: dedicated, in-VPC or bare metal. The OSS library is Apache-2.0 (v0.27.10, 2026-09-27) and markets an OSS path to air-gapped use ([Unstructured](https://unstructured.io/insights/on-prem-air-gapped-document-ai-regulated-industries)) | OSS `hi_res` scores 0.841 at 3.0 s/page on the benchmark |
| **Docling** (LF / IBM) | **Free, MIT** (v2.130.0, 2026-09-22) | Yes, fully local, "air-gapped environments" ([repo](https://github.com/docling-project/docling)). Red Hat AI ships hardened builds ([Red Hat](https://developers.redhat.com/articles/2026/06/30/scale-document-ingestion-docling-and-ray-openshift-ai)); support comes with Red Hat subscriptions (price not public). An aggregator reports an OpenShift operator aimed at banks (*unverified*, [IDP-Software](https://idp-software.com/vendors/docling/)) | The default choice. It wins on tables and OCR; folio wins on CPU speed |
| **Marker / Datalab** | API: Convert $4 per 1k (fast) or $10 per 1k (accurate); Team $400/mo; Enterprise custom ([pricing](https://www.datalab.to/pricing)). Code Apache-2.0 (marker-pdf 2.0.0, 2026-07-20); weights free under **$2M (pricing page) or $5M (Marker licence)** revenue or funding, with no competing use | Enterprise: "your infrastructure", VPC, **air-gapped**. Self-serve on-prem licence covers 1–3 instances on GPUs such as H100, L40S, A10 or T4 ([on-prem](https://github.com/datalab-to/datalab-on-prem)); price not public | The model to copy; GPU-bound |
| **OpenDataLoader PDF** (Hancom) | **Free, Apache-2.0** (v2.5.11, 2026-09-22). The hybrid, OCR, table, formula and chart add-ons are free. The Enterprise tier (PDF/UA accessibility export, tag editor) is "contact us" ([repo](https://github.com/opendataloader-project/opendataloader-pdf), [PR, 2026-03-13](https://www.prnewswire.com/news-releases/hancom-tops-open-source-pdf-benchmarks-with-opendataloader-pdf-v2-0--302713099.html)) | Yes, fully local, "no GPU required" for standard mode | Runs the benchmark folio tops, and leads the maintainer leaderboard at 0.907 |
| **Nutrient** PDF-to-Markdown *(added; the closest substitute)* | Standard: **free and unlimited for any organisation**, proprietary binary. Vision: $29–299/mo or $299–2,990/yr, pay-as-you-go $0.0036–0.007 per page, free only under $1M revenue **and** 20 staff ([pricing](https://www.nutrient.io/api/pricing/pdf-to-markdown/), [licence](https://github.com/PSPDFKit/pdf-to-markdown)) | Runs locally. Vision "may require connectivity to verify entitlements", the SDK "may also send… telemetry", and OEM use needs a separate agreement. Air-gapped use goes through the SDK's custom licence | Self-reported **0.89 Standard / 0.93 Vision** at 0.004 / 0.354 s/page ([benchmark](https://www.nutrient.io/blog/pdf-extraction-benchmark-opendataloader-bench/)) |

## 7. Uncertainties and risks to keep in view

1. **The benchmark claim is contested.**
   - folio's 0.9235 comes from its own harness and is not on the leaderboard.
   - Nutrient claims 0.93 with a local, OCR-capable mode.
   - On the held-out split, folio trails opendataloader-hybrid.

   Lead with speed, determinism and licensing, not "most accurate".
2. **Speed isn't unique either.** Nutrient Standard (0.004 s/page) and OpenDataLoader's non-hybrid mode (0.015 s/page) are faster than folio. folio's edge is accuracy *among* engines faster than 0.1 s/page (0.92 against 0.89 and 0.83), which is a narrower claim.
3. **Scans.** Every direct-finance prospect has some scanned input: NBC runs PaddleOCR, and Sparkassen agents read incoming paperwork. A scan-routing hook is the minimum; bundling an OCR partner may be necessary.
4. **Red Hat–backed Docling** gives bank procurement a supported, free default. folio has to be framed as complementary: a fast path for text-native pages in front of Docling.
5. **Unverified items.**
   - The NBC posting is known only from a search snippet.
   - The Docling OpenShift-operator-for-banks claim comes from an aggregator.
   - The Azure DI disconnected figure comes from the earlier report.
   - The LinkedIn note-length limit is from memory.
   - The AI Source List intake status is not current.
6. **Mercor.**
   - Law firms (#23–27) and any bank with an investment-banking arm (#13) sit next to Mercor's stated expansion thesis.
   - The OEM vendors (#1–4, #8–10) are "AI app developers", a group Mercor says it serves. There is no known link, but it can't be ruled out.
   - Clarence (#11) is built on Google technology.

   Clear the list with Mercor or counsel before contact.
