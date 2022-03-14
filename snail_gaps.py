import os


class SnailGapsController:
    def __init__(self, meta_dir, images_dir):
        self.meta_dir = meta_dir
        self.images_dir = images_dir

    def run(self):
        meta_list = os.listdir(self.meta_dir)
        image_list = os.listdir(self.images_dir)
        sorted_meta = sorted(meta_list)
        self.fill_gaps(sorted_meta, image_list)

    def fill_gaps(self, sorted_meta, image_list):
        running_number = 1
        for metaname in sorted_meta:
            snail_number = metaname.replace('.json', '')
            if self.exists_image(snail_number, image_list):
                if running_number < int(snail_number):
                    padded_running = f'{running_number:05}'
                    self.rename_meta(padded_running, snail_number)
                    self.rename_image(padded_running, snail_number)
                running_number += 1
            else:
                self.delete_meta(metaname)

    def delete_meta(self, filename):
        full_filename = f'{self.meta_dir}/{filename}'
        print(f'Removing {full_filename}')
        os.remove(full_filename)

    def exists_image(self, snail_number, image_list):
        name = f'{snail_number}.png'
        return name in image_list

    def rename_meta(self, running_number, snail_number):
        print(f'Renaming {snail_number} to {running_number}')
        full_src = f'{self.meta_dir}/{snail_number}.json'
        full_dest = f'{self.meta_dir}/{running_number}.json'
        os.rename(full_src, full_dest)

    def rename_image(self, running_number, snail_number):
        full_src = f'{self.images_dir}/{snail_number}.png'
        full_dest = f'{self.images_dir}/{running_number}.png'
        os.rename(full_src, full_dest)

META_LIST = ['0001.json','0002.json','0003.json','0004.json','0005.json','0006.json','0007.json','0008.json']
IMG_LIST = ['0001.png','0003.png','0005.png','0006.png','0008.png',]

if __name__ == '__main__':
    ctrl = SnailGapsController('./snails/metadata', '/Users/darko/Downloads/images')
    ctrl.run()
