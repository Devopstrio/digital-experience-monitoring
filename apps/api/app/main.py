import logging
import time
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
from pythonjsonlogger import jsonlogger

# Logger setup
logger = logging.getLogger("dem-api")
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.INFO)

app = FastAPI(title="Digital Experience Monitoring API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Metrics
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Path: {request.url.path} Duration: {duration:.4f}s Status: {response.status_code}")
    return response

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/metrics/web-vitals")
def get_web_vitals():
    return {
        "lcp_p75": "1.4s",
        "fid_p75": "24ms",
        "cls_p75": 0.04,
        "inp_p75": "120ms",
        "status": "GOOD"
    }

@app.get("/metrics/rum")
def get_rum_metrics():
    return {
        "active_sessions": 14200,
        "avg_session_duration": "4m 12s",
        "js_error_rate": "0.12%",
        "rage_click_count": 42,
        "performance_index": 0.94
    }

@app.get("/journeys/summary")
def get_journeys_summary():
    return [
        {"path": "/home -> /product -> /checkout", "success_rate": "92%", "avg_duration": "2m 14s"},
        {"path": "/search -> /product -> /add-to-cart", "success_rate": "84%", "avg_duration": "1m 45s"}
    ]

@app.get("/synthetics/results")
def get_synthetics_results():
    return {
        "global_availability": "99.98%",
        "active_probes": 12,
        "failed_checks_last_24h": 2,
        "top_failing_region": "Tokyo (Latency Spike)"
    }

@app.get("/alerts")
def get_active_alerts():
    return [
        {"id": "alert-1", "severity": "CRITICAL", "message": "Checkout Success Rate Drop (US-East)", "timestamp": "2026-04-28T10:00:00Z"},
        {"id": "alert-2", "severity": "WARNING", "message": "High JS Error Rate (Chrome 124)", "timestamp": "2026-04-28T10:05:00Z"}
    ]

@app.get("/scores/summary")
def get_scores_summary():
    return {
        "global_experience_index": 0.92,
        "sla_compliance": "99.8%",
        "reliability_rating": "ELITE",
        "risk_level": "LOW"
    }

@app.get("/dashboard/summary")
def get_dashboard_summary():
    return {
        "total_properties_monitored": 45,
        "events_processed_last_hour": "2.4M",
        "platform_roi_est": "$12.4M / year",
        "user_satisfaction_score": 4.5
    }
