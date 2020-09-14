import os
from news.settings import BASE_DIR


def new_image_directory(instance, filename):
    """Загружает файл в дерикторию to MEDIA_ROOT/section_<title>/new_<title>/<filename>"""
    return f"section_{instance.section}/new_{instance.title.replace(' ', '_')}/{filename}"


def section_image_directory(instance, filename):
    """Загружает файл в дерикторию to MEDIA_ROOT/section_<title>/<filename>"""
    return f"section_{0}/{1}".format(instance.title, filename)


def redact_directory(self):
    """Проверяет наличие папки со старым названием и переименовывает её"""
    root = f"{BASE_DIR}/media/section_{self.section}/"
    oldtitle = 'new_' + str(self.old_title).replace(" ", "_")
    if os.path.isdir(root + oldtitle):
        last_title = 'new_' + str(self.title).replace(" ", "_")
        os.chdir(root)
        os.rename(oldtitle, last_title)
        self.old_title = self.title
