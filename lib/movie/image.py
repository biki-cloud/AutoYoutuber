from PIL import Image

def resize(img_path, size: tuple):
    """
    画像をリサイズする
    :param img_path: 画像のパス
    :param save_path: 保存先のパス
    :param size: リサイズ後のサイズ
    :return:
    """
    img = Image.open(img_path)
    img_resize = img.resize(size)
    img_resize.save(img_path)