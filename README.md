# Ocean Container Demurrage & Detention Free-Time Countdown Sentinel Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

Ocean container free time window countdown, port gate-in/gate-out turnaround, demurrage per-diem accrual curve, and chassis split fee audit. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `track_demurrage_detention_accrual`: Calculate daily demurrage and detention penal accruals once port or equipment free time expires.
- `recommend_urgent_drayage_evacuation_priority`: Rank active containers at port terminal by financial burn rate to dispatch emergency drayage truckers.

## 🚀 Installation & Usage
```bash
python -m genpark_agentic_commerce_ocean_container_demurrage_sentinel_skill.server --test
```
