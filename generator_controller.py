import datetime
import json
import os
import random

from PIL import Image

WEIGHT_MAP = {1: 0.4, 2: 0.25, 3: 0.2, 4: 0.1, 5: 0.05}

RARITY_COUNTS = {
    1: {
        'bg': 8,
        'eyes': 3,
        'mouth': 7,
        'above': 12,
        'bellow': 10
    },
    2: {
        'bg': 7,
        'eyes': 3,
        'mouth': 4,
        'above': 9,
        'bellow': 8
    },
    3: {
        'bg': 6,
        'eyes': 2,
        'mouth': 3,
        'above': 8,
        'bellow': 8
    },
    4: {
        'bg': 4,
        'eyes': 2,
        'mouth': 3,
        'above': 8,
        'bellow': 8
    },
    5: {
        'bg': 8,
        'eyes': 3,
        'mouth': 7,
        'above': 12,
        'bellow': 10
    },
}


def gen_random():
    categories = list(WEIGHT_MAP.keys())
    weights = list(WEIGHT_MAP.values())
    return random.choices(categories, weights)


picked_imgs = {
    1: {
        'eyes': [],
        'mouth': [],
        'backgrounds': [],
        'object-above': [],
        'object-under': []
    },
    2: {
        'eyes': [],
        'mouth': [],
        'backgrounds': [],
        'object-above': [],
        'object-under': []
    },
    3: {
        'eyes': [],
        'mouth': [],
        'backgrounds': [],
        'object-above': [],
        'object-under': []
    },
    4: {
        'eyes': [],
        'mouth': [],
        'backgrounds': [],
        'object-above': [],
        'object-under': []
    },
    5: {
        'eyes': [],
        'mouth': [],
        'backgrounds': [],
        'object-above': [],
        'object-under': []
    }
}


def pick_next(full_list, used_list):
    for el in full_list:
        if el not in used_list:
            return el


def perform_picking(el_list, prev_picked):
    el_name = pick_next(el_list, prev_picked)
    if el_name:
        prev_picked.append(el_name)
    else:
        el_name = random.choice(el_list)
    return el_name


def pick_random_image(el_type, no_overlapping=False):
    category_id = gen_random()[0]
    el_dir = f'{RARITIES_DIR}/{category_id}/{el_type}'
    el_list = os.listdir(el_dir)
    if no_overlapping:
        filtered_list = [el for el in el_list if 'overlaping' not in el.lower()]
        el_name = perform_picking(filtered_list, picked_imgs[category_id][el_type])
    else:
        el_name = perform_picking(el_list, picked_imgs[category_id][el_type])
    el_img = Image.open(f'{el_dir}/{el_name}')
    return el_img, el_name


def extract_body_names(body_full_name):
    parts = body_full_name.split('.')[0].split('-shell-')
    body = parts[0]
    shell = parts[1]
    return body, shell


def extract_part_name(part_name):
    if '-' not in part_name:
        return part_name
    parts = part_name.split('-')
    return parts[3].strip()


def get_body_eyes(body_theme):
    dir_list = os.listdir('./images/skins')
    if 'squid' in body_theme.lower():
        body_dirname = 'DM - Squid Games'
    elif body_theme == 'HermitCrabBlue':
        body_dirname = 'DM - Hermit Crab Snail Blue'
    elif body_theme == 'HermitCrab':
        body_dirname = 'DM - Hermit Crab Snail'
    elif body_theme == 'TheSnail':
        return Image.open('./base-eyes.png')
    elif body_theme == 'YellowZebra':
        body_dirname = 'DM - Zebra Yellow'
    elif body_theme == 'Zebra':
        body_dirname = 'DM - Zebra White Skin'
    else:
        body_dirname = get_body_dir(dir_list, body_theme)
    if body_dirname is None:
        raise Exception(f'no dir found for {body_theme}')
    body_dir = f'./images/skins/{body_dirname}'
    eyes_file = None
    for filename in os.listdir(body_dir):
        if 'eyes' in filename.lower():
            eyes_file = filename
            break
    if not eyes_file:
        raise Exception('Cant find eyes for skin')
    return Image.open(f'{body_dir}/{eyes_file}')


def get_body_dir(dir_list, theme):
    if theme == 'PurpleRobot':
        return 'DM - Robot Purple'
    elif theme == 'Robot':
        return 'DM - Robot snail'
    for dirname in dir_list:
        merged_dir = dirname.replace(' ', '')
        if theme.lower() in merged_dir.lower():
            return dirname
    return None


def extract_skin_name(full_body):
    name = full_body.split('-')[0]
    return name


def generate_complete_snails_once(snails_dir, start=0, limit=None):
    i = start
    for body_full_name in os.listdir(snails_dir):
        i += 1
        skin_name = extract_skin_name(body_full_name)
        body_img_name = f'{snails_dir}/{body_full_name}'
        padded_i = gen_snail_for_body(body_img_name, skin_name, i)
        if not padded_i:
            i -= 1
            print(f'Not saved snail {padded_i}, trying again')
            continue
        print(f'Saved snail {padded_i}')
        if limit and i >= limit:
            return


def get_random_body():
    bodies = os.listdir('./results/all_bodies')
    body_name = random.choice(bodies)
    body_img = Image.open(f'./results/all_bodies/{body_name}')
    return body_img, body_name


def generate_random_snails(count, start_idx=0):
    i = start_idx
    for _ in range(count):
        all_skin_dirs = os.listdir('./images/skins')
        _, body_name = get_random_body()
        i += 1
        padded_i = gen_snail_for_body(all_skin_dirs, body_name, i)
        print(f'Saved snail {padded_i}')


RARITIES_DIR = '/Users/darko/Documents/RARITIES'


def gen_snail_for_body(body_img_name, skin_name, i):
    is_miscreation = False
    if 'miscreation' in skin_name:
        body_eyes = None
        is_miscreation = True
    else:
        body_eyes = get_body_eyes(skin_name)
    eyewear_img, eyewear_name = extract_eyewear()
    bg_img, bg_name = pick_random_image('backgrounds')
    mouth_img, mouth_name = pick_random_image('mouth')
    above_img, above_name, bellow_img, bellow_name = extract_above_bellow(is_miscreation)
    body_img = Image.open(body_img_name)
    if bellow_img:
        first = Image.alpha_composite(bg_img, bellow_img)
    else:
        first = bg_img
    second = Image.alpha_composite(first, body_img)
    if above_img:
        third = Image.alpha_composite(second, above_img)
    else:
        third = second
    if body_eyes:
        four = Image.alpha_composite(third, body_eyes)
    else:
        four = third
    if 'hellboy' in skin_name.lower():
        horns = Image.open('./horns.png')
        four = Image.alpha_composite(four, horns)
    if eyewear_img:
        final = Image.alpha_composite(four, eyewear_img)
    else:
        final = four
    if 'squid' in skin_name.lower():
        final = final
        mouth_name = 'None'
    else:
        final = Image.alpha_composite(final, mouth_img)
    padded_i = f'{i:05}'
    final.save(f'./snails/images/{padded_i}.png')
    save_metadata(above_name, bellow_name, bg_name,
                  skin_name, eyewear_name, mouth_name, padded_i)
    return padded_i


def extract_eyewear():
    object_probs = random.random()
    if object_probs <= 0.5:
        eyes_img, eyes_name = pick_random_image('eyes')
    else:
        eyes_img, eyes_name = None, 'None'
    return eyes_img, eyes_name


def extract_above_bellow(is_miscreation):
    above_img, above_name = None, 'None'
    bellow_img, bellow_name = None, 'None'
    object_probs = random.random()
    if object_probs <= 0.05:
        above_img, above_name = pick_random_image('object-above', no_overlapping=is_miscreation)
        bellow_img, bellow_name = pick_random_image('object-under')
    elif object_probs <= 0.35:
        above_img, above_name = pick_random_image('object-above', no_overlapping=is_miscreation)
    elif object_probs <= 0.95:
        bellow_img, bellow_name = pick_random_image('object-under')
    return above_img, above_name, bellow_img, bellow_name


def save_metadata(above_name, below_name, bg_name, skin_name, eyes_name, mouth_name, padded_i):
    birthday_day = random.randint(0, 364)
    snail_birthday = datetime.datetime(
        year=2021, month=1, day=1) + datetime.timedelta(days=birthday_day)
    snail_name = f'Cheeky Snail #{padded_i}'
    metadata = {
        "description": "CheekySnails from the Blockchain.",
        "external_url": "https://cheekysnails.com",
        "image": "{image-ipfs}",
        "name": snail_name,
        "attributes": [
            {
                "display_type": "date",
                "trait_type": "Birthday",
                "value": int(snail_birthday.timestamp())
            },
            {
                "trait_type": "Skin",
                "value": skin_name
            },
            {
                "trait_type": "Background",
                "value": extract_part_name(bg_name)
            },
            {
                "trait_type": "Eyewear",
                "value": extract_part_name(eyes_name)
            },
            {
                "trait_type": "Mouth",
                "value": extract_part_name(mouth_name)
            },
            {
                "trait_type": "Object above",
                "value": extract_part_name(above_name)
            },
            {
                "trait_type": "Object under",
                "value": extract_part_name(below_name)
            },
        ]
    }
    with open(f'./snails/metadata/{padded_i}.json', 'w') as f:
        f.write(json.dumps(metadata))


def generate_one_original(dirname):
    eyes = None
    skin1 = None
    skin2 = None
    shell = None
    for filename in os.listdir(f'./images/skins/{dirname}'):
        if 'eyes' in filename.lower():
            eyes = Image.open(f'./images/skins/{dirname}/{filename}')
        if 'shell' in filename.lower():
            shell = Image.open(f'./images/skins/{dirname}/{filename}')
        if 'skin 1' in filename.lower():
            skin1 = Image.open(f'./images/skins/{dirname}/{filename}')
        if 'skin 2' in filename.lower():
            skin2 = Image.open(f'./images/skins/{dirname}/{filename}')
    l1 = skin2
    l2 = Image.alpha_composite(l1, shell)
    l3 = Image.alpha_composite(l2, skin1)
    final = Image.alpha_composite(l3, eyes)
    theme = dirname.split('-')[-1]
    print(f'generated {theme}')
    final.save(f'./results/originals/{theme}.png')


def generate_originals():
    for dirname in os.listdir('./images/skins'):
        generate_one_original(dirname)


def extract_part(dirname, part_name):
    part_filename = None
    for filename in os.listdir('./images/skins/' + dirname):
        if part_name in filename.lower():
            part_filename = filename
            break
    return Image.open(f'./images/skins/{dirname}/{part_filename}')


def generate_all_bodies():
    i = 0
    for dirname_body in os.listdir('./images/skins'):
        create_combos_for_body(dirname_body)


def create_combos_for_body(dirname_body):
    eyes = extract_part(dirname_body, 'eyes')
    skin1 = extract_part(dirname_body, 'skin 1')
    skin2 = extract_part(dirname_body, 'skin 2')
    i = 0
    for dirname_shell in os.listdir('./images/skins'):
        i += 1
        shell = extract_part(dirname_shell, 'shell')
        l1 = skin2
        l2 = Image.alpha_composite(l1, shell)
        l3 = Image.alpha_composite(l2, skin1)
        final = Image.alpha_composite(l3, eyes)
        theme_body = dirname_body.split('-')[-1].strip()
        theme_shell = dirname_shell.split('-')[-1].strip()
        name = f'{theme_body}-shell-{theme_shell}'
        print(f'{i}. {name}')
        final.save(f'./results/all_bodies/{name}.png')


def generate_base_combos(dirname_body):
    create_combos_for_body(dirname_body)


def cleanup_snails(limit=None):
    i = 0
    for bodyname in os.listdir('./results/all_bodies'):
        justname = bodyname.split('.')[0]
        parts = justname.split('-shell-')
        try:
            m, n = parts[0], parts[1]
        except IndexError:
            print('error with', bodyname)
            continue
        remove = False
        if n == 'Lava Snail':
            remove = True
        elif m == n:
            remove = True
        elif 'Squid Game' in n:
            remove = True
        elif 'Hermit Crab' in n:
            remove = True
        if remove:
            i += 1
            os.remove(f'./results/all_bodies/{bodyname}')
            print(f'Removed {bodyname}')
            if limit and i >= limit:
                break


class GeneratorController:

    def __init__(self, base_dir, img_dir, meta_dir, weights_map, traits_order):
        self.base_dir = base_dir
        self.img_dir = img_dir
        self.meta_dir = meta_dir
        self.weights_map = weights_map
        self.traits_order = traits_order

    def generate_all_images(self, total_count, start=0):
        i = start
        unique_names = set()
        while i < start + total_count:
            attributes = {}
            unique_name = None
            print(f'Generating image {i}')
            result_img = None
            for trait_type in self.traits_order:
                category_id = self.get_random_category()
                trait_val = self.gen_random_trait_by_category(category_id, trait_type)
                trait_img = self.open_img(f'{self.base_dir}/{category_id}/{trait_type}/{trait_val}').convert('RGBA')
                if not result_img:
                    result_img = trait_img
                else:
                    result_img = Image.alpha_composite(result_img, trait_img)
                if not unique_name:
                    unique_name = trait_val
                else:
                    unique_name += f'-{trait_val}'
                attributes[trait_type] = trait_val
            if unique_name in unique_names:
                continue
            else:
                i += 1
                unique_names.add(unique_name)
            image_name = f'{i}.png'
            result_img.save(f'{self.img_dir}/{image_name}')
            self.store_metadata(i, attributes)

    def store_metadata(self, idx, attributes):
        attrs_list = [{key: value} for key, value in attributes.items()]
        nft_name = f'Girl #{idx}'
        full_metadata = {
            "description": "Daydreaming on the Blockchain.",
            "external_url": "https://daydreaming.com",
            "image": "{image-ipfs}",
            "name": nft_name,
            'attributes': attrs_list,
        }
        metadata_file = open(f'{self.meta_dir}/{idx}.json', 'w')
        metadata_file.write(json.dumps(full_metadata))
        metadata_file.close()

    def gen_random_trait_by_category(self, category_id, trait_name):
        trait_list = os.listdir(f'{self.base_dir}/{category_id}/{trait_name}')
        random_trait_val = random.choice(trait_list)
        return random_trait_val

    def get_random_category(self):
        categories = list(self.weights_map.keys())
        weights = list(self.weights_map.values())
        return random.choices(categories, weights)[0]

    def open_img(self, full_path):
        return Image.open(f'{full_path}')


if __name__ == '__main__':
    ctrl = GeneratorController('./data/rarities-daydreaming', './data/results-img', './data/results-metadata',
                               WEIGHT_MAP,
                               ['background', 'backhair', 'name', 'earrings', 'clothes', 'necklaces', 'fronthair',
                                'headwear', 'glasses'])
    ctrl.generate_all_images(2, 50)
