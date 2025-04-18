from celery_app import celery
import docker

client=docker.from_env()

@celery.task(bind=True)
def build_image(self, image_name, project_path):
    self.update_state(state="PROGRESS")
    try:
        client.images.build(
            path=project_path,
            tag=image_name,
            rm=True
        )
        self.update_state(state="")
        return 
    except Exception as e:
        return e
    return {"status": "built", "tag": image_name}
