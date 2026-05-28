# flashgui Manual QA Checklist (Theme + Settings + Layout)

Date: 2026-05-18  
Scope: `flashgui.py` desktop UI behaviors around theme preview/apply/revert, settings load/save, and tab/sidebar mode persistence.

## Automation status (as of 2026-05-28)

The following checklist coverage is now automated in `pytest`:

- `tests/test_theme_automation.py`
  - A1, A2, A3, A4
- `tests/test_settings_layout_automation.py`
  - B1, B2, B3, C1, C2, E5
- `tests/test_issue4_release_gate_automation.py`
  - D, E1, E2, E3, E4

Notes:

- Current automation is deterministic regression coverage focused on behavior contracts in code paths and persistence flow.
- Keep manual execution for subjective visual checks (exact color/contrast/look-and-feel), platform UX polish, and end-to-end hardware validation.
- Run automation with: `pytest -q`

## Pre-check

- Launch app from `flashgui/`.
- Open **Settings** tab.
- Confirm app is writable in current workspace (for settings file updates).

---

## A. Theme interaction sweep

### A1. Preview should be visual-only (not persisted)

1. In **Behavior > Theme**, pick a different theme than current.
2. Click **Preview**.

Expected:

- UI colors update immediately.
- Log contains: `Theme preview: <theme> (not yet saved)`.
- Close app **without Apply/Apply & Save**.
- Reopen app: previous saved theme should still be active.

Pass/Fail: \_**\_  
Notes: \_\_**

### A2. Revert should return to baseline (and visuals update)

1. From a previewed theme, click **Revert**.

Expected:

- Theme returns to baseline used when entering Settings (or last applied one if Apply was used in same session).
- UI visuals refresh accordingly.
- Log contains: `Theme reverted to: <theme>`.

Pass/Fail: \_**\_  
Notes: \_\_**

### A3. Default should apply first available theme and refresh visuals

1. Click **Default**.

Expected:

- Theme switches immediately.
- Visual palette refreshes (combobox list colors/bg updated for dark/light mode).
- Log contains: `Theme reset to default: <theme>`.

Pass/Fail: \_**\_  
Notes: \_\_**

### A4. Apply should persist and update future revert baseline

1. Select any valid theme.
2. Click **Apply**.
3. Preview another theme.
4. Click **Revert**.

Expected:

- Apply logs: `Theme applied and saved: <theme>`.
- Revert returns to the newly applied theme (not an older baseline).
- After restart, applied theme remains active.

Pass/Fail: \_**\_  
Notes: \_\_**

---

## B. Settings Management load/save sweep

### B1. Save to file should include current form values

1. Set obvious values in Settings form:
   - Theme
   - Tab mode checkbox
   - Beep checkbox
   - Font size
   - Flashrom/flashprog paths (dummy values are fine)
2. Click **Save to file…** and inspect JSON.

Expected JSON keys:

- `preferred_font`
- `font_size`
- `flashrom_bin`
- `flashprog_bin`
- `workspace_dir`
- `window_geometry`
- `log_file_path`
- `use_sudo`
- `auto_detect_programmer`
- `theme`
- `layout_mode`
- `beep_on_complete`

Pass/Fail: \_**\_  
Notes: \_\_**

### B2. Load from file should populate all mapped controls

1. Prepare a JSON with explicit values for all keys above.
2. Click **Load from file…**.

Expected controls update before Apply:

- Font family + size
- Flashrom/flashprog paths
- Workspace/log paths
- Use sudo / auto-detect / beep checkboxes
- Tab mode checkbox
- Theme combo value

Pass/Fail: \_**\_  
Notes: \_\_**

### B3. Boolean string tolerance (hardening check)

1. In the JSON used for load, set boolean-like strings:
   - `"use_sudo": "false"`
   - `"auto_detect_programmer": "true"`
   - `"beep_on_complete": "off"`
2. Load from file.

Expected:

- `use_sudo` unchecked.
- `auto_detect_programmer` checked.
- `beep_on_complete` unchecked.

Pass/Fail: \_**\_  
Notes: \_\_**

---

## C. Layout mode persistence sweep

### C1. Apply sidebar -> tab mode and restart

1. Check **Use tab navigation (instead of sidebar)**.
2. Click **Apply & Save**.
3. Restart app.

Expected:

- App starts in tab mode immediately.
- Sidebar is hidden on startup.
- No manual toggle needed.

Pass/Fail: \_**\_  
Notes: \_\_**

### C2. Apply tab -> sidebar mode and restart

1. Uncheck **Use tab navigation (instead of sidebar)**.
2. Click **Apply & Save**.
3. Restart app.

Expected:

- Sidebar visible on startup.
- Navigation buttons usable.

Pass/Fail: \_**\_  
Notes: \_\_**

---

## D. Regression spot-checks

1. Click **Apply & Save** with a valid theme and font size.
2. Confirm no exceptions in console/log.
3. Confirm operations pages still open and controls respond.

Expected:

- No crash.
- `Settings saved.` appears.
- Theme/font remain coherent after switching pages.

Pass/Fail: \_**\_  
Notes: \_\_**

---

## Quick verdict

- Theme flow: PASS / FAIL
- Settings load/save flow: PASS / FAIL
- Layout persistence: PASS / FAIL
- Overall: PASS / FAIL

Tester: \***\*\_\_\*\***  
Date: \***\*\_\_\*\***

---

## E. Issue #4 stabilization re-test (release gate)

### E1. Editable path + command visibility

1. Open **Read ROM** and **Write ROM** pages.
2. Paste a full absolute path into file fields.
3. Verify `Commands:` auto-populates and can be edited.

Expected:

- Path fields accept manual paste/edit.
- `Commands:` remains editable and reflects operation context.

Pass/Fail: \_**\_  
Notes: \_\_**

### E2. Completion clarity and timing

1. Run one successful operation (read or verify).
2. Confirm final status fields/log entries.

Expected:

- `TimeTaken: ...` appears.
- `Completed: Ok` (or error state) appears clearly.

Pass/Fail: \_**\_  
Notes: \_\_**

### E3. Oversized image write behavior

1. Choose a ROM image larger than target chip.
2. Run **Write ROM**.

Expected:

- Write is blocked by preflight before flashing starts.
- Error clearly reports image size and chip size.
- Completion state is fail/error with no ambiguity.

Pass/Fail: \_**\_  
Notes: \_\_**

### E4. Detect during active write (race check)

1. Start a write operation.
2. While write is active, trigger detect chip.

Expected:

- Detect action is blocked while write is active (no misleading mid-write probe result).
- Log/status clearly instructs user to wait until operation completes.

Pass/Fail: \_**\_  
Notes: \_\_**

### E5. FT232H divisor persistence

1. Set divisor to `2`.
2. Detect programmer and run an operation.
3. Restart app and verify saved value.

Expected:

- Selected divisor remains applied/persisted.
- No unexpected reset to `4` unless invalid value is provided.

Pass/Fail: \_**\_  
Notes: \_\_**
