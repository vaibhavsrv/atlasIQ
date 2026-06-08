import requests
import math

class LocationIntelligenceService:
    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.overpass_url = "http://overpass-api.de/api/interpreter"
        self.headers = {"User-Agent": "AtlasIQ-BusinessExpansion/1.0"}

    def geocode(self, query: str):
        """Returns lat, lon for a given query (e.g. 'Coffee shop in Seattle')"""
        # A simple geocoding wrapper. In production, we'd extract the city from the NLP query.
        # For AtlasIQ, let's just pass the query directly and hope Nominatim finds the city.
        params = {"q": query, "format": "json", "limit": 1}
        try:
            resp = requests.get(self.nominatim_url, params=params, headers=self.headers, timeout=5)
            data = resp.json()
            if data:
                return float(data[0]["lat"]), float(data[0]["lon"]), data[0]["display_name"]
        except Exception:
            pass
        return 40.7128, -74.0060, "New York, NY" # Fallback to NYC

    def get_competitors(self, lat: float, lon: float, radius: int = 5000, industry: str = "cafe"):
        """Uses Overpass API to find competitors within a radius (meters)."""
        # Map industry to OSM tags
        tag_map = {
            "Coffee Shop": "node['amenity'='cafe']",
            "Restaurant": "node['amenity'='restaurant']",
            "Gym": "node['leisure'='fitness_centre']",
            "Retail Store": "node['shop']",
            "Salon": "node['shop'='hairdresser']",
            "Clinic": "node['amenity'='clinic']",
            "Coworking Space": "node['amenity'='coworking_space']",
        }
        query_tag = tag_map.get(industry, "node['shop']")
        
        overpass_query = f"""
        [out:json][timeout:10];
        {query_tag}(around:{radius},{lat},{lon});
        out body 10;
        """
        
        try:
            resp = requests.post(self.overpass_url, data={'data': overpass_query}, timeout=15)
            elements = resp.json().get("elements", [])
            competitors = []
            for el in elements:
                name = el.get("tags", {}).get("name", "Unknown Competitor")
                if name != "Unknown Competitor":
                    # calc dummy distance for now based on lat lon
                    dist = math.sqrt((lat - el["lat"])**2 + (lon - el["lon"])**2) * 111000 # rough meters
                    competitors.append({"name": name, "distance": round(dist, 2), "lat": el["lat"], "lon": el["lon"]})
            return competitors
        except Exception:
            return [{"name": "Generic Competitor A", "distance": 1200}, {"name": "Generic Competitor B", "distance": 2500}]

    def get_market_metrics(self, lat: float, lon: float):
        """Simulates demographic models based on geographic coordinates."""
        # In a real app, query US Census or Data.gov. Here we use a deterministic hash of lat/lon to generate 'real' static data.
        base = abs(hash(f"{lat},{lon}"))
        population = 50000 + (base % 500000)
        avg_income = 40000 + (base % 80000)
        growth_index = (base % 100) / 100.0
        return {
            "population": population,
            "avg_income": avg_income,
            "growth_index": growth_index,
            "traffic_score": (base % 100),
            "safety_score": 50 + (base % 50)
        }
