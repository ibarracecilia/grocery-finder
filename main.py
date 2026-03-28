from flask import Flask, request, jsonify, make_response
import sqlite3
import os
from datetime import datetime, timedelta

app = Flask(__name__)
DATABASE = '/tmp/grocery.db'

def init_db():
    if os.path.exists(DATABASE):
        return
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('CREATE TABLE supermarkets (id INTEGER PRIMARY KEY, nombre TEXT)')
    c.execute('CREATE TABLE productos (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, cantidad TEXT)')
    c.execute('CREATE TABLE precios (id INTEGER PRIMARY KEY, supermercado_id INTEGER, producto_id INTEGER, precio REAL, precio_promo REAL, promo_vence TEXT, fecha_scraping TEXT)')
    c.execute("INSERT INTO supermarkets VALUES (1, 'Coto')")
    c.execute("INSERT INTO supermarkets VALUES (2, 'Jumbo')")
    c.execute("INSERT INTO supermarkets VALUES (3, 'Disco')")
    productos = [
        (1,'Leche Entera','1L'),(2,'Yogur Natural','200g'),(3,'Naranjas','1kg'),
        (4,'Huevos','12 unidades'),(5,'Queso Cremoso','1kg'),(6,'Manteca','200g'),
        (7,'Pan Lactal','500g'),(8,'Arroz','1kg'),(9,'Fideos Secos','500g'),
        (10,'Aceite de Girasol','1.5L'),(11,'Az\u00facar','1kg'),(12,'Harina','1kg'),
        (13,'Galletitas Dulces','300g'),(14,'Gaseosa Cola','2.25L'),(15,'Agua Mineral','2L'),
        (16,'Papel Higi\u00e9nico','4 rollos'),(17,'Detergente','750ml'),(18,'Jab\u00f3n en Polvo','800g'),
        (19,'Pollo Entero','1kg'),(20,'Carne Picada','1kg'),(21,'Banana','1kg'),
        (22,'Tomate','1kg'),(23,'Papa','1kg'),(24,'Cebolla','1kg'),
    ]
    for p in productos:
        c.execute('INSERT INTO productos VALUES (?, ?, ?)', p)
    hoy = datetime.now().strftime('%Y-%m-%d')
    pv1 = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
    pv2 = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
    precios = [
        (1,1,1,1250,1100,pv1,hoy),(2,2,1,1240,None,None,hoy),(3,3,1,1230,1150,pv2,hoy),
        (4,1,2,890,None,None,hoy),(5,2,2,850,790,pv1,hoy),(6,3,2,920,None,None,hoy),
        (7,1,3,1500,1350,pv1,hoy),(8,2,3,1420,None,None,hoy),(9,3,3,1380,None,None,hoy),
        (10,1,4,2300,None,None,hoy),(11,2,4,2190,1990,pv2,hoy),(12,3,4,2410,None,None,hoy),
        (13,1,5,4200,None,None,hoy),(14,2,5,4100,3800,pv1,hoy),(15,3,5,4350,None,None,hoy),
        (16,1,6,1800,None,None,hoy),(17,2,6,1750,None,None,hoy),(18,3,6,1900,1700,pv1,hoy),
        (19,1,7,1600,1400,pv1,hoy),(20,2,7,1550,None,None,hoy),(21,3,7,1580,None,None,hoy),
        (22,1,8,1100,None,None,hoy),(23,2,8,1050,950,pv2,hoy),(24,3,8,1150,None,None,hoy),
        (25,1,9,750,None,None,hoy),(26,2,9,720,None,None,hoy),(27,3,9,780,690,pv1,hoy),
        (28,1,10,2200,1990,pv1,hoy),(29,2,10,2150,None,None,hoy),(30,3,10,2300,None,None,hoy),
        (31,1,11,950,None,None,hoy),(32,2,11,920,None,None,hoy),(33,3,11,980,850,pv2,hoy),
        (34,1,12,650,None,None,hoy),(35,2,12,630,550,pv1,hoy),(36,3,12,680,None,None,hoy),
        (37,1,13,1200,None,None,hoy),(38,2,13,1150,None,None,hoy),(39,3,13,1250,1100,pv1,hoy),
        (40,1,14,1800,1600,pv2,hoy),(41,2,14,1750,None,None,hoy),(42,3,14,1850,None,None,hoy),
        (43,1,15,800,None,None,hoy),(44,2,15,780,None,None,hoy),(45,3,15,820,700,pv1,hoy),
        (46,1,16,1500,None,None,hoy),(47,2,16,1450,1300,pv1,hoy),(48,3,16,1550,None,None,hoy),
        (49,1,17,950,None,None,hoy),(50,2,17,920,None,None,hoy),(51,3,17,980,880,pv2,hoy),
        (52,1,18,2100,1900,pv1,hoy),(53,2,18,2050,None,None,hoy),(54,3,18,2200,None,None,hoy),
        (55,1,19,2800,None,None,hoy),(56,2,19,2700,2500,pv1,hoy),(57,3,19,2900,None,None,hoy),
        (58,1,20,4500,None,None,hoy),(59,2,20,4400,None,None,hoy),(60,3,20,4600,4200,pv2,hoy),
        (61,1,21,1200,1050,pv1,hoy),(62,2,21,1150,None,None,hoy),(63,3,21,1250,None,None,hoy),
        (64,1,22,1800,None,None,hoy),(65,2,22,1750,1600,pv1,hoy),(66,3,22,1850,None,None,hoy),
        (67,1,23,900,None,None,hoy),(68,2,23,850,None,None,hoy),(69,3,23,950,800,pv1,hoy),
        (70,1,24,800,700,pv2,hoy),(71,2,24,780,None,None,hoy),(72,3,24,820,None,None,hoy),
    ]
    for p in precios:
        c.execute('INSERT INTO precios VALUES (?, ?, ?, ?, ?, ?, ?)', p)
    conn.commit()
    conn.close()

HTML_PAGE = r'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GroceryFinder</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
<style>
:root{
--bg:#fafaf8;--card:#fff;--card2:#f5f3ef;--border:#e8e5df;--text:#1a1a18;--text2:#6b6960;--text3:#9e9a90;
--accent:#0d9488;--accent2:#06b6a4;--accent-bg:#e6faf7;--accent-glow:rgba(13,148,136,0.12);
--red:#e8553a;--red-bg:#fef0ec;--green:#1a9e6f;--green-bg:#e8f8f0;
--shadow-sm:0 1px 2px rgba(26,26,24,0.04);--shadow-md:0 4px 20px rgba(26,26,24,0.06);--shadow-lg:0 12px 40px rgba(26,26,24,0.08);
--shadow-glow:0 0 40px rgba(13,148,136,0.08);--radius:16px;
}
[data-theme="dark"]{
--bg:#111110;--card:#1c1c1a;--card2:#242422;--border:#333330;--text:#f0ede6;--text2:#a09d94;--text3:#6b6960;
--accent:#2dd4bf;--accent2:#5eead4;--accent-bg:#0d2d28;--accent-glow:rgba(45,212,191,0.15);
--red:#f87171;--red-bg:#3b1515;--green:#34d399;--green-bg:#0d3320;
--shadow-sm:0 1px 2px rgba(0,0,0,0.2);--shadow-md:0 4px 20px rgba(0,0,0,0.3);--shadow-lg:0 12px 40px rgba(0,0,0,0.4);
--shadow-glow:0 0 40px rgba(45,212,191,0.1);
}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'DM Sans',sans-serif;background:var(--bg);color:var(--text);min-height:100vh;transition:background .4s,color .4s}
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes scaleIn{from{transform:scale(.95);opacity:0}to{transform:scale(1);opacity:1}}
@keyframes pulseNode{0%,100%{opacity:.2;r:2.5}50%{opacity:.8;r:3.5}}
@keyframes glowCore{0%,100%{opacity:.5}50%{opacity:1}}
@keyframes pulsePin{0%,100%{opacity:.4}50%{opacity:.8}}
@keyframes splashFade{from{opacity:1}to{opacity:0;pointer-events:none}}
@keyframes splashPulse{0%,100%{transform:scale(1);opacity:.7}50%{transform:scale(1.08);opacity:1}}
@keyframes splashBar{from{width:0}to{width:100%}}
.logo-node{animation:pulseNode 2.5s ease-in-out infinite}
.logo-node:nth-child(2){animation-delay:.4s}.logo-node:nth-child(3){animation-delay:.8s}
.logo-node:nth-child(4){animation-delay:1.2s}.logo-node:nth-child(5){animation-delay:1.6s}
.logo-core{animation:glowCore 3s ease-in-out infinite}
.logo-pin{animation:pulsePin 2s ease-in-out infinite}
.logo-pin:nth-child(odd){animation-delay:.3s}
.logo-svg:hover .logo-node{animation-duration:1s}
.logo-svg:hover .logo-core{opacity:1;animation-duration:1s}
/* Splash */
.splash{position:fixed;inset:0;background:var(--bg);z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;transition:opacity .5s}
.splash.hide{animation:splashFade .5s ease-out forwards}
.splash svg{height:100px;width:auto;animation:splashPulse 1.5s ease-in-out infinite}
.splash-text{font-family:'Space Grotesk',sans-serif;font-size:14px;color:var(--text3);margin-top:16px;letter-spacing:1px}
.splash-bar-wrap{width:180px;height:3px;background:var(--border);border-radius:3px;margin-top:14px;overflow:hidden}
.splash-bar{height:100%;background:var(--accent);border-radius:3px;animation:splashBar 2s ease-out forwards}
nav{max-width:800px;margin:0 auto;padding:16px 20px;display:flex;justify-content:space-between;align-items:center}
nav .logo svg{height:72px;width:auto}
nav .controls{display:flex;align-items:center;gap:8px}
.pill-toggle{display:flex;background:var(--card2);border-radius:10px;padding:3px;border:1px solid var(--border)}
.pill-btn{padding:5px 12px;border:none;border-radius:8px;font-size:12px;font-weight:600;cursor:pointer;background:transparent;color:var(--text3);font-family:'DM Sans',sans-serif;transition:all .2s}
.pill-btn.active{background:var(--accent);color:#fff;box-shadow:0 2px 8px rgba(13,148,136,.3)}
.theme-btn{width:36px;height:36px;border-radius:10px;border:1px solid var(--border);background:var(--card2);cursor:pointer;font-size:15px;display:flex;align-items:center;justify-content:center;transition:all .2s}
.theme-btn:hover{border-color:var(--accent);background:var(--accent-bg)}
.hero{max-width:800px;margin:0 auto;padding:0 20px 24px;animation:fadeUp .6s ease-out}
.hero h1{font-family:'Space Grotesk',sans-serif;font-size:clamp(28px,5vw,38px);font-weight:700;letter-spacing:-1.5px;line-height:1.1;margin-bottom:8px}
.hero h1 em{font-style:normal;color:var(--accent);position:relative}
.hero p{color:var(--text2);font-size:16px;max-width:480px}
.main{max-width:800px;margin:0 auto;padding:0 20px 40px}
.search-wrap{position:relative;margin-bottom:24px;animation:fadeUp .6s ease-out .1s both}
.search-wrap input{width:100%;padding:16px 20px 16px 48px;border:2px solid var(--border);border-radius:14px;font-size:16px;background:var(--card);color:var(--text);font-family:'DM Sans',sans-serif;outline:none;transition:all .25s;box-shadow:var(--shadow-sm)}
.search-wrap input:focus{border-color:var(--accent);box-shadow:var(--shadow-glow),0 0 0 4px var(--accent-glow)}
.search-wrap input::placeholder{color:var(--text3)}
.search-wrap .search-icon{position:absolute;left:16px;top:50%;transform:translateY(-50%);width:20px;height:20px;color:var(--text3)}
.autocomplete-list{position:absolute;top:100%;left:0;right:0;background:var(--card);border:1px solid var(--border);border-radius:0 0 14px 14px;max-height:220px;overflow-y:auto;z-index:10;display:none;box-shadow:var(--shadow-lg)}
.autocomplete-item{padding:12px 20px;cursor:pointer;font-size:14px;border-bottom:1px solid var(--border);color:var(--text);transition:background .15s}
.autocomplete-item:hover{background:var(--accent-bg)}
.autocomplete-item .qty{color:var(--text3);font-size:12px;margin-left:6px}
.coupons{margin-bottom:28px;animation:fadeUp .6s ease-out .2s both}
.coupons-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:var(--text3);margin-bottom:12px}
.coupons-scroll{display:flex;gap:14px;overflow-x:auto;padding-bottom:8px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch}
.coupons-scroll::-webkit-scrollbar{height:0}
.coupon{min-width:240px;border-radius:16px;padding:20px;position:relative;overflow:hidden;cursor:pointer;transition:transform .25s;flex-shrink:0;scroll-snap-align:start}
.coupon:hover{transform:translateY(-4px) scale(1.01)}
.coupon:active{transform:scale(.98)}
.coupon-coto{background:linear-gradient(135deg,#E31E24,#f25058)}
.coupon-jumbo{background:linear-gradient(135deg,#009B3A,#2ecc71)}
.coupon-disco{background:linear-gradient(135deg,#6A1B9A,#9C27B0)}
.coupon *{color:#fff}
.coupon .store{font-size:13px;font-weight:600;opacity:.85;margin-bottom:6px}
.coupon .disc{font-family:'Space Grotesk',sans-serif;font-size:32px;font-weight:700;line-height:1}
.coupon .cdesc{font-size:13px;margin-top:4px;opacity:.85}
.coupon .ccode{display:inline-block;background:rgba(255,255,255,.22);backdrop-filter:blur(4px);padding:4px 12px;border-radius:8px;font-size:11px;font-weight:700;margin-top:10px;letter-spacing:1.5px}
.coupon .cexp{font-size:10px;opacity:.6;margin-top:6px}
.coupon .blob{position:absolute;border-radius:50%;background:rgba(255,255,255,.1)}
.coupon .blob1{width:80px;height:80px;right:-20px;top:-20px}
.coupon .blob2{width:60px;height:60px;right:30px;bottom:-25px;background:rgba(255,255,255,.06)}
.cats{display:flex;gap:8px;overflow-x:auto;margin-bottom:24px;padding-bottom:4px;animation:fadeUp .6s ease-out .25s both;-webkit-overflow-scrolling:touch}
.cats::-webkit-scrollbar{height:0}
.cat{padding:9px 18px;border:1.5px solid var(--border);border-radius:28px;background:var(--card);cursor:pointer;font-size:14px;font-weight:600;color:var(--text2);white-space:nowrap;transition:all .2s;font-family:'DM Sans',sans-serif}
.cat:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-bg)}
.cat.active{background:var(--accent);color:#fff;border-color:var(--accent);box-shadow:0 4px 14px rgba(13,148,136,.25)}
.sec-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:var(--text3);margin-bottom:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px;margin-bottom:24px}
.item{background:var(--card);border-radius:var(--radius);padding:20px 14px;text-align:center;cursor:pointer;border:1.5px solid var(--border);transition:all .3s;position:relative;overflow:hidden}
.item:hover{border-color:var(--accent);transform:translateY(-6px);box-shadow:var(--shadow-lg),var(--shadow-glow)}
.item:active{transform:scale(.97)}
.item .emo{font-size:42px;display:block;margin-bottom:10px;transition:transform .3s}
.item:hover .emo{transform:scale(1.15) rotate(-5deg)}
.item .nm{font-size:14px;font-weight:700;color:var(--text);display:block;letter-spacing:-.2px}
.item .qt{font-size:12px;color:var(--text3);display:block;margin-top:3px}
.item .pr{font-family:'Space Grotesk',sans-serif;font-size:16px;color:var(--accent);font-weight:700;margin-top:8px;display:block}
.item .best-store-tag{display:inline-block;margin-top:6px;padding:3px 10px;border-radius:20px;font-size:11px;font-weight:700;background:var(--green-bg);color:var(--green);border:1px solid var(--green);letter-spacing:.2px}
.results{animation:fadeUp .4s ease-out}
.product{margin-bottom:18px;padding:22px;background:var(--card);border-radius:var(--radius);border:1.5px solid var(--border);box-shadow:var(--shadow-sm);animation:scaleIn .3s ease-out;transition:box-shadow .3s}
.product:hover{box-shadow:var(--shadow-md)}
.product h3{font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;letter-spacing:-.5px;margin-bottom:2px}
.product .qlabel{color:var(--text3);font-size:13px;margin-bottom:14px;font-weight:500}
.price-row{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;margin:4px 0;border-radius:12px;cursor:pointer;transition:all .2s;background:var(--card2);border:1px solid transparent}
.price-row:hover{border-color:var(--accent);background:var(--accent-bg)}
.price-row.best{background:var(--green-bg);border:1.5px solid var(--green)}
.sm-name{font-size:15px;font-weight:600;color:var(--text)}
.pr-info{text-align:right}
.pr-val{font-family:'Space Grotesk',sans-serif;font-weight:700;color:var(--accent);font-size:18px}
.pr-promo{font-size:13px}
.pr-old{text-decoration:line-through;color:var(--text3);margin-right:8px}
.pr-sale{color:var(--red);font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:16px}
.tag{display:inline-block;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;margin-left:8px}
.tag-best{background:var(--green);color:#fff}
.tag-sale{background:var(--red);color:#fff}
.promo-exp{font-size:11px;color:var(--red);display:block;margin-top:3px}
.no-results{text-align:center;padding:50px 20px;color:var(--text3)}
.no-results .big{font-size:56px;display:block;margin-bottom:12px}
.scrape-info{text-align:center;font-size:11px;color:var(--text3);margin-top:16px}
.wa-share{display:inline-flex;align-items:center;gap:8px;padding:10px 20px;border-radius:12px;background:#25D366;color:#fff;font-family:'DM Sans',sans-serif;font-size:14px;font-weight:700;border:none;cursor:pointer;margin-top:14px;transition:all .2s;box-shadow:0 4px 14px rgba(37,211,102,.3)}
.wa-share:hover{background:#1ebe5a;transform:translateY(-2px);box-shadow:0 6px 20px rgba(37,211,102,.4)}
.wa-share:active{transform:scale(.97)}
.wa-share svg{width:18px;height:18px;fill:#fff}
.loc-hero{max-width:800px;margin:0 auto 20px;padding:0 20px;animation:fadeUp .5s ease-out .1s both}
.loc-box{background:var(--card);border:1.5px solid var(--border);border-radius:20px;padding:24px;box-shadow:var(--shadow-md);position:relative;overflow:hidden}
.loc-box::before{content:'';position:absolute;right:-30px;top:-30px;width:160px;height:160px;border-radius:50%;background:var(--accent-glow);pointer-events:none}
.loc-box::after{content:'';position:absolute;right:40px;bottom:-40px;width:100px;height:100px;border-radius:50%;background:var(--accent-glow);pointer-events:none}
.loc-header{display:flex;align-items:center;gap:12px;margin-bottom:16px}
.loc-pin-icon{width:44px;height:44px;border-radius:12px;background:var(--accent);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.loc-pin-icon svg{width:22px;height:22px;color:#fff}
.loc-title{font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:700;color:var(--text);letter-spacing:-.3px}
.loc-subtitle{font-size:13px;color:var(--text3);margin-top:2px}
.loc-input-wrap{position:relative;margin-bottom:16px}
.loc-input{width:100%;padding:14px 18px 14px 44px;border:1.5px solid var(--border);border-radius:14px;font-size:15px;background:var(--card2);color:var(--text);font-family:'DM Sans',sans-serif;outline:none;transition:all .25s}
.loc-input:focus{border-color:var(--accent);background:var(--card);box-shadow:0 0 0 3px var(--accent-glow)}
.loc-input::placeholder{color:var(--text3)}
.loc-input-wrap svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);width:18px;height:18px;color:var(--text3)}
.loc-suggestions{position:absolute;top:100%;left:0;right:0;background:var(--card);border:1px solid var(--border);border-radius:0 0 14px 14px;max-height:200px;overflow-y:auto;z-index:10;display:none;box-shadow:var(--shadow-lg)}
.loc-sug-item{padding:12px 18px;cursor:pointer;font-size:14px;border-bottom:1px solid var(--border);color:var(--text);transition:background .15s}
.loc-sug-item:hover{background:var(--accent-bg)}
.loc-sug-item .loc-zone{color:var(--text3);font-size:11px;display:block;margin-top:2px}
.loc-results{display:grid;gap:12px}
.loc-card{background:var(--card2);border:1.5px solid var(--border);border-radius:14px;padding:16px;display:flex;gap:14px;align-items:flex-start;transition:all .25s;animation:scaleIn .3s ease-out;cursor:pointer}
.loc-card:hover{border-color:var(--accent);background:var(--accent-bg);transform:translateX(4px)}
.loc-icon{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:800;color:#fff;flex-shrink:0;font-family:'Space Grotesk',sans-serif}
.loc-icon.coto{background:linear-gradient(135deg,#E31E24,#f25058)}
.loc-icon.jumbo{background:linear-gradient(135deg,#009B3A,#2ecc71)}
.loc-icon.disco{background:linear-gradient(135deg,#6A1B9A,#9C27B0)}
.loc-info{flex:1}
.loc-name{font-family:'Space Grotesk',sans-serif;font-size:15px;font-weight:700;color:var(--text);margin-bottom:2px}
.loc-addr{font-size:12px;color:var(--text2);margin-bottom:8px}
.loc-meta{display:flex;gap:8px;flex-wrap:wrap}
.loc-tag{font-size:11px;padding:3px 10px;border-radius:20px;font-weight:600}
.loc-tag.open{background:var(--green-bg);color:var(--green)}
.loc-tag.closed{background:var(--red-bg);color:var(--red)}
.loc-tag.dist{background:var(--card);color:var(--text2);border:1px solid var(--border)}
.loc-tag.hours{background:var(--accent-bg);color:var(--accent)}
.modal-bg{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);backdrop-filter:blur(6px);z-index:100;justify-content:center;align-items:center;padding:20px}
.modal-bg.on{display:flex}
.modal{background:var(--card);border-radius:20px;padding:30px;max-width:440px;width:100%;box-shadow:var(--shadow-lg);position:relative;animation:scaleIn .25s ease-out;border:1px solid var(--border)}
.modal .mx{position:absolute;top:14px;right:16px;width:34px;height:34px;border-radius:10px;border:1px solid var(--border);background:var(--card2);cursor:pointer;font-size:16px;display:flex;align-items:center;justify-content:center;color:var(--text3);transition:all .15s}
.modal .mx:hover{background:var(--border);color:var(--text)}
.modal h3{font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;margin-bottom:4px}
.modal .msub{font-size:13px;color:var(--text3);margin-bottom:18px}
.mrow{display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid var(--border);font-size:14px}
.mrow:last-child{border-bottom:none}
.mlbl{color:var(--text2)}.mval{font-weight:700;color:var(--text)}
.mval.promo{color:var(--red)}.mval.best{color:var(--green)}
.msrc{margin-top:18px;padding:16px;background:var(--card2);border-radius:12px;font-size:12px;color:var(--text2);line-height:1.7;border:1px solid var(--border)}
.msrc strong{color:var(--text);display:block;margin-bottom:4px;font-size:13px}
.toast{position:fixed;bottom:30px;left:50%;transform:translateX(-50%);background:var(--text);color:var(--bg);padding:12px 24px;border-radius:12px;font-size:13px;font-weight:600;z-index:200;display:none;animation:fadeUp .3s ease-out}
/* Add to list button */
.add-btn{padding:5px 12px;border:1.5px solid var(--accent);border-radius:10px;background:var(--accent-bg);color:var(--accent);font-family:'DM Sans',sans-serif;font-size:12px;font-weight:700;cursor:pointer;transition:all .2s;margin-top:8px;display:inline-block}
.add-btn:hover{background:var(--accent);color:#fff}
.add-btn.added{background:var(--green);color:#fff;border-color:var(--green)}
/* Cart bar */
.cart-bar{position:fixed;bottom:0;left:0;right:0;background:var(--card);border-top:1.5px solid var(--border);padding:14px 20px;box-shadow:0 -4px 20px rgba(0,0,0,.1);z-index:50;transform:translateY(100%);transition:transform .35s ease-out;display:flex;flex-direction:column;align-items:center;gap:10px}
.cart-bar.show{transform:translateY(0)}
.cart-header{display:flex;align-items:center;justify-content:space-between;width:100%;max-width:800px}
.cart-title{font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:700;color:var(--text)}
.cart-count{font-size:13px;color:var(--text3)}
.cart-actions{display:flex;gap:6px}
.cart-clear{padding:5px 12px;border:1px solid var(--border);border-radius:8px;background:var(--card2);color:var(--red);font-family:'DM Sans',sans-serif;font-size:11px;font-weight:600;cursor:pointer;transition:all .2s}
.cart-clear:hover{background:var(--red-bg);border-color:var(--red)}
.cart-wa{padding:5px 12px;border:1px solid #25D366;border-radius:8px;background:#25D366;color:#fff;font-family:'DM Sans',sans-serif;font-size:11px;font-weight:600;cursor:pointer;transition:all .2s}
.cart-wa:hover{background:#1ebe5a}
.cart-items{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;width:100%;max-width:800px}
.cart-pill{padding:4px 10px;border-radius:8px;background:var(--card2);border:1px solid var(--border);font-size:12px;color:var(--text2);display:flex;align-items:center;gap:4px}
.cart-pill .cart-x{cursor:pointer;color:var(--text3);font-weight:700;transition:color .15s}
.cart-pill .cart-x:hover{color:var(--red)}
.cart-summary{display:flex;gap:14px;flex-wrap:wrap;justify-content:center;width:100%;max-width:800px}
.cart-store{flex:1;min-width:140px;padding:10px 14px;border-radius:14px;border:1.5px solid var(--border);background:var(--card2);text-align:center;transition:all .2s}
.cart-store.best-store{border-color:var(--green);background:var(--green-bg)}
.cart-store-name{font-size:12px;font-weight:700;color:var(--text);margin-bottom:2px}
.cart-store-total{font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:700;color:var(--text)}
.cart-store.best-store .cart-store-total{color:var(--green)}
.cart-saving{font-size:11px;font-weight:700;color:var(--green);margin-top:2px}
/* About section - compact */
.about-section{max-width:800px;margin:0 auto;padding:24px 20px 8px}
.about-box{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap}
.about-name{font-family:'DM Sans',sans-serif;font-size:13px;font-weight:600;color:var(--text2)}
.about-role{font-size:12px;color:var(--text3)}
.about-sep{color:var(--border);font-size:12px}
.about-link{display:inline-flex;align-items:center;gap:4px;font-size:12px;font-weight:600;color:var(--text3);text-decoration:none;transition:color .2s}
.about-link:hover{color:var(--accent)}
.about-link svg{width:12px;height:12px}
/* Footer */
.site-footer{max-width:800px;margin:0 auto;padding:20px 20px 32px;text-align:center;border-top:1px solid var(--border)}
.footer-brand{font-family:'Space Grotesk',sans-serif;font-size:14px;font-weight:700;color:var(--text);letter-spacing:-.3px}
.footer-brand span{color:var(--accent)}
.footer-sub{font-size:12px;color:var(--text3);margin-top:4px}
.footer-copy{font-size:11px;color:var(--text3);margin-top:10px;opacity:.6}
@media(max-width:600px){
nav{padding:12px 16px}.hero h1{font-size:28px}.main{padding:0 16px 30px}
.grid{grid-template-columns:repeat(3,1fr);gap:10px}.item{padding:14px 8px}.item .emo{font-size:32px}
.coupon{min-width:200px;padding:16px}
.cart-store{min-width:100px;padding:8px}.cart-store-total{font-size:16px}
}
</style>
</head>
<body>
<!-- SPLASH SCREEN -->
<div class="splash" id="splash">
  <svg class="logo-svg" viewBox="0 0 420 100" xmlns="http://www.w3.org/2000/svg">
    <path d="M62 8A52 52 0 1 0 62 114" fill="none" stroke="var(--accent)" stroke-width="9" stroke-linecap="round"/>
    <line x1="62" y1="61" x2="40" y2="61" stroke="var(--accent)" stroke-width="9" stroke-linecap="round"/>
    <path d="M60 59L100 59 94 96 48 96Z" fill="none" stroke="var(--accent)" stroke-width="3.5" stroke-linejoin="round"/>
    <circle cx="59" cy="108" r="6" fill="none" stroke="var(--accent)" stroke-width="2.5"/>
    <circle cx="86" cy="108" r="6" fill="none" stroke="var(--accent)" stroke-width="2.5"/>
    <rect x="64" y="69" width="17" height="17" rx="2.5" fill="none" stroke="var(--accent)" stroke-width="1.5" opacity=".8"/>
    <circle class="logo-core" cx="73" cy="78" r="3" fill="var(--accent)" opacity=".7"/>
    <text x="125" y="55" style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:700;letter-spacing:-1px" fill="var(--text)">Grocery</text>
    <text x="262" y="55" style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:700;letter-spacing:-1px" fill="var(--accent)">Finder</text>
    <text x="125" y="76" style="font-family:'DM Sans',sans-serif;font-size:10px;font-weight:700;letter-spacing:2px" fill="var(--accent)" opacity=".6">AI-POWERED PRICE COMPARISON</text>
  </svg>
  <div class="splash-text" id="splash-text">Cargando precios...</div>
  <div class="splash-bar-wrap"><div class="splash-bar"></div></div>
</div>
<nav>
  <div class="logo">
    <svg class="logo-svg" viewBox="0 0 420 140" xmlns="http://www.w3.org/2000/svg">
      <line x1="8" y1="30" x2="28" y2="45" stroke="var(--accent)" stroke-width="1.5" opacity=".3"/>
      <line x1="4" y1="72" x2="24" y2="62" stroke="var(--accent)" stroke-width="1.5" opacity=".25"/>
      <line x1="10" y1="105" x2="28" y2="92" stroke="var(--accent)" stroke-width="1.5" opacity=".3"/>
      <line x1="100" y1="10" x2="85" y2="26" stroke="var(--accent)" stroke-width="1.5" opacity=".2"/>
      <line x1="108" y1="45" x2="98" y2="52" stroke="var(--accent)" stroke-width="1.5" opacity=".25"/>
      <circle class="logo-node" cx="8" cy="30" r="2.5" fill="var(--accent)"/>
      <circle class="logo-node" cx="4" cy="72" r="2.5" fill="var(--accent)"/>
      <circle class="logo-node" cx="10" cy="105" r="2.5" fill="var(--accent)"/>
      <circle class="logo-node" cx="100" cy="10" r="2.5" fill="var(--accent)"/>
      <circle class="logo-node" cx="108" cy="45" r="2.5" fill="var(--accent)"/>
      <path d="M62 8A52 52 0 1 0 62 114" fill="none" stroke="var(--accent)" stroke-width="9" stroke-linecap="round"/>
      <line x1="62" y1="61" x2="40" y2="61" stroke="var(--accent)" stroke-width="9" stroke-linecap="round"/>
      <path d="M60 59L100 59 94 96 48 96Z" fill="none" stroke="var(--accent)" stroke-width="3.5" stroke-linejoin="round"/>
      <circle cx="59" cy="108" r="6" fill="none" stroke="var(--accent)" stroke-width="2.5"/>
      <circle cx="86" cy="108" r="6" fill="none" stroke="var(--accent)" stroke-width="2.5"/>
      <rect x="64" y="69" width="17" height="17" rx="2.5" fill="none" stroke="var(--accent)" stroke-width="1.5" opacity=".8"/>
      <line class="logo-pin" x1="70" y1="69" x2="70" y2="65" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="77" y1="69" x2="77" y2="65" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="64" y1="76" x2="60" y2="76" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="64" y1="81" x2="60" y2="81" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="81" y1="76" x2="85" y2="76" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="81" y1="81" x2="85" y2="81" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="70" y1="86" x2="70" y2="90" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <line class="logo-pin" x1="77" y1="86" x2="77" y2="90" stroke="var(--accent)" stroke-width="1.2" opacity=".5"/>
      <circle class="logo-core" cx="73" cy="78" r="3" fill="var(--accent)" opacity=".7"/>
      <text x="125" y="55" style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:700;letter-spacing:-1px" fill="var(--text)">Grocery</text>
      <text x="262" y="55" style="font-family:'Space Grotesk',sans-serif;font-size:30px;font-weight:700;letter-spacing:-1px" fill="var(--accent)">Finder</text>
      <text x="125" y="76" style="font-family:'DM Sans',sans-serif;font-size:10px;font-weight:700;letter-spacing:2px" fill="var(--accent)" opacity=".6">AI-POWERED PRICE COMPARISON</text>
      <text x="125" y="96" style="font-family:'DM Sans',sans-serif;font-size:11px" fill="var(--text3)">Buenos Aires, Argentina</text>
    </svg>
  </div>
  <div class="controls">
    <div class="pill-toggle">
      <button class="pill-btn active" id="btn-es" onclick="setLang('es')">ES</button>
      <button class="pill-btn" id="btn-en" onclick="setLang('en')">EN</button>
    </div>
    <button class="theme-btn" id="theme-btn" onclick="toggleTheme()">&#9728;&#65039;</button>
  </div>
</nav>
<div class="hero">
  <h1 data-es="Encontr&aacute; el <em>mejor precio</em> para tu compra" data-en="Find the <em>best price</em> for your groceries" class="i18n-html" id="hero-title"></h1>
  <p data-es="Compar&aacute; Coto, Jumbo y Disco al instante" data-en="Compare Coto, Jumbo and Disco instantly" class="i18n"></p>
</div>
<div class="loc-hero">
  <div class="loc-box">
    <div class="loc-header">
      <div class="loc-pin-icon"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z"/><circle cx="12" cy="9" r="2.5"/></svg></div>
      <div>
        <div class="loc-title i18n" data-es="Supermercados cerca tuyo" data-en="Supermarkets near you"></div>
        <div class="loc-subtitle i18n" data-es="Escrib&iacute; tu barrio o localidad en CABA y GBA" data-en="Type your neighborhood in Buenos Aires metro area"></div>
      </div>
    </div>
    <div class="loc-input-wrap">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>
      <input class="loc-input" type="text" id="loc-input" autocomplete="off"/>
      <div class="loc-suggestions" id="loc-sug"></div>
    </div>
    <div class="loc-results" id="loc-results"></div>
  </div>
</div>
<div class="main">
  <div class="search-wrap">
    <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><line x1="16.5" y1="16.5" x2="21" y2="21"/></svg>
    <input type="text" id="search" autocomplete="off"/>
    <div class="autocomplete-list" id="autocomplete"></div>
  </div>
  <div class="coupons">
    <div class="coupons-title i18n" data-es="Cupones disponibles" data-en="Available coupons" id="coup-title"></div>
    <div class="coupons-scroll" id="coup-scroll"></div>
  </div>
  <div class="cats" id="cats">
    <button class="cat active" onclick="filtrarCat('todos')" data-es="Todos" data-en="All" class="i18n"></button>
    <button class="cat" onclick="filtrarCat('lacteos')"><span data-es="&#129371; L&aacute;cteos" data-en="&#129371; Dairy" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('frutas')"><span data-es="&#127822; Frutas" data-en="&#127822; Fruits" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('carnes')"><span data-es="&#129385; Carnes" data-en="&#129385; Meats" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('almacen')"><span data-es="&#127978; Almac&eacute;n" data-en="&#127978; Pantry" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('bebidas')"><span data-es="&#129380; Bebidas" data-en="&#129380; Drinks" class="i18n"></span></button>
    <button class="cat" onclick="filtrarCat('limpieza')"><span data-es="&#129529; Limpieza" data-en="&#129529; Cleaning" class="i18n"></span></button>
  </div>
  <div id="home">
    <div class="sec-title i18n" data-es="Productos disponibles" data-en="Available products" id="prod-title"></div>
    <div class="grid" id="grid"></div>
  </div>
  <div id="results" class="results"></div>
  <div class="scrape-info" id="scrape-info"></div>
</div>
<!-- ABOUT -->
<div class="about-section">
  <div class="about-box">
    <span class="about-name">Cecilia Ibarra</span>
    <span class="about-sep">&middot;</span>
    <span class="about-role">Tech Enthusiast &amp; Builder</span>
    <span class="about-sep">&middot;</span>
    <a class="about-link" href="https://github.com/ibarracecilia" target="_blank"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>GitHub</a>
  </div>
</div>
<!-- FOOTER -->
<footer class="site-footer">
  <div class="footer-brand">Grocery<span>Finder</span></div>
  <div class="footer-sub i18n" data-es="Comparador de precios de supermercados en Buenos Aires" data-en="Supermarket price comparison in Buenos Aires"></div>
  <div class="footer-copy">&copy; 2026 Cecilia Ibarra. Buenos Aires, Argentina.</div>
</footer>
<!-- CART BAR -->
<div class="cart-bar" id="cart-bar">
  <div class="cart-header">
    <div><span class="cart-title" id="cart-title"></span> <span class="cart-count" id="cart-count"></span></div>
    <div class="cart-actions">
      <button class="cart-wa" id="cart-wa-btn" onclick="shareCartWA()">WhatsApp</button>
      <button class="cart-clear" id="cart-clear-btn" onclick="clearCart()"></button>
    </div>
  </div>
  <div class="cart-items" id="cart-items"></div>
  <div class="cart-summary" id="cart-summary"></div>
</div>
<div class="modal-bg" id="modal-bg" onclick="closeModal(event)">
  <div class="modal"><button class="mx" onclick="closeModal()">&times;</button><div id="modal-c"></div></div>
</div>
<div class="toast" id="toast"></div>
<script>
var AP=[], lang='es', dark=false, cart=[];

var EMOJIS = {};
EMOJIS['Leche Entera'] = '\ud83e\udd5b';
EMOJIS['Yogur Natural'] = '\ud83e\udd5b';
EMOJIS['Naranjas'] = '\ud83c\udf4a';
EMOJIS['Huevos'] = '\ud83e\udd5a';
EMOJIS['Queso Cremoso'] = '\ud83e\uddc0';
EMOJIS['Manteca'] = '\ud83e\uddc8';
EMOJIS['Pan Lactal'] = '\ud83c\udf5e';
EMOJIS['Arroz'] = '\ud83c\udf5a';
EMOJIS['Fideos Secos'] = '\ud83c\udf5d';
EMOJIS['Aceite de Girasol'] = '\ud83e\uded2';
EMOJIS['Az\u00facar'] = '\ud83c\udf6c';
EMOJIS['Harina'] = '\ud83c\udf3e';
EMOJIS['Galletitas Dulces'] = '\ud83c\udf6a';
EMOJIS['Gaseosa Cola'] = '\ud83e\udd64';
EMOJIS['Agua Mineral'] = '\ud83d\udca7';
EMOJIS['Papel Higi\u00e9nico'] = '\ud83e\uddfb';
EMOJIS['Detergente'] = '\ud83e\uddf4';
EMOJIS['Jab\u00f3n en Polvo'] = '\ud83e\uddfc';
EMOJIS['Pollo Entero'] = '\ud83c\udf57';
EMOJIS['Carne Picada'] = '\ud83e\udd69';
EMOJIS['Banana'] = '\ud83c\udf4c';
EMOJIS['Tomate'] = '\ud83c\udf45';
EMOJIS['Papa'] = '\ud83e\udd54';
EMOJIS['Cebolla'] = '\ud83e\uddc5';

var PROD_EN = {};
PROD_EN['Leche Entera'] = 'Whole Milk';
PROD_EN['Yogur Natural'] = 'Plain Yogurt';
PROD_EN['Naranjas'] = 'Oranges';
PROD_EN['Huevos'] = 'Eggs';
PROD_EN['Queso Cremoso'] = 'Cream Cheese';
PROD_EN['Manteca'] = 'Butter';
PROD_EN['Pan Lactal'] = 'Sliced Bread';
PROD_EN['Arroz'] = 'Rice';
PROD_EN['Fideos Secos'] = 'Dry Pasta';
PROD_EN['Aceite de Girasol'] = 'Sunflower Oil';
PROD_EN['Az\u00facar'] = 'Sugar';
PROD_EN['Harina'] = 'Flour';
PROD_EN['Galletitas Dulces'] = 'Sweet Cookies';
PROD_EN['Gaseosa Cola'] = 'Cola Soda';
PROD_EN['Agua Mineral'] = 'Mineral Water';
PROD_EN['Papel Higi\u00e9nico'] = 'Toilet Paper';
PROD_EN['Detergente'] = 'Detergent';
PROD_EN['Jab\u00f3n en Polvo'] = 'Powder Soap';
PROD_EN['Pollo Entero'] = 'Whole Chicken';
PROD_EN['Carne Picada'] = 'Ground Beef';
PROD_EN['Banana'] = 'Banana';
PROD_EN['Tomate'] = 'Tomato';
PROD_EN['Papa'] = 'Potato';
PROD_EN['Cebolla'] = 'Onion';

function prodName(nombre) {
  if (lang === 'en' && PROD_EN[nombre]) return PROD_EN[nombre];
  return nombre;
}

var CATS = {};
CATS['lacteos'] = ['Leche Entera','Yogur Natural','Queso Cremoso','Manteca'];
CATS['frutas'] = ['Naranjas','Banana','Tomate','Papa','Cebolla'];
CATS['carnes'] = ['Pollo Entero','Carne Picada','Huevos'];
CATS['almacen'] = ['Pan Lactal','Arroz','Fideos Secos','Aceite de Girasol','Az\u00facar','Harina','Galletitas Dulces'];
CATS['bebidas'] = ['Gaseosa Cola','Agua Mineral'];
CATS['limpieza'] = ['Papel Higi\u00e9nico','Detergente','Jab\u00f3n en Polvo'];

var T = {
  es: {desde:'Desde',ph:'\u00bfQu\u00e9 producto busc\u00e1s?',nr1:'No encontramos',nr2:'Prob\u00e1 con otro t\u00e9rmino',na:'No hay resultados para',upd:'Precios actualizados',rp:'Precio regular',pp:'Precio promocional',sav:'Ahorro',pe:'Promo vence',days:'d\u00edas',exp:'Vencida',verd:'Veredicto',bp:'Mejor precio disponible',st:'Datos del scraping',src:'Fuente',ed:'Fecha de extracci\u00f3n',meth:'M\u00e9todo',as:'Scraping autom\u00e1tico',prod:'Producto',nd:'No disponible',cheap:'M\u00c1S BARATO',offer:'OFERTA',expires:'Vence',cc:'Cup\u00f3n copiado',ct:'Cupones disponibles',pt:'Productos disponibles',off:'OFF',vu:'V\u00e1lido hasta',cm:'Compra m\u00edn.',onl:'Online'},
  en: {desde:'From',ph:'What are you looking for?',nr1:"We couldn't find",nr2:'Try another term',na:'No results for',upd:'Prices updated',rp:'Regular price',pp:'Promo price',sav:'Savings',pe:'Promo expires',days:'days',exp:'Expired',verd:'Verdict',bp:'Best price available',st:'Scraping data',src:'Source',ed:'Extraction date',meth:'Method',as:'Auto website scraping',prod:'Product',nd:'Not available',cheap:'CHEAPEST',offer:'SALE',expires:'Expires',cc:'Coupon copied',ct:'Available coupons',pt:'Available products',off:'OFF',vu:'Valid until',cm:'Min. purchase',onl:'Online'}
};

function t(k) { return T[lang][k] || k; }

function toggleTheme() {
  dark = !dark;
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : '');
  document.getElementById('theme-btn').innerHTML = dark ? '\ud83c\udf19' : '\u2600\ufe0f';
}

var coups = [
  {store:'Coto',cls:'coupon-coto',disc:'15%',des:'en L\u00e1cteos',den:'on Dairy',code:'COTO15LAC',min:'$5.000',exp:7},
  {store:'Jumbo',cls:'coupon-jumbo',disc:'20%',des:'en Frutas',den:'on Fruits',code:'JUMBO20FRU',min:'$3.000',exp:5},
  {store:'Disco',cls:'coupon-disco',disc:'10%',des:'en todo',den:'on everything',code:'DISCO10ALL',min:'$8.000',exp:10},
  {store:'Coto',cls:'coupon-coto',disc:'25%',des:'en Bebidas',den:'on Drinks',code:'COTO25BEB',min:'$2.000',exp:3},
  {store:'Jumbo',cls:'coupon-jumbo',disc:'2x1',des:'en Limpieza',den:'on Cleaning',code:'JUMBO2X1CL',min:'$4.000',exp:12}
];

function renderCoups() {
  var s = document.getElementById('coup-scroll');
  var now = new Date();
  var html = '';
  for (var i = 0; i < coups.length; i++) {
    var c = coups[i];
    var expDate = new Date(now.getTime() + c.exp * 864e5);
    var e = expDate.toLocaleDateString(lang === 'es' ? 'es-AR' : 'en-US', {day:'numeric', month:'short'});
    html += '<div class="coupon ' + c.cls + '" onclick="copyCoup(\'' + c.code + '\')">';
    html += '<div class="blob blob1"></div><div class="blob blob2"></div>';
    html += '<div class="store">' + c.store + '</div>';
    html += '<div class="disc">' + c.disc + ' ' + t('off') + '</div>';
    html += '<div class="cdesc">' + (lang === 'es' ? c.des : c.den) + '</div>';
    html += '<div class="ccode">' + c.code + '</div>';
    html += '<div class="cexp">' + t('vu') + ' ' + e + ' \u00b7 ' + t('cm') + ' ' + c.min + '</div>';
    html += '</div>';
  }
  s.innerHTML = html;
}

function copyCoup(c) {
  navigator.clipboard.writeText(c).then(function() {
    var el = document.getElementById('toast');
    el.textContent = '\u2705 ' + t('cc') + ': ' + c;
    el.style.display = 'block';
    setTimeout(function() { el.style.display = 'none'; }, 2000);
  });
}

function setLang(l) {
  lang = l;
  document.getElementById('btn-es').classList.toggle('active', l === 'es');
  document.getElementById('btn-en').classList.toggle('active', l === 'en');
  document.querySelectorAll('.i18n').forEach(function(e) {
    if (e.dataset[l]) e.textContent = e.dataset[l];
  });
  document.querySelectorAll('.i18n-html').forEach(function(e) {
    if (e.dataset[l]) e.innerHTML = e.dataset[l];
  });
  document.getElementById('search').placeholder = t('ph');
  document.getElementById('coup-title').textContent = t('ct');
  document.getElementById('prod-title').textContent = t('pt');
  document.getElementById('loc-input').placeholder = lang === 'es' ? 'Escrib\u00ed tu barrio...' : 'Type your neighborhood...';
  document.getElementById('splash-text').textContent = lang === 'es' ? 'Cargando precios...' : 'Loading prices...';
  renderCoups();
  if (AP.length) showPop(AP);
}

async function loadProds() {
  try {
    var r = await fetch('/api/products');
    AP = await r.json();
    showPop(AP);
    // Hide splash after products load
    setTimeout(function() {
      var sp = document.getElementById('splash');
      if (sp) { sp.classList.add('hide'); setTimeout(function() { sp.style.display = 'none'; }, 600); }
    }, 400);
  } catch(e) {
    console.error(e);
    // Hide splash even on error
    var sp = document.getElementById('splash');
    if (sp) { sp.classList.add('hide'); setTimeout(function() { sp.style.display = 'none'; }, 600); }
  }
}

function getEmoji(nombre) {
  return EMOJIS[nombre] || '\ud83d\uded2';
}

function escName(n) {
  return n.replace(/'/g, "\\'");
}

function showPop(ps) {
  var html = '';
  for (var i = 0; i < ps.length; i++) {
    var p = ps[i];
    var storeTag = '';
    if (p.best_store) {
      storeTag = '<span class="best-store-tag">\ud83c\udfc6 ' + p.best_store + '</span>';
    }
    var inCart = cart.indexOf(p.nombre) !== -1;
    html += '<div class="item" style="animation-delay:' + (i * 40) + 'ms;animation:fadeUp .4s ease-out ' + (i * 40) + 'ms both">';
    html += '<span class="emo" onclick="pickProd(\'' + escName(p.nombre) + '\')">' + getEmoji(p.nombre) + '</span>';
    html += '<span class="nm" onclick="pickProd(\'' + escName(p.nombre) + '\')">' + prodName(p.nombre) + '</span>';
    html += '<span class="qt">' + p.cantidad + '</span>';
    html += '<span class="pr">' + t('desde') + ' $' + p.precio_min + '</span>';
    html += storeTag;
    html += '<button class="add-btn' + (inCart ? ' added' : '') + '" onclick="event.stopPropagation();toggleCart(\'' + escName(p.nombre) + '\')">' + (inCart ? '\u2713' : '+') + '</button>';
    html += '</div>';
  }
  document.getElementById('grid').innerHTML = html;
}

function pickProd(n) {
  document.getElementById('search').value = n;
  buscar();
}

function filtrarCat(c) {
  document.querySelectorAll('.cat').forEach(function(b) { b.classList.remove('active'); });
  event.target.closest('.cat').classList.add('active');
  if (c === 'todos') {
    showPop(AP);
  } else {
    var list = CATS[c] || [];
    var filtered = AP.filter(function(p) { return list.indexOf(p.nombre) !== -1; });
    showPop(filtered);
  }
  document.getElementById('home').style.display = 'block';
  document.getElementById('results').innerHTML = '';
}

var si = document.getElementById('search');
var al = document.getElementById('autocomplete');

si.addEventListener('input', function() {
  var q = this.value.toLowerCase().trim();
  if (q.length < 1) { al.style.display = 'none'; return; }
  var m = AP.filter(function(p) { return p.nombre.toLowerCase().indexOf(q) !== -1; });
  if (!m.length) {
    al.innerHTML = '<div class="autocomplete-item" style="color:var(--text3)">' + t('na') + ' "' + q + '"</div>';
    al.style.display = 'block';
    return;
  }
  var html = '';
  for (var i = 0; i < m.length; i++) {
    html += '<div class="autocomplete-item" onclick="pickProd(\'' + escName(m[i].nombre) + '\')">' + prodName(m[i].nombre) + ' <span class="qty">' + m[i].cantidad + '</span></div>';
  }
  al.innerHTML = html;
  al.style.display = 'block';
});

document.addEventListener('click', function(e) {
  if (!e.target.closest('.search-wrap')) al.style.display = 'none';
});

async function buscar() {
  al.style.display = 'none';
  var q = si.value.trim();
  if (!q) return;
  document.getElementById('home').style.display = 'none';
  try {
    var r = await fetch('/api/search?q=' + encodeURIComponent(q));
    var data = await r.json();
    var h = '';
    var fs = '';
    var keys = Object.keys(data);
    if (!keys.length) {
      h = '<div class="no-results"><span class="big">\ud83d\udd0d</span><p><strong>' + t('nr1') + '</strong> "' + q + '"</p><p style="margin-top:8px;font-size:14px;color:var(--text3)">' + t('nr2') + '</p></div>';
      document.getElementById('home').style.display = 'block';
    }
    for (var k = 0; k < keys.length; k++) {
      var prod = keys[k];
      var info = data[prod];
      var ps = info.precios;
      var best = Infinity;
      for (var i = 0; i < ps.length; i++) {
        if (ps[i].precio_final < best) best = ps[i].precio_final;
      }
      var cartInList = cart.indexOf(prod) !== -1;
      var addBtnText = cartInList ? '\u2713' : '+';
      var addBtnCls = cartInList ? 'add-btn added' : 'add-btn';
      h += '<div class="product"><h3>' + prodName(prod) + ' <button class="' + addBtnCls + '" onclick="event.stopPropagation();toggleCart(\'' + escName(prod) + '\')" style="font-size:14px;vertical-align:middle">' + addBtnText + '</button></h3><div class="qlabel">' + info.cantidad + '</div>';
      for (var j = 0; j < ps.length; j++) {
        var p = ps[j];
        var ib = p.precio_final === best;
        var cls = ib ? 'best' : '';
        var md = encodeURIComponent(JSON.stringify({
          producto: prod, cantidad: info.cantidad, supermarket: p.supermarket,
          precio: p.precio, precio_promo: p.precio_promo, precio_final: p.precio_final,
          promo_vence: p.promo_vence, fecha_scraping: p.fecha_scraping, esMejor: ib
        }));
        var ph = '';
        if (p.precio_promo) {
          ph = '<span class="pr-promo"><span class="pr-old">$' + p.precio + '</span><span class="pr-sale">$' + p.precio_promo + '</span><span class="tag tag-sale">' + t('offer') + '</span></span>';
          if (p.promo_vence) ph += '<span class="promo-exp">' + t('expires') + ': ' + fmtD(p.promo_vence) + '</span>';
        } else {
          ph = '<span class="pr-val">$' + p.precio + '</span>';
        }
        h += '<div class="price-row ' + cls + '" onclick="openModal(\'' + md + '\')"><span class="sm-name">\ud83c\udfea ' + p.supermarket + '</span><div class="pr-info">' + ph + (ib ? '<span class="tag tag-best">' + t('cheap') + '</span>' : '') + '</div></div>';
        if (p.fecha_scraping) fs = p.fecha_scraping;
      }
      h += '</div>';
    }
    // Single WhatsApp button for ALL results
    if (keys.length) {
      var waMsg = '';
      for (var k2 = 0; k2 < keys.length; k2++) {
        var wp = keys[k2];
        var wi = data[wp];
        var wps = wi.precios;
        var wbest = Infinity;
        for (var w = 0; w < wps.length; w++) { if (wps[w].precio_final < wbest) wbest = wps[w].precio_final; }
        var wbestStore = '';
        for (var w = 0; w < wps.length; w++) { if (wps[w].precio_final === wbest) wbestStore = wps[w].supermarket; }
        waMsg += '*' + prodName(wp) + '* (' + wi.cantidad + ')\n';
        for (var w = 0; w < wps.length; w++) {
          var wpr = wps[w];
          var wprice = wpr.precio_promo ? '$' + wpr.precio_promo + ' _(promo)_' : '$' + wpr.precio;
          var arrow = wpr.precio_final === wbest ? ' << ' + (lang === 'es' ? 'MEJOR' : 'BEST') : '';
          waMsg += '  ' + wpr.supermarket + ': ' + wprice + arrow + '\n';
        }
        waMsg += '\n';
      }
      waMsg += (lang === 'es' ? 'Compara precios en GroceryFinder' : 'Compare prices at GroceryFinder') + '\nhttps://grocery-finder.onrender.com';
      h += '<div style="text-align:center;margin-top:16px"><button class="wa-share" onclick="shareWA(\'' + encodeURIComponent(waMsg) + '\')"><svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>' + (lang === 'es' ? 'Compartir por WhatsApp' : 'Share on WhatsApp') + '</button></div>';
    }
    document.getElementById('results').innerHTML = h;
    if (fs) document.getElementById('scrape-info').innerHTML = t('upd') + ': ' + fmtD(fs);
  } catch(e) {
    document.getElementById('results').innerHTML = '<p>Error</p>';
  }
}

function fmtD(d) {
  return new Date(d + 'T00:00:00').toLocaleDateString(lang === 'es' ? 'es-AR' : 'en-US', {day:'numeric', month:'long', year:'numeric'});
}

function shareWA(msg) {
  window.open('https://wa.me/?text=' + msg, '_blank');
}

// ========== SHOPPING LIST ==========
function toggleCart(nombre) {
  var idx = cart.indexOf(nombre);
  if (idx === -1) {
    cart.push(nombre);
  } else {
    cart.splice(idx, 1);
  }
  updateCartBar();
  showPop(getCurrentProducts());
}

function getCurrentProducts() {
  var activeCat = document.querySelector('.cat.active');
  if (!activeCat) return AP;
  var catText = activeCat.textContent || activeCat.innerText;
  if (catText.indexOf('Todos') !== -1 || catText.indexOf('All') !== -1) return AP;
  return AP;
}

function clearCart() {
  cart = [];
  updateCartBar();
  showPop(getCurrentProducts());
}

function updateCartBar() {
  var bar = document.getElementById('cart-bar');
  if (!cart.length) {
    bar.classList.remove('show');
    return;
  }
  bar.classList.add('show');
  document.getElementById('cart-title').textContent = lang === 'es' ? 'Tu lista' : 'Your list';
  document.getElementById('cart-count').textContent = '(' + cart.length + (lang === 'es' ? ' productos)' : ' items)');
  document.getElementById('cart-clear-btn').textContent = lang === 'es' ? 'Vaciar' : 'Clear';

  // Render pills
  var pillsHtml = '';
  for (var i = 0; i < cart.length; i++) {
    pillsHtml += '<div class="cart-pill">' + prodName(cart[i]) + ' <span class="cart-x" onclick="toggleCart(\'' + escName(cart[i]) + '\')">\u2715</span></div>';
  }
  document.getElementById('cart-items').innerHTML = pillsHtml;

  // Calculate totals per store
  calcCartTotals();
}

function calcCartTotals() {
  var promises = [];
  var allData = {};
  var pending = cart.length;
  if (!pending) return;

  for (var i = 0; i < cart.length; i++) {
    (function(nombre) {
      fetch('/api/search?q=' + encodeURIComponent(nombre))
        .then(function(r) { return r.json(); })
        .then(function(data) {
          for (var prod in data) {
            if (prod === nombre) {
              allData[prod] = data[prod];
            }
          }
          pending--;
          if (pending === 0) renderCartTotals(allData);
        })
        .catch(function() {
          pending--;
          if (pending === 0) renderCartTotals(allData);
        });
    })(cart[i]);
  }
}

function renderCartTotals(allData) {
  var stores = {Coto: 0, Jumbo: 0, Disco: 0};

  for (var prod in allData) {
    var precios = allData[prod].precios;
    for (var i = 0; i < precios.length; i++) {
      var p = precios[i];
      var pf = p.precio_promo || p.precio;
      if (stores[p.supermarket] !== undefined) {
        stores[p.supermarket] += pf;
      }
    }
  }

  var vals = [];
  for (var s in stores) { if (stores[s] > 0) vals.push(stores[s]); }
  var bestVal = Math.min.apply(null, vals);
  var worstVal = Math.max.apply(null, vals);
  var saving = worstVal - bestVal;

  var html = '';
  for (var name in stores) {
    var total = stores[name];
    var isBest = total === bestVal && total > 0;
    html += '<div class="cart-store' + (isBest ? ' best-store' : '') + '">';
    html += '<div class="cart-store-name">' + name + '</div>';
    html += '<div class="cart-store-total">$' + total.toLocaleString('es-AR') + '</div>';
    if (isBest && saving > 0) {
      html += '<div class="cart-saving">' + (lang === 'es' ? 'Ahorr\u00e1s $' + saving.toLocaleString('es-AR') : 'You save $' + saving.toLocaleString('es-AR')) + '</div>';
    }
    html += '</div>';
  }
  document.getElementById('cart-summary').innerHTML = html;

  // Store data for WhatsApp sharing
  window._cartStores = stores;
  window._cartBest = bestVal;
  window._cartSaving = saving;
}

function shareCartWA() {
  if (!cart.length) return;
  var stores = window._cartStores || {};
  var saving = window._cartSaving || 0;
  var bestStore = '';
  var bestVal = window._cartBest || 0;
  for (var s in stores) { if (stores[s] === bestVal && stores[s] > 0) bestStore = s; }

  var msg = '*' + (lang === 'es' ? 'Mi lista de compras' : 'My shopping list') + '* (' + cart.length + (lang === 'es' ? ' productos)\n\n' : ' items)\n\n');
  for (var i = 0; i < cart.length; i++) {
    msg += '- ' + prodName(cart[i]) + '\n';
  }
  msg += '\n';
  for (var name in stores) {
    var isBest = name === bestStore;
    msg += name + ': $' + stores[name].toLocaleString('es-AR') + (isBest ? ' << ' + (lang === 'es' ? 'MEJOR' : 'BEST') : '') + '\n';
  }
  if (saving > 0) {
    msg += '\n' + (lang === 'es' ? 'Ahorras $' + saving.toLocaleString('es-AR') + ' yendo a *' + bestStore + '*' : 'You save $' + saving.toLocaleString('es-AR') + ' shopping at *' + bestStore + '*');
  }
  msg += '\n\n' + (lang === 'es' ? 'Compara precios en GroceryFinder' : 'Compare prices at GroceryFinder') + '\nhttps://grocery-finder.onrender.com';
  window.open('https://wa.me/?text=' + encodeURIComponent(msg), '_blank');
}

si.addEventListener('keypress', function(e) { if (e.key === 'Enter') buscar(); });

function openModal(ed) {
  var d = JSON.parse(decodeURIComponent(ed));
  var pF = d.precio_promo || d.precio;
  var h = '<h3>\ud83c\udfea ' + d.supermarket + '</h3>';
  h += '<div class="msub">' + prodName(d.producto) + ' \u2014 ' + d.cantidad + '</div>';
  h += '<div class="mrow"><span class="mlbl">' + t('rp') + '</span><span class="mval">$' + d.precio + '</span></div>';
  if (d.precio_promo) {
    h += '<div class="mrow"><span class="mlbl">' + t('pp') + '</span><span class="mval promo">$' + d.precio_promo + '</span></div>';
    h += '<div class="mrow"><span class="mlbl">' + t('sav') + '</span><span class="mval promo">-$' + (d.precio - d.precio_promo) + ' (' + Math.round((1 - d.precio_promo / d.precio) * 100) + '%)</span></div>';
    if (d.promo_vence) {
      var dias = Math.ceil((new Date(d.promo_vence + 'T00:00:00') - new Date()) / 864e5);
      h += '<div class="mrow"><span class="mlbl">' + t('pe') + '</span><span class="mval promo">' + fmtD(d.promo_vence) + ' (' + (dias > 0 ? dias + ' ' + t('days') : t('exp')) + ')</span></div>';
    }
  }
  if (d.esMejor) {
    h += '<div class="mrow"><span class="mlbl">' + t('verd') + '</span><span class="mval best">\u2705 ' + t('bp') + '</span></div>';
  }
  h += '<div class="msrc"><strong>\ud83d\udcca ' + t('st') + '</strong>';
  h += t('src') + ': ' + d.supermarket + ' ' + t('onl') + '<br>';
  h += t('ed') + ': ' + (d.fecha_scraping ? fmtD(d.fecha_scraping) : t('nd')) + '<br>';
  h += t('meth') + ': ' + t('as') + '<br>';
  h += t('prod') + ': ' + d.producto + ' (' + d.cantidad + ')</div>';
  document.getElementById('modal-c').innerHTML = h;
  document.getElementById('modal-bg').classList.add('on');
}

function closeModal(e) {
  if (!e || e.target === document.getElementById('modal-bg') || e.target.classList.contains('mx'))
    document.getElementById('modal-bg').classList.remove('on');
}

document.addEventListener('keydown', function(e) { if (e.key === 'Escape') closeModal(); });

setLang('es');
loadProds();
renderCoups();

var STORES = [
  {name:'Coto', cls:'coto', letter:'C', stores:[
    {addr:'Av. Cabildo 2571, Belgrano', barrios:['Belgrano','N\u00fa\u00f1ez','Colegiales'], hours:'8:00 - 22:00'},
    {addr:'Av. Rivadavia 5150, Caballito', barrios:['Caballito','Flores','Almagro'], hours:'8:00 - 22:00'},
    {addr:'Av. Corrientes 3247, Abasto', barrios:['Balvanera','Abasto','Once','Almagro'], hours:'8:00 - 22:00'},
    {addr:'Av. Directorio 2820, Parque Chacabuco', barrios:['Parque Chacabuco','Boedo','Caballito'], hours:'8:00 - 21:30'},
    {addr:'Av. C\u00f3rdoba 5650, Palermo', barrios:['Palermo','Villa Crespo','Chacarita'], hours:'8:00 - 22:00'},
    {addr:'Av. Juan B. Justo 3563, Villa Crespo', barrios:['Villa Crespo','Palermo','Chacarita'], hours:'8:00 - 22:00'},
    {addr:'Ag\u00fcero 616, Abasto', barrios:['Abasto','Balvanera','Once'], hours:'8:00 - 22:00'},
    {addr:'Av. Mart\u00edn Garc\u00eda 495, Barracas', barrios:['Barracas','La Boca','San Telmo'], hours:'8:00 - 21:30'},
    {addr:'Av. Ricardo Balb\u00edn 2030, San Mart\u00edn', barrios:['San Mart\u00edn','Villa Ballester','Caseros'], hours:'8:00 - 22:00'},
    {addr:'Comesa\u00f1a 4056, Ciudadela', barrios:['Ciudadela','Ramos Mej\u00eda','Liniers'], hours:'8:00 - 21:30'},
    {addr:'Av. Rivadavia 14452, Ramos Mej\u00eda', barrios:['Ramos Mej\u00eda','Ciudadela','Haedo'], hours:'8:00 - 22:00'},
    {addr:'Av. Hip\u00f3lito Yrigoyen 8627, Lomas de Zamora', barrios:['Lomas de Zamora','Banfield','Temperley'], hours:'8:00 - 22:00'},
    {addr:'Av. Calchaqui 3101, Quilmes', barrios:['Quilmes','Quilmes Oeste','Bernal'], hours:'8:00 - 22:00'},
    {addr:'Av. Mitre 2530, Avellaneda', barrios:['Avellaneda','Sarand\u00ed','Lan\u00fas'], hours:'8:00 - 21:30'},
    {addr:'Autopista Panamericana Km 35, Tortugas', barrios:['Tortugas','Pacheco','Tigre'], hours:'8:00 - 22:00'},
    {addr:'Av. Vergara 3560, Hurlingham', barrios:['Hurlingham','Mor\u00f3n','Ituzaing\u00f3'], hours:'8:00 - 21:30'}
  ]},
  {name:'Jumbo', cls:'jumbo', letter:'J', stores:[
    {addr:'Av. Bullrich 345, Palermo', barrios:['Palermo','Recoleta','Belgrano'], hours:'9:00 - 21:30'},
    {addr:'Av. Rivadavia 7550, Flores', barrios:['Flores','Floresta','Caballito'], hours:'9:00 - 21:00'},
    {addr:'Av. Santa Fe 4950, Palermo', barrios:['Palermo','Recoleta','Barrio Norte','Belgrano'], hours:'9:00 - 21:30'},
    {addr:'Av. Corrientes 5559, Villa Crespo', barrios:['Villa Crespo','Chacarita','Almagro'], hours:'9:00 - 21:00'},
    {addr:'Lola Mora 450, Puerto Madero', barrios:['Puerto Madero','San Telmo','Retiro'], hours:'9:00 - 21:00'},
    {addr:'Av. Juan B. Justo 4701, Palermo', barrios:['Palermo','Villa Crespo'], hours:'9:00 - 21:00'},
    {addr:'Av. Calchaqui 3950, Quilmes Oeste', barrios:['Quilmes','Quilmes Oeste','Bernal','Ezpeleta'], hours:'8:30 - 21:30'},
    {addr:'Av. Mitre 1075, Quilmes', barrios:['Quilmes','Bernal'], hours:'9:00 - 21:00'},
    {addr:'Av. Ant\u00e1rtida Argentina 799, Lomas de Zamora', barrios:['Lomas de Zamora','Banfield','Temperley'], hours:'9:00 - 21:00'},
    {addr:'Blvd. Juan Manuel de Rosas 658, Mor\u00f3n', barrios:['Mor\u00f3n','Haedo','Castelar'], hours:'9:00 - 21:00'},
    {addr:'San Lorenzo 3773, San Mart\u00edn', barrios:['San Mart\u00edn','Villa Ballester','Caseros'], hours:'9:00 - 21:00'},
    {addr:'Av. Paran\u00e1 3745, Mart\u00ednez', barrios:['Mart\u00ednez','San Isidro','Olivos','Vicente L\u00f3pez'], hours:'9:00 - 21:00'},
    {addr:'Av. Libertador 2261, San Fernando', barrios:['San Fernando','Victoria','Tigre'], hours:'9:00 - 21:00'},
    {addr:'Boulogne Sur Mer 1275, Pacheco', barrios:['Pacheco','Tigre','Tortugas'], hours:'8:00 - 21:00'},
    {addr:'Las Magnolias 698, Pilar', barrios:['Pilar','Del Viso','Escobar'], hours:'8:00 - 21:00'}
  ]},
  {name:'Disco', cls:'disco', letter:'D', stores:[
    {addr:'Av. Libertador 2475, Recoleta', barrios:['Recoleta','Palermo','Retiro','Barrio Norte'], hours:'8:30 - 21:00'},
    {addr:'Av. Cabildo 1550, Belgrano', barrios:['Belgrano','N\u00fa\u00f1ez','Colegiales'], hours:'8:30 - 21:00'},
    {addr:'Av. Acoyte 440, Caballito', barrios:['Caballito','Almagro','Boedo'], hours:'8:30 - 21:00'},
    {addr:'Av. Scalabrini Ortiz 3178, Palermo', barrios:['Palermo','Villa Crespo'], hours:'8:30 - 21:00'},
    {addr:'Av. Entre R\u00edos 361, San Telmo', barrios:['San Telmo','Monserrat','Barracas'], hours:'8:30 - 21:00'},
    {addr:'Av. Quintana 366, Recoleta', barrios:['Recoleta','Barrio Norte','Retiro'], hours:'8:30 - 21:00'},
    {addr:'J.E. Uriburu 1230, Recoleta', barrios:['Recoleta','Barrio Norte','Balvanera'], hours:'8:30 - 21:00'},
    {addr:'Gorostiaga 1632, Las Ca\u00f1itas', barrios:['Palermo','Belgrano','Colegiales'], hours:'8:30 - 21:00'},
    {addr:'Av. Meeks 256, Lomas de Zamora', barrios:['Lomas de Zamora','Banfield','Temperley'], hours:'8:00 - 21:00'},
    {addr:'Intendente Garc\u00eda Silva 855, Mor\u00f3n', barrios:['Mor\u00f3n','Haedo','Castelar'], hours:'8:00 - 20:00'},
    {addr:'Av. Centenario 388, San Isidro', barrios:['San Isidro','Mart\u00ednez','Olivos'], hours:'8:30 - 21:00'},
    {addr:'Av. Maipu 1819, Vicente L\u00f3pez', barrios:['Vicente L\u00f3pez','Olivos','Mart\u00ednez'], hours:'8:30 - 21:00'},
    {addr:'Amenedo 302, Adrogu\u00e9', barrios:['Adrogu\u00e9','Lomas de Zamora','Temperley'], hours:'8:30 - 21:00'},
    {addr:'Vieytes 1042, Banfield', barrios:['Banfield','Lomas de Zamora','Lan\u00fas'], hours:'8:30 - 21:00'},
    {addr:'Blanco Encalada 2509, B\u00e9ccar', barrios:['B\u00e9ccar','San Isidro','Mart\u00ednez'], hours:'8:30 - 21:00'},
    {addr:'Gdor. Inocencio Arias 3247, Castelar', barrios:['Castelar','Mor\u00f3n','Ituzaing\u00f3'], hours:'8:30 - 21:00'}
  ]}
];

var BARRIOS = ['Belgrano','N\u00fa\u00f1ez','Colegiales','Palermo','Recoleta','Barrio Norte','Retiro','Caballito','Flores','Floresta','Almagro','Balvanera','Abasto','Once','Boedo','Parque Chacabuco','Villa Crespo','Chacarita','San Telmo','La Boca','Monserrat','San Nicol\u00e1s','Puerto Madero','Barracas','Devoto','Villa Urquiza','Saavedra','Liniers','Mataderos','Villa Lugano','Pompeya','Quilmes','Quilmes Oeste','Bernal','Ezpeleta','Avellaneda','Sarand\u00ed','Lan\u00fas','Lomas de Zamora','Banfield','Temperley','Adrogu\u00e9','Mor\u00f3n','Haedo','Castelar','Ituzaing\u00f3','Ramos Mej\u00eda','Ciudadela','Hurlingham','San Mart\u00edn','Villa Ballester','Caseros','San Isidro','Mart\u00ednez','Olivos','Vicente L\u00f3pez','B\u00e9ccar','San Fernando','Victoria','Tigre','Pacheco','Tortugas','Pilar','Del Viso','Escobar'];

var locInput = document.getElementById('loc-input');
var locSug = document.getElementById('loc-sug');

locInput.addEventListener('input', function() {
  var q = this.value.toLowerCase().trim();
  if (q.length < 2) { locSug.style.display = 'none'; return; }
  var m = BARRIOS.filter(function(b) { return b.toLowerCase().indexOf(q) !== -1; });
  if (!m.length) {
    locSug.innerHTML = '<div class="loc-sug-item" style="color:var(--text3)">' + (lang === 'es' ? 'No encontramos ese barrio' : 'Neighborhood not found') + '</div>';
    locSug.style.display = 'block';
    return;
  }
  var html = '';
  for (var i = 0; i < m.length; i++) {
    html += '<div class="loc-sug-item" onclick="selectBarrio(\'' + escName(m[i]) + '\')">' + m[i] + '<span class="loc-zone">Buenos Aires</span></div>';
  }
  locSug.innerHTML = html;
  locSug.style.display = 'block';
});

document.addEventListener('click', function(e) {
  if (!e.target.closest('.loc-input-wrap')) locSug.style.display = 'none';
});

function selectBarrio(b) {
  locInput.value = b;
  locSug.style.display = 'none';
  var results = [];
  for (var i = 0; i < STORES.length; i++) {
    var s = STORES[i];
    for (var j = 0; j < s.stores.length; j++) {
      var st = s.stores[j];
      var found = false;
      for (var k = 0; k < st.barrios.length; k++) {
        if (st.barrios[k].toLowerCase() === b.toLowerCase()) { found = true; break; }
      }
      if (found) {
        results.push({name: s.name, cls: s.cls, letter: s.letter, addr: st.addr, hours: st.hours});
      }
    }
  }
  results.sort(function(a, bb) { return a.name.localeCompare(bb.name); });
  var now = new Date().getHours();
  var lr = document.getElementById('loc-results');
  if (!results.length) {
    lr.innerHTML = '<div style="text-align:center;padding:20px;color:var(--text3)">' + (lang === 'es' ? 'No hay sucursales cercanas en ' + b : 'No nearby stores in ' + b) + '</div>';
    return;
  }
  var html = '';
  for (var i = 0; i < results.length; i++) {
    var r = results[i];
    var open = now >= 8 && now < 21;
    html += '<div class="loc-card"><div class="loc-icon ' + r.cls + '">' + r.letter + '</div><div class="loc-info"><div class="loc-name">' + r.name + '</div><div class="loc-addr">' + r.addr + '</div><div class="loc-meta"><span class="loc-tag ' + (open ? 'open' : 'closed') + '">' + (open ? (lang === 'es' ? 'Abierto' : 'Open') : (lang === 'es' ? 'Cerrado' : 'Closed')) + '</span><span class="loc-tag hours">' + r.hours + '</span></div></div></div>';
  }
  lr.innerHTML = html;
}
</script>
</body>
</html>'''

@app.route('/')
def index():
    resp = make_response(HTML_PAGE)
    resp.headers['Cache-Control'] = 'public, max-age=300'
    resp.headers['Content-Type'] = 'text/html; charset=utf-8'
    return resp

@app.route('/api/products')
def products():
    init_db()
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('''SELECT p.nombre, p.cantidad,
        MIN(CASE WHEN pr.precio_promo IS NOT NULL THEN pr.precio_promo ELSE pr.precio END) as precio_min,
        s.nombre as best_store
        FROM productos p
        JOIN precios pr ON p.id = pr.producto_id
        JOIN supermarkets s ON pr.supermercado_id = s.id
        WHERE (CASE WHEN pr.precio_promo IS NOT NULL THEN pr.precio_promo ELSE pr.precio END) = (
            SELECT MIN(CASE WHEN pr2.precio_promo IS NOT NULL THEN pr2.precio_promo ELSE pr2.precio END)
            FROM precios pr2 WHERE pr2.producto_id = p.id
        )
        GROUP BY p.id
        ORDER BY p.nombre''')
    results = c.fetchall()
    conn.close()
    return jsonify([{'nombre': r['nombre'], 'cantidad': r['cantidad'], 'precio_min': r['precio_min'], 'best_store': r['best_store']} for r in results])

@app.route('/api/search')
def search():
    init_db()
    q = request.args.get('q', '').lower()
    if not q: return jsonify({})
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT p.nombre, p.cantidad, s.nombre as supermarket, pr.precio, pr.precio_promo, pr.promo_vence, pr.fecha_scraping FROM precios pr JOIN productos p ON pr.producto_id = p.id JOIN supermarkets s ON pr.supermercado_id = s.id WHERE LOWER(p.nombre) LIKE ? ORDER BY p.nombre, pr.precio', (f'%{q}%',))
    results = c.fetchall()
    conn.close()
    grouped = {}
    for row in results:
        prod = row['nombre']
        if prod not in grouped: grouped[prod] = {'cantidad': row['cantidad'], 'precios': []}
        pf = row['precio_promo'] if row['precio_promo'] else row['precio']
        grouped[prod]['precios'].append({'supermarket': row['supermarket'], 'precio': row['precio'], 'precio_promo': row['precio_promo'], 'precio_final': pf, 'promo_vence': row['promo_vence'], 'fecha_scraping': row['fecha_scraping']})
    return jsonify(grouped)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
