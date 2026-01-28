def generate(validation):
    report = f"""
GGWB-CARTOGRAPHER REPORT (V13 CORE)
-----------------------
Candidates found: {validation['count']}
Statistically valid: {validation['valid']}
Status: OPERATIONAL
"""
    return report