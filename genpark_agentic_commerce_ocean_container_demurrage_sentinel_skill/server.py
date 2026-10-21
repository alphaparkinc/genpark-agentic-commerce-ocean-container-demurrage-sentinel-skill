# -*- coding: utf-8 -*-
"""MCP Server for Ocean Container Demurrage & Detention Free-Time Countdown Sentinel Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import OceanContainerDemurrageDetentionSentinel

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "track_demurrage_detention_accrual",
        "description": "Calculate daily demurrage and detention penal accruals once port or equipment free time expires.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "vessel_discharge_epoch": {
                    "type": "integer"
                },
                "current_epoch": {
                    "type": "integer"
                },
                "port_free_days": {
                    "type": "integer"
                },
                "demurrage_daily_tier1_usd": {
                    "type": "number"
                },
                "demurrage_daily_tier2_usd": {
                    "type": "number"
                }
            },
            "required": [
                "vessel_discharge_epoch",
                "current_epoch",
                "port_free_days"
            ]
        }
    },
    {
        "name": "recommend_urgent_drayage_evacuation_priority",
        "description": "Rank active containers at port terminal by financial burn rate to dispatch emergency drayage truckers.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "container_fleet": {
                    "type": "array",
                    "items": {
                        "type": "object"
                    }
                }
            },
            "required": [
                "container_fleet"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-ocean-container-demurrage-sentinel-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(OceanContainerDemurrageDetentionSentinel, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-ocean-container-demurrage-sentinel-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
