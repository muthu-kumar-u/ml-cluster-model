import numpy as np
import pickle
import os

kmeans = None
vectorizer = None

async def load_startup():
    global kmeans, vectorizer
    model_path = os.getenv("MODEL_PATH")
    vectorizer_path = os.getenv("VECTORIZER_PATH")

    if model_path and os.path.exists(model_path):
        with open(model_path, 'rb') as f:
            kmeans = pickle.load(f)
        print("KMeans model loaded successfully.")
    else:
        raise FileNotFoundError("Model not found. Please check the MODEL_PATH environment variable.")
    
    if vectorizer_path and os.path.exists(vectorizer_path):
        with open(vectorizer_path, 'rb') as f:
            vectorizer = pickle.load(f)
        print("Vectorizer loaded successfully.")
    else:
        raise FileNotFoundError("Vectorizer not found. Please check the VECTORIZER_PATH environment variable.")


async def get_cluster_label(q: str):
    if kmeans is None or vectorizer is None:
        print("Model or Vectorizer is None")
        return None
    
    query_vector = vectorizer.transform([q]).toarray()

    try:
        cluster_label = kmeans.predict(query_vector)[0]
    except Exception as e:
        print(e)
        return e

    if cluster_label is None or not isinstance(cluster_label, (int, np.integer)):
        print("No suggestions found for the given quer")
        return None

    result = {"query": q, "label": int(cluster_label)}

    return result