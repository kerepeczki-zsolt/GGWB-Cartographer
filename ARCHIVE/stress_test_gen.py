import os
import shutil
import random

def prepare_stress_test():
    source_base = r"C:\Users\vivob\Documents\TrainingSet"
    target_dir = r"C:\Users\vivob\Desktop\GGWB-Clone\IDEGEN_TESZT"
    
    # Takarítás
    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)
    os.makedirs(target_dir)
    
    all_samples = []
    categories = [d for d in os.listdir(source_base) if os.path.isdir(os.path.join(source_base, d))]
    
    for cat in categories:
        cat_path = os.path.join(source_base, cat)
        images = [f for f in os.listdir(cat_path) if f.lower().endswith(('.png', '.jpg'))]
        for img in images:
            all_samples.append((cat, os.path.join(cat_path, img)))
    
    # Kiválasztunk 20 véletlenszerű hibát
    test_selection = random.sample(all_samples, 20)
    
    print(f"--- STRESSZ-TESZT ELŐKÉSZÍTÉSE ---")
    log_truth = []
    for i, (original_cat, path) in enumerate(test_selection):
        new_name = f"mystery_glitch_{i+1}.png"
        shutil.copy(path, os.path.join(target_dir, new_name))
        log_truth.append(f"{new_name}: {original_cat}")
        print(f"Minta {i+1}/20 átmásolva...")

    # Elmentjük a "valóságot", hogy ellenőrizni tudjuk a gépet
    with open("truth_log.txt", "w") as f:
        f.write("\n".join(log_truth))
    
    print(f"\nSiker! 20 hiba bekeverve az IDEGEN_TESZT mappába.")
    print(f"A megoldókulcs elmentve: truth_log.txt")

if __name__ == "__main__":
    prepare_stress_test()