# 🚦 AI Traffic Signal System

## Folder Structure
```
traffic-ai-system/
├── run_app.py                  ← Launch dashboard from here
├── generate_data.py            ← Generate synthetic training data
├── requirements.txt
├── config/                     ← All settings
├── data/raw/                   ← traffic_dataset.csv goes here
├── data/processed/             ← Auto-generated after training
├── models/                     ← Auto-generated after training
├── training/                   ← Train & evaluate ML model
├── ai/                         ← Feature builder, predictor, decision engine
├── simulation/                 ← SUMO + TraCI control
│   └── sumo_config/            ← SUMO XML files
├── ui/
│   ├── dashboard.py            ← Streamlit app
│   └── components/             ← UI components
└── utils/                      ← Logger, helpers, metrics store
```

## Quick Start

### 1. Create venv (Python 3.14 Windows fix)
```powershell
py -3.14 -m venv venv --copies
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Set SUMO_HOME
```powershell
# Windows (set permanently)
setx SUMO_HOME "C:\Program Files (x86)\Eclipse\Sumo"
# Then restart terminal
```

### 3. Build the SUMO network
```powershell
netconvert --node-files simulation/sumo_config/nodes.nod.xml ^
           --edge-files simulation/sumo_config/edges.edg.xml ^
           --output-file simulation/sumo_config/network.net.xml
```

### 4. Generate synthetic training data (skip if you have real data)
```powershell
python generate_data.py
```

### 5. Train the model
```powershell
python -m training.train
```

### 6. Launch dashboard
```powershell
python run_app.py
# OR directly:
streamlit run ui/dashboard.py
```

Open browser at **http://localhost:8501** → click **▶️ Run Simulation**
