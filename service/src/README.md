# Service Source Code (`service/src`)

This directory contains the core business logic for the GrantAid Python service.

## Modules

### `models.py`
**Purpose**: Defines Pydantic models for data validation and type safety.
**Key Classes**:
- `Experience`: User's professional/academic history.
- `GrantDefinition`: Static info about grants.
- `RemixedExperienceRequest`: Payload for the LLM remixer.

### `utils.py`
**Purpose**: Shared utility functions.
**Key Functions**:
- `get_logger`: Centralized logging configuration.
- `sanitize_json_response`: JSON serialization helper for dates.
- `format_error_response`: Standard error formatting.

### `llm_client.py` (Planned)
**Purpose**: Handles interactions with Google GenAI (Gemini).

### `remixer.py` (Planned)
**Purpose**: Contains logic to rewrite user experiences based on grant requirements.

### `diff_engine.py` (Planned)
**Purpose**: Compares different versions of grant requirements (e.g., year-over-year changes).


