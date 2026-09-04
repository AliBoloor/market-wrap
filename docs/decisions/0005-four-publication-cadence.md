# ADR 0005: Adopt four publication families and closing cadences

Status: Accepted

## Decision

Publish four products on one static site:

1. Daily Market Wrap after every completed U.S. session, reviewing the close
   and the next session.
2. Weekly Market Wrap after the week's final U.S. session, normally Friday or
   Thursday when Friday is a market holiday.
3. Monthly Market Wrap after the final U.S. session of the calendar month, with
   U.S./global macro, earnings, growth, rates, policy, and markets.
4. Canadian Economy once after each calendar month, with educational macro and
   political analysis plus balanced policy reading.

Daily, Weekly, and Monthly include global context. Each publication has an
independent archive and idempotency key.

## Consequences

- The former opening/mid-session workflow is retired; Daily always means closing.
- Friday holidays require trading-calendar awareness.
- Month-end tasks must serialize Git work and use type-specific markers.
- Canadian policy links represent credible, varied viewpoints without implying
  endorsement.
