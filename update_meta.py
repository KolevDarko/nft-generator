import json
import os
import data

full_map = {
    'Background': {
        'Purple Dark': 'Dark Purple',
        'Purple Light': 'Light Purple',
        'Green Dark': 'Dark Green',
        'Green Light': 'Light Green',
        'Blue Dark': 'Dark Blue',
        'Blue Light': 'Light Blue',
        'Grey': 'Gray'
    },
    'Skin': {
        'PurpleMutant': 'Purple Mutant',
        'BlueFish': 'Fish Scales'
    },
    'Mouth': {
        'Tongue': 'Tongue Out',
        '01.png': 'Grin Smile'
    },
    'Object above': {
        'Cap Red': 'Red Cap',
        'Cap Blue': 'Blue Cap'
    },
    'Object under': {
        'UFO Purple': 'Purple UFO',
        'UFO Green': 'Green UFO',
        'UFO Orange': 'Orange UFO',
        'Surfboard Blue': 'Blue Surfboard',
        'Surfboard Green': 'Green Surfboard',
        'Surfboard Orange': 'Striped Surfboard',
        'Broom Green': 'Green Broom',
        'Broom Purple': 'Purple Broom',
        'Skateboard Blue': 'Blue Skateboard',
        'Skateboard Green': 'Green Skateboard',
        'Skateboard Red': 'Red Skateboard',
        'Skateboard Rainbow': 'Rainbow Skateboard',
        'Slime Green': 'Green Slime',
        'Slime Yellow': 'Yellow Slime',
        'Tank Blue': 'Blue Tank',
        'Tank Red': 'Red Tank',
        'Umbrella Blue': 'Blue Umbrella',
    }
}

class MetaController:
    DESCRIPTION = 'A collection of 7777 Cheeky Snails sliding over the congested ethereum blockchain.'
    BASE_IMG_URL = 'https://ipfs.io/ipfs/QmYRcTUetx1UGgLRFPxb1mq6DmHmaLiLuepuLv8bQKvgUb'

    def gen_meta(self, source, dest):
        meta_files = sorted(os.listdir(source))
        for filename in meta_files:
            fr = open(f'{source}/{filename}', 'r')
            raw = fr.read()
            json_data = json.loads(raw)
            fr.close()
            long_num = filename.split('.')[0]
            new_num = int(long_num) - 1
            new_img_num = f'{new_num:05}'
            json_data['name'] = f'Cheeky Snail #{new_num}'
            json_data['description'] = MetaController.DESCRIPTION
            json_data['image'] = f'{MetaController.BASE_IMG_URL}/{new_img_num}.png'
            fixed_attributes = self.fix_errors(json_data)
            json_data['attributes'] = fixed_attributes
            self.fix_greens(new_num, json_data)
            fw = open(f'{dest}/{new_num}', 'w+')
            fw.write(json.dumps(json_data))
            fw.close()
        print('finished')

    def fix_errors(self, data):
        results = list(data['attributes'])
        for idx, vals in enumerate(data['attributes']):
            trait_type = vals['trait_type']
            value = vals['value']
            fixed_value = self.fix_attr(value, trait_type)
            results[idx]['value'] = fixed_value
        return results

    def fix_attr(self, value, trait_type):
        if trait_type in full_map:
            clean_val = ' '.join(value.split())
            category_map = full_map[trait_type]
            if category_map.get(clean_val):
                print(f'Cleaned {trait_type}, {clean_val} into {category_map[clean_val]}')
                return category_map[clean_val]
            return clean_val

    def fix_greens(self, number, json_data):
        pale_green_int = [int(n) for n in data.pale_green]
        grey_int = [int(n) for n in data.gray]
        if number in pale_green_int:
            print('Fixing pale green')
            bg_idx = [i for i, a in enumerate(json_data['attributes']) if a['trait_type'] == 'Background'][0]
            assert json_data['attributes'][bg_idx]['trait_type'] == 'Background'
            json_data['attributes'][bg_idx]['value'] = 'Pale Green'
        elif number in grey_int:
            print('fixing grey')
            bg_idx = [i for i, a in enumerate(json_data['attributes']) if a['trait_type'] == 'Background'][0]
            assert json_data['attributes'][bg_idx]['trait_type'] == 'Background'
            json_data['attributes'][bg_idx]['value'] = 'Grey'

if __name__ == '__main__':
    surf_extractor = MetaController()
    surf_extractor.gen_meta('./snails/metadata', './snails/rez')
