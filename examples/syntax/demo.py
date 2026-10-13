import json
from core import empty_prices, labels, prices, unique

if __name__ == "__main__":
    print(json.dumps({"empty": list(empty_prices()),
                      "labels": list(labels().ordered_entries()),
                      "prices": list(prices()),
                      "unique": list(unique().ordered_values())},
                     sort_keys=True, separators=(",", ":")))
