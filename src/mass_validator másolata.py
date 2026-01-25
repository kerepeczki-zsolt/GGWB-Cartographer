from gwpy.timeseries import TimeSeries
from geometrical_glitch_detector import GeometricalExpertSystem
import os

def run_stress_test():
    expert = GeometricalExpertSystem()
    test_bench = [
        ("H1", 1126259462, "GW EVENT"),
        ("L1", 1187008882, "SCATTERED LIGHT"),
        ("H1", 1242442967, "BLIP GLITCH"),
        ("L1", 1164556817, "WHISTLE"),
        ("H1", 1239082483, "POWER LINE")
    ]
    
    print("\n" + "="*60)
    print("GGWB-CARTOGRAPHER: TÖMEGES VALIDÁCIÓS TESZT")
    print("="*60)

    for det, gps, expected in test_bench:
        try:
            print(f"\nElemzés: {expected} ({det} @ {gps})")
            data = TimeSeries.fetch_open_data(det, gps - 1, gps + 1)
            white_data = data.whiten()
            q_trans = white_data.q_transform(frange=(20, 1500))
            
            freq_max = q_trans.frequencies[q_trans.argmax() // q_trans.shape[1]].value
            
            # A rendszered diagnózisa
            diag = expert.analyze_modification(det, "O3", 0.2, 50.0, freq_max, 0.05)
            
            print(f"-> Eredmény: {diag}")
            
            # Mentés az utókornak
            plot = q_trans.plot()
            ax = plot.gca()
            ax.set_title(f"TEST: {expected} | RESULT: {diag}")
            plot.save(f"research_gallery/VALIDATION_{expected.replace(' ', '_')}.png")
            plot.close()
            
        except Exception as e:
            print(f"Hiba a(z) {expected} tesztelésekor: {e}")

if __name__ == "__main__":
    run_stress_test()