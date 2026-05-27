# Issue #4 Maintainer Comment Template

Thanks for the detailed report and screenshots 🙌

We have published a stabilization checkpoint to `main` and re-checked the multi-topic items from #4.

## Current status

- ✅ File path fields are editable (paste/edit supported).
- ✅ `TimeTaken` and completion status (`Completed: ...`) are shown.
- ✅ FT232H divisor option (`2` / `4`) is available and persisted.
- ⚠️ Detecting chip while a write is still running can still be confusing in some cases.
- ⚠️ Oversized image write errors are safe/failing correctly, but clarity can still be improved.

## Help us close remaining items quickly

Please re-test on latest `main`. If anything is still wrong, open **one issue per symptom** and include:

1. Tool + programmer + chip used.
2. Exact reproduction steps.
3. The full `Commands:` line shown in UI.
4. Relevant global log excerpt.
5. Screenshot/video if possible.

This helps us reproduce and fix each remaining item faster and avoids mixing unrelated problems in one thread.
