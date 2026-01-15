# NOC-Insight

CLI tool per **troubleshooting operativo in NOC (L2/L3)**.

NOC-Insight nasce per **ridurre il tempo di diagnosi** su ticket reali come:

* "AP down"
* "porta switch non funziona"
* "su che VLAN sta questo IP?"

È pensato per **aiutare l’operatore**, non per sostituire il troubleshooting umano.

---

## 📁 Struttura del progetto

```
noc-insight/
│
├── noc_insight/
│   │
│   ├── cli/
│   │   └── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── context_loader.py
│   │   ├── ip_lookup.py
│   │   └── ap_diagnose.py
│   │
│   └── data/
│       └── (file JSON di contesto)
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧠 Concetto chiave

Il tool lavora su un **contesto di rete strutturato** (file JSON) che rappresenta:

* dispositivi
* porte
* VLAN
* mapping IP

Il core elabora questi dati e la CLI li espone con comandi semplici e veloci.

---

## 🔹 CLI (`noc_insight/cli/main.py`)

**Entry point dell’applicazione.**

Responsabilità:

* definire i comandi CLI con `click`
* passare input e parametri al core
* stampare l’output

### Comandi attuali

```bash
ip-lookup <ip>
ap-diagnose <ap_id>
```

---

## 🔹 Core

### `models.py`

Definisce i modelli dati:

* `Device`
* `Port`
* `VLAN`
* `IPMapping`

Serve a evitare dizionari non strutturati e rendere il codice leggibile e scalabile.

---

### `context_loader.py`

Carica il contesto dai file JSON:

* `devices.json`
* `ports.json`
* `vlans.json`
* `ip_map.json`

Converte i dati in oggetti Python pronti per il troubleshooting.

---

### `ip_lookup.py`

Funzione principale:

```python
lookup_ip(ip: str, ctx: ContextLoader) -> str
```

Cosa fa:

* lookup diretto IP → VLAN / device
* fallback per subnet VLAN
* stampa informazioni operative:

  * VLAN
  * subnet
  * device
  * switch / porta / PoE (se disponibili)

Pensato per rispondere subito a:

> "Su che VLAN sta questo IP?"

---

### `ap_diagnose.py`

Funzione:

```python
diagnose_ap(ap_id: str, ctx: ContextLoader) -> str
```

Cosa fa:

* verifica esistenza AP
* risale a switch e porta
* controlla PoE
* mostra VLAN associate
* status placeholder (`Unknown`)

È il primo comando **realmente orientato al lavoro NOC**.

---

## 🔹 Data (`noc_insight/data/`)

Contiene il **contesto di rete**.

File attesi:

* `devices.json`
* `ports.json`
* `vlans.json`
* `ip_map.json`

Questi file:

* non contengono logica
* rappresentano lo stato noto della rete
* in futuro potranno essere generati automaticamente (SSH, SNMP, backup)

---

## ⚙️ Installazione rapida

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

## ▶️ Esempi d’uso

```bash
python -m noc_insight.cli.main ip-lookup 10.10.10.45
python -m noc_insight.cli.main ap-diagnose AP-3F-023
```

---

## 🛣️ Roadmap

* Analisi log per aggiornare lo `Status`
* Diagnostica porte switch
* Lookup VLAN / porta
* Raccolta dati live via SSH
* Integrazione SNMP

---

## 🎯 Filosofia

* CLI pura
* output testuale
* utile in turno
* modulare
* estendibile

NOC-Insight è pensato per **semplificare il lavoro reale**, non per fare bella figura.
