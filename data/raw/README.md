# BusinessIntelligence.ai Prototype Dataset

Synthetic multi-source retail dataset for Accenture Innovation Challenge 2026,
Round 2 — Problem Track 3: BusinessIntelligence.ai.

Designed for:
- material KPI movement detection
- driver/contribution analysis
- evidence-backed narrative generation
- confidence/abstention
- action recommendations
- lineage and source-freshness reasoning

Intentional scenarios:
- 2026-02-20 to 2026-02-28: supply disruption
- 2026-03-01: spring promotion
- 2026-03-18: price increase with demand elasticity
- 2026-04-05 to 2026-04-12: Electronics stockout
- 2026-05-01: marketing budget cut
- 2026-05-20: new product launch
- 2026-06-15: summer promotion

Files:
- sales.csv — transaction-level sales
- marketing.csv — campaign/day/region performance
- inventory.csv — product/region/day inventory
- business_events.csv — contextual events
- kpi_dictionary.csv — KPI semantic contract
- source_metadata.csv — grain, refresh, owner, quality and security metadata

Approximate rows:
sales=161,847
marketing=3,620
inventory=21,720
