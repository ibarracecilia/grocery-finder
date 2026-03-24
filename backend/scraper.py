import requests
from bs4 import BeautifulSoup
import json

# URL de Coto (página de promociones)
url = "https://www.cotodigital3.com.ar/sitios/supermercado/listado-de-ofertas/"

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Datos de ejemplo (mientras aprendemos)
    data = {
        "coto": {
            "name": "Coto",
            "products": {
                "leche": 180,
                "yogur": 150,
                "naranjas": 250,
                "huevos": 160
            }
        },
        "jumbo": {
            "name": "Jumbo",
            "products": {
                "leche": 175,
                "yogur": 140,
                "naranjas": 240,
                "huevos": 175
            }
        },
        "disco": {
            "name": "Disco",
            "products": {
                "leche": 190,
                "yogur": 155,
                "naranjas": 220,
                "huevos": 170
            }
        }
    }
    
    # Guardar en JSON
    with open('../data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("✅ Datos guardados en data.json")
    
except Exception as e:
    print(f"❌ Error: {e}")
