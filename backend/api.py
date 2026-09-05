from flask import Flask, jsonify

from backend.database.connection import SessionLocal
from backend.database.models import Player
from backend.services.home import generate_home_summary


app = Flask(__name__)


@app.get("/api/home")
def get_home():
    db = SessionLocal()

    try:
        player = db.query(Player).first()

        if player is None:
            return jsonify({"error": "No player found"}), 404

        home = generate_home_summary(
            player_id=player.player_id,
            player=player,
            db=db,
        )

        return jsonify(home)

    finally:
        db.close()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )