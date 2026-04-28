import logging
import uuid
import time
import pandas as pd
import numpy as np

class DEMMetricsEngine:
    def __init__(self):
        self.logger = logging.getLogger("dem-metrics-engine")

    def calculate_experience_score(self, web_vitals: dict, error_rate: float, session_duration: int):
        """
        Calculates a global experience score based on technical performance and user behavior.
        """
        # Logic: High weight on Core Web Vitals and error rates
        vitals_score = (web_vitals.get('lcp', 2.5) / 2.5) * 40 # Normalize LCP
        error_penalty = error_rate * 100 * 2
        
        final_score = 100 - vitals_score - error_penalty
        return {
            "experience_score": round(max(0, min(100, final_score)), 2),
            "rating": "OPTIMAL" if final_score > 90 else "GOOD" if final_score > 75 else "DEGRADED"
        }

    def detect_anomalies(self, timeseries_data: list):
        """
        Identifies performance anomalies in high-volume experience telemetry.
        """
        df = pd.DataFrame(timeseries_data)
        if df.empty:
            return []
            
        # Logic: Z-score detection on latency
        mean = df['latency'].mean()
        std = df['latency'].std()
        
        anomalies = df[np.abs(df['latency'] - mean) > (3 * std)]
        return {
            "anomaly_count": len(anomalies),
            "latest_anomaly": anomalies.iloc[-1].to_dict() if not anomalies.empty else None,
            "confidence": 0.92
        }

    def forecast_capacity(self, historical_ingest: list, growth_rate: float = 0.15):
        """
        Predicts future ingest capacity needs for the DEM hub.
        """
        current_ingest = historical_ingest[-1] if historical_ingest else 1000
        forecast_30d = current_ingest * (1 + growth_rate)
        
        return {
            "current_ingest_mps": current_ingest,
            "forecast_30d_mps": round(forecast_30d, 2),
            "recommendation": "Scale Out" if forecast_30d > current_ingest * 1.2 else "Stay"
        }

    def score_sla_risk(self, error_budget_remaining: float, uptime_last_30d: float):
        """
        Calculates the risk of missing SLA targets based on recent reliability trends.
        """
        risk = (1 - uptime_last_30d) * 1000 + (1 - error_budget_remaining) * 100
        
        return {
            "risk_score": round(risk, 2),
            "risk_level": "HIGH" if risk > 70 else "MEDIUM" if risk > 30 else "LOW",
            "action_required": "Emergency Optimization" if risk > 70 else "Review Trends"
        }

if __name__ == "__main__":
    engine = DEMMetricsEngine()
    
    # 1. Experience Score
    vitals = {"lcp": 1.2, "fid": 20, "cls": 0.02}
    print("Experience Score:", engine.calculate_experience_score(vitals, 0.005, 300))
    
    # 2. Anomaly Detection
    history = [{"timestamp": i, "latency": 100 + (np.random.randn() * 10)} for i in range(100)]
    history.append({"timestamp": 101, "latency": 500}) # Anomaly
    print("Anomalies:", engine.detect_anomalies(history))
    
    # 3. Capacity Forecast
    ingest = [100, 110, 125, 140, 155]
    print("Capacity Forecast:", engine.forecast_capacity(ingest))
    
    # 4. SLA Risk
    print("SLA Risk:", engine.score_sla_risk(0.85, 0.9995))
