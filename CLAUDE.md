# AGENT.md - Project Guidelines (`my-agentics`)

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
