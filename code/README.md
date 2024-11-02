# Результаты кластеризации данных

В данном репозитории представлены результаты различных методов кластеризации с использованием t-SNE визуализации.

## Методы кластеризации

### K-Means
| Метрика | Ссылка на визуализацию |
|---------|------------------------|
| Silhouette score | [Просмотр](https://github.com/victorsemipalatin/sirius_2024/blob/main/code/tsne_visualization_kmeans.html) |
| Calinski-Harabasz index | [Просмотр](https://github.com/victorsemipalatin/sirius_2024/blob/main/code/tsne_visualization_kmeans_calinski_harabasz.html) |
| Davies-Bouldin index | [Просмотр](https://github.com/victorsemipalatin/sirius_2024/blob/main/code/tsne_visualization_kmeans_davies_bouldin.html) |

### Другие алгоритмы кластеризации
| Алгоритм | Ссылка на визуализацию |
|----------|------------------------|
| Agglomerative Clustering | [Просмотр](https://github.com/victorsemipalatin/sirius_2024/blob/main/code/tsne_visualization_agglomerative_silhouette.html) |
| K-Medoids | [Просмотр](https://github.com/victorsemipalatin/sirius_2024/blob/main/code/tsne_visualization_kmedoids.html) |
| Spectral Clustering | [Просмотр](https://github.com/victorsemipalatin/sirius_2024/blob/main/code/tsne_visualization_spectral.html) |
| Affinity Propagation | [Просмотр](https://github.com/victorsemipalatin/sirius_2024/blob/main/code/tsne_visualization_affinity_propagation.html) |

## Описание визуализаций

Каждая визуализация представляет собой интерактивный HTML-файл, содержащий:
- t-SNE проекцию данных
- Цветовую кодировку кластеров
- Возможность масштабирования и перемещения по графику
- Информацию о принадлежности точек к кластерам

## Использование

Для просмотра визуализаций:
1. Перейдите по соответствующей ссылке
2. Дождитесь загрузки интерактивного графика
3. Используйте мышь для навигации по визуализации:
   - Колесико мыши для масштабирования
   - Зажатая ЛКМ для перемещения
   - Наведение на точки для получения дополнительной информации

## Размер файлов
Каждый HTML-файл с визуализацией занимает примерно 3.96 MB.
