# flashgui Manual QA Checklist (Theme + Settings + Layout)

Date: 2026-05-18  
Scope: `flashgui.py` desktop UI behaviors around theme preview/apply/revert, settings load/save, and tab/sidebar mode persistence.

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

Tester: ****\_\_****  
Date: ****\_\_****
