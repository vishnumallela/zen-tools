from __future__ import annotations

import inspect
from typing import Annotated, get_args, get_origin, get_type_hints

from pydantic.fields import FieldInfo

from zen_tools.tools import ALL_TOOLS, NAMESPACES, ToolDef


def _field_info(annotation: object) -> FieldInfo | None:
    if get_origin(annotation) is Annotated:
        for arg in get_args(annotation)[1:]:
            if isinstance(arg, FieldInfo):
                return arg
    return None


def _type_label(annotation: object) -> str:
    if annotation is inspect.Parameter.empty:
        return "string"
    if get_origin(annotation) is Annotated:
        return _type_label(get_args(annotation)[0])
    # Union / X | None
    origin = get_origin(annotation)
    if origin is not None and hasattr(origin, "__name__") is False:
        args = [a for a in get_args(annotation) if a is not type(None)]
        if args:
            return " | ".join(_type_label(a) for a in args)
    if annotation in (int, float):
        return "number"
    if annotation is bool:
        return "boolean"
    if annotation is dict or (
        origin is not None and issubclass(origin, dict) if isinstance(origin, type) else False
    ):
        return "object"
    if annotation is list or (
        origin is not None and issubclass(origin, list) if isinstance(origin, type) else False
    ):
        return "array"
    literal_args = get_args(annotation)
    if literal_args and all(isinstance(a, str) for a in literal_args):
        return " | ".join(str(a) for a in literal_args)
    return "string"


def _html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _render_tool(td: ToolDef) -> str:
    try:
        hints = get_type_hints(td.fn, include_extras=True)
    except Exception:
        hints = {}
    sig = inspect.signature(td.fn)

    rows = ""
    for pname, param in sig.parameters.items():
        if pname in ("ctx", "self", "return"):
            continue
        annotation = hints.get(pname, inspect.Parameter.empty)
        fi = _field_info(annotation)
        required = param.default is inspect.Parameter.empty
        ptype = _html(_type_label(annotation))
        pdesc = _html(fi.description or "") if fi and fi.description else ""
        req_badge = '<span class="pr">*</span>' if required else ""
        rows += f"""
        <tr>
          <td><span class="pn">{pname}</span>{req_badge}</td>
          <td><span class="pt">{ptype}</span></td>
          <td>{pdesc}</td>
        </tr>"""

    examples_html = ""
    if td.examples:
        examples_html = f"""
    <div class="ex">
      <div class="ex-label">Examples</div>
      <pre>{_html(td.examples)}</pre>
    </div>"""

    tool_id = f"tool-{td.name.replace('_', '-')}"
    desc = _html(td.description)
    return f"""
  <div class="tool" id="{tool_id}">
    <div class="tool-hd">
      <span class="tool-name">{td.name}</span>
    </div>
    <div class="tool-desc">{desc}</div>
    <table>
      <thead><tr><th>Param</th><th>Type</th><th>Description</th></tr></thead>
      <tbody>{rows}
      </tbody>
    </table>{examples_html}
  </div>"""


def generate_docs_html() -> str:
    ns_map: dict[str, list[ToolDef]] = {}
    for td in ALL_TOOLS.values():
        ns_map.setdefault(td.namespace, []).append(td)

    nav_links = ""
    for ns in NAMESPACES:
        nav_links += f'\n  <a href="#{ns.name}" class="ns">{ns.name}/</a>'
        for td in ns_map.get(ns.name, []):
            tool_id = f"tool-{td.name.replace('_', '-')}"
            nav_links += f'\n  <a href="#{tool_id}" class="sub">{td.name}</a>'

    ns_sections = ""
    for ns in NAMESPACES:
        tools_html = "\n".join(_render_tool(td) for td in ns_map.get(ns.name, []))
        ns_sections += f"""
  <h2 id="{ns.name}" class="ns">{ns.name}/</h2>
  <p class="domain-desc">{_html(ns.description)}</p>
{tools_html}"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>zen-tools</title>
  <link href="https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Geist:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --bg: #fff; --surface: #fafafa; --border: #e4e4e7;
      --text: #18181b; --muted: #71717a; --subtle: #a1a1aa;
      --c-ns: #7c3aed; --c-tool: #059669;
      --sans: 'Geist', system-ui, sans-serif;
      --mono: 'Geist Mono', monospace;
    }}
    body {{
      background: var(--bg); color: var(--text); font-family: var(--sans);
      font-size: 15px; line-height: 1.7; -webkit-font-smoothing: antialiased;
      display: flex; min-height: 100vh;
    }}
    nav {{
      width: 200px; flex-shrink: 0; border-right: 1px solid var(--border);
      padding: 2rem 1.5rem; position: sticky; top: 0; height: 100vh; overflow-y: auto;
      display: flex; flex-direction: column;
    }}
    .logo {{ font-family: var(--mono); font-size: 1.1rem; font-weight: 600; }}
    .nav-cat {{ font-size: 0.65rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.1em; color: var(--subtle); margin: 1.5rem 0 0.5rem; }}
    nav a {{ font-size: 0.9rem; color: var(--muted); text-decoration: none;
      padding: 0.2rem 0; display: block; }}
    nav a:hover {{ color: var(--text); }}
    nav a.ns {{ color: var(--c-ns); font-weight: 500; }}
    nav a.sub {{ font-size: 0.85rem; color: var(--c-tool); }}
    .nav-logo {{ margin-top: auto; padding-top: 2rem; }}
    .nav-logo img {{ width: 100%; height: auto; opacity: 0.7; }}
    main {{ flex: 1; min-width: 0; max-width: 900px; padding: 3rem; }}
    .code {{ font-family: var(--mono); font-size: 0.85rem; background: var(--surface);
      padding: 0.2rem 0.5rem; border-radius: 4px; border: 1px solid var(--border); }}
    h2 {{ font-size: 0.75rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.1em; color: var(--subtle); margin: 3rem 0 1rem; }}
    h2.ns {{ color: var(--c-ns); font-size: 1.25rem; text-transform: none;
      letter-spacing: normal; margin-bottom: 0.5rem; }}
    p {{ font-size: 1rem; color: var(--muted); line-height: 1.8; margin-bottom: 1.25rem; }}
    .domain-desc {{ font-size: 0.9rem; color: var(--muted); margin-bottom: 1.5rem; }}
    .diagram-wrap {{ position: relative; margin: 1.5rem 0; }}
    .diagram {{ background: #fafafa; border: 1px solid var(--border);
      border-radius: 12px; padding: 2.5rem; }}
    .diagram svg {{ width: 100%; min-height: 320px; height: auto; display: block; }}
    .diagram-btn {{
      position: absolute; top: 1rem; right: 1rem; font-family: var(--mono);
      font-size: 0.7rem; color: var(--subtle); background: var(--bg);
      border: 1px solid var(--border); border-radius: 4px;
      padding: 0.25rem 0.6rem; cursor: pointer; user-select: none;
    }}
    .diagram-btn:hover {{ color: var(--text); border-color: var(--text); }}
    .diagram-modal {{
      display: none; position: fixed; inset: 0; z-index: 100;
      background: rgba(0,0,0,0.5); align-items: center; justify-content: center;
    }}
    .diagram-modal.open {{ display: flex; }}
    .diagram-modal-inner {{
      background: #fafafa; border-radius: 12px; padding: 2.5rem;
      width: 92vw; max-height: 90vh; overflow: auto;
    }}
    .diagram-modal-inner svg {{ width: 100%; height: auto; display: block; }}
    .tool {{ border: 1px solid var(--border); border-radius: 8px;
      overflow: hidden; margin: 1rem 0; }}
    .tool-hd {{ display: flex; align-items: baseline; padding: 0.875rem 1rem;
      background: var(--surface); border-bottom: 1px solid var(--border); }}
    .tool-name {{ font-family: var(--mono); font-weight: 500; font-size: 1rem;
      color: var(--c-tool); }}
    .tool-desc {{ font-size: 0.9rem; color: var(--muted);
      padding: 0.75rem 1rem; border-bottom: 1px solid var(--border); }}
    table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
    th {{ text-align: left; font-size: 0.6rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.08em; color: var(--subtle); padding: 0.625rem 1rem;
      border-bottom: 1px solid var(--border); background: var(--bg); }}
    td {{ padding: 0.625rem 1rem; border-bottom: 1px solid var(--border); }}
    tr:last-child td {{ border-bottom: none; }}
    .pn {{ font-family: var(--mono); font-size: 0.85rem; color: var(--text); }}
    .pr {{ color: var(--subtle); font-size: 0.6rem; vertical-align: super; margin-left: 2px; }}
    .pt {{ font-family: var(--mono); font-size: 0.8rem; color: var(--subtle); }}
    .ex {{ padding: 0.875rem 1rem; background: var(--bg);
      border-top: 1px solid var(--border); }}
    .ex-label {{ font-size: 0.6rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: 0.08em; color: var(--subtle); margin-bottom: 0.5rem; }}
    .ex pre {{ font-family: var(--mono); font-size: 0.8rem; color: var(--muted);
      line-height: 1.6; overflow-x: auto; }}
    @media (max-width: 800px) {{ nav {{ display: none; }} main {{ padding: 2rem; }} }}
  </style>
</head>
<body>
<nav>
  <div class="logo">zen-tools</div>
  <div class="nav-cat">Guide</div>
  <a href="#intro">Introduction</a>
  <a href="#architecture">Architecture</a>
  <div class="nav-cat">Namespaces &amp; Tools</div>{nav_links}
  <div class="nav-logo">
    <img src="https://www.oraczen.ai/assets/white-logo.svg" alt="Oraczen">
  </div>
</nav>
<main>
  <h2 id="intro">Introduction</h2>
  <p style="font-size:1.05rem;color:var(--text);font-weight:500;margin-bottom:1rem">
    One MCP endpoint. Any tool combination. Each agent gets exactly what it needs.
  </p>
  <p>zen-tools is a capability layer built specifically for AI agents. It exposes a single
  <span class="code">/mcp</span> endpoint over Streamable HTTP that any MCP-compatible agent
  can connect to and use immediately, with no custom integration work required.</p>
  <p>The core design principle is <strong>scoped visibility</strong>. When an agent connects,
  it passes a <span class="code">?tools=</span> query parameter listing the tools it needs.
  Only those tools are registered in that session. Tools that were not requested do not
  appear as forbidden. They simply do not exist in that session.</p>
  <p>Tools are grouped into namespaces, where each namespace represents a distinct capability
  domain. Each tool does exactly one thing. Agents select only what is relevant to their task.
  Nothing outside that selection exists in their session.</p>

  <h2 id="architecture">Architecture</h2>

  <p>When an agent connects for the first time, it sends a POST to <span class="code">/mcp?tools=web_search</span> with no session ID. The server generates a unique ID like <span class="code">abc123</span>, creates a <strong>transport</strong> for that client — two pipes, one for receiving messages and one for sending responses — and stores it in a dictionary as <span class="code">sessions["abc123"] = Transport</span>. At the same moment, a <strong>background job</strong> is started: a function that calls <span class="code">mcp_server.run(read_stream, write_stream)</span> with that client's pipes. This is not a new server — it is a long-running call into the one shared server, sleeping when idle and waking when a message arrives. The session ID is returned in the response header and the client must include it on every future request. On returning requests the server looks up the ID in the dictionary, finds the existing transport, and routes the message straight into it. Nothing is recreated. The same transport and background job are reused for the entire lifetime of that client's session.</p>

  <p>There is exactly one MCP server shared by all clients. Tool isolation is not done with separate servers per client. The real mechanism is the <span class="code">ContextVar</span> — and it is the most important piece of this architecture. Every time an HTTP POST arrives, before any routing happens, the server stores the full HTTP request object into a ContextVar that is <strong>private to that specific async execution</strong>. This means Client A's request object and Client B's request object never share the same slot, even if they arrive at the exact same millisecond. When the Tool Scoping Middleware runs, it reads <span class="code">?tools=</span> from that ContextVar — and because the ContextVar is isolated per request, Client A's middleware always reads <span class="code">?tools=web_search</span> and Client B's always reads <span class="code">?tools=web_fetch</span>, even though they are hitting the same server at the same time. The ContextVar is what makes one server safely serve thousands of clients with different tool scopes simultaneously.</p>

  <div class="diagram-wrap">
  <button class="diagram-btn" onclick="openDiagram()">expand</button>
  <div class="diagram">
    <pre class="mermaid" id="diagramSrc">
flowchart TD
    subgraph CLIENTS ["CLIENT SIDE"]
        CA["Client A - returning\nPOST /mcp?tools=web_search\nHeader: mcp-session-id: abc123"]
        CB["Client B - first connect\nPOST /mcp?tools=web_fetch\nno session ID header"]
    end

    CA --> AUTH_A
    CB --> AUTH_B

    AUTH_A{{"auth OK?"}}
    AUTH_B{{"auth OK?"}}
    AUTH_A -->|No| ERR_A["401 Unauthorized"]
    AUTH_B -->|No| ERR_B["401 Unauthorized"]
    AUTH_A -->|Yes| CTX_A
    AUTH_B -->|Yes| CTX_B

    subgraph PER_REQ ["2. PER REQUEST - ContextVar created before routing, discarded after response"]
        CTX_A["ContextVar - Client A\nstores HTTP request object privately\ncontains: ?tools=web_search\nvisible to this request only\nnever shared with Client B"]
        CTX_B["ContextVar - Client B\nstores HTTP request object privately\ncontains: ?tools=web_fetch\nvisible to this request only\nnever shared with Client A"]
    end

    CTX_A -->|session ID found in store| TA
    CTX_B -->|no session ID - first connect| CREATE

    CREATE["First Connect\n1. generate session ID: xyz789\n2. create Transport B\n3. start Background Job B\n4. save to session store\n5. return mcp-session-id: xyz789 in response"]

    DICT[("Session Store - persists for server lifetime\nabc123 - Transport A\nxyz789 - Transport B\nlooked up on every request")]

    CREATE --> DICT
    CREATE --> TB_
    DICT -->|abc123 found| TA

    subgraph PER_SESSION ["3. PER SESSION - created on first connect, stays alive until client disconnects"]
        TA["Transport A - session abc123\nreceives messages from Client A\nsends responses back to Client A\nreused on every Client A request - never recreated"]
        TB_["Transport B - session xyz789\nreceives messages from Client B\nsends responses back to Client B\nreused on every Client B request - never recreated"]
        BG_A["Background Job A - persistent\ncalls mcp_server.run with Transport A streams\nsleeps when idle, wakes when message arrives\nnot a new server - a long-running call into the shared server\nends when Client A disconnects"]
        BG_B["Background Job B - persistent\ncalls mcp_server.run with Transport B streams\nsleeps when idle, wakes when message arrives\nnot a new server - a long-running call into the shared server\nends when Client B disconnects"]
        TA --> BG_A
        TB_ --> BG_B
    end

    BG_A --> FILTER
    BG_B --> FILTER

    subgraph SHARED ["4. SHARED - one instance for all clients, never recreated"]
        FILTER["Tool Scoping Middleware\nreads ContextVar for THIS request only\nClient A: filters tool list to web_search only\nClient B: filters tool list to web_fetch only\nconcurrent requests never share each other's ContextVar"]
        SERVER["One MCP Server\nexecutes the tool\nwrites result back through client transport"]
        FILTER --> SERVER
    end

    SERVER --> RESP_A["Response to Client A"]
    SERVER --> RESP_B["Response to Client B"]

    style CA fill:#fff,stroke:#18181b,stroke-width:1.5px
    style CB fill:#fff,stroke:#18181b,stroke-width:1.5px
    style ERR_A fill:#fafafa,stroke:#a1a1aa,stroke-width:1px
    style ERR_B fill:#fafafa,stroke:#a1a1aa,stroke-width:1px
    style AUTH_A fill:#fafafa,stroke:#a1a1aa,stroke-width:1px
    style AUTH_B fill:#fafafa,stroke:#a1a1aa,stroke-width:1px
    style CTX_A fill:#fef9c3,stroke:#ca8a04,stroke-width:1.5px
    style CTX_B fill:#fef9c3,stroke:#ca8a04,stroke-width:1.5px
    style CREATE fill:#fafafa,stroke:#18181b,stroke-width:1.5px
    style DICT fill:#f0fdf4,stroke:#059669,stroke-width:1.5px
    style TA fill:#eff6ff,stroke:#3b82f6,stroke-width:1.5px
    style TB_ fill:#eff6ff,stroke:#3b82f6,stroke-width:1.5px
    style BG_A fill:#eff6ff,stroke:#3b82f6,stroke-width:1.5px
    style BG_B fill:#eff6ff,stroke:#3b82f6,stroke-width:1.5px
    style FILTER fill:#fff,stroke:#7c3aed,stroke-width:2px
    style SERVER fill:#fff,stroke:#7c3aed,stroke-width:2px
    style RESP_A fill:#fff,stroke:#18181b,stroke-width:1.5px
    style RESP_B fill:#fff,stroke:#18181b,stroke-width:1.5px
    </pre>
  </div>
  </div>
  <div class="diagram-modal" id="diagramModal"
       onclick="if(event.target===this)this.classList.remove('open')">
    <div class="diagram-modal-inner" id="diagramModalInner"></div>
  </div>
  <p style="font-size:0.85rem;color:var(--muted);margin-top:1rem">
    Yellow = ContextVar, set per request, private per async execution.
    Blue = Transport and Background Job, created once per session, reused until disconnect.
    Purple = shared across all clients.
  </p>
{ns_sections}
</main>
<script>
  mermaid.initialize({{
    startOnLoad: true, theme: 'base',
    flowchart: {{ nodeSpacing: 60, rankSpacing: 80 }},
    themeVariables: {{
      primaryColor: '#fff', primaryTextColor: '#18181b',
      primaryBorderColor: '#18181b', lineColor: '#71717a',
      secondaryColor: '#fafafa', tertiaryColor: '#f5f5f5',
      fontFamily: 'Geist Mono', fontSize: '15px'
    }}
  }});
  function openDiagram() {{
    const svg = document.querySelector('#diagramSrc svg');
    const modal = document.getElementById('diagramModal');
    const inner = document.getElementById('diagramModalInner');
    if (svg) {{
      inner.innerHTML = '';
      const clone = svg.cloneNode(true);
      clone.style.width = '100%'; clone.style.height = 'auto';
      inner.appendChild(clone);
    }}
    modal.classList.add('open');
  }}
</script>
</body>
</html>"""
