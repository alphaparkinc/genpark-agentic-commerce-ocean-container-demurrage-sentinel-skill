# -*- coding: utf-8 -*-
"""Ocean Container Demurrage & Detention Sentinel for GenPark Agentic Commerce."""
import json
from typing import Dict, Any, List

class OceanContainerDemurrageDetentionSentinel:
    @staticmethod
    def track_demurrage_detention_accrual(vessel_discharge_epoch: int, current_epoch: int, port_free_days: int = 4, demurrage_daily_tier1_usd: float = 175.0, demurrage_daily_tier2_usd: float = 275.0) -> Dict[str, Any]:
        seconds_elapsed = max(0, current_epoch - vessel_discharge_epoch)
        days_on_dock = seconds_elapsed / 86400.0
        free_days_remaining = max(0.0, round(port_free_days - days_on_dock, 1))
        
        penal_days = max(0.0, days_on_dock - port_free_days)
        tier1_days = min(penal_days, 5.0)
        tier2_days = max(0.0, penal_days - 5.0)
        
        accrued_demurrage_usd = round((tier1_days * demurrage_daily_tier1_usd) + (tier2_days * demurrage_daily_tier2_usd), 2)
        
        status = "FREE_TIME_ACTIVE" if free_days_remaining > 0 else "ACCRUING_DEMURRAGE_PENALTIES"
        return {
            "days_on_terminal": round(days_on_dock, 1),
            "port_free_days_allowed": port_free_days,
            "free_days_remaining": free_days_remaining,
            "penal_days_overdue": round(penal_days, 1),
            "accrued_demurrage_usd": accrued_demurrage_usd,
            "status": status,
            "current_daily_burn_rate_usd": demurrage_daily_tier2_usd if tier2_days > 0 else (demurrage_daily_tier1_usd if penal_days > 0 else 0.0)
        }

    @staticmethod
    def recommend_urgent_drayage_evacuation_priority(container_fleet: List[Dict[str, Any]]) -> Dict[str, Any]:
        # Rank by highest daily burn rate and days overdue
        ranked = sorted(container_fleet, key=lambda c: (c.get("penal_days", 0), c.get("daily_burn_rate_usd", 0)), reverse=True)
        return {
            "total_containers_tracked": len(container_fleet),
            "evacuation_dispatch_queue": ranked,
            "action_order": "Dispatch chassis and pre-pull drayage drivers for top tier containers immediately."
        }
