"""
api.py — Serveur HTTP Flask pour Smart Garden IoT
Tourne sur http://172.16.206.37:9090 en parallèle de la boucle principale.

Endpoints :
  GET  /api/sensors   → dernières valeurs lues
  GET  /api/status    → état pompe, lumière, connexion
  POST /api/command   → envoyer une commande (START_WATERING, STOP_WATERING, SET_INTENSITY)
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.logger import logger

app = Flask(__name__)
CORS(app)  # autoriser les requêtes depuis le frontend React

# ── State partagé (mis à jour par main.py via update_state) ────────────
_state = {
    "sensors": {
        "temperature": None,
        "humidity":    None,
        "moisture":    None,
        "light":       None,
        "water_level": None,
        "rain":        None,
    },
    "actuators": {
        "pump":       False,
        "grow_light": False,
    },
    "alerts": [],
}

# Référence aux gestionnaires logique (injectée par main.py)
_irrigation  = None
_grow_light  = None


def init(irrigation, grow_light):
    """Appelé par main.py pour injecter les dépendances."""
    global _irrigation, _grow_light
    _irrigation = irrigation
    _grow_light = grow_light


def update_state(temp, hum, moisture, light, water_level, rain,
                 pump_on, light_on, alert=None):
    """Appelé à chaque cycle de main.py pour mettre à jour les données."""
    _state["sensors"].update({
        "temperature": temp,
        "humidity":    hum,
        "moisture":    moisture,
        "light":       light,
        "water_level": water_level,
        "rain":        rain,
    })
    _state["actuators"]["pump"]       = pump_on
    _state["actuators"]["grow_light"] = light_on
    if alert:
        _state["alerts"] = [alert] + _state["alerts"][:9]  # max 10 alertes


# ── Routes ─────────────────────────────────────────────────────────────

@app.route("/api/sensors")
def get_sensors():
    return jsonify(_state["sensors"])


@app.route("/api/status")
def get_status():
    return jsonify({
        "actuators": _state["actuators"],
        "alerts":    _state["alerts"][:5],
        "online":    True,
    })


@app.route("/api/command", methods=["POST"])
def post_command():
    data = request.get_json(force=True, silent=True) or {}
    command = data.get("command", "")
    logger.info(f"API: Commande reçue → {command} {data}")

    if command == "START_WATERING":
        if _irrigation:
            _irrigation.start_watering_manual(data.get("duration", 10))
            return jsonify({"ok": True, "message": "Arrosage démarré"})

    elif command == "STOP_WATERING":
        if _irrigation:
            _irrigation.stop_watering_manual()
            return jsonify({"ok": True, "message": "Arrosage arrêté"})

    elif command == "SET_INTENSITY":
        if _grow_light:
            _grow_light.set_intensity(data.get("value", 0))
            return jsonify({"ok": True, "message": f"Intensité → {data.get('value')}%"})

    return jsonify({"ok": False, "message": f"Commande inconnue: {command}"}), 400


def run(host="0.0.0.0", port=9090):
    """Lance le serveur Flask en mode production (sans debug)."""
    logger.info(f"API: Serveur HTTP démarré sur http://{host}:{port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)
