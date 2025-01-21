# Isolated Environments

_Always_ isolate projects with either an Anaconda environment or a virtualenv. **Do not mix them.**

## Steps to create a broken environment

```bash
# Create a conda environment with tensorflow
conda create --name unstable tensorflow

# Activate the environment
conda activate unstable

# Check that tensorflow is working
python3 -c "import tensorflow; print('Working')"

# Install matplotlib with pip
python3 -m pip install matplotlib

# Confirm that tensorflow is broken
python3 -c "import tensorflow; print('Working')"
```
