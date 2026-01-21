# Backend Route Update: Four-Facet Scoring

## Issue Fixed
The backend routes in `service/src/routes/funding.py` were still using the old `experience_rating` field instead of the new four facet scores, causing validation errors when trying to create/read analysis data.

## Changes Made

### File: `service/src/routes/funding.py`

#### 1. Reading Cached Analyses (Line 83-88)
**Before:**
```python
analysis = StoryTellingResponse(
    experience_id=exp_id,
    experience_rating=item['experience_rating'],  # ❌ Old field
    story=item['story'],
    rationale=item['rationale']
)
```

**After:**
```python
analysis = StoryTellingResponse(
    experience_id=exp_id,
    experience_rating_facet_a=item['experience_rating_facet_a'],  # ✅ New facet fields
    experience_rating_facet_b=item['experience_rating_facet_b'],
    experience_rating_facet_c=item['experience_rating_facet_c'],
    experience_rating_facet_d=item['experience_rating_facet_d'],
    story=item['story'],
    rationale=item['rationale']
)
```

#### 2. Loading from Cache (Line 141-147)
**Before:**
```python
analysis = StoryTellingResponse(
    experience_id=cached_data['experience_id'],
    experience_rating=cached_data['experience_rating'],  # ❌ Old field
    story=cached_data['story'],
    rationale=cached_data['rationale']
)
```

**After:**
```python
analysis = StoryTellingResponse(
    experience_id=cached_data['experience_id'],
    experience_rating_facet_a=cached_data['experience_rating_facet_a'],  # ✅ New facet fields
    experience_rating_facet_b=cached_data['experience_rating_facet_b'],
    experience_rating_facet_c=cached_data['experience_rating_facet_c'],
    experience_rating_facet_d=cached_data['experience_rating_facet_d'],
    story=cached_data['story'],
    rationale=cached_data['rationale']
)
```

#### 3. Saving to Database (Line 154-161)
**Before:**
```python
insert_data = {
    "user_id": current_user.id,
    "experience_id": experience.id,
    "funding_id": funding.id,
    "story": analysis.story,
    "rationale": analysis.rationale,
    "experience_rating": analysis.experience_rating  # ❌ Old field
}
```

**After:**
```python
insert_data = {
    "user_id": current_user.id,
    "experience_id": experience.id,
    "funding_id": funding.id,
    "story": analysis.story,
    "rationale": analysis.rationale,
    "experience_rating_facet_a": analysis.experience_rating_facet_a,  # ✅ New facet fields
    "experience_rating_facet_b": analysis.experience_rating_facet_b,
    "experience_rating_facet_c": analysis.experience_rating_facet_c,
    "experience_rating_facet_d": analysis.experience_rating_facet_d
}
```

## Error Fixed

### Original Error:
```
pydantic_core._pydantic_core.ValidationError: 4 validation errors for StoryTellingResponse
experience_rating_facet_a
  Field required [type=missing, ...]
experience_rating_facet_b
  Field required [type=missing, ...]
experience_rating_facet_c
  Field required [type=missing, ...]
experience_rating_facet_d
  Field required [type=missing, ...]
```

### Root Cause:
The route was trying to construct `StoryTellingResponse` objects using the old `experience_rating` field name, but the model now expects four separate facet score fields.

## Impact

✅ **GET `/fundings/{funding_id}/analyses`** - Now correctly reads four facet scores from database  
✅ **POST `/fundings/{funding_id}/analyze-experiences`** - Now correctly:
  - Reads cached analyses with four facet scores
  - Receives LLM responses with four facet scores  
  - Saves four facet scores to database

## Data Flow (Complete)

```
User Request → Analyze Experiences
    ↓
Check Database Cache
    ↓
If cached: Load StoryTellingResponse(facet_a, facet_b, facet_c, facet_d, ...)
    ↓
If not cached: Call LLM → StoryTeller.tell_story()
    ↓
LLM Returns: {facet_a: 4, facet_b: 3, facet_c: 5, facet_d: 4, story: "...", rationale: "..."}
    ↓
Save to DB: INSERT experience_rating_facet_a/b/c/d
    ↓
Return ExperienceAnalysis to Frontend
    ↓
Frontend Displays: Four color-coded progress bars
```

## Testing

The server automatically hot-reloaded with these changes. Try:
1. Analyze experiences on a funding detail page
2. Verify LLM returns four facet scores  
3. Check database has all four facet score columns populated
4. Verify frontend displays four progress bars correctly

## Complete Migration Checklist

✅ **SQL Schema** - experience_analysis table has facet_a/b/c/d columns  
✅ **Python Models** - StoryTellingResponse uses facet fields  
✅ **Story Teller** - Prompt and schema request facet scores  
✅ **Routes** - funding.py reads/writes facet scores  
✅ **TypeScript Types** - StoryTellingResponse interface updated  
✅ **Frontend UI** - FundingDetail.tsx displays four facet scores  

## Status: ✅ COMPLETE

All components are now aligned and using the four-facet scoring system!
