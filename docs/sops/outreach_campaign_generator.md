# Directive: Outreach Campaign Generator

## Goal
Generate personalized cold emails for a list of leads using a 2-step AI process (Research -> Writing).

## Inputs
- **Source**: Google Sheet (or CSV export if API not ready).
- **Columns**: `First Name`, `Last Name`, `Company`, `Website`, `LinkedIn`.

## Tools / APIs
- **Language**: Python.
- **APIs**:
    -   **Research**: OpenRouter (Perplexity Sonar).
    -   **Writing**: OpenRouter (GPT-4o mini).
- **Libraries**: `pandas`, `requests`, `dotenv`.

## Process Flow
1.  **Load Leads**: Read from input source.
2.  **Iterate**: For each lead:
    -   **Step 1: Research**: Call Perplexity Sonar to get `first_name`, `role_type`, `niche_focus`, `recent_signal`.
        -   *Constraint*: Handle "Generalist Trap" (default to "Growth-Stage" or "SMB").
    -   **Step 2: Write**: Call GPT-4o mini to generate the email body.
        -   *Constraint*: Adapt based on `role_type` (Owner vs Employee).
    -   **Step 3: Save**: Update the record with the generated email.
3.  **Output**: Save results to a new CSV/Sheet.

## Error Handling
- **Rate Limits**: Implement backoff/retry logic for API calls.
- **Timeouts**: Set reasonable timeouts (e.g., 60s) and handle exceptions gracefully.
- **Checkpointing**: Save progress periodically to avoid losing data on crash.

## Output
- A CSV/Excel file with the original columns plus `Generated Email`, `Research Data`.
