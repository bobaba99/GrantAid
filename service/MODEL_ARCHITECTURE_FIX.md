# Model Architecture Fix: Database vs API Models

## Issue
After updating to the four-facet scoring system, there was confusion between:
1. **Database schema** (experience_analysis table)
2. **API contract** (what endpoints return to frontend)

The `ExperienceAnalysis` model was incorrectly changed to represent the database table, breaking the API contract that the frontend expected.

## Solution
Separated concerns by creating distinct models:

### 1. Database Model: `ExperienceAnalysis`
Maps 1:1 with the `experience_analysis` SQL table:
```python
class ExperienceAnalysis(BaseModel):
    id: Optional[str]
    user_id: str
    experience_id: str
    funding_id: str
    story: str
    rationale: str
    experience_rating_facet_a: int (1-5)
    experience_rating_facet_b: int (1-5)
    experience_rating_facet_c: int (1-5)
    experience_rating_facet_d: int (1-5)
    created_at: Optional[str]
```

### 2. API Response Model: `ExperienceAnalysisResponse`
Used by endpoints, matches frontend expectations:
```python
class ExperienceAnalysisResponse(BaseModel):
    experience: Experience
    analysis: StoryTellingResponse
```

Where `StoryTellingResponse` contains:
```python
class StoryTellingResponse(BaseModel):
    experience_id: Optional[str]
    story: str
    rationale: str
    experience_rating_facet_a: int (1-5)
    experience_rating_facet_b: int (1-5)
    experience_rating_facet_c: int (1-5)
    experience_rating_facet_d: int (1-5)
```

## Changes Made

### `service/src/models.py`
- ✅ Kept `ExperienceAnalysis` as database model
- ✅ Added `ExperienceAnalysisResponse` for API responses
- ✅ `StoryTellingResponse` contains facet scores

### `service/src/routes/funding.py`
- ✅ Updated imports to include `ExperienceAnalysisResponse`
- ✅ Changed endpoint return types from `List[ExperienceAnalysis]` to `List[ExperienceAnalysisResponse]`
- ✅ Updated `results.append()` calls to use `ExperienceAnalysisResponse`

### `frontend/src/api/funding.ts`
- ✅ Already correct! `ExperienceAnalysis` interface matches the API response structure

## Data Flow

### Backend (Database → API)
```
experience_analysis table (ExperienceAnalysis)
    ↓ Read from DB
    {
        user_id, experience_id, funding_id,
        story, rationale,
        facet_a, facet_b, facet_c, facet_d
    }
    ↓ Transform
StoryTellingResponse created from DB row
    {
        experience_id, story, rationale,
        facet_a, facet_b, facet_c, facet_d
    }
    ↓ Combine with Experience
ExperienceAnalysisResponse
    {
        experience: { ... },
        analysis: { ... }
    }
    ↓ Return to Frontend
```

### Frontend (API → UI)
```
ExperienceAnalysis (TypeScript interface)
    {
        experience: Experience,
        analysis: StoryTellingResponse
    }
    ↓
React Component maps over array
    ↓
Displays: experience.title + analysis.facet scores
```

## Key Principle: Separation of Concerns

| Model | Purpose | Location | Audience |
|-------|---------|----------|----------|
| `ExperienceAnalysis` | Database ORM | Database layer | Supabase/SQL |
| `ExperienceAnalysisResponse` | API Contract | API endpoints | Frontend |
| `StoryTellingResponse` | LLM Output | Transient | Both |

## Benefits

1. **Clear Boundaries**: Database schema != API contract
2. **Flexibility**: Can change database structure without breaking API
3. **Type Safety**: Backend validates both database and API models
4. **Maintainability**: Each model has a single, clear purpose

## Errors Fixed

### Before Fix:
```
ValidationError: 9 validation errors for ExperienceAnalysis
user_id: Field required
experience_id: Field required
funding_id: Field required
...
```

**Cause**: Trying to create database model with API response data

### After Fix:
✅ No errors - correct model used for each purpose

## Testing Checklist

- [x] Database inserts use `ExperienceAnalysis` fields
- [x] Database reads transform to `StoryTellingResponse`
- [x] API endpoints return `ExperienceAnalysisResponse`
- [x] Frontend receives correct structure
- [ ] Test full flow: Analyze → Save to DB → Load from cache → Display

## Summary

The fix properly separates database concerns from API contracts:
- **Database layer** uses `ExperienceAnalysis` (flat, with all DB fields)
- **API layer** uses `ExperienceAnalysisResponse` (nested, frontend-friendly)
- **Transformation** happens in the route handlers

This architecture follows best practices and maintains clean separation of concerns! ✅
