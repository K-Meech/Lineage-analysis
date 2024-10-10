import logging
from pathlib import Path

import numpy as np
import pandas as pd

from track_converter.src.preprocess_ctc import preprocess_ctc_file
from track_converter.src.utils import check_dead_spots_have_no_children, convert_to_ctc

logging.basicConfig(format="%(levelname)s: %(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def _read_trackmate_csv(csv_filepath: Path) -> pd.DataFrame:
    # First four rows of a trackmate csv are headers - keep first and discard rest
    return pd.read_csv(csv_filepath, skiprows=[1, 2, 3])


def _read_dead_cell_labels(spots: pd.DataFrame, edges: pd.DataFrame, dead_label: str) -> np.array:
    dead_spots = spots.loc[dead_label == spots.LABEL, :]
    check_dead_spots_have_no_children(dead_spots, edges, "ID", "SPOT_SOURCE_ID")
    return dead_spots.ctc_label.unique()


def preprocess_trackmate_file(
    spots_csv_filepath: Path, edges_csv_filepath: Path, output_ctc_filepath: Path, dead_label: str | None = None
) -> None:
    """Preprocess trackmate format files."""
    spots = _read_trackmate_csv(spots_csv_filepath)
    edges = _read_trackmate_csv(edges_csv_filepath)

    ctc_table, spots = convert_to_ctc(spots, edges, "ID", "FRAME", "SPOT_SOURCE_ID", "SPOT_TARGET_ID", "TRACK_ID")

    if dead_label is not None:
        dead_ctc_labels = _read_dead_cell_labels(spots, edges, dead_label)
    else:
        dead_ctc_labels = []

    logger.info("Extracted CTC table from trackmate files")

    preprocess_ctc_file(ctc_table, output_ctc_filepath, default_right_censor=True, dead_cell_labels=dead_ctc_labels)
