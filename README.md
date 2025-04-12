# VoluMetric: A 3D Model Embedding and Retrieval Framework Using Vision Transformers

## About the Project
VoluMetric is a system designed for efficient embedding and retrieval of 3D models. By leveraging Vision Transformers (ViTs) and a robust multi-angle rendering pipeline, the system encodes 3D models into high-dimensional vector spaces, enabling accurate content-based retrieval. The embeddings are stored and managed using scalable vector databases like Qdrant, integrated with PostgreSQL for metadata handling. VoluMetric aims to address the challenges of traditional keyword-based searches, offering a scalable and efficient solution suitable for applications in gaming, design, and education. Silhouette-based embeddings were also explored as an alternative, although they exhibited limitations in performance compared to ViT-based embeddings.


Example:

There is an input image

![image](https://github.com/user-attachments/assets/6f400c50-30d8-477f-90cf-0847bcfc9bea)

And the resulting models that are found among the downloaded sketchfab local library (consisting of 5000 models)

![image](https://github.com/user-attachments/assets/ced0b247-b8cc-4664-88b0-d35104cd3fe9)

![image](https://github.com/user-attachments/assets/b933e8c2-cd5b-4753-9dde-bffd0a78f1e4)

![image](https://github.com/user-attachments/assets/424fd594-6019-40e7-89b5-d19ce1adcc05)

The images are not exactly perfect, since the library was limited in size because of sketchfab API restrictions.

Using this method, the whole library of Sketchfab can be loaded and efficiently processed using just 200 GB of disk space
