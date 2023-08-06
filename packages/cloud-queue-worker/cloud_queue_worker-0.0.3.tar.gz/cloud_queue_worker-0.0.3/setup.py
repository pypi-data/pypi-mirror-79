from setuptools import setup, find_packages

setup(
    name="cloud_queue_worker",
    version="0.0.3",
    author="Enlaps Open Source",
    author_email="contact@enlaps.fr",
    description="Library to create workers for aws, azure and gcp queue services",
    url="https://gitlab.com/enlaps-public/web/cloud_queue_worker",
    packages=find_packages(),
    python_requires='>=3.6',
)
