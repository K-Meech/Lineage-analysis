from contextlib import nullcontext as does_not_raise
from pathlib import Path

import pytest

from track_converter.src.preprocess_ctc import preprocess_ctc_file


@pytest.fixture
def test_data_dir():
    return Path(__file__).parent.resolve() / "data"


@pytest.mark.parametrize(
    "tracks_file,expectation",
    [
        ("tracks_begin_larger_than_end_frame_by_one.txt", does_not_raise()),
        (
            "tracks_begin_larger_than_end_frame_by_many.txt",
            pytest.raises(ValueError, match=r"tracks start frame must be <= the tracks end frame"),
        ),
    ],
)
def test_validate_track_begin_end_frames(tracks_file, expectation, tmp_path, test_data_dir):
    """Test exception is raised for begin > than end, unless it is by a single frame."""
    tracks_in_path = test_data_dir / tracks_file
    tracks_out_path = tmp_path / "tracks_out.txt"

    with expectation:
        preprocess_ctc_file(tracks_in_path, tracks_out_path)
