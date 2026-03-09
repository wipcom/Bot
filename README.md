# AI AutoTrading Bot (ICT/SMC)

Framework modular en Python para autotrading institucional 24/7 basado en Smart Money Concepts (ICT), con capa de ML, optimización con IA y dashboard web desacoplado.

## Estructura

```text
ai_autotrading_bot/
  data_engine/
  market_structure/
  liquidity_engine/
  smc_patterns/
  session_engine/
  strategy_engine/
  risk_engine/
  execution_engine/
  trade_manager/
  backtesting_engine/
  analytics_engine/
  machine_learning/
  ai_optimizer/
  database/
  visualization/
  web_dashboard/
  config/
  scripts/
main.py
```

## Ejecución

- Bot:

```bash
./ai_autotrading_bot/scripts/start_bot.sh
```

- Dashboard (API + Streamlit):

```bash
./ai_autotrading_bot/scripts/start_dashboard.sh
```

## Estado actual

Sí, el proyecto **ya tiene portal web** (FastAPI + Streamlit) y también tiene **autotrading automático en modo paper** ejecutado desde `main.py` sin depender del dashboard.

## Qué falta para producción institucional

1. Integración real de CCXT para Bitunix/Bitget/Bingx (autenticación, órdenes, manejo de errores).
2. Persistencia completa de OHLCV en Parquet + SQLite/PostgreSQL.
3. Lógica SMC avanzada (OB/Breaker/Mitigation/Inducement completos con validaciones robustas).
4. Backtesting walk-forward + costos reales (fees, slippage, funding).
5. ML entrenado (no placeholder) y pipeline de features/model registry.
6. Optimizador IA con Ollama real analizando logs históricos.
7. Hardening operacional: retries, circuit breakers, alertas, supervisión de procesos.
8. Pruebas unitarias/integración y despliegue (Docker + CI/CD).
