import io
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile


def generate_test_image(name='test_image.jpg', size=(100, 100), color=(255, 0, 0)):
    """Génère une petite image pour les tests."""
    file = io.BytesIO()
    image = Image.new('RGB', size, color)
    image.save(file, 'JPEG')
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type='image/jpeg')
