install:
	pip install -r requirements.txt

api:
	uvicorn app.api:app --reload --port 8000

ui:
	streamlit run streamlit_app.py

test:
	pytest -q

docker:
	docker compose up --build
