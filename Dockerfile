FROM base_image
WORKDIR /testbed
ENV PATH=/root/.pyenv/shims:/root/.pyenv/bin:${PATH}
COPY . .
RUN pyenv global 3.11.12 && pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]