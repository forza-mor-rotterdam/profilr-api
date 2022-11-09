FROM registry.access.redhat.com/ubi8/python-39

RUN mkdir build

# We create folder named build for our stuff.

WORKDIR /build

# Basic WORKDIR is just /
# Now we just want to our WORKDIR to be /build

COPY . .

# FROM [path to files from the folder we run docker run]
# TO [current WORKDIR]
# We copy our files (files from .dockerignore are ignored)
# to the WORKDIR

RUN pip install --no-cache-dir -r requirements.txt

# OK, now we pip install our requirements

EXPOSE 8001

# Instruction informs Docker that the container listens on port 80

WORKDIR /build/app

# Now we just want to our WORKDIR to be /build/app for simplicity
# We could skip this part and then type
# python -m uvicorn main.app:app ... below

CMD python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

# This command runs our uvicorn server
# See Troubleshoots to understand why we need to type in --host 0.0.0.0 and --port 80
