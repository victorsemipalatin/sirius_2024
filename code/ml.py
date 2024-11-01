import numpy as np
import pandas as pd
import torch
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_distances
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
from sklearn.preprocessing import normalize

# инициализация модели
tokenizer = AutoTokenizer.from_pretrained("ai-forever/sbert_large_nlu_ru")
model = AutoModel.from_pretrained("ai-forever/sbert_large_nlu_ru")
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)


def find_closest_vector_to_mean(cluster_vectors): # нахождение ближайшего вектора к среднему по косиносному расстоянию
    mean_vector = np.mean(cluster_vectors, axis=0)
    distances = cosine_distances(cluster_vectors, mean_vector.reshape(1, -1))
    sorted_indices = np.argsort(distances.ravel())
    closest_indices = sorted_indices[:3]
    return closest_indices


def mean_pooling(model_output, attention_mask): # усреднённая агрегация
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


def max_pooling(model_output, attention_mask): # макс агрегация
    token_embeddings = model_output[0]
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    masked_embeddings = token_embeddings * input_mask_expanded
    max_embeddings = torch.max(masked_embeddings, dim=1)[0]
    return max_embeddings


def process(path): # processing fucntion
    dataset = pd.read_excel(path)
    new_data = {i: [] for i in dataset.columns}
    for i in range(dataset.shape[1]):
        col_embs = []
        for j in range(dataset.shape[0]):
            elem = dataset.iloc[j][i]
            if pd.isna(elem):
                continue

            for sent in elem.split('.'):
                sent = sent.strip()
                if sent and len(sent) > 3 and any(c.isalpha() for c in sent):
                    col_embs.append(sent.lower())
        new_data[dataset.columns[i]] = col_embs
    columns = dataset.columns
    overall_len = len(dataset)
    emb_dict = {i: [] for i in dataset.columns}
    batch_size = 16
    for column in dataset.columns:
        for start in tqdm(range(0, len(new_data[column]), batch_size)):
            end = min(start + batch_size, len(new_data[column]))
            batch_data = new_data[column][start:end]
            encoded_data = tokenizer(batch_data, padding=True, truncation=True, max_length=32, return_tensors='pt').to(
                device)

            with torch.no_grad():
                output = model(**encoded_data)

            embeddings = mean_pooling(output, encoded_data['attention_mask']).cpu().numpy()

            emb_dict[column].extend(embeddings.tolist())

    labels_list = []
    for col in columns:
        data = np.array(emb_dict[col])
        normalized_data = normalize(data)
        kmeans = KMeans(n_clusters=min(len(columns), 15), random_state=0, max_iter=5000).fit(
            normalized_data)
        labels = kmeans.labels_
        labels_list.append(labels)

    final_list = []
    for idx, col in enumerate(columns):
        arr1 = new_data[col]
        arr2 = emb_dict[col]
        labels = labels_list[idx]

        clusters_sentences = {}

        for i in range(len(arr1)):
            cluster_id = labels[i]
            if cluster_id not in clusters_sentences:
                clusters_sentences[cluster_id] = []
            clusters_sentences[cluster_id].append((arr1[i], arr2[i]))

        top_clusters = sorted(clusters_sentences.keys(), key=lambda x: len(clusters_sentences[x]), reverse=True)[:10]

        final_dict = {}
        for cluster in top_clusters:
            array = clusters_sentences[cluster]
            embs = np.array([array[i][1] for i in range(len(array))])
            indx = find_closest_vector_to_mean(embs)
            sent = ''
            for ind in indx:
                sent += array[ind][0] + '\n'

            for ind in indx:
                final_dict[sent] = round(len(clusters_sentences[cluster]) / overall_len * 100, 1)
        final_list.append(final_dict)
    return columns, final_list
