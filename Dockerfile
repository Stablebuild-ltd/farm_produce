FROM base_image
WORKDIR /testbed
RUN git clone https://github.com/sahaanadas/FarmPay.git . && pyenv global 3.11.12 && pip install flask flask-login flask-bootstrap pytest hashlib && pip install -r requirements.txt || true
CMD ["python", "app.py"]