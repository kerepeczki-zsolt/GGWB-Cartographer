from gwpy.timeseries import TimeSeries
from geometrical_glitch_detector import GeometricalExpertSystem
import os

def hunt_for_event(event_name):
    # Híres LIGO események GPS koordinátái
    events = {
        "FIRST_WAVE": 1126259462,      # Az első (GW150914)
        "NEUTRON_STAR": 1187008882,    # Két neutroncsillag (GW170817)
        "BIG_BLACK_HOLE": 1242442967   # Óriás fekete lyukak (GW190521)
    }
    
    gps_time = events.get(event_name)
    if not gps_time:
        print("Ismeretlen esemény!")
        return

    print(f"\n--- VADÁSZAT INDÍTÁSA: {event_name} ---")
    expert = GeometricalExpertSystem()
    
    try:
        data = TimeSeries.fetch_open_data('H1', gps_time - 2, gps_time + 2)
        white_data = data.whiten()
        q_trans = white_data.q_transform(frange=(20, 1000))
        
        # A legerősebb pont keresése az elemzéshez
        freq_at_max = q_trans.frequencies[q_trans.argmax() // q_trans.shape[1]].value
        diagnosis = expert.analyze_modification('H1', "O3", 0.2, 50.0, freq_at_max, 0.05)
        
        plot = q_trans.plot()
        ax = plot.gca()
        ax.set_title(f"EVENT: {event_name} | DIAGNOSIS: {diagnosis}")
        ax.set_yscale('log')
        
        save_path = f"research_gallery/HUNTED_{event_name}.png"
        plot.save(save_path)
        print(f"A vadászat sikeres! A trófea itt van: {save_path}")
        print(f"Szakértői besorolás: {diagnosis}")

    except Exception as e:
        print(f"A vadászat sikertelen: {e}")

if __name__ == "__main__":
    # Válassz egyet: "FIRST_WAVE", "NEUTRON_STAR", "BIG_BLACK_HOLE"
    hunt_for_event("NEUTRON_STAR")