build:
	@echo "Building go binary..."
	@go build -o bin/vws-api

compile:
	@echo "Compiling for every OS and Platform"
	GOOS=freebsd GOARCH=386 go build -o bin/main-freebsd-386 main.go
	GOOS=linux GOARCH=386 go build -o bin/main-linux-386 main.go
	GOOS=windows GOARCH=386 go build -o bin/main-windows-386 main.go

publish:
	@docker push nanthony007/vws-api

test:
	@go test -v .

web:
	@echo "==> Downloading latest Docker image..."
	@docker pull nanthony007/vws-api
	@echo "==> Starting website in Docker..."
	@docker run \
		--interactive \
		--rm \
		--publish "3000:8080" 


#.DEFAULT_GOAL := test
