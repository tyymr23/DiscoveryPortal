from celery_app import celery
import docker
from dotenv import load_dotenv
import os
import shutil
client=docker.from_env()
load_dotenv()

upload_dir=os.getenv("UPLOAD_DIR")

@celery.task(bind=True)
def build_image(self, image_name, project_path):
    self.update_state(state="PROGRESS")
    try:
        client.images.build(
            path=project_path,
            tag=image_name,
            rm=True
        )
        self.update_state(state="SUCCESS")
        code_path=os.path.join(upload_dir,image_name) 
        shutil.rmtree(code_path)
        return {"status": "built"}
    except:
        self.update_state(state="FAILURE")
        return {"status": "failed"}
