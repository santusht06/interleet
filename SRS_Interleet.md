# Software Requirements Specification (SRS)

*Interleet Platform — Enterprise AI-Powered Developer Assessment & Competitive Coding Ecosystem
Document ID: SRS-INT-2026-ENT-V3.5 | IEEE Std 830-1998 & ISO/IEC/IEEE 29148 Compliance*


## 1. Executive Summary & Legal Licensing Architecture


### 1.1 System Executive Summary

This Software Requirements Specification (SRS) establishes the complete, authoritative technical specification for the Interleet Platform. Interleet is an enterprise-grade, self-hosted developer evaluation and competitive programming ecosystem. It integrates a multi-language containerized online judge engine, an adaptive LangGraph-driven AI mock interview simulator, an interactive system design canvas, real-time multiplayer coding contests, an Experience Points (XP) progression economy, and an enterprise recruiter candidate portal.

Designed to address the limitations of legacy assessment platforms, Interleet provides end-to-end evaluation capabilities ranging from foundational data structure challenges to multi-container DevOps scenarios, Playwright headless browser DOM testing, and conversational AI technical interviews with live speech-to-text and audio synthesis.


### 1.2 Dual-Licensing Legal & IP Framework

Interleet operates under a strict dual-licensing legal framework designed to foster community open-source core development while protecting commercial enterprise extensions:

- **1. Core Infrastructure & Open Source Component (Apache License 2.0): ** The core FastAPI backend, basic API controllers, standard frontend layout components, and open-source Docker sandbox execution scripts are released under the Apache License 2.0 (Copyright 2026 Sharexpress Contributors). Users are granted non-exclusive, royalty-free rights to inspect, modify, and self-host the open-source core.
- **2. Enterprise Recruiter & Commercial Modules (Sharexpress Proprietary License): ** The Enterprise Candidate Management Portal, Custom AI Candidate Assessment Scoring Algorithms, Challenge Quality Gate Test Generators, Differential Testing Framework, and Premium Presets are protected under the Sharexpress Commercial Proprietary IP License. Commercial redistribution, white-labeling, or re-selling of these enterprise assets without explicit licensing contracts is strictly prohibited.

### 1.3 Third-Party License Compliance Directory


## 2. Infrastructure & System Architecture Topology


### 2.1 Platform Deployment Topology

Interleet is deployed as a resilient multi-process architecture on Linux host environments:

- **• Host Server Operating System: ** Ubuntu Linux 22.04 LTS / 24.04 LTS (x86_64 architecture).
- **• Process Management & Daemon: ** PM2 Daemon running `interleet-backend` (`.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8001 --workers 4`), autostarted via systemd (`pm2-root.service`).
- **• Reverse Proxy & SSL Termination: ** Nginx Web Server configured with TLS 1.3 termination, proxying requests from Cloudflare CDN (`interleet.sharexpress.in` and `interleet-backend.sharexpress.in`).
- **• Primary Database Persistence: ** MongoDB 7.0 Jammy using Motor async driver (Database name: `interleet`).
- **• In-Memory Cache & Job Queue: ** Redis 7.0 Alpine (Asyncio client, 512MB maxmemory LRU eviction policy).
- **• Container Execution Runtime: ** Docker Engine 26+ mounted via host socket `/var/run/docker.sock`.

### 2.2 System Process Interconnection Diagram


> **📌 SYSTEM INTERCONNECT ARCHITECTURE DIRECTIVE**
> The client browser connects via HTTPS (Port 443) through Cloudflare and Nginx to the PM2 Uvicorn backend pool (Port 8001). Code execution requests are enqueued in Redis (`interleet:execution_jobs`), dequeued by 4 async worker tasks, and dispatched to pre-warmed persistent Docker container sandboxes via socket connection.


## 3. Containerized Execution Engine Architecture


### 3.1 Sandbox Runtime Specifications

The Interleet Judge Engine maintains 8 persistent, pre-warmed container sandboxes executing user code via `exec_run()` to eliminate container cold-start latency:


### 3.2 9-Layer Sandbox Security Containment Matrix

- **1. Network Disabling: ** `network_disabled=True` (prevents external socket access or data exfiltration).
- **2. Hard Memory Limit: ** `mem_limit=512m` (boosted to `1.5g` for headless browser sandbox).
- **3. CPU Allocation Cap: ** `nano_cpus=2_000_000_000` (capped at max 2 CPU cores).
- **4. Process Limit (PID Bomb Guard): ** `pids_limit=256`.
- **5. Privilege Escalation Prevention: ** `security_opt: ["no-new-privileges:true"]`.
- **6. Linux Capability Drop: ** `cap_drop: ["ALL"]` (drops all root/system capabilities).
- **7. Ephemeral Scratch Filesystem: ** `tmpfs /tmp` mounted with `noexec, nosuid`.
- **8. Execution Timeout Enforcement: ** `timeout` wrapper command; exit code 124 triggers TLE verdict.
- **9. Output Size Guard: ** 10 MB hard cap on stdout/stderr buffers.

## 4. MongoDB Collection Schemas & Data Model Specifications

MongoDB 7.0 serves as the primary data store. Below are the field-level schema definitions across all 15 system collections:


## 5. Exhaustive Functional Requirements Directory

This section specifies 60 discrete functional requirements across 11 core functional modules:


## 6. Complete API Directory & Technical Interface Protocols

This section contains the technical API dictionary listing endpoints, authentication levels, and data definitions:


## 7. Non-Functional Requirements & Security Architecture


### 7.1 Performance & Latency SLAs

- **• Code Execution Latency: ** Interpreted languages (Python/Node/JS) execute in < 600ms wall time inside persistent containers. Compiled languages (C++/Go/Rust/Java) execute in < 1500ms.
- **• Thread Pool Isolation: ** All Docker SDK calls execute in a dedicated `_DOCKER_THREAD_POOL` (12 worker threads) to eliminate async event loop starvation.
- **• AI Parallelization: ** Current answer evaluation and next-question generation run concurrently via `asyncio.gather()`, maintaining per-turn response latency < 1.8 seconds.
- **• Voice TTS Caching: ** OpenAI TTS responses are cached for 24 hours (`Cache-Control: public, max-age=86400`), serving audio responses in < 50ms.

### 7.2 Account Soft-Deletion & Data Anonymization Routine

When a candidate requests account deletion via `DELETE /api/settings/account`, the system executes an automated PII anonymization routine (`SettingsController.delete_account()`):

- **1. PII Anonymization: ** Email replaced with `deleted_user_<id>@deleted.local`, full_name set to "Deleted User", avatar cleared.
- **2. Security Revocation: ** `is_active` set to `false`, `is_locked` set to `true`, OAuth identifiers removed.
- **3. Activity Preservation: ** Submission statistics and leaderboard history retained anonymously to preserve competitive integrity.

## 8. Traceability Matrix & Document Approvals


### Document Approval Sign-Off Block
