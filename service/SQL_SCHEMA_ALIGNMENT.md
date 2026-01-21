# SQL Schema Alignment Report

## ✅ Alignment Status: COMPLETE

The Python models in `service/src/models.py` are now fully aligned with the `experience_analysis` table schema defined in `supabase/migrations/20260118000000_initial_schema.sql`.

---

## SQL Schema (Source of Truth)

```sql
CREATE TABLE IF NOT EXISTS public.experience_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    experience_id UUID NOT NULL REFERENCES public.experience(id) ON DELETE CASCADE,
    funding_id UUID NOT NULL REFERENCES public.funding(id) ON DELETE CASCADE,
    story TEXT NOT NULL,
    rationale TEXT NOT NULL,
    experience_rating_facet_a INTEGER NOT NULL,  -- Competency & Capacity
    experience_rating_facet_b INTEGER NOT NULL,  -- Fit with Program Priorities
    experience_rating_facet_c INTEGER NOT NULL,  -- Impact & Value
    experience_rating_facet_d INTEGER NOT NULL,  -- Narrative Flow & Coherence
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    UNIQUE(experience_id, funding_id)
);
```

---

## Python Model Alignment

### `ExperienceAnalysis` (Database Model)

Maps 1:1 with the `experience_analysis` SQL table:

```python
class ExperienceAnalysis(BaseModel):
    id: Optional[str]                           # ✅ UUID primary key
    user_id: str                                # ✅ UUID references auth.users
    experience_id: str                          # ✅ UUID references experience
    funding_id: str                             # ✅ UUID references funding
    story: str                                  # ✅ TEXT NOT NULL
    rationale: str                              # ✅ TEXT NOT NULL
    experience_rating_facet_a: int (1-5)        # ✅ INTEGER NOT NULL
    experience_rating_facet_b: int (1-5)        # ✅ INTEGER NOT NULL
    experience_rating_facet_c: int (1-5)        # ✅ INTEGER NOT NULL
    experience_rating_facet_d: int (1-5)        # ✅ INTEGER NOT NULL
    created_at: Optional[str]                   # ✅ TIMESTAMP WITH TIME ZONE
```

### `StoryTellingResponse` (API Response Model)

Transient model for LLM responses, matches the structure needed for database insertion:

```python
class StoryTellingResponse(BaseModel):
    experience_id: Optional[str]                # ✅ Maps to experience_id
    story: str                                  # ✅ Maps to story
    rationale: str                              # ✅ Maps to rationale
    experience_rating_facet_a: int (1-5)        # ✅ Maps to facet_a
    experience_rating_facet_b: int (1-5)        # ✅ Maps to facet_b
    experience_rating_facet_c: int (1-5)        # ✅ Maps to facet_c
    experience_rating_facet_d: int (1-5)        # ✅ Maps to facet_d
    # Note: user_id, funding_id, id, created_at added during persistence
```

---

## Field Name Mapping

| SQL Column | Python Field | Type | Notes |
|-----------|--------------|------|-------|
| `id` | `id` | UUID | Auto-generated |
| `user_id` | `user_id` | UUID | Added during save |
| `experience_id` | `experience_id` | UUID | From request |
| `funding_id` | `funding_id` | UUID | Added during save |
| `story` | `story` | TEXT | LLM-generated |
| `rationale` | `rationale` | TEXT | LLM-generated |
| `experience_rating_facet_a` | `experience_rating_facet_a` | INTEGER | 1-5 score |
| `experience_rating_facet_b` | `experience_rating_facet_b` | INTEGER | 1-5 score |
| `experience_rating_facet_c` | `experience_rating_facet_c` | INTEGER | 1-5 score |
| `experience_rating_facet_d` | `experience_rating_facet_d` | INTEGER | 1-5 score |
| `created_at` | `created_at` | TIMESTAMP | Auto-generated |

---

## Facet Definitions

| Facet | SQL Column | Description |
|-------|-----------|-------------|
| **Facet A** | `experience_rating_facet_a` | Competency & Capacity: Technical skills, leadership, transferable skills |
| **Facet B** | `experience_rating_facet_b` | Fit with Program Priorities: Strategic alignment, EDI, KMb |
| **Facet C** | `experience_rating_facet_c` | Impact & Value: Reach, influence, DORA-aligned evidence |
| **Facet D** | `experience_rating_facet_d` | Narrative Flow & Coherence: Storytelling, clarity, persuasion |

---

## Changes Made

### 1. ❌ Removed
- `FacetScores` nested model (didn't match flat SQL structure)
- Old `experience_rating: int` single rating field

### 2. ✅ Updated
- **`ExperienceAnalysis`**: Now maps directly to SQL table with all fields
- **`StoryTellingResponse`**: Uses flat facet fields matching SQL columns
- **`story_teller.py` schema**: Updated JSON schema to use database field names
- **`story_teller.py` prompt**: Added explicit JSON output format specification

### 3. ✅ Added
- Database-specific fields: `id`, `user_id`, `funding_id`, `created_at`
- Validation constraints: `ge=1, le=5` for facet scores
- Comprehensive docstrings explaining the 1:1 SQL mapping

---

## Data Flow

```
User Request
    ↓
StoryTellingRequest (experience + funding)
    ↓
LLM Processing
    ↓
StoryTellingResponse (facet_a/b/c/d + story + rationale)
    ↓
Add user_id, funding_id
    ↓
ExperienceAnalysis (complete database model)
    ↓
Supabase INSERT
    ↓
experience_analysis table
```

---

## Database Constraints

The SQL schema enforces:
- ✅ **UNIQUE constraint** on `(experience_id, funding_id)` - prevents duplicate analyses
- ✅ **NOT NULL** on all facet ratings, story, and rationale
- ✅ **CASCADE DELETE** on foreign keys - analyses deleted when user/experience/funding deleted
- ✅ **RLS Policy** - users can only access their own analyses

---

## Testing Checklist

- [ ] Test LLM response parsing with new field names
- [ ] Verify StoryTellingResponse → ExperienceAnalysis conversion
- [ ] Test database insertion with all required fields
- [ ] Verify UNIQUE constraint behavior (duplicate prevention)
- [ ] Test RLS policies (user isolation)
- [ ] Validate facet score constraints (1-5 range)

---

## Summary

✅ **All fields aligned** - Python models exactly match SQL schema  
✅ **Field names match** - Using `experience_rating_facet_a/b/c/d`  
✅ **Data types match** - UUID ↔ str, INTEGER ↔ int, TEXT ↔ str  
✅ **Constraints enforced** - Pydantic validation matches SQL constraints  
✅ **Documentation updated** - Clear mapping between models and schema
