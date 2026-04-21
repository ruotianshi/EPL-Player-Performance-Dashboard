"""
body_map.py — SVG Human Body Map Generator
Uses string.replace() to inject data, avoiding f-string conflicts with CSS/JS braces.
"""

def get_injury_color(count: int, is_active: bool = False) -> str:
    if is_active:
        return "#FF1744"
    scale = ["#F5F5F5", "#FCE4EC", "#F48FB1", "#E91E63", "#C62828", "#880E4F"]
    return scale[min(count, 5)]


def prepare_injury_json(injury_df, player_id: str) -> str:
    import json
    df = injury_df[injury_df["player_id"] == player_id].copy()
    result = {}
    for part_key in df["body_part_key"].unique():
        part_df = df[df["body_part_key"] == part_key]
        records = []
        for _, row in part_df.iterrows():
            records.append({
                "date": str(row["injury_date"]),
                "type": str(row["injury_type"]),
                "sev": str(row["severity"]),
                "days": int(row["days_out"]),
            })
        is_active = bool(part_df["is_active"].any())
        result[part_key] = {
            "count": len(part_df),
            "records": sorted(records, key=lambda x: x["date"], reverse=True),
            "total_days": int(part_df["days_out"].sum()),
            "status": "🔴 Currently Injured" if is_active else "✅ Healthy",
        }
    return json.dumps(result)


def _get_part_attrs(part_key, injury_counts, active_parts, label):
    count = injury_counts.get(part_key, 0)
    is_active = part_key in active_parts
    fill = get_injury_color(count, is_active)
    css_class = "body-part active-injury" if is_active else "body-part"
    safe_label = label.replace("'", "\\'")
    mouse_enter = f"showTooltip(event,'{part_key}','{safe_label}')"
    mouse_move = "moveTooltip(event)"
    mouse_leave = "hideTooltip()"
    on_click = f"showDetail('{part_key}','{safe_label}')"
    return fill, css_class, mouse_enter, mouse_move, mouse_leave, on_click


def _build_anterior_svg(injury_counts, active_parts):
    def attrs(key, label):
        f, cl, me, mm, ml, oc = _get_part_attrs(key, injury_counts, active_parts, label)
        return f'fill="{f}" class="{cl}" onmouseenter="{me}" onmousemove="{mm}" onmouseleave="{ml}" onclick="{oc}"'

    lines = []
    lines.append('<svg viewBox="0 0 220 390" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-width:220px;display:block;margin:auto;">')
    lines.append(f'<ellipse cx="110" cy="30" rx="22" ry="26" {attrs("head","Head")}/>')
    lines.append(f'<rect x="100" y="54" width="20" height="14" rx="4" {attrs("neck","Neck / Cervical Region")}/>')
    lines.append(f'<path d="M78,68 L142,68 L148,120 L72,120 Z" {attrs("chest","Chest")}/>')
    lines.append(f'<path d="M76,122 L144,122 L140,165 L80,165 Z" {attrs("abdomen","Abdomen")}/>')
    lines.append(f'<ellipse cx="155" cy="80" rx="16" ry="14" {attrs("left_shoulder","Left Shoulder")}/>')
    lines.append(f'<ellipse cx="65" cy="80" rx="16" ry="14" {attrs("right_shoulder","Right Shoulder")}/>')
    lines.append(f'<rect x="148" y="94" width="20" height="36" rx="8" {attrs("left_upper_arm","Left Upper Arm")}/>')
    lines.append(f'<rect x="52" y="94" width="20" height="36" rx="8" {attrs("right_upper_arm","Right Upper Arm")}/>')
    lines.append(f'<ellipse cx="158" cy="136" rx="10" ry="8" {attrs("left_elbow","Left Elbow")}/>')
    lines.append(f'<ellipse cx="62" cy="136" rx="10" ry="8" {attrs("right_elbow","Right Elbow")}/>')
    lines.append(f'<rect x="150" y="146" width="18" height="34" rx="7" {attrs("left_forearm","Left Forearm")}/>')
    lines.append(f'<rect x="52" y="146" width="18" height="34" rx="7" {attrs("right_forearm","Right Forearm")}/>')
    lines.append(f'<ellipse cx="159" cy="190" rx="10" ry="12" {attrs("left_wrist","Left Wrist/Hand")}/>')
    lines.append(f'<ellipse cx="61" cy="190" rx="10" ry="12" {attrs("right_wrist","Right Wrist/Hand")}/>')
    lines.append(f'<path d="M110,165 L142,165 L138,185 L110,185 Z" {attrs("left_groin","Left Groin / Adductors")}/>')
    lines.append(f'<path d="M110,165 L78,165 L82,185 L110,185 Z" {attrs("right_groin","Right Groin / Adductors")}/>')
    lines.append(f'<path d="M111,187 L138,187 L136,255 L111,255 Z" {attrs("left_quad","Left Anterior Thigh")}/>')
    lines.append(f'<path d="M109,187 L82,187 L84,255 L109,255 Z" {attrs("right_quad","Right Anterior Thigh")}/>')
    lines.append(f'<ellipse cx="124" cy="262" rx="13" ry="10" {attrs("left_knee_front","Left Knee (Patella)")}/>')
    lines.append(f'<ellipse cx="96" cy="262" rx="13" ry="10" {attrs("right_knee_front","Right Knee (Patella)")}/>')
    lines.append(f'<rect x="114" y="274" width="20" height="52" rx="8" {attrs("left_shin","Left Shin / Tibia")}/>')
    lines.append(f'<rect x="86" y="274" width="20" height="52" rx="8" {attrs("right_shin","Right Shin / Tibia")}/>')
    lines.append(f'<ellipse cx="124" cy="333" rx="12" ry="9" {attrs("left_ankle_front","Left Ankle")}/>')
    lines.append(f'<ellipse cx="96" cy="333" rx="12" ry="9" {attrs("right_ankle_front","Right Ankle")}/>')
    lines.append('<ellipse cx="126" cy="350" rx="13" ry="7" class="body-part" fill="#EEEEEE" onmouseenter="showTooltip(event,\'\',\'Left Foot\')" onmousemove="moveTooltip(event)" onmouseleave="hideTooltip()"/>')
    lines.append('<ellipse cx="94" cy="350" rx="13" ry="7" class="body-part" fill="#EEEEEE" onmouseenter="showTooltip(event,\'\',\'Right Foot\')" onmousemove="moveTooltip(event)" onmouseleave="hideTooltip()"/>')
    lines.append('<text x="110" y="375" text-anchor="middle" font-size="11" fill="#9E9E9E" font-family="Segoe UI">ANTERIOR</text>')
    lines.append('</svg>')
    return "\n".join(lines)


def _build_posterior_svg(injury_counts, active_parts):
    def attrs(key, label):
        f, cl, me, mm, ml, oc = _get_part_attrs(key, injury_counts, active_parts, label)
        return f'fill="{f}" class="{cl}" onmouseenter="{me}" onmousemove="{mm}" onmouseleave="{ml}" onclick="{oc}"'

    lines = []
    lines.append('<svg viewBox="0 0 220 390" xmlns="http://www.w3.org/2000/svg" width="100%" style="max-width:220px;display:block;margin:auto;">')
    lines.append(f'<ellipse cx="110" cy="30" rx="22" ry="26" {attrs("head","Head (Posterior)")}/>')
    lines.append(f'<rect x="100" y="54" width="20" height="14" rx="4" {attrs("neck","Neck / Cervical Region")}/>')
    lines.append(f'<path d="M78,68 L142,68 L148,115 L72,115 Z" {attrs("upper_back","Upper Back / Trapezius")}/>')
    lines.append(f'<path d="M80,117 L140,117 L136,162 L84,162 Z" {attrs("lower_back","Lumbar Region")}/>')
    lines.append(f'<ellipse cx="155" cy="80" rx="16" ry="14" {attrs("left_shoulder","Left Shoulder")}/>')
    lines.append(f'<ellipse cx="65" cy="80" rx="16" ry="14" {attrs("right_shoulder","Right Shoulder")}/>')
    lines.append(f'<rect x="148" y="94" width="20" height="36" rx="8" {attrs("left_upper_arm","Left Upper Arm")}/>')
    lines.append(f'<rect x="52" y="94" width="20" height="36" rx="8" {attrs("right_upper_arm","Right Upper Arm")}/>')
    lines.append(f'<ellipse cx="158" cy="136" rx="10" ry="8" {attrs("left_elbow","Left Elbow")}/>')
    lines.append(f'<ellipse cx="62" cy="136" rx="10" ry="8" {attrs("right_elbow","Right Elbow")}/>')
    lines.append(f'<rect x="150" y="146" width="18" height="34" rx="7" {attrs("left_forearm","Left Forearm")}/>')
    lines.append(f'<rect x="52" y="146" width="18" height="34" rx="7" {attrs("right_forearm","Right Forearm")}/>')
    lines.append(f'<path d="M110,164 L138,164 L140,195 L110,195 Z" {attrs("left_glute","Left Gluteal")}/>')
    lines.append(f'<path d="M110,164 L82,164 L80,195 L110,195 Z" {attrs("right_glute","Right Gluteal")}/>')
    lines.append(f'<path d="M111,197 L138,197 L136,260 L111,260 Z" {attrs("left_hamstring","Left Hamstring")}/>')
    lines.append(f'<path d="M109,197 L82,197 L84,260 L109,260 Z" {attrs("right_hamstring","Right Hamstring")}/>')
    lines.append(f'<ellipse cx="124" cy="267" rx="13" ry="9" {attrs("left_knee_front","Left Knee")}/>')
    lines.append(f'<ellipse cx="96" cy="267" rx="13" ry="9" {attrs("right_knee_front","Right Knee")}/>')
    lines.append(f'<rect x="114" y="278" width="20" height="50" rx="8" {attrs("left_calf","Left Calf")}/>')
    lines.append(f'<rect x="86" y="278" width="20" height="50" rx="8" {attrs("right_calf","Right Calf")}/>')
    lines.append(f'<ellipse cx="124" cy="334" rx="10" ry="7" {attrs("left_achilles","Left Achilles Tendon")}/>')
    lines.append(f'<ellipse cx="96" cy="334" rx="10" ry="7" {attrs("right_achilles","Right Achilles Tendon")}/>')
    lines.append('<ellipse cx="126" cy="350" rx="13" ry="7" class="body-part" fill="#EEEEEE" onmouseenter="showTooltip(event,\'\',\'Left Foot\')" onmousemove="moveTooltip(event)" onmouseleave="hideTooltip()"/>')
    lines.append('<ellipse cx="94" cy="350" rx="13" ry="7" class="body-part" fill="#EEEEEE" onmouseenter="showTooltip(event,\'\',\'Right Foot\')" onmousemove="moveTooltip(event)" onmouseleave="hideTooltip()"/>')
    lines.append('<text x="110" y="375" text-anchor="middle" font-size="11" fill="#9E9E9E" font-family="Segoe UI">POSTERIOR</text>')
    lines.append('</svg>')
    return "\n".join(lines)


# CSS and JS as plain strings (no f-string, uses .format() with escaped braces)
_CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: transparent; font-family: 'Segoe UI', sans-serif; }

.body-part {
  cursor: pointer;
  transition: filter 0.2s, opacity 0.2s;
  stroke: #9E9E9E;
  stroke-width: 1.2;
}
.body-part:hover {
  filter: brightness(0.80) drop-shadow(0 0 5px rgba(0,0,0,0.4));
  opacity: 0.88;
}
@keyframes pulse {
  0%   { filter: brightness(1)   drop-shadow(0 0 2px #FF1744); }
  50%  { filter: brightness(1.3) drop-shadow(0 0 9px #FF1744); }
  100% { filter: brightness(1)   drop-shadow(0 0 2px #FF1744); }
}
.active-injury {
  animation: pulse 1.4s ease-in-out infinite;
  stroke: #FF1744 !important;
  stroke-width: 2 !important;
}
#tooltip {
  position: fixed; display: none;
  background: rgba(10,15,30,0.97);
  color: #fff;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 12px;
  pointer-events: none;
  z-index: 9999;
  max-width: 230px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.5);
  line-height: 1.7;
}
#tooltip .tt-title { font-size: 13px; font-weight: 700; color: #90CAF9; margin-bottom: 4px; }
#tooltip .tt-count { color: #FFCC02; }
#tooltip .tt-status { margin-top: 2px; color: #A5D6A7; }
#detail-panel {
  position: absolute; right: 0; top: 0;
  width: 290px;
  background: rgba(10,15,30,0.97);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: 10px;
  padding: 14px 16px;
  display: none;
  color: #E0E0E0;
  font-size: 12px;
  max-height: 480px;
  overflow-y: auto;
  z-index: 100;
}
#detail-panel h3 { color: #90CAF9; font-size: 14px; margin-bottom: 10px;
  border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 6px; }
#detail-panel table { width: 100%; border-collapse: collapse; }
#detail-panel th { color: #90CAF9; padding: 4px 5px; text-align: left; font-size: 11px; font-weight: 600; }
#detail-panel td { padding: 4px 5px; border-bottom: 1px solid rgba(255,255,255,0.06); font-size: 11px; }
#detail-panel .close-btn { float: right; cursor: pointer; color: #888; font-size: 18px; line-height: 1; }
#detail-panel .close-btn:hover { color: #fff; }
.stat-box { margin-top: 10px; padding: 8px 10px;
  background: rgba(255,255,255,0.05); border-radius: 7px; font-size: 12px; }
.wrapper { position: relative; display: inline-block; width: 100%; }
"""

_JS = """
const injuryData = INJURY_DATA_PLACEHOLDER;

function showTooltip(e, partKey, label) {
  const d = injuryData[partKey] || {count:0, records:[], status:'✅ Healthy'};
  document.getElementById('tt-title').textContent = label;
  document.getElementById('tt-count').textContent = 'Injury count: ' + d.count;
  document.getElementById('tt-status').textContent = d.status;
  const t = document.getElementById('tooltip');
  t.style.display = 'block';
  t.style.left = (e.clientX + 14) + 'px';
  t.style.top  = (e.clientY - 10) + 'px';
}
function moveTooltip(e) {
  const t = document.getElementById('tooltip');
  t.style.left = (e.clientX + 14) + 'px';
  t.style.top  = (e.clientY - 10) + 'px';
}
function hideTooltip() {
  document.getElementById('tooltip').style.display = 'none';
}
function showDetail(partKey, label) {
  const d = injuryData[partKey] || {count:0, records:[], status:'✅ Healthy', total_days:0};
  document.getElementById('panel-title').textContent = label;
  let html = '';
  if (d.count === 0) {
    html = '<p style="color:#888;padding:10px 0">No injury history recorded for this region.</p>';
  } else {
    html += '<table><tr><th>Date</th><th>Type</th><th>Severity</th><th>Days</th></tr>';
    d.records.forEach(function(r) {
      const sevColor = r.sev === 'Grade III' ? '#EF9A9A' : r.sev === 'Grade II' ? '#FFCC80' : '#E0E0E0';
      html += '<tr><td>' + r.date + '</td><td>' + r.type + '</td><td style="color:' + sevColor + '">' + r.sev + '</td><td>' + r.days + '</td></tr>';
    });
    html += '</table>';
    html += '<div class="stat-box"><span style="color:#FFCC02">&#9679; ' + d.count + ' injuries</span> &nbsp;·&nbsp; <span style="color:#EF9A9A">&#9679; ' + d.total_days + ' days out</span></div>';
  }
  document.getElementById('panel-content').innerHTML = html;
  document.getElementById('detail-panel').style.display = 'block';
}
function closePanel() {
  document.getElementById('detail-panel').style.display = 'none';
}
"""


def build_body_map_html(injury_counts: dict, active_parts: set, view: str = "anterior") -> str:
    """
    Build complete HTML with embedded SVG body map.
    injury_counts: {body_part_key: count}
    active_parts: set of currently injured part keys
    view: 'anterior' or 'posterior'
    """
    if view == "anterior":
        svg_content = _build_anterior_svg(injury_counts, active_parts)
    else:
        svg_content = _build_posterior_svg(injury_counts, active_parts)

    # Build full HTML using plain string concatenation (no f-string)
    html = (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        "<style>" + _CSS + "</style>"
        "</head><body>"
        "<div class='wrapper'>"
        + svg_content +
        "<div id='detail-panel'>"
        "<span class='close-btn' onclick='closePanel()'>&#10005;</span>"
        "<h3 id='panel-title'>Region Detail</h3>"
        "<div id='panel-content'></div>"
        "</div>"
        "</div>"
        "<div id='tooltip'>"
        "<div class='tt-title' id='tt-title'></div>"
        "<div class='tt-count' id='tt-count'></div>"
        "<div class='tt-status' id='tt-status'></div>"
        "</div>"
        "<script>" + _JS + "</script>"
        "</body></html>"
    )
    # Use a safe placeholder that won't clash with CSS/JS
    html = html.replace("INJURY_DATA_PLACEHOLDER", "{injury_data_json}")
    return html
