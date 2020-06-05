from pathlib import Path
import pandas as pd
from django.core.management.base import BaseCommand
from backend import settings
from api import models
import pickle


class Command(BaseCommand):
    help = "initialize database"
    DATA_DIR = Path(settings.BASE_DIR).parent / "data"
    DATA_FILE = str(DATA_DIR / "dump.pkl")

    def _load_dataframes(self):
        '''
        데이터프레임을 읽어옵니다.
        '''
        try:
            data = pd.read_pickle(Command.DATA_FILE)
        except:
            print(f"[-] Reading {Command.DATA_FILE} failed")
            exit(1)
        return data

    def _initialize(self):
        '''
        기존의 dataframe pkl파일을 읽어와서 DB에 저장합니다.
        '''
        print("Loading part data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "part.p"
        with open(cur_file, 'rb') as f:
            part_list = pickle.load(f)
        print("complete")
        print("Loading set data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "set.p"
        with open(cur_file, 'rb') as f:
            set_list = pickle.load(f)
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "set2.p"
        with open(cur_file, 'rb') as f:
            set_list2 = pickle.load(f)
        print("complete")
        print("Loading color data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "color.p"
        with open(cur_file, 'rb') as f:
            color_list = pickle.load(f)["results"]
        print("complete")
        print("Loading part_categories data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "part_categories.p"
        with open(cur_file, 'rb') as f:
            part_categories_list = pickle.load(f)["results"]
        print("complete")
        print("Loading theme data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "theme.p"
        with open(cur_file, 'rb') as f:
            theme_list = pickle.load(f)
        print("complete")
        print("Loading setpart data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "setpart.p"
        with open(cur_file, 'rb') as f:
            setpart_list = pickle.load(f)
        print("complete")
        print("Loading user data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "user.p"
        with open(cur_file, 'rb') as f:
            user_list = pickle.load(f)
        print("complete")
        print("Loading review data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "review.p"
        with open(cur_file, 'rb') as f:
            review_list = pickle.load(f)
        print("complete")
        
        print("[*] Delete all data...")
        # DB에 저장된 정보를 모두 지워 초기화해 줍니다.
        models.CustomUser.objects.all().delete()
        models.Theme.objects.all().delete()
        models.LegoSet.objects.all().delete()
        models.OfficialMapping.objects.all().delete()
        models.Category.objects.all().delete()
        models.Review.objects.all().delete()
        models.LegoPart.objects.all().delete()
        models.Color.objects.all().delete()
        models.UserPart.objects.all().delete()
        models.SetPart.objects.all().delete()
        print("[+] Done")

        print("[*] Initializing categories...")
        categories_bulk = [
            models.Category(
                id=category["id"],
                name=category["name"],
                part_count=category["part_count"]
            )
            for category in part_categories_list
        ]
        models.Category.objects.bulk_create(categories_bulk)
        print("[+] Done")

        print("[*] Initializing colors...")
        colors_bulk = [
            models.Color(
                id=color["id"],
                name=color["name"],
                rgb=color["rgb"],
                bricklink_ids="|".join(map(str, color["external_ids"]["BrickLink"]["ext_ids"])) if color["external_ids"].get("BrickLink") and color["external_ids"]["BrickLink"].get("ext_ids") else "",
                bricklink_descrs="|".join(color["external_ids"]["BrickLink"]["ext_descrs"][0]) if color["external_ids"].get("BrickLink") and color["external_ids"]["BrickLink"].get("ext_descrs") else "",
                official_ids="|".join(map(str, color["external_ids"]["LEGO"]["ext_ids"])) if color["external_ids"].get("LEGO") and color["external_ids"]["LEGO"].get("ext_ids") else "",
                official_descrs="|".join(color["external_ids"]["LEGO"]["ext_descrs"][0]) if color["external_ids"].get("LEGO") and color["external_ids"]["LEGO"].get("ext_descrs") else "",
            )
            for color in color_list
        ]
        models.Color.objects.bulk_create(colors_bulk)
        models.Color.objects.create(id=9999, name="not a color", rgb="000000")
        models.Color.objects.create(id=-1, name="Unknown", rgb="0033B2")
        print("[+] Done")

        print("[*] Initializing themes...")
        themes_bulk = [
            models.Theme(
                id=theme["id"],
                parent_id=theme["parent_id"],
                name=theme["name"],
                root_id=theme["root_id"]
            )
            for theme in theme_list
        ]
        models.Theme.objects.bulk_create(themes_bulk)
        print("[+] Done")
        
        print("[*] Initializing sets...")
         # theme     name    n  um_parts     images  review_count
        sets_bulk = [
            models.LegoSet(
                theme_id=legoset[0],
                name=legoset[1],
                num_parts=legoset[2],
                images=legoset[3],
                review_count=legoset[4],
            )
            for legoset in set_list
        ]
        models.LegoSet.objects.bulk_create(sets_bulk)
        print("[+] Done")

        print("[*] Initializing official mapping table...")
        mapping_table = [
            models.OfficialMapping(
                id=v["set_num"],
                lego_set_id=i
            )
            for i, v in enumerate(set_list2, 1)
        ]
        models.OfficialMapping.objects.bulk_create(mapping_table)
        print("[+] Done")
        
        print("[*] Initializing lego parts...")
        lego_part_bulk = [
            models.LegoPart(
                id=part["part_num"],
                name=part["name"],
                category_id=part["part_cat_id"],
                image=part["part_img_url"] if part["part_img_url"] else "",
                bricklink_ids="|".join(part["external_ids"]["BrickLink"]) if part["external_ids"].get("BrickLink") else "",
                official_ids="|".join(part["external_ids"]["LEGO"]) if part["external_ids"].get("LEGO") else ""
            )
            for part in part_list
        ]
        models.LegoPart.objects.bulk_create(lego_part_bulk)
        print("[+] Done")

        print("[*] Initializing setparts...")
        # inventory_id	part_num	color_id	quantity
        setpart_bulk = [
            models.SetPart(
                lego_set_id=part[0],
                quantity=part[3],
                color_id=part[2],
                part_id=part[1]
            )
            for part in setpart_list
        ]
        models.SetPart.objects.bulk_create(setpart_bulk)
        print("[+] Done")

        print("[*] Initializing users...")
        #   id  username    nickname    age gender  review_count
        user_bulk = [
            models.CustomUser(
                id=user[0],
                username=user[1],
                nickname=user[1],
                age=user[3],
                gender=user[4],
                review_count=user[5]
            )
            for user in user_list
        ]
        models.CustomUser.objects.bulk_create(user_bulk)
        print("[+] Done")

        print("[*] Initializing reviews...")
        # score user_id lego_set_id
        review_bulk = [
            models.Review(
                score=review[0],
                user_id=review[1],
                lego_set_id=review[2]
            )
            for review in review_list
        ]
        models.Review.objects.bulk_create(review_bulk)
        print("[+] Done")

    def handle(self, *args, **kwargs):
        # python manage.py initialize를 실행하면 가장 먼저 들어오는 부분
        # _initialize함수를 실행한다.
        self._initialize()
