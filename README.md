# trimmed-wombo-fastapi-signoz
Trimmed down version to allow debugging and issue reproduction for integration with signoz

Run via docker:
```bash
sudo ./run_locally.sh
```

Run without docker after ensuring the main dependencies are installed:
```
opentelemetry-instrument --traces_exporter otlp_proto_grpc gunicorn wombo.fastapi:app --workers 2 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8000
```