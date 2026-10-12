# Decision log - Acme Retail

## 2026-09-15 D1: Build a dbt revenue mart on the ERP replica (not a real-time dashboard)
- **Context:** Maria asked for a "real-time revenue dashboard"; the underlying need is a faster, trusted month close.
- **Options considered:** A) real-time streaming dashboard (high effort, nobody acts intraday); B) daily dbt mart reconciled to GL (medium effort, solves the close); C) clean up the existing Excel process (low effort, doesn't scale)
- **Decision:** B, by Alex
- **Why:** Solves the close-speed outcome; reuses existing Snowflake + dbt
- **Consequences / revisit when:** No intraday data; revisit if an intraday use case shows up
- **Communicated to:** Maria, 2026-09-16
