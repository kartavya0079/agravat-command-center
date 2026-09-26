# AGRAVAT Automation Hub

This directory is the execution layer for AGRAVAT business automations.

## Planned modules
- amazon — marketplace reporting, inventory and performance alerts
- blinkit — quick-commerce monitoring and reporting
- instamart — onboarding/operations monitoring
- leads — lead normalization, routing and follow-up triggers
- whatsapp — AiSensy integration helpers
- seo — SEO monitoring and content operations
- website — uptime, deployment and technical checks
- reports — CEO summaries and operational reporting

## Operating rules
1. Never commit API keys, passwords, tokens, customer data or patient data.
2. Store credentials in GitHub Actions Secrets or the appropriate external secret manager.
3. Test new automations manually before enabling schedules.
4. Keep business-critical writes behind explicit safeguards.
5. Prefer reusable modules over duplicated workflows.
