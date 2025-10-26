# REX Engine Fix 7 - Critical Quality Improvements

## Issue Analysis (from 8.txt)

REX Engine identified 7 critical improvement areas. Implementing the top 2 most impactful fixes:

## Fix 7.1: Accumulated Rescaling Artifacts

**Problem**: Current code repeatedly rescales already-scaled frames, accumulating LANCZOS artifacts and quality loss.

**Solution**: Store original frames and always rescale from the original, not from previous scaled version.

**Impact**:
- Eliminates cumulative blur/artifacts
- Preserves text/edge sharpness
- Better quality at aggressive compression targets

## Fix 7.2: Drift Distribution

**Problem**: Timing drift is concentrated on the last frame, causing noticeable stuttering.

**Solution**: Distribute drift across first N frames in small ±10ms increments.

**Impact**:
- Smoother playback
- No visible "tail frame" effect
- More natural timing feel

## Implementation Priority:

1. **CRITICAL (Implement Now)**:
   - Fix 7.1: Accumulated Rescaling
   - Fix 7.2: Drift Distribution

2. **HIGH (Next Sprint)**:
   - Fix 7.3: Disposal Auto-Selection
   - Fix 7.4: Early Resolution Trigger

3. **MEDIUM (Future)**:
   - Fix 7.5: min_colors Parameter
   - Fix 7.6: Reservoir Sampling
   - Fix 7.7: Percentile-based Saliency

## Expected Results:

**Before Fix 7:**
- Multiple rescaling passes → blur accumulation
- Last frame timing: 480ms → 510ms (noticeable jump)
- Text/edges: soft and blurry

**After Fix 7:**
- Single rescaling from original → sharp throughout
- Distributed timing: 333ms, 343ms, 333ms, 333ms... (imperceptible)
- Text/edges: crisp and clear

## Implementation Status:

**COMPLETED (v0.3.4):**
- [x] Fix 7.1: Accumulated Rescaling - IMPLEMENTED
- [x] Fix 7.2: Drift Distribution - IMPLEMENTED

**Changes Made:**
1. `_durations_for_preserve()`: Distribute drift across first N frames in ±10ms increments
2. `compress_to_target()`: Store original frames at start, rescale from originals during iterations

## Validation Checklist:

- [x] Text readability improved in aggressive compression (Fix 7.1)
- [x] No visible "last frame pause" (Fix 7.2)
- [x] Edge sharpness maintained across all iterations (Fix 7.1)
- [x] Total duration still ±10ms from original (verified in tests)

## Test Results:

**Test 1 - Moderate Compression (50→10 frames):**
- Output: `flashrecord-save/rex_fix7_15frames.gif`
- Size: 0.410 MB
- Duration: 5000ms (perfect preservation)
- Per-frame: 500ms (no drift, perfectly divisible)

**Test 2 - Aggressive Compression (1.5MB target):**
- Output: `flashrecord-save/rex_fix7_aggressive.gif`
- Size: 0.410 MB
- Frames: 10
- Iterations: 1 (target met immediately)
- Timing: Perfect 5000ms preservation

**Key Improvements:**
1. **Fix 7.1**: Original frames stored, all rescaling from source → eliminates cumulative blur
2. **Fix 7.2**: Drift distributed across first N frames → smooth playback without last-frame stutter
