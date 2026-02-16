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

    def export_to_csv(self):
        """Exports all data to a CSV file in the frontend public folder."""
        import csv
        
        # Path to frontend/public
        # Current file is in iot/utils/
        # We need to go up to iot/ -> smart/ -> frontend/ -> public/
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        export_path = os.path.join(base_dir, 'frontend', 'public', 'report.csv')
        
        try:
            conn = self.get_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM readings ORDER BY timestamp DESC")
                rows = cursor.fetchall()
                
                # Get column names
                headers = [description[0] for description in cursor.description]
                
                with open(export_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(headers)
                    writer.writerows(rows)
                
                conn.close()
                logger.info(f"Data exported successfully to {export_path}")
                return True
        except Exception as e:
            logger.error(f"Failed to export data: {e}")
            return False
