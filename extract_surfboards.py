import json
import shutil
import os
class SurfExtractor:

    def extract(self):
        img_file_list = self.extract_img_names()
        for img_file in img_file_list:
            try:
                img_path = f'/Users/darko/Downloads/images/{img_file}'
                shutil.copyfile(img_path, f'./surfboarders/{img_file}')
            except:
                print("Missed", img_file)
        print('finished')

    def extract_img_names(self):
        results = []
        with open('./surfboards.txt', 'r') as f:
            for line in f:
                data = line.strip()
                number = data.split('.')[0]
                img_name = f'{number}.png'
                results.append(img_name)
        return results

    def fix(self, blue_dir, green_dir):
        blue_ones = os.listdir(green_dir)
        for blue_file in sorted(blue_ones):
            num = blue_file.split('.')[0]
            meta_filename = f'./snails/metadata/{num}.json'
            self.update_meta(meta_filename, 'Surfboard Green')
            print('updated', meta_filename)

    def update_meta(self, meta_filename, surfboard_value):
        updated = False
        with open(meta_filename, 'r') as f:
            json_data = json.loads(f.read())
            for i, attr in enumerate(json_data['attributes']):
                if attr['trait_type'] == 'Object under':
                    if not attr['value']:
                        json_data['attributes'][i]['value'] = surfboard_value
                        updated = True
                    else:
                        print('skipping', meta_filename)
                    break
        if updated:
            with open(meta_filename, 'w+') as f:
                f.write(json.dumps(json_data))


if __name__ == '__main__':
    surf_extractor = SurfExtractor()
    surf_extractor.fix('./surfboarders/blue', './surfboarders/green')

