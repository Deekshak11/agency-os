# Lead Magnet V2.0 Optimizations

## Apify Actor Learnings

**8. Apify Actor Parameter Precision**
- **Rule**: Each Apify actor has unique input schema. Never assume parameter names across actors.
- **Tactic**: ALWAYS check actor documentation first. For `code_crafter/leads-finder`, use `fetch_count` (not `maxResults` or `maxItems`). Default is 50,000 if not specified!
- **Protocol**: Print payload before API calls: `print(f"Apify payload: {json.dumps(payload, indent=2)}")`

**11. Multi-Layer Deduplication Strategy**
- **Rule**: For third-party data sources (Apify, etc.), assume duplicates exist.
- **Tactic**: 
  1. Deduplicate at API result processing
  2. Deduplicate when loading from cache
  3. Auto-refetch if unique count < target (up to 3 attempts)
  4. Track `seen_companies` set across batches, not per-batch
- **Protocol**: Increase fetch count iteratively (30 → 50 → 70) until quota met.

**12. Cache Quality vs Speed**
- **Rule**: Caching is for speed, not perpetuating bad data.
- **Tactic**: Add cache validation and auto-repair:
  - Deduplicate on cache load
  - Warn if cache has insufficient unique entries
  - Suggest cache clearing for reseeding
- **Future**: Implement cache versioning or TTL (30-day expiry).

## Perplexity Integration

**13. Perplexity via OpenRouter**
- **Rule**: Check existing codebase for API integration patterns before implementing new ones.
- **Discovery**: Perplexity Sonar accessed via OpenRouter (not Perplexity API directly). Use `perplexity/sonar` model.
- **Tactic**: Reuse `call_openrouter()` helper with different models instead of creating new API clients.

**14. Research Data Flow Clarity**
- **Rule**: Always clarify data provenance (where data comes from) and data flow (where it goes).
- **Pattern**: For lead magnet generation:
  - FCFO authority = Column G (AI Emails) - already researched
  - Lead research = Top 3 leads via Perplexity
  - Combine both for hyper-personalization

**16. Niche Detection Accuracy**
- **Rule**: Use the most specific data source available, even if it requires parsing.
- **Tactic**: Parse AI Email content for niche keywords before falling back to generic "Industry" column.

## Content Generation

**9. Model Cost Awareness**
- **Rule**: ALWAYS verify model selection in cost-sensitive operations.
- **Tactic**: GPT-4o vs GPT-4o-mini = 10-20x cost difference. Add logging: `print(f"🔵 OpenRouter: model={model}")`
- **Protocol**: Review all LLM calls quarterly to catch cost drift.

**10. Markdown Artifact Contamination**
- **Rule**: Always sanitize AI-generated content before inserting into formatted documents.
- **Tactic**: Strip markdown code fences:
  ```python
  if "```markdown" in content:
      content = content.split("```markdown")[1].split("```")[0].strip()
  ```

**15. Full Name vs Partial Name**
- **Rule**: For professional documents, always use full names unless specifically casual.
- **Tactic**: Extract both `First Name` and `Last Name`, combine as `lead_full_name`. Add fallbacks: `lead_full_name=None` → fallback to `user_name`.
