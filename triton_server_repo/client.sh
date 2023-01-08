docker run -it --rm --net=host nvcr.io/nvidia/tritonserver:22.07-py3-sdk
# run this after getting into docker shell
# /workspace/install/bin/image_client -m densenet_onnx -c 3 -s INCEPTION /workspace/images/mug.jpg