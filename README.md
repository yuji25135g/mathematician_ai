# Mathematician_AI

## Setup

1. Install [Docker](https://www.docker.com/get-started/).

2. Build image.

```bash
cd mathematician_ai
docker-compose build
```

3. Run container.

```bash
docker-compose up -d
```

4. Execute a bash command in a running container.

```bash
docker-compose exec python bash
```

**NOTE** : Run this command when you stop running container

```bash
docker-compose stop
```

## Test

1. Move to test directory.

```bash
cd src/verifier/test
```

2. Run test.

```bash
pytest
```
