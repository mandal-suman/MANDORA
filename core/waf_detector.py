import os
from wafw00f.main import WAFW00F


def _format_detection(entry):
    if isinstance(entry, dict):
        name = entry.get("name") or entry.get("WAF") or entry.get("waf_name") or entry.get("id")
        vendor = entry.get("manufacturer") or entry.get("vendor")
        reasons = entry.get("reason") or entry.get("evidence") or entry.get("detections")
        notes = []
        if vendor:
            notes.append(f"vendor={vendor}")
        if isinstance(reasons, (list, tuple)) and reasons:
            notes.append("signals=" + ", ".join(str(r) for r in reasons))
        elif reasons:
            notes.append(f"signal={reasons}")
        return (name or "Unknown"), notes

    if isinstance(entry, (list, tuple)) and entry:
        name = entry[0] if entry[0] else "Unknown"
        notes = []
        if len(entry) > 1 and isinstance(entry[1], dict):
            for key, value in entry[1].items():
                notes.append(f"{key}={value}")
        elif len(entry) > 1 and entry[1]:
            notes.append(str(entry[1]))
        return str(name), notes

    if isinstance(entry, str):
        return entry, []

    return "Unknown", []


def _normalize_results(raw_results):
    if not raw_results:
        return []
    if isinstance(raw_results, (list, tuple)):
        return list(raw_results)
    return [raw_results]


def _meaningful_name(name):
    if not name:
        return False
    lowered = name.lower().strip()
    if lowered.startswith("http"):
        return False
    if any(token in lowered for token in ("<script", "union select", "%3cscript", "sleep(", "../")):
        return False
    if len(name) > 120:
        return False
    return True


def _gather_candidates(waf, raw_results):
    ordered = []
    preferred_sources = [
        getattr(waf, "wafdetections", None),
        getattr(waf, "wafinfo", None),
        getattr(waf, "lastwaf", None),
    ]

    for source in preferred_sources:
        if not source:
            continue
        ordered.extend(_normalize_results(source))

    if not ordered:
        ordered.extend(_normalize_results(raw_results))

    return ordered


def detect_waf(target_url, output_folder):
    print("🔍 Running WAF detection...")
    detections = []
    try:
        waf = WAFW00F(target_url)
        raw_results = waf.identwaf(findall=True)
        if not raw_results:
            raw_results = waf.identwaf(findall=False)

        candidates = _gather_candidates(waf, raw_results)

        seen = set()
        for entry in candidates:
            if not entry:
                continue
            name, notes = _format_detection(entry)
            if not _meaningful_name(name):
                continue
            key = name.strip().lower()
            if key in seen:
                continue
            seen.add(key)
            detections.append((name.strip(), notes))
            if len(detections) >= 5:
                break

        if detections:
            print("🔒 WAF detected:")
            for name, notes in detections:
                details = f" - {name}"
                if notes:
                    details += " (" + "; ".join(notes) + ")"
                print(details)
        else:
            print("✅ No WAF detected (or not identifiable)")

        os.makedirs(output_folder, exist_ok=True)
        with open(os.path.join(output_folder, 'waf_detected.txt'), 'w') as file_handle:
            if detections:
                for name, notes in detections:
                    line = name
                    if notes:
                        line += " | " + "; ".join(notes)
                    file_handle.write(line + "\n")
            else:
                file_handle.write("No WAF Detected\n")

        return detections

    except KeyboardInterrupt:
        print("[!] WAF detection interrupted by user.")
        os.makedirs(output_folder, exist_ok=True)
        with open(os.path.join(output_folder, 'waf_detected.txt'), 'w') as file_handle:
            file_handle.write("WAF detection interrupted by user\n")
        raise

    except Exception as exc:
        print(f"❌ Error in WAF detection: {exc}")
        os.makedirs(output_folder, exist_ok=True)
        with open(os.path.join(output_folder, 'waf_detected.txt'), 'w') as file_handle:
            file_handle.write(f"Error detecting WAF: {exc}\n")
        return []
