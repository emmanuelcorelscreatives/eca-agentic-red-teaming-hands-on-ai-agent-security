# PROPOSED — NO RUN PERFORMED
# Application contract; no authorized worker is supplied.
from pathlib import Path
from tempfile import TemporaryDirectory


def proposed_case(case_id, authorized_worker, save_selected_record):
    evidence_dir = Path("evidence") / case_id
    with TemporaryDirectory(prefix=f"{case_id}-") as scratch:
        workspace = Path(scratch)
        # Call only a configured, authorized sandbox adapter.
        selected_record = authorized_worker(workspace)
        # Retain only permitted evidence, before context exit.
        save_selected_record(selected_record, evidence_dir)
    # Disposable workspace ends; persistent evidence stays.
