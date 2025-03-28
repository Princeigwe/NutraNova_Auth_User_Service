from threading import Thread
from utils.upload_image import upload_and_get_image_details
from utils.emit_profile_image_update import emit_profile_image


class UploadImageThread(Thread):
    def __init__(self, file, user_email):
        Thread.__init__(self)
        self.file = file
        self.user_email = user_email

    def run(self) -> None:
        upload = upload_and_get_image_details(self.file)
        # "secure_url" is the cloudinary image url from the get image info response.
        emit_profile_image(upload["secure_url"], self.user_email)
