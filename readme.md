<!-- Structures folders -->

dexscreener_crawling
└── dexscreener_crawling  
 └── tasks.py ---> Initialize a task and set up a periodic run times are here.
└── pyproject.toml ---> Store libraries
└── poetry.lock
docker-compose.yml  
Dockerfile

<!-- Workflow -->

Step 1 : pip install poetry
Step 2 : poetry install
Step 3 : docker compose up --build -d

<!-- Import libraries -->
Step 1 : Make sure your location
    CELERY-WORKER
    └── dexscreener_crawling  
Step 2 : poetry install <library name>
