# Project Tools

Utilities that are not part of the running application live here.

- `presentations/update_kavach_presentation.py` updates the original presentation while preserving it.
- `presentations/build_new_additions_presentation.py` builds the current additions and roadmap deck.

Run from the workspace root with:

```powershell
python kavach/tools/presentations/update_kavach_presentation.py
python kavach/tools/presentations/build_new_additions_presentation.py
```

These scripts write presentations to `docs/presentations/` and do not modify backend or frontend runtime code.
