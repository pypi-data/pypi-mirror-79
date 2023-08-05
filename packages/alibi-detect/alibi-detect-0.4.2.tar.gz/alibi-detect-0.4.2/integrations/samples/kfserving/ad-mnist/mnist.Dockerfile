FROM python:3.6

WORKDIR /workspace

RUN chmod -R a+w /workspace

RUN pip install --upgrade pip

RUN git clone https://github.com/kubeflow/kfserving.git && \
    cd kfserving/python && \
    pip install -e ./kfserving

#RUN git clone https://github.com/seldonio/alibi-detect.git && \
#    cd alibi-detect && \
#    pip install -e .

COPY tmp tmp
RUN cd tmp/alibi_detect && \
    pip install -e .

COPY model_mnist model_mnist
COPY mnist.py mnist.py

ENTRYPOINT ["python", "mnist.py"]

