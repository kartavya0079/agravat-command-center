# AGRAVAT Automation Roadmap

## Phase 1 — Foundation
- GitHub Actions validation
- automation registry
- secret-safe architecture
- manual test-first workflow

## Phase 2 — Revenue operations
1. Amazon daily performance monitor
2. OSMF lead capture and routing
3. AiSensy follow-up triggers
4. SEO monitoring
5. Website health checks
6. Blinkit / Instamart operational monitoring
7. CEO reporting

## Architecture
ChatGPT -> GitHub -> GitHub Actions / n8n -> business systems.

GitHub stores versioned automation code. GitHub Actions runs code and checks. n8n handles cross-app orchestration. ChatGPT helps design, review and improve the system.

## Safety boundary
No patient/customer personal data should be committed to this repository. Secrets must not be stored in source files.
