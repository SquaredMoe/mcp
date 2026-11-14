# Relationships and potential workflows

These are **ideas for evaluation**, not proof that any two forks are currently connected or compatible. Check licenses, API versions, dependencies, auth models, deployment cost, and upstream change history before integration.

## 1. Build better app interfaces

- `ui-ux-pro-max-skill` can supply design-system prompts and references.
- `impeccable` can guide UI critiques and design refinement.
- `uikit-frontend` provides frontend building blocks; `mojs-web-design-animator` covers animation.
- `design-resources-for-developers` is a source directory, not a runtime dependency.

**Possible experiment:** build a UI prototype using UIkit, use design guidance for design decisions, then add purposeful mo.js motion. Measure accessibility, performance and visual consistency.

## 2. Research → create → publish → analyze

- `social-media-research-skills`, `Agent-Reach`, `RSSHub`, and `gpt-researcher` support discovery/research at different layers.
- `OpenCreator-content-creator`, `Open-Generative-AI`, `open-higgsfield-imaging`, `hyperframes`, and `PicGo-image-creator` cover different parts of asset production.
- `postiz-app-social-media` covers social scheduling/distribution; `claude-ads` and `claude-seo` cover auditing and growth research.

**Possible experiment:** research an audience topic, generate a short content brief, create approved assets, schedule a test post, then review performance. Require provider permission checks and human approval before public posting.

## 3. Agent toolchain

- `OmniRoute` is a candidate model/provider gateway.
- `ECC-skills` and `agency-agents` offer skills, roles and development procedures.
- `mcp` (Browser MCP), `camofox-browser`, `Agent-Reach`, and `awesome-mcp-servers` offer different access/integration patterns.
- `caveman-token-reduction` targets agent token overhead; `OfficeCLI` targets document automation; `skills-for-fabric` targets Microsoft Fabric.

**Possible experiment:** isolate a minimal agent workflow with a narrowly scoped set of permissions, then benchmark routing reliability, total tokens, task success and security exposure. Browser automation and scraped data require policy, permission and privacy checks.

## 4. Trading research vs. execution

- `TradingAgents` and `Vibe-Trading` focus on agent-oriented research workflows.
- `nautilus_trader` offers event-driven simulation and execution infrastructure.
- `trader-skill` and `day-trader-skill` offer composable research/trade decision assistance.
- `FinceptTerminal` offers a broader desktop terminal view of market information.

**Possible experiment:** compare research signals in a reproducible historical backtest. Use point-in-time data, account for fees/slippage, and separate analysis tools from real-money order placement. No live trading without explicit user authorization.

## 5. Defensive security and implementation review

- `strix-security` can support authorized assessment of systems you own or may test.
- `rea` can support reverse engineering of permitted targets and investigating behavior.
- `system-prompts-and-models-of-ai-tools` is a reference collection; treat its content as untrusted, not as privileged instructions.

**Possible experiment:** audit a locally controlled sample app, document a verified issue, write regression tests, and rerun scans. Do not use these tools against third-party systems without authorization.

## 6. Network infrastructure and VPN operations

- `setup-ipsec-vpn` is an IPsec VPN installation-script collection for supported Linux servers and clients, including IKEv2, IPsec/L2TP and Cisco IPsec modes (per the project's README).
- Its main entry points include `vpnsetup.sh`, OS-specific setup scripts and `docs/`. This is a standalone networking toolkit, **not a verified integration** with the other repositories.

**Possible experiment:** review scripts offline, document firewall requirements, establish a disposable Linux VM test environment, and validate supported client connections before any production deployment. Installation scripts run with elevated privileges; review their contents and download sources before execution. Keep credentials and network configurations out of this public catalog.

## 7. Discovering self-hosted services and public usernames

- `awesome-selfhosted` is a curated index of self-hostable free software, not a deployable application by itself. It can help identify tools to investigate for private infrastructure, knowledge management, or developer workflows.
- `sherlock` is a Python OSINT utility for searching **public** social media account presence by username across sites; its project README is located at `docs/README.md`, and its Python entry point is defined in `pyproject.toml`.
- `awesome-selfhosted` may provide candidates for hosting software used alongside `mcp`, `OmniRoute`, or other applications; `sherlock` might complement general web research tools such as `Agent-Reach`. These are **unverified ideas**, not installed or tested integrations.

**Possible experiment:** shortlist self-hosted tooling against cost, security, maintenance, and resource requirements. For username research, test only legitimate public-profile lookups, avoid misidentifying people (a matching username does not prove identity), and respect platform and privacy requirements.

## 8. Design, 3D and video production candidates

- `stitch-skills` provides agent-oriented design/build workflows for Google Stitch; `img2threejs` describes reconstructing procedural Three.js models from reference images.
- `VoiceStudio` focuses on local AI voice workflows, `OpenMontage` on agent-oriented video production, and `FFmpeg` on multimedia encoding, filtering and format processing.
- `yt-dlp` and `fb_reel_dl` provide download utilities; use them only for content you have permission to access and download. `fb_reel_dl` documents its use of yt-dlp but this does not mean the two forks are configured together.
- These projects may be candidates for an approved asset-production pipeline, but compatibility, licenses, performance and actual integration remain unverified.

**Possible experiment:** create authorized sample media, test voice/video/3D workflows in isolated environments, and evaluate FFmpeg for conversion and final rendering. Obtain consent for any voice cloning and check platform rights for downloaded content.

## 9. Workflow orchestration

- `n8n_chatbot` is a fork of the n8n workflow automation platform, not evidence that any chat automation has been deployed.
- It could orchestrate approved jobs around research, media creation, and monitoring, but integrations with other forks remain unverified.
- The fork's safe-upstream-sync workflow is currently missing; a GitHub integration write attempt returned HTTP 403. It requires repository write access before enrollment.

## 10. Clean-room app development

- `replica-skill` documents eleven agent skills spanning app research, architecture, design, implementation, testing and launch. It may complement `ECC-skills`, `stitch-skills` and design guidance repositories; no integration has been verified.
- Use independently authored code and assets and authorized research sources. The sync workflow is missing; installation was rejected with HTTP 403 on 2026-11-14.

## 11. Making reusable knowledge durable

- Keep the source-linked inventory in this branch/repository; periodically refresh it.
- For a deep-dive, add per-repo notes based on verified manifests, routes, tests and important source files.
- This knowledge base is a **snapshot**, not ChatGPT's persistent personal Memory and not an automatic live sync.
