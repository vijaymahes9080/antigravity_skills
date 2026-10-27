---
name: workflow-automation-scripting
description: Automated repetitive workflows, batch document processing, Excel/CSV spreadsheet manipulation, headless API pipelines, and cross-platform scripting in Node.js and Python.
---

# Workflow Automation & Data Pipeline Scripting

## 1. Intended Role & Domain
- **Primary Domain**: Automation & Productivity
- **Target Roles**: Workflow Automation Engineer, Business Process Automation Specialist, Spreadsheet Automation Specialist
- **Architectural Layer**: Layer 2 (Specialized Technical Skills)

## 2. Activation Conditions
- **Direct Triggers**: "automate workflow", "batch process files", "spreadsheet automation", "excel csv automation", "data munging script", "automate repetitive tasks", "etl script".
- **Contextual Inferences**: High-frequency repetitive manual tasks, parsing multi-file directories, transforming data formats.
- **Chained Predecessors**: `task-decomposition`.

## 3. Explicit Exclusions
- Do NOT use when:
  - Building complex interactive multi-page frontend web applications.
  - Designing low-level embedded hardware firmware.

## 4. Required Inputs & Context
- Input files or directory path (CSVs, Excel `.xlsx`, JSON, XML, PDFs).
- Transformation and business rules specification.
- Output destination and format requirement.

## 5. Expected Outputs & Artifacts
- Idempotent automation script (Python or Node.js).
- Cleaned and normalized output files with validation audit logs.
- CLI argument interface (`--input`, `--output`, `--dry-run`, `--verbose`).
- Automated integration test asserting data transformation accuracy.

## 6. Step-by-Step Operating Procedure
1. **Input Inspection & Batch Discovery**:
   - Safely discover and count files matching the target glob pattern without loading entire directories into memory.
2. **Schema & Header Normalization**:
   - Handle encoding variations (UTF-8, UTF-16, Latin-1) and normalize dirty column headers.
3. **Chunked Transformation & Idempotency**:
   - Process large datasets in chunks/streams (e.g. streaming CSV parser) to preserve memory.
   - Guarantee idempotency: running the script multiple times produces identical clean output without duplicates.
4. **Dry-Run Mode & Error Logging**:
   - Implement `--dry-run` flag to display proposed changes and record malformed rows to an error ledger (`errors.log`).
5. **Atomic Output Writing**:
   - Write processed results to temporary files before atomically moving them to final destinations.

## 7. Repository Inspection & Planning Requirements
- Non-destructive inspection of source data:
  ```bash
  head -n 5 data/*.csv 2>/dev/null || echo "Data files check"
  ```
- Preservation rule: Never overwrite raw input files; always write transformed data to an output directory or distinct filename.

## 8. Tool & Dependency Requirements
- Python 3.10+ (with `pandas` or `openpyxl`) or Node.js 20+ (with `csv-parse`, `exceljs`), `argparse`.

## 9. Implementation Guidelines & Best Practices
- Always implement a progress indicator or step logger for long-running batch operations.
- Handle missing values and type coercions explicitly:

```python
import argparse
import csv
import sys
from pathlib import Path

def process_records(input_path: Path, output_path: Path, dry_run: bool = False):
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    processed_count = 0
    with open(input_path, mode='r', encoding='utf-8', errors='replace') as infile:
        reader = csv.DictReader(infile)
        fieldnames = [col.strip().lower().replace(" ", "_") for col in reader.fieldnames]
        
        rows = []
        for row in reader:
            normalized_row = {
                k.strip().lower().replace(" ", "_"): v.strip() 
                for k, v in row.items()
            }
            # Business logic transformation
            normalized_row['status'] = normalized_row.get('status', 'PENDING').upper()
            rows.append(normalized_row)
            processed_count += 1

    if dry_run:
        print(f"[DRY-RUN] Processed {processed_count} rows. No files written.")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_output = output_path.with_suffix('.tmp')
    with open(temp_output, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    temp_output.replace(output_path)
    print(f"Successfully wrote {processed_count} records to {output_path}")
```

## 10. Error Handling & Recovery Procedures
- Corrupt row in 1,000,000 line CSV: Catch row parsing error, log line number and raw text to `dead_letter.csv`, and continue processing remaining rows.
- Out of disk space: Check available disk space before writing large uncompressed outputs.

## 11. Security & Privacy Constraints
- Sanitize spreadsheet formula injection: Prepend apostrophes (`'`) to strings starting with `=`, `+`, `-`, or `@` to prevent execution in spreadsheet software.

## 12. Verification & Testing Requirements
- Unit test transformation logic:
  ```bash
  pytest tests/test_automation_script.py -v
  ```
- Test `--dry-run` execution:
  ```bash
  python script.py --input test.csv --dry-run
  ```

## 13. Completion Criteria
- Script processes input files end-to-end without unhandled crashes.
- Dry-run mode functions accurately.
- Transformed data passes schema validation.

## 14. Relevant Official References
- Python Standard Library: `csv`, `pathlib`, `argparse`.
- OWASP CSV Injection Prevention Cheat Sheet.

## 15. Maintenance & Compatibility Notes
- Last audited: October 2026. Cross-platform compatible across Linux, macOS, and Windows.
