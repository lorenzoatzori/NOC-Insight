# NOC-Insight

CLI tool per **troubleshooting operativo in NOC (L2/L3)**.

NOC-Insight nasce per **ridurre il tempo di diagnosi** su ticket reali come:

- "AP down"
- "porta switch non funziona"
- "lo switch è giù?"
- "su che VLAN sta questo IP?"

È pensato per **supportare il troubleshooting umano**, non per sostituirlo.

---

## 🎯 Obiettivo

Fornire **indicazioni operative rapide** partendo da:
- log di rete reali
- informazioni statiche note
- best practice NOC codificate

Il focus è **velocità + chiarezza**, non automazione cieca.

---

## 📁 Struttura del progetto
noc-insight/
│
├── noc_insight/
│ │
│ ├── cli/
│ │ └── main.py # Entry point CLI
│ │
│ ├── commands/
│ │ └── ap_diagnose.py # Diagnostica AP / porta
│ │
│ ├── core/
│ │ ├── log_analyzer.py # Analisi passiva dei log
│ │ ├── decision_engine.py # Ragionamento operativo NOC
│ │
│ └── logs/
│ └── *.log # Log dei dispositivi (1 file = 1 device)
│
├── .gitignore
├── requirements.txt
└── README.md


---

## 🧠 Concetto chiave

NOC-Insight lavora in tre fasi principali:

1. **Log Analyzer**
   - legge file di log testuali
   - estrae segnali come:
     - link down
     - PoE fault
     - err-disable
     - AP join failure

2. **Decision Engine**
   - trasforma i segnali in **ipotesi operative**
   - codifica il ragionamento tipico di un NOC L2/L3

3. **CLI**
   - espone tutto con output chiaro e immediato
   - nessuna GUI, nessuna dipendenza da vendor

---

## 🔹 CLI

### `ap-diagnose`

Diagnostica una porta switch e opzionalmente un Access Point.
```bash
noc-insight ap-diagnose --switch SW-3F-01 --port Gi1/0/24 --ap AP-3F-023

---

## 🔹 Output di esempio
[PORT STATUS]
Switch     : SW-3F-01
Port       : Gi1/0/24
Link state : down
Err-disable: NO
PoE        : fault

Last port-related log event:
%POWER_DENY: Inline power denied on Gi1/0/24

[TROUBLESHOOTING HINTS]
- POSSIBLE CAUSE: PoE fault → verify power budget, cable quality, or AP power requirements
- POSSIBLE CAUSE: Link down → check cable, NIC/AP status, or administrative shutdown

[AP STATUS]
AP         : AP-3F-023
AP status  : join_failed
Last AP-related log event:
%CAPWAP-3-ERRORLOG: AP AP-3F-023 failed to join controller

[AP TROUBLESHOOTING HINTS]
- POSSIBLE CAUSE: AP failed to join WLC → check connectivity, CAPWAP, or AP authorization

---


📄 Log supportati

- syslog
- output di show logging
- export manuali
- estratti da log centralizzati

Formato semplice, esempio:
Jan 14 10:32:19 SW-3F-01 %POWER_DENY: Inline power denied on Gi1/0/24
Jan 14 10:33:01 SW-3F-01 %PM-4-ERR_DISABLE: psecure-violation error detected on Gi1/0/24
Jan 14 10:34:11 WLC-01 %CAPWAP-3-ERRORLOG: AP AP-3F-023 failed to join controller

---

⚙️ Installazione rapida
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt


---

🛣️ Roadmap
- Estensione pattern log (BPDU Guard, STP, flapping)
- Lookup VLAN / porta / IP
- Raccolta dati live via SSH
- Integrazione SNMP
- Supporto multi-vendor


---

🎯 Filosofia
- CLI pura
- output testuale
- pensato per l’uso in turno
- modulare
- estendibile
- sicuro (no azioni invasive)

---