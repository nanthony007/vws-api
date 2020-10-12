FROM golang:alpine AS builder

# Set necessary environmet variables needed for our image
ENV GO111MODULE=on \
    CGO_ENABLED=0 \
    GOOS=linux \
    GOARCH=amd64

# Move to working directory /build
WORKDIR /build

# Copy and download dependency using go mod
COPY go.mod .
COPY go.sum .
RUN go mod download

# Copy the code into the container
COPY . .

# Build the application
RUN go build -o main .

# Move to /dist directory as the place for resulting binary folder
WORKDIR /dist

# Copy binary from build to main folder
RUN cp /build/main .

# Build a small image
FROM scratch

COPY --from=builder /dist/main /
ENV PORT=8080
ENV DB_URI=postgres://ibpfcwfnmikxmw:5f6f81e84894399cc02a1ad09a6a663d21d448e9b4cbe2897d5fc75817818d3a@ec2-54-83-9-36.compute-1.amazonaws.com:5432/dfh945lu8avc08
# Command to run
ENTRYPOINT ["/main"]