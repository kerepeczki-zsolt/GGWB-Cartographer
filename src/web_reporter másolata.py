import os

def generate_multi_view_report():
    image_folder = 'research_gallery'
    images = os.listdir(image_folder)
    
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: 'Segoe UI', sans-serif; background: #0b0e14; color: #e0e0e0; padding: 20px; }
            .event-container { border: 1px solid #333; margin-bottom: 30px; padding: 20px; border-radius: 12px; background: #161b22; }
            .view-box { display: flex; gap: 20px; justify-content: space-around; }
            .view-card { text-align: center; flex: 1; }
            img { width: 100%; border-radius: 8px; border: 1px solid #444; }
            h2 { color: #58a6ff; border-bottom: 1px solid #333; padding-bottom: 10px; }
            .badge { background: #238636; padding: 4px 8px; border-radius: 5px; font-size: 0.8em; }
        </style>
    </head>
    <body>
        <h1>GGWB-Cartographer <span class="badge">Multi-View Expert Interface</span></h1>
    """

    # Csoportosítjuk a fájlokat esemény szerint
    events = set(f.replace('GRAVITY_SPY_', '').replace('DETCHAR_', '') for f in images if f.endswith('.png'))

    for event in sorted(events):
        html_content += f"""
        <div class="event-container">
            <h2>Event Analysis: {event.replace('.png', '').upper()}</h2>
            <div class="view-box">
                <div class="view-card">
                    <p><b>Gravity Spy Perspective</b></p>
                    <img src="{image_folder}/GRAVITY_SPY_{event}">
                </div>
                <div class="view-card">
                    <p><b>LIGO DetChar Perspective</b></p>
                    <img src="{image_folder}/DETCHAR_{event}">
                </div>
            </div>
        </div>
        """

    html_content += "</body></html>"
    with open("EXPERT_REPORT.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Szakértői jelentés legenerálva: EXPERT_REPORT.html")

if __name__ == "__main__":
    generate_multi_view_report()