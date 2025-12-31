# Multi-stage build
FROM ollama/ollama:0.13.5 AS builder

# Copy the locally downloaded GGUF file into the image
COPY ./MamayLM-Gemma-3-4B-IT-v1.0.i1-Q4_K_M.gguf /models/mamaylm.gguf

# Create Modelfile referencing the local GGUF
RUN echo "FROM /models/mamaylm.gguf" > /models/Modelfile

# Start Ollama server and create the model
RUN nohup bash -c "ollama serve &" && \
    sleep 10 && \
    ollama create mamaylm -f /models/Modelfile && \
    echo "✅ MamayLM model created."

# Final production image
FROM ollama/ollama:0.13.5

# Copy the pre-loaded model cache from builder
COPY --from=builder /root/.ollama /root/.ollama

ENV OLLAMA_HOST=0.0.0.0
EXPOSE 11434

CMD ["serve"]

