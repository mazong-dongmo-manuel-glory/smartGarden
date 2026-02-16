import sqlite3
import os
from datetime import datetime
from utils.logger import logger

DB_NAME = "garden.db"

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.init_db()

    def get_connection(self):
        try:
            conn = sqlite3.connect(DB_NAME)
            return conn
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return None

    def init_db(self):
        """Creates the readings table if it doesn't exist."""
        try:
            conn = self.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS readings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        temperature REAL,
                        humidity REAL,
                        soil_moisture REAL,
                        light_intensity INTEGER,
                        water_level REAL
                    )
                """)
                conn.commit()
                conn.close()
                logger.info("Database initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")

    def save_reading(self, temp, hum, soil, light, water_level):
        """Saves a new sensor reading."""
        try:
            conn = self.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO readings (temperature, humidity, soil_moisture, light_intensity, water_level)
                    VALUES (?, ?, ?, ?, ?)
                """, (temp, hum, soil, light, water_level))
                conn.commit()
                conn.close()
                logger.debug("Sensor reading saved to database.")
        except Exception as e:
            logger.error(f"Failed to save reading: {e}")
