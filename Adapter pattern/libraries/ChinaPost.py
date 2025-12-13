class ChinaPostApi:
    def connect(self):
        print("    [ChinaPost External] Connecting to Great Firewall servers... OK.")
    def calculate_delivery_cny(self,weight_grams: int,distance_km: float) -> float:
        price = (weight_grams * 0.05) +10
        print(f"    [ChinaPost External] Calculated: {weight_grams}g over {distance_km}km = {price} CNY")
        return price
    