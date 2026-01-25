# main.py - GGWB-Cartographer V12 Milestone - VÉGLEGES
import cartographer_v12_expert_final as v12

def start_mapping():
    print("--- GGWB-Cartographer V12 ---")
    print("Státusz: Stabil (Nagy adathalmazok leválasztva)")
    
    try:
        # A terminálod alapján ez a pontos funkció név:
        print("Szakértői modul indítása...")
        v12.GGWBCartographerV12_Expert() 
        
        print("\n--- SIKERES ANALÍZIS ---")
    except Exception as e:
        print(f"\nHiba a futtatás során: {e}")

if __name__ == "__main__":
    start_mapping()