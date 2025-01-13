

# Generating proto files for GRPC.
# This has to be run from the root directory in order to achieve successful includes.
generate-proto-files:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/code_ms.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/storage_ms.proto