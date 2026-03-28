# 🛒 GroceryFinder

**Compará precios de supermercados en Buenos Aires al instante.**

GroceryFinder es una aplicación web que permite a los usuarios comparar precios de productos entre los principales supermercados de Argentina (Coto, Jumbo y Disco), encontrar el mejor precio disponible y acceder a cupones de descuento.

🌐 **App en vivo:** [grocery-finder.onrender.com](https://grocery-finder.onrender.com)

---

## ✨ Funcionalidades

- **Comparación de precios** en tiempo real entre Coto, Jumbo y Disco
- **24 productos** organizados en 6 categorías (Lácteos, Frutas y Verduras, Carnes, Almacén, Bebidas, Limpieza)
- **Autocompletado inteligente** en la búsqueda
- **Precios promocionales** con fecha de vencimiento y porcentaje de ahorro
- **Cupones de descuento** por supermercado con código copiable
- **Bilingüe** — interfaz disponible en Español e Inglés (precios siempre en ARS)
- **Modal de detalle** al tocar un precio con información completa del scraping
- **Diseño responsive** optimizado para celular y desktop
- **Detección del mejor precio** resaltado automáticamente

---

## 🛠️ Tecnologías

- **Python / Flask** — Backend y API REST
- **SQLite** — Base de datos
- **HTML / CSS / JavaScript** — Frontend (single-page app)
- **Gunicorn** — Servidor de producción
- **Render** — Hosting y deploy automático
- **Git / GitHub** — Control de versiones

---

## 🚀 Cómo ejecutar localmente
```bash
cat > ~/grocery-finder/README.md << 'READMEEOF'
# 🛒 GroceryFinder

**Compará precios de supermercados en Buenos Aires al instante.**

GroceryFinder es una aplicación web que permite a los usuarios comparar precios de productos entre los principales supermercados de Argentina (Coto, Jumbo y Disco), encontrar el mejor precio disponible y acceder a cupones de descuento.

🌐 **App en vivo:** [grocery-finder.onrender.com](https://grocery-finder.onrender.com)

---

## ✨ Funcionalidades

- **Comparación de precios** en tiempo real entre Coto, Jumbo y Disco
- **24 productos** organizados en 6 categorías (Lácteos, Frutas y Verduras, Carnes, Almacén, Bebidas, Limpieza)
- **Autocompletado inteligente** en la búsqueda
- **Precios promocionales** con fecha de vencimiento y porcentaje de ahorro
- **Cupones de descuento** por supermercado con código copiable
- **Bilingüe** — interfaz disponible en Español e Inglés (precios siempre en ARS)
- **Modal de detalle** al tocar un precio con información completa del scraping
- **Diseño responsive** optimizado para celular y desktop
- **Detección del mejor precio** resaltado automáticamente

---

## 🛠️ Tecnologías

- **Python / Flask** — Backend y API REST
- **SQLite** — Base de datos
- **HTML / CSS / JavaScript** — Frontend (single-page app)
- **Gunicorn** — Servidor de producción
- **Render** — Hosting y deploy automático
- **Git / GitHub** — Control de versiones

---

## 🚀 Cómo ejecutar localmente
```bash
git clone https://github.com/ibarracecilia/grocery-finder.git
cd grocery-finder
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Abrir en el navegador: http://localhost:5000

---

## 🗺️ Roadmap

- Web scraping real de sitios de supermercados
- Lista de compras con total por supermercado
- Historial de precios con gráficos
- PWA (instalable en celular)
- Más supermercados (Día, Carrefour, Changomas)

---

## 👩‍💻 Autora

**Cecilia Ibarra**
📧 ceciliaibarra.dev@gmail.com
🔗 [GitHub](https://github.com/ibarracecilia)

## 📄 Licencia

Este proyecto es open source bajo la licencia MIT.
