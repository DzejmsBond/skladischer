

# Generating proto files for GRPC.
# This has to be run from the root directory in order to achieve successful includes.
generate-proto-files:
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/code_ms.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/storage_ms.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/sensor_ms.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/admin_ms.proto

clean-proto-files:
	find ./proto -name "*_pb2.py" -delete
	find ./proto -name "*_pb2_grpc.py" -delete

generate-documentation:
	sphinx-build ./storage-ms/docs/source storage-ms/build
	sphinx-build ./admin-ms/docs/source admin-ms/build
	sphinx-build ./sensor-ms/docs/source sensor-ms/build
	sphinx-build ./codes-ms/docs/source codes-ms/build