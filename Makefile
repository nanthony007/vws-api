all: hello run

hello: 
	@echo "Hello There!"

build:
	@echo "Building go binary..."
	@go build -o bin/main main.go

run:
	@echo "Starting server..."
	@go run main.go

compile:
	@echo "Compiling for every OS and Platform"
	GOOS=freebsd GOARCH=386 go build -o bin/main-freebsd-386 main.go
	GOOS=linux GOARCH=386 go build -o bin/main-linux-386 main.go
	GOOS=windows GOARCH=386 go build -o bin/main-windows-386 main.go

web:
	website:
	@echo "==> Downloading latest Docker image..."
	@docker pull nanthony007/vws-api
	@echo "==> Starting website in Docker..."
	@docker run \
		--interactive \
		--rm \
		--publish "3000:8080" 


.DEFAULT_GOAL := run
