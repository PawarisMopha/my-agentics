# 🤖 my-agentics

> วิจัย พัฒนา และทดลองสถาปัตยกรรม **Agentic AI & Multi-Agent Workflows** บน GitHub Actions (`gh-aw`), Node.js, Python, และ Go

[![GitHub Agentic Workflows](https://img.shields.io/badge/gh--aw-v1.2.2-blue?logo=github)](https://github.com/github/gh-aw)
[![Node.js](https://img.shields.io/badge/Node.js-v24+-green?logo=node.js)](package.json)
[![Python](https://img.shields.io/badge/Python-3.12+-yellow?logo=python)](requirements.txt)
[![LLM Engine](https://img.shields.io/badge/LLM-Gemini_3_Flash-purple?logo=google-gemini)](https://ai.google.dev/)
[![AI Agent Guidelines](https://img.shields.io/badge/Agent_Rules-AGENT.md-orange)](AGENT.md)

---

## 📌 ภาพรวมโปรเจกต์ (Project Overview)

**`my-agentics`** เป็นคลังโปรเจกต์สำหรับศึกษา พัฒนา และทดลองใช้งานระบบ **AI Agents & Multi-Agent Orchestration** โดยเน้นการผสานความสามารถของ LLM เข้ากับระบบอัตโนมัติบน GitHub ผ่าน **GitHub Agentic Workflows (`gh-aw`)** และ Framework ชั้นนำในฝั่ง TypeScript และ Python

### เสาหลักของโปรเจกต์ (Core Pillars)

1. **GitHub Agentic Workflows (`gh-aw`)**:
   - การเขียนระบบ Automation เชิง Agent ด้วย Markdown (`.github/workflows/*.md`)
   - คอมไพล์เป็น GitHub Actions (`.lock.yml`) อัตโนมัติด้วยคำสั่ง `gh aw compile`
   - ขับเคลื่อนด้วย LLM Engine สมรรถนะสูง เช่น Google Gemini (`gemini-3-flash-preview`)
2. **TypeScript / Node.js Agentic Stack**:
   - พัฒนา State Graph & Agentic Chains ด้วย `@langchain/langgraph`
   - เชื่อมต่อและสตรีมคำตอบของ AI ด้วย Vercel AI SDK (`ai`, `@ai-sdk/openai`)
3. **Python Agentic Stack**:
   - สร้าง Multi-Agent Collaboration ด้วย `crewai`
   - พัฒนา Stateful Multi-Agent Graphs ด้วย `langgraph` และ `langchain-openai`
4. **Go / GenAI Experimental**:
   - ทดสอบการเรียกใช้งาน Google GenAI SDK (`google.golang.org/genai`)

---

## 🚀 Active Agent Workflows

ปัจจุบันมี GitHub Agentic Workflows ที่คอมไพล์พร้อมทำงานบน GitHub Actions ทั้งหมด 2 ตัว:

| Workflow | ไฟล์ต้นทาง | LLM Engine | เหตุการณ์กระตุ้น (Triggers) | ความสามารถหลัก |
| :--- | :--- | :--- | :--- | :--- |
| **`code-helper`** | [code-helper.md](.github/workflows/code-helper.md) | Gemini 3 Flash | • Issues (`opened`, `labeled`)<br>• `workflow_dispatch` | ตรวจสอบ Issue, วางแผนและเขียนโค้ดแก้ไข, รันคำสั่งทดสอบผ่าน bash, และเปิด Pull Request อัตโนมัติ |
| **`daily-repo-status`** | [daily-repo-status.md](.github/workflows/daily-repo-status.md) | Gemini 3 Flash | • ประจำวัน (`schedule: daily`)<br>• `workflow_dispatch` | รวบรวมข้อมูลกิจกรรมใน Repo (Issues, PRs, Commits) และสร้างสรุปรายงานสถานะประจำวันเป็น Issue |

---

## 📂 โครงสร้างโปรเจกต์ (Repository Structure)

```text
my-agentics/
├── .github/
│   ├── agents/
│   │   └── agentic-workflows.md    # Dispatcher prompt สำหรับ gh-aw CLI
│   ├── skills/                     # คลังทักษะเสริมสำหรับ Agentic Workflows
│   └── workflows/
│       ├── code-helper.md          # [Source] Workflow ช่วยเขียนโค้ดและเปิด PR
│       ├── code-helper.lock.yml    # [Compiled] GitHub Actions Workflow (ห้ามแก้โดยตรง)
│       ├── daily-repo-status.md    # [Source] Workflow รายงานสถานะโปรเจกต์ประจำวัน
│       ├── daily-repo-status.lock.yml
│       └── dependabot-auto-merge.yml
├── AGENT.md                        # คู่มือและกฎเหล็กการทำงานของ AI Coding Agents
├── AGENTS.md                       # Symlink ชี้ไปยัง AGENT.md
├── package.json                    # Node.js Agentic dependencies (LangGraph.js, Vercel AI SDK)
├── requirements.txt                # Python Agentic dependencies (LangGraph, CrewAI)
├── main.google                     # ตัวอย่างการเรียกใช้งาน Google GenAI SDK ในภาษา Go
└── README.md                       # เอกสารแนะนำโปรเจกต์ (ไฟล์นี้)
```

---

## 🛠️ เริ่มต้นใช้งาน (Getting Started)

### 1. ความต้องการของระบบ (Prerequisites)
- **Node.js**: v24+
- **Python**: v3.12+
- **GitHub CLI (`gh`)**: พร้อมติดตั้ง Extension `gh-aw`:
  ```bash
  gh extension install github/gh-aw
  ```

### 2. ติดตั้ง Dependencies

```bash
# สำหรับ Node.js Stack
npm install

# สำหรับ Python Stack
pip install -r requirements.txt
```

### 3. การจัดการ GitHub Agentic Workflows (`gh-aw`)

```bash
# ตรวจสอบสถานะของ Workflows ในระบบ
gh aw status

# คอมไพล์ Workflows ทั้งหมดหลังแก้ไขไฟล์ .md
gh aw compile

# สั่งรัน Workflow บน GitHub Actions ด้วยตนเอง
gh aw run code-helper
gh aw run daily-repo-status
```

> [!IMPORTANT]
> **กฎเหล็ก**: ห้ามแก้ไขไฟล์ `*.lock.yml` ด้วยตนเองเด็ดขาด ให้แก้ไขเฉพาะไฟล์ต้นทาง `.github/workflows/*.md` แล้วสั่งรัน `gh aw compile` เพื่อสร้างไฟล์ lock ใหม่อัตโนมัติ

---

## 🔑 การตั้งค่า Environment Variables & Secrets

หากต้องการรัน Workflows หรือสคริปต์ จำเป็นต้องกำหนด Environment Variables / GitHub Secrets ดังต่อไปนี้:

| Secret / Env Var | รายละเอียด |
| :--- | :--- |
| `GEMINI_API_KEY` | API Key สำหรับ Google Gemini API |
| `OPENAI_API_KEY` | API Key สำหรับ OpenAI API |
| `GITHUB_TOKEN` | Token สำหรับให้ GitHub Agentic Workflows ดำเนินการสร้าง PR, Issue, หรือ Comment |

---

## 🤖 แนวทางสำหรับ AI Coding Agents

โปรเจกต์นี้มีคู่มือและข้อตกลงการพัฒนา (SOP & Rulebook) สำหรับ AI Coding Agent ไว้ที่ [AGENT.md](AGENT.md) พร้อม Symlink ไปยังเครื่องมือต่าง ๆ:
- **Claude Code**: `CLAUDE.md`
- **Cursor IDE**: `.cursorrules`
- **Cline / Roo Code**: `.clinerules`
- **Windsurf**: `.windsurfrules`
- **GitHub Copilot**: `.github/copilot-instructions.md`

---

## 📄 ใบอนุญาต (License)

โปรเจกต์นี้เผยแพร่ภายใต้ลิขสิทธิ์โอเพนซอร์ส (Open-source License)
