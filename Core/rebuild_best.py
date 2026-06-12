import json
from Core.best_manager import build_best
from Core.exporter import export_best_sets
from Core.logger import log
def main():
    try:
        log("Loading database for best list rebuild...")
        with open("database/database.json", "r", encoding="utf-8") as f: db = json.load(f)
        log("Building best sets...")
        best_sets = build_best(db)
        log("Exporting best sets...")
        export_best_sets(best_sets)
        log("✅ Best lists rebuilt and exported successfully.")
    except Exception as e:
        log(f"❌ CRITICAL ERROR in rebuild: {e}")
        import traceback
        traceback.print_exc()
if __name__ == "__main__": main()
