from DownloadModel import DownloadModel
from Preprocess import Preprocess
from ImageToEmbed import ImageToEmbed
from KeyValueDB import KeyValueDB
from VectorDB import VectorDB

import time

class PrepareData:
    def __init__(self, uids_path):
        self.uids = self.parse_uids(uids_path)

    def prepare(self, image_folder_path, view_num):
        download_model = DownloadModel("model.zip", "extracted/", "TOKEN.txt")
        preprocess = Preprocess()
        image_converter = ImageToEmbed()

        qdrant = VectorDB()
        qdrant.deleteCollection("vector_collection")
        qdrant.createCollection("vector_collection", 768)

        postgre = KeyValueDB()
        postgre.createTable("vector_model")

        image_cnt = 0
        for uid in self.uids:
            try:
                download_model.download(uid)
            except Exception as e:
                print(e)
                print("Error while downloading occured")
                continue

            print("Model downloaded, extracting...")

            try:
                model_temp_path = download_model.extract_from_zip()
            except Exception as e:
                print("Error while extracting occured")
                continue

            print("Model extracted, rendering...")

            try:
                preprocess.render_gltf_with_rotations(model_temp_path, image_folder_path, image_cnt)
            except Exception as e:
                print("Error while creating renders occured")
                print(e)
                continue
            
            print("Renders created, creating embeddings...")
            
            embeddings = []
            try:
                for i in range(view_num):
                    embeddings.append(image_converter.convert(image_folder_path + "/" + str(image_cnt + i) + ".png"))
            except Exception as e:
                print(e)
                print("Error while creating embeddings occured")
                continue

            print("Embeddings created, writing to vector database...")

            embeddings_less = []
            for i, embedding in enumerate(embeddings):
                embedding_less = []
                for num in embedding:
                    embedding_less.append(float(str(num)[:5]))
                
                embeddings_less.append(embedding_less)
            
            embeddings = embeddings_less.copy()

            for i, embedding in enumerate(embeddings):
                qdrant.addVector("vector_collection", embedding, image_cnt + i)

            print("Wrote to vector database, writing to key-value database...")

            for i, embedding in enumerate(embeddings):
                entry = ""
                for num in embedding:
                    entry += str(num) + " "


                try:
                    postgre.addImage(table_name="vector_model", embedding=entry, url=str(uid))
                except Exception as e:
                    postgre.conn.rollback()
                    print(e)
                    print("Embedding like this was already added, moving further")

            print("All done")
            
            image_cnt += view_num
        
        postgre.cur.close()
        postgre.conn.close()


    def parse_uids(self, uids_path):
        f = open(uids_path, 'r')

        uids = []
        for line in f.readlines():
            uids.append(line[:len(line)-1])

        return uids
    

prepare_data = PrepareData("uids.txt")
prepare_data.prepare('images', 24)