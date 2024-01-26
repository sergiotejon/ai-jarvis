# README

## How to prepare a repo for a model

If you clone this repo o copy it, ensure that you delete the `.git` folder. Then you can create a new repo for your model.

1. First of all, you need to modify the file `values.yaml` with the information of the model. You can find the file in `env/dev/values.yaml`. There you can find comments that explain what you need to change. 

2. Prepare the `predict.py` and `requirements.txt` files. The `predict.py` file is the one that will be used to make the predictions. The `requirements.txt` file is the one that will be used to install the dependencies of the model. You can find examples of the code for predict in HuggingFace's models usually. Here you can find how to prepare the file for using with COG (https://github.com/replicate/cog/blob/main/docs/python.md)
 
3. Maybe you require to add some system packages to the docker image. You can do that in the `Dockerfile` file. Add theses packages using the file cog.yaml. You can find more information in this link (https://github.com/replicate/cog/blob/main/docs/yaml.md#system_packages) 
  
## How to use the repo

1. First, you need to create an image for cache with the command `make cache`. This will create an image with the name of the model. This image will be used to cache the model in the first execution.

2. Obtain the kubeconfig file of the k8s server of AIME. Run `make get-kubeconfig` to put that context in your kubeconfig file.

3. Now you can up the model running `make up`. This will deploy a container in the k8s server of AIME using `tilt`. NOTE: The first time will take a long time because it will create de docker image and download the model in the remote server.

4. OPTIONAL:
   - Replace this file with your own content for the model. An example of a README.md file can be found in the file called README.md.example.
   - Use an example from app_examples to create a new app.

## Makefile

The Makefile has the following commands:

To run a model remotely:

- `make get-kubeconfig`: Get kubeconfig. To interact with a Kubernetes cluster, you need a kubeconfig file.
- `make up`: Deploy the model in the k8s server.
- `make down`: Stop the model in the k8s server.
- `make ci`: For unattended deployments suitable for CI 
- `make port-forward`: Forward the port of the model to your localhost.
- `make app`: Run the client app in your localhost.

For a local run of a model:

- `make docker_run`: Run the model in a docker container.
- `make docker_build`: Build the docker image for the model.
- `make docker_cache`: Create the image for cache the model.
- `make download_model`: Download the model in the remote server.
- `make download_docker_cache`: Download the image for cache the model in the remote server.
- `make check_gpu`: Check if the local server has GPU.
- `make clean`: Clean the model files.