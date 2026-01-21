# Service Source Code (`service/src`)

This directory contains the core business logic for the GrantAid Python service.

## Modules

### `models.py`
**Purpose**: Defines Pydantic models for data validation and type safety.
**Key Classes**:
- `Experience`: User's professional/academic history.
- `GrantDefinition`: Static info about grants.
- `StoryTellingRequest`: Payload for the LLM story teller.

### `utils.py`
**Purpose**: Shared utility functions.
**Key Functions**:
- `get_logger`: Centralized logging configuration.
- `sanitize_json_response`: JSON serialization helper for dates.
- `format_error_response`: Standard error formatting.

### `llm_client.py`
**Purpose**: Handles interactions with Google GenAI (Gemini).

### `story_teller.py`
**Purpose**: Contains logic to rewrite user experiences based on grant requirements.


