# Observability/log-reduction and relational AutoML markets (as of Sept 2026), with a view to tally / tremor / reldfs / TGB heuristics

Research date: 2026-09-27. Pricing was taken from vendor pages fetched on this date where possible. Where only third-party aggregators (Vendr, cubeapm, cloudpricecalculators, getlatka, etc.) were available, this is flagged as **[aggregator]**, meaning lower confidence. Old data is flagged **[stale]**.

## (A1) Who the paying competitors in log analytics and log reduction are, and what they charge and have raised

### Takeaway
List prices put log analytics at about $0.07–$0.50/GB ingest for the cloud-native players (Elastic, Grafana, Mezmo) versus roughly $1.8/GB-equivalent for Datadog's indexed logs and $150–$225 per GB/day/year for Splunk. That spread is what the pipeline/reduction category (Cribl, Edge Delta, Sawmills, Grepr, Observo, Tenzir, Mezmo) monetises. The category has proven itself: Cribl is at about $390M ARR. It has also consolidated fast in 2025–26, with Chronosphere going to Palo Alto Networks for $3.35B, Observe to Snowflake for about $1B, and Observo to SentinelOne for $225M.

### Cited Findings

**Destination platforms (the bills customers want to cut)**
- **Datadog Logs**, list prices: ingestion is $0.10/GB. Standard indexing (15-day retention) is $1.70 per million events/month on an annual plan, or $2.55 on demand. Flex Logs storage is $0.05 per million events/month annual ($0.075 on demand), and Flex Starter is $0.60 per million events/month. Forwarding to custom destinations costs $0.25/GB per destination — [Datadog pricing](https://www.datadoghq.com/pricing/?product=log-management)
- Datadog Flex Logs do not support monitors or Watchdog Insights; only standard indexing gets full alerting and anomaly detection. Customers who push logs to cheap tiers therefore lose anomaly features — [Finout, Datadog pricing guide](https://www.finout.io/blog/datadog-pricing-explained) [aggregator]
- Datadog Q2 2026 revenue was $1.12B (+36% YoY), with about 4,720 customers above $100k ARR. Datadog disclosed reduced usage from its largest customer starting in Q3 2026 — [Datadog 10-Q Q2 FY2026, SEC](https://www.sec.gov/Archives/edgar/data/0001561550/000162828026054458/ddog-20260630.htm) (via search summary; I did not read the filing text directly)
- The price of Datadog Observability Pipelines was **not found** on the public pricing page (it is listed as a product without a price) — [Datadog pricing](https://www.datadoghq.com/pricing/?product=observability-pipelines)
- **Splunk Cloud**, ingest pricing: list is about $150–$225 per GB/day on an annual subscription, and 40–70% enterprise discounts are routine. Effective cost is about $1,000 per GB/day/yr at 50 GB/day, rising toward $1,620 at single-digit volumes. Workload (SVC) pricing runs about $55–75k per SVC per year — [SIEMCostCalculator](https://siemcostcalculator.com/splunk-pricing); [MonitoringCost](https://monitoringcost.com/splunk-pricing) [aggregator; Splunk does not publish list prices, see [Splunk ingest pricing page](https://www.splunk.com/en_us/products/pricing/ingest-pricing.html)]
- **Elastic Observability Serverless**: Logs Essentials is $0.07/GB ingested and $0.017/GB retained per month. Complete is $0.09/GB ingested and $0.019/GB retained. Billing is on uncompressed volume after the ingest pipeline — [Elastic serverless observability pricing](https://www.elastic.co/pricing/serverless-observability); [Elastic billing docs](https://www.elastic.co/docs/deploy-manage/cloud-organization/billing/elastic-observability-billing-dimensions)
- **Grafana Cloud Logs (Loki)**:
  - Free tier: 50 GB/month with 14-day retention.
  - Pro: $19/month base including 50 GB, then from $0.05/GB process, $0.40/GB write and $0.10/GB retain, with 30-day retention.
  - Enterprise: minimum commit of $25,000/year — [Grafana pricing](https://grafana.com/pricing/)
- **Grafana Adaptive Logs** is free on all tiers. It groups log lines into patterns, checks which patterns were queried in the last 15 days, and recommends drop rates. Grafana claims up to 50% cost reduction. Dropped data reduces *written* volume but not *processed* volume — [Grafana pricing](https://grafana.com/pricing/); [Grafana Adaptive Logs intro](https://grafana.com/docs/grafana-cloud/observe-and-act/adaptive-telemetry/adaptive-logs/introduction/)
- **Mezmo** (ex-LogDNA): contract pricing is $0.20/GB ingested plus $0.20/GB retained per month, which Mezmo says is about 90% below its old $1.80/GB. Self-serve plans start at $10/month, with $0.80–$1.80/GB depending on 3–30 day retention — [APMdigest](https://www.apmdigest.com/mezmo-introduces-transparent-straightforward-pricing); [Mezmo pricing](https://www.mezmo.com/pricing)
- **Chronosphere**: Palo Alto Networks agreed to buy it for $3.35B. The deal closed on January 29, 2026, with purchase consideration of about $3.0B ($2,842M cash plus $109M of replacement awards). Chronosphere had more than $160M ARR at the end of September 2025. It is now folded into Cortex AgentiX — [PANW press release](https://www.paloaltonetworks.com/company/press/2025/palo-alto-networks-to-acquire-chronosphere--next-gen-observability-leader--for-the-ai-era); [PANW 10-Q FY2026](https://www.sec.gov/Archives/edgar/data/1327567/000132756726000005/panw-20260131.htm); [Constellation Research](https://www.constellationr.com/insights/news/palo-alto-networks-acquires-chronosphere-335-billion-reports-strong-q1). I found no current public Chronosphere price list.
- **Observe Inc.**: Snowflake acquired it for about $1B as reported. Snowflake's 10-Q gives preliminary purchase consideration at fair value of $595.8M, closed early February 2026 — [DevOps.com](https://devops.com/snowflake-plans-1b-acquisition-of-observe-to-expand-ai-powered-observability/); [Snowflake 10-K FY2026](https://www.sec.gov/Archives/edgar/data/1640147/000164014726000008/snow-20260131.htm). I found no current Observe price list.
- Total observability market: about $28.5B in 2025, heading for about $34.1B by end of 2026. Per Gartner (as cited), 36% of enterprise clients spend more than $1M/yr on observability and 4% spend more than $10M. 84% of users report struggling with cost — [Augment Code summary citing Gartner/Elastic](https://www.augmentcode.com/tools/best-observability-platforms) [aggregator of analyst figures; primary Gartner doc not accessed]

**Pipeline / reduction vendors**
- **Cribl**:
  - Founded July 2018 by three ex-Splunk people (Clint Sharp, Ledion and Dritan Bitincka) — [Wikipedia](https://en.wikipedia.org/wiki/Cribl.io)
  - ARR: $117M at end of 2023, $200M at end of 2024, $305M at end of 2025, and about $390M in August 2026 (Sacra estimate).
  - Funding: about $600M raised in total. The last priced round was a $319M Series E at a $3.5B valuation (Aug 2024).
  - Customers: 43 of the Fortune 100 and about 25% of the Fortune 500 — [Sacra](https://sacra.com/c/cribl/); [Cribl $300M ARR press](https://cribl.io/news/cribl-surpasses-usd300-million-in-arr-powering-the-essential-infrastructure/); [Cribl Series E](https://cribl.io/news/cribl-announces-319m-series-e/)
- **Cribl Stream pricing**:
  - Free: up to 1 TB/day with community support.
  - Standard: up to 5 TB/day, contact sales.
  - Enterprise: unlimited volume.
  - Cloud ingest: Enterprise is 0.32 credits/GB on Cribl-managed workers or 0.26 on hybrid workers; Standard is 0.27 credits/GB. 1 credit = $1 — [Cribl Stream pricing](https://cribl.io/pricing/stream/); [Cribl cloud pricing blog](https://cribl.io/blog/cribl-cloud-pricing/)
- **Edge Delta**: raised a $63M Series B in May 2022 led by Quiet Capital, for $81M total **[stale: no newer round found]** — [Edge Delta press](https://edgedelta.com/company/blog/series-b-announcement)
- **Edge Delta pricing**: pipeline throughput became *free* on April 8, 2026. Customers now pay only for stored data and AI tokens. Before that it was about $0.12/GB for pipelines and $0.20/GB for log search — [APMdigest](https://www.apmdigest.com/edge-delta-makes-all-telemetry-pipelines-data-throughput-limitless-and-free); [ITDigest](https://itdigest.com/cloud-computing-mobility/big-data/edge-delta-eliminates-data-throughput-costs-to-accelerate-ai-driven-observability-adoption/)
- **Grepr**:
  - Founded 2023 by Jad Naous in San Francisco. Raised about $18.2M, with the latest round a seed on Jan 22, 2025. Investors are a16z, Boldstart and E14 — [Tracxn](https://tracxn.com/d/companies/grepr/__rtSg_LVqfOTDRIsKi1QMyhr2OudSZCaqk7Qku2qbgvE/funding-and-investors); [PitchBook](https://pitchbook.com/profiles/company/601862-23)
  - Pricing: charges for compute units plus SaaS ingest volume plus data-lake query volume. There are no per-seat or per-host fees, and it explicitly does not charge a share of savings. No public $/GB. Self-serve signup is free.
  - Claims: "90% or more" volume reduction, with case studies of FOSSA at 95% and Goldsky at a 96% cut in Datadog cost — [Grepr FAQ](https://www.grepr.ai/faq)
- **Sawmills**: $10M seed in Feb 2025 led by Team8, with Mayfield and Alumni Ventures. Founders are ex-New Relic/CloudBees/Tricentis. Built on the OTel Collector — [SiliconANGLE](https://siliconangle.com/2025/02/19/sawmills-raises-10m-cut-observability-data-costs-ai/). Pricing **starts at $2,500/month on an annual commitment, scaled by ingest** — [Sawmills pricing](https://www.sawmills.ai/pricing)
- **Observo AI**: SentinelOne announced the acquisition for about $225M in Sept 2025. Observo was a 42-person company founded in 2022 with a $15M seed (Felicis, Lightspeed) — [SentinelOne press](https://www.sentinelone.com/press/sentinelone-to-acquire-observo-ai-to-revolutionize-siem-and-security-operations/); [Dark Reading](https://www.darkreading.com/cybersecurity-operations/sentinelone-acquire-observo-ai)
- **Tenzir** (Hamburg, open-source security data pipelines): about $5.9M raised, including a €3M seed (G+D Ventures, eCAPITAL). The Community edition is free until aggregate ingress exceeds 1 TB/day — [Tenzir pricing](https://tenzir.com/pricing/); [Tracxn](https://tracxn.com/d/companies/tenzir/__jvu4XOGZZV7cgteJQrHvQxd_1lHSp_KdMr6JqHctUTE)
- Other named Cribl alternatives: Datadog Observability Pipelines, Splunk Edge Processor, Axoflow, Realm, NXLog, Bindplane, and open-source Vector (Rust) — [Last9 Cribl alternatives](https://last9.io/blog/cribl-alternatives/)
- Gartner Market Guide for Telemetry Pipelines (Sept 2025) predicts that 40% of log telemetry will go through a pipeline product by 2027, up from less than 20% in 2024. It also warns buyers not to spend "a dollar on pipelines to save a nickel" — [Cribl summary of Gartner guide](https://cribl.io/resources/rpt/understanding-the-importance-of-gartners-market-guide-for-telemetry-pipelines/); [Gartner doc listing](https://www.gartner.com/en/documents/6906466)

### Inferences
- **Worked cost example (my own arithmetic from the Datadog list prices above).** Datadog 15-day indexed logs at about 1 KB/event come to roughly $0.10 + $1.70 ≈ $1.80/GB-equivalent per month. That is 20–25x Elastic Serverless ingest ($0.07–0.09/GB). The size of this gap explains why pipelines sell.
- Pipeline pricing is converging downward: Cribl at $0.26–0.32/GB, Edge Delta's throughput now $0, and Grafana Adaptive Logs free. Selling a *stand-alone* reduction product priced per GB is now much harder than in 2021–23.

### Gaps
- There is no public $/GB for Grepr, Datadog Observability Pipelines, Chronosphere (post-acquisition) or Observe (post-acquisition).
- Splunk list prices come only from aggregators.
- Edge Delta may have raised after 2022, but I found no source.
- I did not check Axoflow, Bindplane, Realm or Databahn funding.

## (A2) Is a "log template clustering to cut ingestion volume" product viable?

### Takeaway
The technique works and is proven: Loki uses Drain, Grafana Adaptive Logs does pattern-based drop recommendations, Datadog has Log Patterns, and OpenTelemetry accepted a Drain processor in 2026. That same proof is the problem: template clustering is becoming a **free, commodity feature** inside every platform and the OTel Collector. It is not a stand-alone product. Grepr and Sawmills sell a workflow (safe drop and aggregate, a data lake with rehydration, savings reports) on top of it, not the parser. For tally, the realistic routes are:
- upstream into the OTel/Vector ecosystem for credibility, or
- win on parse accuracy, throughput or CPU cost inside someone else's pipeline, or
- a services/consulting wedge ("cut your Datadog bill 50% in 30 days").

### Cited Findings
- Grafana Loki ships a Drain-based pattern ingester (`pkg/pattern/drain`) as a first-class component since Loki 3.0 — [search summary citing Loki/OTel discussion](https://github.com/open-telemetry/opentelemetry-collector-contrib/issues/47235)
- The OpenTelemetry Collector-contrib issue #47235, "processor/drain", was opened March 30, 2026 and is marked **Accepted Component** with two sponsors. It annotates logs with a `log.record.template` so operators can write durable filter rules at the edge. It uses the MIT-licensed `go-drain3` port. Snapshot persistence and multi-instance sync were deferred — [OTel issue #47235](https://github.com/open-telemetry/opentelemetry-collector-contrib/issues/47235)
- ClickHouse has an open issue asking for built-in log-mining (pattern extraction) functions — [ClickHouse #77009](https://github.com/ClickHouse/ClickHouse/issues/77009)
- IBM's Drain3 is used in production for IBM Cloud network syslog via Kafka — [IBM Developer](https://developer.ibm.com/blogs/how-mining-log-templates-can-help-ai-ops-in-cloud-scale-data-centers/); [logpai/Drain3](https://github.com/logpai/Drain3)
- Datadog Log Patterns clusters similar messages into patterns with variable slots — [search summary](https://github.com/logpai/Drain3) (Datadog docs not fetched directly)
- Grafana Adaptive Logs, free, is the closest "template clustering → drop recommendations" product — [Grafana Adaptive Logs](https://grafana.com/docs/grafana-cloud/observe-and-act/adaptive-telemetry/adaptive-logs/introduction/)
- **What Cribl and Grepr charge:**
  - Cribl: 0.26–0.32 credits ($) per GB for cloud ingest, and free up to 1 TB/day self-managed — [Cribl pricing](https://cribl.io/pricing/stream/)
  - Grepr: compute units, ingest and query, with no public rate — [Grepr FAQ](https://www.grepr.ai/faq)
  - Sawmills: from $2,500/month annual — [Sawmills pricing](https://www.sawmills.ai/pricing)
- Cribl positions itself as cutting Splunk spend by 30–90% — [Sacra](https://sacra.com/c/cribl/). Third parties typically report 40–70% filtering of low-value logs — [Last9](https://last9.io/blog/cribl-alternatives/) [aggregator]
- Exits for small pipeline startups: Observo reached $225M within about 3 years of founding on $15M raised — [SentinelOne](https://www.sentinelone.com/press/sentinelone-to-acquire-observo-ai-to-revolutionize-siem-and-security-operations/). This suggests security vendors will buy pipeline teams that have traction.

### Inferences
- **Don't build:** a head-on "we parse better than Drain" SaaS. Customers don't buy parser accuracy. They buy $ saved, with no lost alerts. The accuracy gap between tally and Drain on Loghub-2.0 will not show up in a sales conversation unless it turns into fewer false "drop this" recommendations or more stable templates across deploys.
- **Plausible wedges for tally:**
  1. Contribute a tally-based processor (or benchmark it against go-drain3) to the OTel Collector or Vector. This is credibility-building, not revenue.
  2. License or embed it into a pipeline vendor. The acquirer universe includes SentinelOne/Observo, PANW/Chronosphere, Snowflake/Observe and CrowdStrike, who have all bought pipeline or observability companies.
  3. An open-source "Datadog/Splunk bill audit" CLI that reads a log sample, clusters templates, and shows the $ per template joined to query usage. This is a lead magnet for a services offer.
  4. Security and SIEM logs, where Splunk-style $/GB/day is highest and Tenzir and Observo play.
- A solo founder can win pilots at the SMB end, where Sawmills' $2.5k/month floor suggests willingness to pay. But enterprises expect SOC2, 24x7 support and an agent footprint, and that is where Cribl dominates.

### Gaps
- I found no pricing data proving what share of observability spend buyers will pay for reduction; Grepr explicitly rejects savings-share pricing.
- Datadog's own Log Patterns / Observability Pipelines pricing was not confirmed.

## (A3) What the anomaly-detection tooling market looks like (Anodot, Datadog Watchdog, open source)

### Takeaway
Stand-alone time-series anomaly detection is a **shrinking, bundled** category:
- Anodot was absorbed by Glassbox (Nov 2025, terms undisclosed).
- Datadog bundles Watchdog and anomaly monitors into Infrastructure Enterprise and indexed logs.
- Snowflake ships anomaly detection as a SQL ML function billed as warehouse compute.
- Open source (PyOD, Merlion, Anomstack) covers most algorithms for free.

tremor's benchmark strength is most useful as an embedded component or as consulting credibility, not as a SaaS.

### Cited Findings
- Glassbox announced the acquisition of Anodot (founded 2014) on Nov 4, 2025, with terms not disclosed — [Glassbox press](https://www.glassbox.com/news/glassbox-anodot-acquisition/); [Finovate](https://finovate.com/glassbox-acquires-business-monitoring-and-analytics-specialist-anodot/). Anodot's recent product focus had shifted to cloud cost management and MSPs — [Anodot MSP page](https://www.anodot.com/cloud-cost-management/msp/multi-cloud-visibility-and-reporting/)
- Datadog: Watchdog automated insights and ML-based anomaly alerts are features of the Infrastructure Pro/Enterprise tiers, not separately priced — [Datadog pricing page](https://www.datadoghq.com/pricing/?product=observability-pipelines). Flex Logs lose Watchdog Insights — [Finout](https://www.finout.io/blog/datadog-pricing-explained) [aggregator]
- Snowflake ML Functions provide Anomaly Detection and Classification in SQL, billed as warehouse compute plus model storage, with no per-function fee — [Snowflake anomaly detection docs](https://docs.snowflake.com/en/user-guide/ml-functions/anomaly-detection); [Snowflake classification docs](https://docs.snowflake.com/en/user-guide/ml-functions/classification)
- Open source:
  - PyOD: 60+ detectors and more than 46M downloads, now with "ADEngine" orchestration and an agentic workflow — [PyOD GitHub](https://github.com/yzhao062/pyod)
  - Salesforce Merlion: uni- and multivariate TS anomaly detection — [Merlion](https://github.com/salesforce/Merlion)
  - Anomstack: an open-source monitoring platform on PyOD with optional LLM explanations — [Anomstack](https://andrewm4894.github.io/anomstack/)
  - Curated list of tools — [awesome-TS-anomaly-detection](https://github.com/rob-med/awesome-TS-anomaly-detection)
- Gartner's Market Guide for AI SRE Tooling (Jan 2026) projects 85% of enterprises will use AI SRE tooling by 2029, up from less than 5% in 2025 — [Augment Code, citing Gartner](https://www.augmentcode.com/tools/best-observability-platforms) [aggregator]

### Inferences
- The live money in "anomaly detection" in 2026 is flowing into **AI SRE / incident-investigation agents** (per the Gartner framing), not classic TS detectors. Accurate, cheap CPU anomaly scores from tremor could be a *feature* those agents call, which again points to B2B embedding or OSS.
- Business-metric anomaly detection (Anodot's original market: revenue and KPI drops) is a buyer persona (data/analytics teams) distinct from SRE, and it overlaps with dbt/Snowflake data-observability tools (Monte Carlo, Elementary). I did not research their pricing.

### Gaps
- I found no public Anodot or Glassbox pricing.
- I found no Datadog Watchdog add-on price.
- I did not research data-observability vendor pricing (Monte Carlo, Elementary, Bigeye).

## (B1) Relational/tabular AutoML and predictive modelling: the landscape (Kumo, DataRobot, H2O, Featuretools/Alteryx, getML, Snowflake/Databricks)

### Takeaway
The flagship "predictive queries on relational data" company, Kumo (Jure Leskovec's startup; Leskovec also leads the RelBench/PyG work), was **acquired by Nvidia in June 2026 (reported at more than $400M)**. kumo.ai/pricing now 301-redirects to Nvidia docs for "NVIDIA Kumo Relational", served as a NIM. Separately, SAP bought Prior Labs (TabPFN) in May–July 2026 with a commitment of more than €1B.

So relational and tabular foundation models are being absorbed by platform giants. That validates the space. It also means the leading commercial alternatives are now bundled into the Nvidia, SAP and Snowflake ecosystems, and legacy AutoML (DataRobot, H2O) sells at $60k–$1M+ per year enterprise contracts.

### Cited Findings
- **Kumo**:
  - Acquired by Nvidia and reported by Fortune on June 3, 2026. The price was not disclosed by Nvidia; The Information reported "more than $400M".
  - Kumo had raised about $37M across two 2022 rounds, including from Sequoia. Customers included DoorDash, Reddit and Sainsbury's. All three co-founders (Vanja Josifovski, Hema Raghavan, Jure Leskovec) moved to Nvidia — [Fortune](https://fortune.com/2026/06/03/nvidia-snaps-up-kumo-ai-in-latest-acquisition/); [Yahoo Finance/Barron's](https://finance.yahoo.com/markets/stocks/articles/nvidia-acquires-kumo-ai-400-190441222.html); [Forbes](https://www.forbes.com/sites/janakirammsv/2026/06/10/nvidia-buys-kumo-ai-to-take-foundation-models-to-enterprise-data/)
- `kumo.ai/pricing/` now redirects to `docs.nvidia.com/sdgm/rfm/overview`: "Kumo Relational, a pre-trained relational foundation model" accessed through the `kumo-relational-client` Python package against an NVIDIA NIM endpoint. No pricing is published — [NVIDIA Kumo Relational docs](https://docs.nvidia.com/sdgm/rfm/overview) (redirect observed 2026-09-27)
- Before the acquisition: Kumo was a Snowflake Native App payable with Snowflake credits, with a 30-day trial. It was sold as enterprise contracts by data volume, prediction throughput and deployment surface. KumoRFM had a developer tier but no public price card — [Kumo Snowflake native app](https://kumo.ai/company/news/snowflake-kumo-native-app/); [NeuronFeed](https://neuronfeed.com/startups/kumo-ai) [aggregator]. Getlatka estimated about $11M ARR in 2024 — [Getlatka](https://getlatka.com/companies/kumoai) [aggregator, low confidence]
- **Prior Labs (TabPFN)**: €9M pre-seed Feb 2025 (Balderton). SAP announced the acquisition on May 4, 2026 and closed it on July 17, 2026, with more than €1B of committed investment through 2030 — [TNW](https://thenextweb.com/news/sap-prior-labs-acquisition-tabular-foundation-model); [EU-Startups](https://www.eu-startups.com/2026/07/germanys-prior-labs-raises-e1-billion-and-exits-to-sap-18-months-after-being-founded/)
- **DataRobot** (quote-based) [aggregator]:
  - By tier: Essentials about $75k/yr, Business Critical about $150k/yr, Enterprise $300k+ (commonly $500k–$1M+).
  - By customer size: small-enterprise contracts from about $100k/yr; mid-market $250k–$500k.
  - Priced by edition, named seats and consumption credits — [Vendr](https://www.vendr.com/marketplace/datarobot); [cloudpricecalculators](https://cloudpricecalculators.com/datarobot-calculator/)
- **H2O Driverless AI** (custom quotes) [aggregator]:
  - A small team on 2–3 nodes with 5–10 users pays about $60k–$120k/yr plus compute.
  - 30 users with MLOps pay about $250k–$550k/yr.
  - The overall range runs from under $50k to more than $1M — [cloudpricecalculators H2O](https://cloudpricecalculators.com/h2o-ai-calculator/)
- **Featuretools → Alteryx**: Feature Labs, an MIT spin-out and maker of open-source Featuretools (Deep Feature Synthesis), was acquired by Alteryx in October 2019 with undisclosed terms — [TechCrunch](https://techcrunch.com/2019/10/04/alteryx-acquires-machine-learning-startup-feature-labs/); [Alteryx IR](https://investor.alteryx.com/news-and-events/press-releases/press-release-details/2019/Alteryx-Acquires-Feature-Labs-to-Advance-Machine-Learning-for-the-Enterprise/)
- **getML**: open-core. Community edition on GitHub. The relational feature-learning algorithms (Multirel, Relboost, RelMT) are Enterprise-only. Enterprise pricing is not published ("contact us") — [getML feature learning docs](https://getml.com/latest/reference/feature_learning/); [getml-community GitHub](https://github.com/getml/getml-community)
- **Pecan AI** (no-code predictive analytics for business teams):
  - Raised $116M in total, the last round a $66M Series C in 2022 [stale].
  - Est. $8.6M ARR in 2025 [aggregator].
  - Pricing: Starter about $760/month (2 prediction batches/month, 500M rows); Team about $1,400/month (10 batches, 2B rows), billed annually — [Getlatka](https://getlatka.com/companies/pecan.ai); [Pecan pricing](https://www.pecan.ai/pricing/) (figures via search summary, some sources say from $950/month)
- **Snowflake**: Classification and Anomaly Detection ML Functions run in SQL and are billed as warehouse compute — [Snowflake classification docs](https://docs.snowflake.com/en/user-guide/ml-functions/classification). Snowflake also integrated KumoRFM into Snowflake Intelligence before the acquisition — [Kumo news](https://kumo.ai/company/news/powering-predictions-in-snowflake-intelligence-with-kumorfm/)
- **Databricks AutoML** (`databricks.automl.classify`) is still documented. A Nov 2025 community thread titled "AutoML Deprecation?" exists, but I could not confirm its status — [Databricks AutoML API](https://docs.databricks.com/aws/en/machine-learning/automl/automl-api-reference); [Databricks community](https://community.databricks.com/t5/machine-learning/automl/td-p/35469)
- **Continual** ("AutoML for the modern data stack/dbt", $4M seed Dec 2021) was the earliest pure "predictive layer over your warehouse" startup. I found no evidence of later rounds; its current status is unconfirmed — [BusinessWire](https://www.businesswire.com/news/home/20211213006045/en/Continual-Launches-With-4-Million-in-Seed-to-Bring-AI-to-the-Modern-Data-Stack%C2%A0); [TechCrunch](https://techcrunch.com/2021/12/16/continual-raises-4m-for-its-ai-powered-data-platform/embed/)

### Inferences
- reldfs (automated relational feature synthesis plus LightGBM, 4th on RelBench, beating GNN baselines) is technically in the same class as Featuretools/getML: a CPU, explainable, cheap approach. Its commercial pitch would be "Kumo-class accuracy without a GPU foundation model, runs in your warehouse, and you own the model". That pitch is sharper now that Kumo is inside Nvidia (NIM/GPU lock-in) and TabPFN is inside SAP.
- The "predictive query over your warehouse" **product** category has a weak stand-alone record:
  - Continual stayed small (status unconfirmed).
  - Pecan raised $116M for an estimated about $8.6M ARR.
  - Kumo exited at about 11x capital raised but with modest reported ARR.

  The strategic buyers pay for the *team and model*, not the revenue.
- The warehouses (Snowflake ML Functions, Databricks AutoML, and Nvidia/Kumo via NIM) are commoditising "basic churn classifier in SQL".

### Gaps
- There is no public Kumo price card (before or after the acquisition).
- DataRobot and H2O figures come only from aggregators.
- Databricks AutoML deprecation is unconfirmed.
- The getML Enterprise price is unknown.
- I did not research Google BigQuery ML or AWS SageMaker Canvas pricing.

## (B2) What mid-market companies pay for churn, fraud and propensity models, whether there is demand for "predictive query over warehouse", and what consulting costs

### Takeaway
Mid-market buyers either pay for:
- a self-serve tool at about $750–$2,500/month (Pecan-style), or
- $5k–$100k consulting projects at about $120–$300/hr.

Enterprise AutoML platforms start around $60–100k/yr. For a solo founder, the fastest revenue is a **productised service**: fixed-price "churn/propensity model on your Snowflake/BigQuery in 2–4 weeks" using reldfs. It can later be packaged as a warehouse-native app.

### Cited Findings
- Freelance ML engineer rates:
  - Experienced freelancers: about $118–$195/hr in 2026.
  - Seniors: $150–$240/hr.
  - Specialist/PhD: $250–$500/hr — [goLance](https://golance.com/hiring/best-freelance-machine-learning-engineers-hourly-rate) [aggregator]
- AI consultant rates: average $150–$300/hr. Solo experts charge $80–$200, boutiques $150–$300, and Big 4 $300–$600 — [nicolalazzari.ai](https://nicolalazzari.ai/guides/ai-consultant-pricing-us); [groovyweb](https://www.groovyweb.co/blog/ai-consulting-rates-2026) [aggregator]
- The data science/ML consulting average is about $131/hr (2025) — [contractrates.fyi](https://www.contractrates.fyi/Data-Science-Machine-Learning-Consulting/hourly-rates)
- Project sizes: pilots and assessments $5k–$25k, mid-size builds $25k–$100k, production ML pipelines $120k–$500k+ — [Leanware](https://leanware.co/insights/how-much-does-an-ai-consultant-cost); [Opinosis Analytics](https://www.opinosis-analytics.com/blog/machine-learning-consulting-rates/) [aggregator]
- Self-serve tool pricing: Pecan Starter about $760/month and Team about $1,400/month on annual billing — [Pecan pricing](https://www.pecan.ai/pricing/)
- Evidence of demand: Kumo named DoorDash, Reddit and Sainsbury's as customers, and pitched churn, recommendations, fraud and credit default from relational data — [Fortune](https://fortune.com/2026/06/03/nvidia-snaps-up-kumo-ai-in-latest-acquisition/). Snowflake built KumoRFM into Snowflake Intelligence — [Kumo news](https://kumo.ai/company/news/powering-predictions-in-snowflake-intelligence-with-kumorfm/)

### Inferences
- Mid-market churn and propensity budgets are about $20k–$100k per use case per year, whether spent as a project or a tool. Fraud is usually bought from specialised vendors (Sift, Sardine, etc.; not researched), so reldfs is weaker there.
- The predictive-query demand is real, but the *buyer* often wants an answer ("which customers will churn") rather than a platform. Consulting, or a "done-for-you" warehouse app, fits a solo founder better than competing with Nvidia/Kumo and Snowflake on platform.

### Gaps
- I found no hard survey of mid-market spend on churn or propensity specifically; the numbers above come from consulting-rate aggregators.

## (C) Which buyer personas have budget, how long sales cycles are, and open-source-to-company precedents

### Takeaway
- **Market A:** budget sits with platform engineering / SRE / observability leads, and increasingly with FinOps and the CISO for SIEM logs, because observability is a $1M+/yr line item at about a third of enterprises.
- **Market B:** budget sits with heads of data / analytics and growth/CRM owners.

Enterprise cycles are long and procurement-heavy. I found no hard sales-cycle data. The OSS-to-company precedents (Cribl's free tier, Featuretools → Alteryx, PyG/Stanford → Kumo → Nvidia, TabPFN → Prior Labs → SAP) show that the most common outcome for a strong OSS or benchmark asset in these markets is **acqui-hire or tuck-in M&A within 2–4 years**, not an IPO.

### Cited Findings
- Per Gartner (as cited), 36% of enterprise clients spend more than $1M/yr on observability. The Elastic 2026 survey finds 54% of IT decision-makers are asked to justify observability spend and 97% have hit unexpected overages — [Augment Code summary](https://www.augmentcode.com/tools/best-observability-platforms) [aggregator]
- The FinOps Foundation's State of FinOps 2026 finds 90% of practitioners now manage SaaS spend, up from 65% — [OneUptime blog](https://oneuptime.com/blog/post/2026-03-17-datadog-bill-shock-real-cost-observability-2026/view) [vendor blog, secondary]
- Security persona: Observo AI was bought to feed SIEM/SOC pipelines, and Tenzir targets security teams — [SentinelOne](https://www.sentinelone.com/press/sentinelone-to-acquire-observo-ai-to-revolutionize-siem-and-security-operations/); [Tenzir](https://tenzir.com/pricing/)
- **Cribl's GTM precedent**: the founders came from Splunk and started with LogStream, a "Cribl in the middle" product sitting in front of Splunk. It had a generous free tier: originally free up to 1 TB/day in the cloud, and for a period free up to 5 TB/day self-managed — [Cribl blog, free 5TB/day](https://cribl.io/blog/the-new-cribl-logstream-free-up-to-5tb-day/); [Cribl.Cloud free 1TB/day](https://cribl.io/blog/cribl-cloud-get-logstream-instantly-for-free-up-to-1tb-day/). Note that Cribl is *free-tier* proprietary, not OSS.
- **Featuretools → Alteryx (2019)**: open-source DFS library, MIT spin-out, undisclosed acquisition price — [TechCrunch](https://techcrunch.com/2019/10/04/alteryx-acquires-machine-learning-startup-feature-labs/)
- **PyG/RelBench → Kumo → Nvidia**: the Stanford academic lineage (Leskovec) became Kumo (2021/22), which raised $37M and exited to Nvidia (June 2026, reported at more than $400M) — [Fortune](https://fortune.com/2026/06/03/nvidia-snaps-up-kumo-ai-in-latest-acquisition/). Note: I did not independently confirm PyG's corporate ownership (it is widely known to be maintained by Kumo engineers).
- **TabPFN → Prior Labs → SAP**: an open tabular foundation model went to an SAP acquisition within 18 months — [TNW](https://thenextweb.com/news/sap-prior-labs-acquisition-tabular-foundation-model)
- **Drain/Loghub (logpai) → Drain3 (IBM) → Loki / OTel**: academic log parsing that became a free component inside commercial products — [logpai/Drain3](https://github.com/logpai/Drain3); [OTel #47235](https://github.com/open-telemetry/opentelemetry-collector-contrib/issues/47235)

### Inferences
- **Crowdedness, candidly:**
  - Market A (log reduction) is crowded and consolidating. Incumbents give template clustering away free (Grafana, Loki, soon OTel), and Cribl owns the enterprise pipeline with about $390M ARR and about $600M raised. A solo founder cannot out-sell Cribl. They *can*:
    1. become a known OSS/benchmark contributor (tally in OTel/Vector),
    2. sell bill-reduction services to SMB/mid-market Datadog users, or
    3. aim to be acqui-hired by a security or observability vendor that is filling a pipeline gap, following the Observo precedent of $225M on a $15M seed with 42 people.
  - Market B (relational AutoML) had its category leader and its tabular-FM leader both bought by giants in 2026. That leaves an open-source and CPU-cheap niche for reldfs, which beats GNN baselines without GPUs. The monetisation path is most credibly consulting or a productised service at first. Publishing a strong RelBench result plus an open-source library is the proven path to acquisition interest (Feature Labs, Prior Labs, Kumo).
- Sales cycles (no citation found): enterprise observability and AutoML deals typically involve procurement, security review and POCs, while SMB self-serve (Grafana Pro, Pecan Starter, Grepr signup) is fast. Treat any number here as unverified.
- TGB heuristics have no obvious direct buyer. Their value is as research credibility, or as a feature inside fraud/recommendation modelling.

### Gaps
- I found no sourced data on typical sales-cycle length for either market.
- I found no sourced data on Cribl's first-year revenue or its seed-stage GTM metrics.
- I did not confirm Kumo's revenue at exit or the post-acquisition product pricing.
- I did not research AWS, GCP or BigQuery ML offerings.
