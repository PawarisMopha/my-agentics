# AGENT.md - Project Guidelines (`my-agentics`)

## 🧭 Chrome DevTools MCP on Termux (Android)

### 1. Connect Chrome DevTools via ADB
```bash
termux-adb forward tcp:9222 localabstract:chrome_devtools_remote
```

### 2. MCP Server configuration
Create or edit `~/.gemini/config/mcp_config.json` with:
```json
{
  "servers": {
    "chrome-devtools": {
      "package": "chrome-devtools-mcp@latest",
      "args": ["--no-usage-statistics", "--browser-url=http://127.0.0.1:9222"]
    }
  }
}
```

### 3. Usage Tips
- Keep Google Chrome running in the foreground or in split‑screen mode to prevent Android from suspending the background process.
- Use Antigravity MCP commands (e.g., `mcp list_pages`, `mcp evaluate_script`) to interact with the page.

## 📦 Termux Container Agent (`termux_container_agent.py`)

- Provides a lightweight wrapper to run Linux commands inside udocker containers on Android.
- The agent auto‑creates and manages containers, exposing a simple CLI:

```bash
python termux_container_agent.py <command>
```

- Example: `python termux_container_agent.py ls -la /data` runs `ls -la /data` inside a container.

Refer to the script comments for advanced usage and automatic container lifecycle handling.


## 1. Tech Stack & Scope
- **Repo:** `PawarisMopha/my-agentics` (Agentic AI & Multi-Agent Workflows).
- **Stack:** GitHub Agentic Workflows (`gh-aw`), TypeScript/Node.js (LangGraph, Vercel AI SDK), Python (LangGraph, CrewAI, Google GenAI SDK).

## 2. Golden Rules
1. **GitHub Agentic Workflows (`gh-aw`):**
   - **NEVER** edit `.lock.yml` files directly. Edit `.github/workflows/*.md` only.
   - Always run `gh aw compile` after editing any workflow `.md` file.
   - Apply **Least Privilege** (`permissions`, `tools`, `safe-outputs`).
2. **Security:**
   - **NEVER** hardcode API keys/tokens (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `GITHUB_TOKEN`). Always use environment variables or GitHub Secrets.
3. **Verification & Dependencies:**
   - Always run/verify code via Bash before finishing.
   - Record any newly installed packages in `package.json` or `requirements.txt`.
4. **Git Commits:**
   - Use Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`).

## 3. Communication & Workflow
- **Workflow:** Analyze -> Explore context -> Implement cleanly -> Verify (`gh aw compile` / run tests) -> Summarize briefly.
- **Language:** Explain and summarize in **Thai** (keep technical terms in English). Be concise, use bullet points, and reference files as `file://path/to/file`.
