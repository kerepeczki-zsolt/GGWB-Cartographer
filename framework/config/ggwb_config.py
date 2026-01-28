# framework/config/ggwb_config.py

CONFIG = {
    "sample_rate": 4096,
    "f_min": 20,
    "f_max": 2000,
    "detectors": ["H1", "L1"],
    "channels": {
        "H1": "H1:GDS-CALIB_STRAIN",
        "L1": "L1:GDS-CALIB_STRAIN"
    },
    "file_names": {
        "H1": "GITHUB_STRESS_TEST_1000.csv",
        "L1": "L1_O3b_mini.csv"
    },
    "paths": {
        "data": "data/raw/",
        "results": "results/",
        "archive": "archive/"
    }
}