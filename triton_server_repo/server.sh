cd server/docs/examples
./fetch_models.sh
# note v22.07 works for dev container in windows wsl2, v22.12 does not work
docker run --gpus=1 --rm -p8000:8000 -p8001:8001 -p8002:8002 -v ${PWD}/model_repository:/models nvcr.io/nvidia/tritonserver:22.07-py3 tritonserver --model-repository=/models