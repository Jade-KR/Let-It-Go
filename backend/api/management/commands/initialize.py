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
        print("complete")
        print("Loading color data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "color.p"
        with open(cur_file, 'rb') as f:
            color_list = pickle.load(f)
        print("complete")
        print("Loading part_categories data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "part_categories.p"
        with open(cur_file, 'rb') as f:
            part_categories_list = pickle.load(f)
        print("complete")
        print("Loading theme data")
        cur_file = Path(settings.BASE_DIR) / "crawling" / "data" / "theme.p"
        with open(cur_file, 'rb') as f:
            theme_categories_list = pickle.load(f)
        print("complete")


        
        # print("Reading part ")
        # parts = []
        # for i in range(1, 37):

        #     cur_file = Path(settings.BASE_DIR) / "crawling" /  "data" / "part_{}".format(i)
        #     try:
        #         print(cur_file)
        #         with open(cur_file, 'rb') as f:
        #             data = pickle.load(f)
        #             parts = parts + data["results"]
        #     except:
        #         print("error")
        # cur_file = Path(settings.BASE_DIR) / "crawling" /  "data" / "part"
        # with open(cur_file, 'wb') as f:
        #     pickle.dump(parts, f)
        # print(len(parts))
        # # print(Path(settings.BASE_DIR))
        # sets = []
        # for i in range(1, 17):
        #     cur_file = Path(settings.BASE_DIR) / "crawling" /  "data" / "temp" / "set_{}".format(i)
        #     try:
        #         print(cur_file)
        #         with open(cur_file, 'rb') as f:
        #             data = pickle.load(f)
        #             sets = sets + data["results"]
        #     except:
        #         print("error")
        # print(len(sets))
        # cur_file = Path(settings.BASE_DIR) / "crawling" /  "data" / "set"
        # with open(cur_file, 'wb') as f:
        #     pickle.dump(sets, f)
        # print(sets)
        # # with open
        print("[*] Loading data...")
        # dataframe pkl 파일을 읽어오는 _load_dataframes함수를 실행합니다.
        dataframes = self._load_dataframes()
        store_images = pd.read_pickle('store_image.p')
        store_review_count_df = dataframes["reviews"][["store", "user"]].groupby("store").count()
        user_review_count_df = dataframes["reviews"][["store", "user"]].groupby("user").count()
        store_review_count_df_index_set = set(store_review_count_df.index)
        user_review_count_df_index_set = set(user_review_count_df.index)
        # 데이터 중 빈 값들을 0.0으로 입력해 줍니다.
        dataframes["stores"]["latitude"] = dataframes["stores"]["latitude"].fillna(0.0)
        dataframes["stores"]["longitude"] = dataframes["stores"]["longitude"].fillna(0.0)
        dataframes["menues"]["price"]=dataframes["menues"]["price"].fillna(0).astype(int)
        
        print("[*] Delete all data...")
        # DB에 저장된 정보를 모두 지워 초기화해 줍니다.
        models.Store.objects.all().delete()
        models.CustomUser.objects.all().delete()
        models.Review.objects.all().delete()
        models.Menu.objects.all().delete()
        models.StoreImage.objects.all().delete()
        models.UserLikeStore.objects.all().delete()
        models.Algorithm.objects.all().delete()
        print("[+] Done")

        print("[*] Initializing stores...")
        # DB에 데이터를 작성합니다.

        stores = dataframes["stores"]
        # 데이터프레임에서 매장 정보를 가져옵니다.
        stores_bulk = [
            models.Store(
                id=store.id,
                store_name=store.store_name,
                branch=store.branch,
                area=store.area,
                tel=store.tel,
                address=store.address,
                latitude=store.latitude,
                longitude=store.longitude,
                category=store.category,
                review_count=store_review_count_df.loc[store.id] if store.id in store_review_count_df_index_set else 0,
                tag=store.tag
            )
            for store in stores.itertuples()
        ]
        # 벌크데이터 리스트를 만들고 모델에 입력합니다.
        models.Store.objects.bulk_create(stores_bulk)
        print("[+] Done")

        print("[*] Initializing users...")
        # store와 거의 동일.
        users = dataframes["users"]
        users_bulk = [
            models.CustomUser(
                id=user.id,
                username=user.id,
                gender=user.gender,
                age=user.age,
                # 유저가 작성한 리뷰 갯수를 입력합니다.
                # 머신러닝에서 DB 데이터를 활용하기 위해 미리 계산해 칼럼에 입력합니다.
                review_count=user_review_count_df.loc[user.id] if user.id in user_review_count_df_index_set else 0
            )
            for user in users.itertuples()
        ]
        models.CustomUser.objects.bulk_create(users_bulk)
        print("[+] Done")

        print("[*] Initializing menues...")
        menues = dataframes["menues"]
        menues_bulk = [
            models.Menu(
                id=menu.id,
                store_id=menu.store,
                menu_name=menu.menu_name,
                price=menu.price,
            )
            for menu in menues.itertuples()
        ]
        models.Menu.objects.bulk_create(menues_bulk)
        print("[+] Done")

        print("[*] Initializing reviews...")
        reviews = dataframes["reviews"]
        reviews_bulk = [
            models.Review(
                store_id=review.store,
                store_name=models.Store.objects.get(id=review.store).store_name,
                user_id=review.user,
                score=review.score,
                content=review.content,
                reg_time=review.reg_time,
            )
            for review in reviews.itertuples()
        ]
        models.Review.objects.bulk_create(reviews_bulk)
        print("[+] Done")

        print("[*] Initializing Algorithm...")
        models.Algorithm.objects.create(alg_name="svdpp")
        print("[+] Done")
        
        print("[*] Initializing learning dataframe...")
        userset = set()
        for user in models.CustomUser.objects.filter(review_count__gte=10).values("id"):
            userset.add(user['id'])
        # 리뷰가 열개 이상인 매장
        storeset = set()
        for store in models.Store.objects.filter(review_count__gte=10).values("id"):
            storeset.add(store['id'])
        df = pd.DataFrame(models.Review.objects.all().values("user", "store", "score"))
        df = df[df["user"].isin(userset) & df["store"].isin(storeset)]
        
        with open('learning_dataframe.p', 'wb') as f:
            pickle.dump(df, f)

        print("[+] Done")


        print("[*] Initializing store_image...")
        
        store_image_bulk = [
            models.StoreImage(
                store_id=store_image.store_id,
                url=store_image.url,
            )
            for store_image in store_images.itertuples()
        ]
        models.StoreImage.objects.bulk_create(store_image_bulk)
        print("[+] Done")
        

    def handle(self, *args, **kwargs):
        # python manage.py initialize를 실행하면 가장 먼저 들어오는 부분
        # _initialize함수를 실행한다.
        self._initialize()
