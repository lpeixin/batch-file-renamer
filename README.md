# batch-file-renamer
A lightweight project for batch renaming files using customizable rules.

## Scripts

### 1. Smart Sequence Renamer (`scripts/smart_sequence_rename.py`)

This script renames files in a target directory based on a sequence rule (e.g., `IMG_1020`). It intelligently handles files that already match the naming convention.

**Features:**
- Renames non-compliant files to match the pattern `PREFIX + NUMBER + EXT`.
- Preserves files that already match the pattern.
- Skips numbers that are already taken to avoid collisions.
- Supports case-insensitive extension matching.

**Usage:**

```bash
python3 scripts/smart_sequence_rename.py <RULE> <TARGET_PATH> <EXTENSION>
```

**Arguments:**
- `RULE`: The naming pattern including the starting number (e.g., `IMG_1020`).
- `TARGET_PATH`: The path to the folder containing the files.
- `EXTENSION`: The file extension to target (e.g., `jpg`, `png`).

**Example:**

Rename all `.jpg` files in `./photos` to start from `IMG_1020`:

```bash
python3 scripts/smart_sequence_rename.py IMG_1020 ./photos jpg
```

If `./photos` contains:
- `random.jpg`
- `IMG_1020.jpg` (Already exists)
- `vacation.jpg`

The result will be:
- `IMG_1020.jpg` (Unchanged)
- `IMG_1021.jpg` (Was `random.jpg`)
- `IMG_1022.jpg` (Was `vacation.jpg`)
