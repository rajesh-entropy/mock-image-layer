### Testing
### set env variables
```bash
export AWS_PROFILE=localstack
export LOCALSTACK_URL=http://localhost:4566/
export aws_access_key_id=test
export aws_secret_access_key=test
```

Run a fresh instance of LocalStack and initialize the resources required for the project.
```bash
docker compose up -d
```

### Make the localstack-entrypoint.sh script executable
```bash
 chmod +x localstack_entrypoint.sh
```

### Run the localstack-entrypoint.sh script to set up LocalStack environment variables
```bash
 . ./localstack-entrypoint.sh > /dev/null
```

To stop localstack
```bash
docker compose down
```

