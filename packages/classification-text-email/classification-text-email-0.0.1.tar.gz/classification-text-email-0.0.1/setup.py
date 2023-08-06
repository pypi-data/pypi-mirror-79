# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 14:38:19 2020

@author: Ataul154943
"""

#https://packaging.python.org/tutorials/packaging-projects/

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="classification-text-email", # Replace with your own username
    version="0.0.1",
    author="Ataul Karim Baig",
    author_email="ataul.baig@exlservice.com",
    description="compiled packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=["numpy==1.17.3","scikit-learn==0.23.1",
                      "spacy==2.3.2","autocorrect","lime",
                      "gensim==3.4.0",
                      "pyLDAvis==2.1.2","docx2pdf==0.1.7",
                      "python-docx==0.8.10","pyPDF2==1.26.0",
                      "pywin32==227","wordninja","nltk==3.4.1",
                      "pandas==0.25.3","tensorflow==1.15.3",
                      "tensorflow-gpu==1.15.3","tensorflow-hub==0.7.0",
                      "bert-tensorflow==1.0.1","keras==2.2.4","autoviml","typed-ast>=1.3.0",
                      "dask[complete]","requests==2.22.0","flask==1.1.1",
                      "joblib==0.16.0","dask-ml","bert-for-tf2","networkx","wordcloud","cntk"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
