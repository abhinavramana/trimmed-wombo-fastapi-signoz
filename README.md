# trimmed-wombo-fastapi-signoz
Trimmed down version to allow debugging and issue reproduction for integration with signoz

Run via docker:
```bash
sudo ./run_locally.sh
```

Run without docker after ensuring the main dependencies are installed:
```bash
pip install -r requirements.txt

opentelemetry-bootstrap --action=install
```
Ensure your python environment is setup properly via pycharm or source activate commands
```bash
opentelemetry-instrument  --logs_exporter otlp_proto_grpc --traces_exporter otlp_proto_grpc gunicorn wombo.fastapi:app --workers 2 --worker-class uvicorn.workers.UvicornH11Worker --bind 0.0.0.0:8000
```