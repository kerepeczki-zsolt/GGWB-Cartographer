INTERFEROMETER_DATABASE = {
    "LHO": {"O3": {"width": 0.25, "height": 20.0}},
    "LLO": {"O3": {"width": 0.28, "height": 22.0}},
    "VIRGO": {"O3": {"width": 0.40, "height": 18.0}}
}

GLITCH_DICTIONARY = {
    "BLIP": {"desc": "Standard Blip (Tüske)", "tilt_limit": 0.1},
    "BLIP_TILTED": {"desc": "Dőlt Blip (Aszimmetrikus tüske)", "tilt_limit": 0.4},
    "TOMTE": {"desc": "Tomte (Rövid, zömök)", "tilt_limit": 0.1},
    "KOI_FISH": {"desc": "Koi Fish (Uszonyos talp)", "tilt_limit": 0.2},
    "WHISTLE": {"desc": "Whistle (Rádiófrekvenciás fütty)", "tilt_limit": 0.5},
    "SCATTERED_LIGHT": {"desc": "Scattered Light (Szórt fény)", "tilt_limit": 0.8},
    "HELIX": {"desc": "Helix (Spirális szerkezet)", "tilt_limit": 0.4},
    "SCRATCH": {"desc": "Scratch (Vízszintes karcolás)", "tilt_limit": 0.9},
    "POWER_LINE": {"desc": "Power Line (Hálózati zaj)", "tilt_limit": 1.0},
    "EXTREMELY_LOUD": {"desc": "Extremely Loud (Telítettség)", "tilt_limit": 0.0},
    "1080_LINES": {"desc": "1080 Lines (Vibrációs zaj)", "tilt_limit": 1.0}
}