# Modal Deployment & OAuth Learnings

## OAuth Automation Patterns

**17. OAuth Automation Resilience**
- **Rule**: OAuth tokens expire, authorization codes expire faster (~10 minutes). Never assume previous OAuth state is valid.
- **Tactic**: Fully automate OAuth using browser_subagent:
  1. Navigate to OAuth URL
  2. Sign in (auto-select account)
  3. Approve permissions automatically
  4. Capture authorization code from redirect
  5. Exchange IMMEDIATELY via direct HTTP POST (not OAuth library)
- **Why**: Python's OAuth library (`run_local_server()`) doesn't open browsers reliably across systems. Browser_subagent is deterministic and works every time.
- **Protocol**: Store both `credentials.json` AND `token.json` in gitignore. For cloud deployment, base64-encode token.json and store as environment variable.

**18. Authorization Code Race Condition**
- **Rule**: OAuth authorization codes expire in 10 minutes. The clock starts when user approves, NOT when you exchange.
- **Tactic**: Exchange code within seconds of capturing it. Use direct HTTP POST to `https://oauth2.googleapis.com/token`
- **Why**: OAuth library's `fetch_token()` can hang. Direct HTTP is faster and more reliable.

**19. Credentials File Format Validation**
- **Rule**: Google OAuth has TWO credential types: "web" and "installed". They are NOT interchangeable.
- **Tactic**: 
  - Desktop scripts need "installed" type (has `"installed"` key in JSON)
  - Web apps need "web" type (has `"web"` key in JSON)
  - Check file structure BEFORE assuming it works
- **Why**: Error messages are cryptic and don't clearly indicate wrong credential type.

## Modal Deployment Patterns

**21. Modal Deployment Pattern**
- **Rule**: Modal can't deploy FastAPI apps directly. They need a Modal wrapper.
- **Tactic**: Create wrapper file (`modal_<app_name>.py`):
  ```python
  import modal
  app = modal.App("app-name")
  image = modal.Image.debian_slim().pip_install("fastapi", "requests", ...)
  
  with image.imports():
      from scripts.app_file import app as fastapi_app
  
  @app.function(image=image)
  @modal.asgi_app()
  def fastapi_wrapper():
      return fastapi_app
  ```
- **Protocol**: Keep original FastAPI app unchanged. Modal wrapper is deployment-only.

**31. Modal File Access Limitations**
- **Rule**: Modal containers cannot access local directories via import after deployment.
- **Failed Attempts**:
  1. `modal.Mount.from_local_dir()` → AttributeError
  2. `image.copy_local_dir()` → AttributeError  
  3. `with image.imports(): from scripts.module import ...` → ModuleNotFoundError
- **Working Solution**: Inline all code directly into Modal function OR package as proper Python module with `__init__.py` files

## General Deployment Learnings

**20. Parallel Strategy Attempts**
- **Rule**: When automation fails repeatedly (>3 attempts), try multiple approaches simultaneously.
- **Tactic**: Deploy what CAN work immediately while fixing what's broken:
  - Deploy System 1 (doesn't need Google OAuth) while fixing OAuth for Systems 2 & 3
  - Test with direct HTTP while debugging OAuth library
  - Provide manual fallback URLs while automating browser flows

**24. Incremental Testing Strategy**
- **Rule**: Test each component independently BEFORE deploying full system.
- **Tactic**: 
  1. Verify Google APIs work (create test doc)
  2. Verify Modal authentication (`modal profile list`)
  3. Test webhook locally (`uvicorn app:app`)
  4. Deploy to Modal
  5. Test deployed webhook

**25. Environment Variable Strategy for Cloud**
- **Rule**: OAuth tokens can't be stored as files in serverless environments. Use environment variables.
- **Tactic**: Base64-encode token.json and store as `GOOGLE_TOKEN_B64`
- **Protocol**: Scripts should check for `GOOGLE_TOKEN_JSON` env var FIRST, then fall back to local `token.json`

**26. Strategic Pivoting vs Persistence**
- **Rule**: Know when to pivot vs when to persist.
- **Pivot criteria**: >30 minutes stuck on same approach with no progress
- **Persist criteria**: Making incremental progress
- **Hybrid approach**: Deploy what works NOW while fixing what's broken LATER

**30. Time-Boxing Failed Approaches**
- **Rule**: Set 15-minute timer for debugging. If no progress, switch approaches.
- **Example**: 
  - Attempt 1: Python OAuth library (15 min) → FAILED
  - Attempt 2: Manual URL + user paste code (15 min) → WORKED but not automated
  - Attempt 3: Browser_subagent automation (15 min) → WORKED perfectly
