#!/usr/bin/env python3
import json, os, sys, math
from datetime import datetime, timezone
from pathlib import Path

# ---- CONFIG via env ----
SIGNAL_NAME = os.getenv("SIGNAL_NAME", "Tank_Litres")
MAX_LITRES  = float(os.getenv("MAX_LITRES", "600"))
MF4_PATH    = Path(os.getenv("MF4_PATH", "input.mf4"))
DBC_PATH    = Path(os.getenv("DBC_PATH", "input.dbc"))
CAN_CH      = int(os.getenv("CAN_CHANNEL", "0"))  # 0/1
OUT_PATH    = Path("latest.json")
# ------------------------

def main():
    if not MF4_PATH.exists(): raise SystemExit("Missing MF4 file")
    if not DBC_PATH.exists(): raise SystemExit("Missing DBC file")

    from asammdf import MDF
    mapping = {"CAN": [(str(DBC_PATH), CAN_CH)]}
    decoded = MDF(str(MF4_PATH)).extract_bus_logging(mapping)

    # Try exact, then case-insensitive
    sig = None
    try:
        sig = decoded.get(SIGNAL_NAME)
    except Exception:
        pass
    if sig is None:
        names = [c.name for c in decoded.channels_db]
        t = SIGNAL_NAME.lower()
        for n in names:
            if n.lower() == t or t in n.lower():
                sig = decoded.get(n); break
    if sig is None:
        raise SystemExit(f"Signal '{SIGNAL_NAME}' not found")

    # last numeric
    samples = sig.samples
    val = next((float(x) for x in reversed(samples)
               if isinstance(x, (int,float)) and not (isinstance(x,float) and math.isnan(x))), None)
    if val is None: raise SystemExit("No numeric samples")

    litres = max(0.0, min(MAX_LITRES, val))
    payload = {"litres": round(litres,1),
               "timestamp": datetime.now(timezone.utc).isoformat()}
    OUT_PATH.write_text(json.dumps(payload, indent=2))
    print(f"Wrote {OUT_PATH}: {payload}")

if __name__ == "__main__":
    sys.exit(main())
