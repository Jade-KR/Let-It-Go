from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, Theme, LegoSet, OfficialMapping, Category, Review, LegoPart, Color, UserPart, UserPart2, SetPart, UserLikeLegoSet
from api import models, serializers
from allauth.account.models import EmailAddress
from rest_framework import viewsets, mixins
from rest_framework.schemas import AutoSchema
from rest_framework.decorators import api_view, action, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction
import requests
from rest_auth.views import LoginView
import pandas as pd
import surprise
import pickle
from sklearn.cluster import KMeans

API_key = '08d368a0e1830b9fec088091be154133'
headers = {
    'Authorization': 'key ' + API_key,
    'Accept': 'application/json'
}
# 추천할 아이템 갯수
recommend_num = 10
# 콜드스타트 기준 리뷰 갯수
recommend_review_num = 10
# 성별정보 수치화
male_value = 5
female_value = 0
# 리뷰를 평가하기 위해 필요한 최소 리뷰 갯수
min_review = 5
# user_based knn 알고리즘에서 적용할 클러스터 갯수
cluster_num = 4

with open("data/knn_item_based.p", "rb") as f:
    global knn_item_based
    knn_item_based = pickle.load(f)

with open("data/knn_user_based.p", "rb") as f:
    global knn_user_based
    knn_user_based = pickle.load(f)

with open("data/k_means_item_based.p", "rb") as f:
    global theme_legoset, legoset_theme_root, all_legoset_calculated
    theme_legoset = pickle.load(f)
    legoset_theme_root = pickle.load(f)
    all_legoset_calculated = pickle.load(f)

with open('data/k_means_user_based.p', 'rb') as f:
    global cluster_list, centroid
    cluster_list = pickle.load(f)
    centroid = pickle.load(f)

def get_cluster(age, gender):
    gtoi = female_value if gender else male_value

    index = -1
    init_distance = 9999999
    if cluster_num != len(centroid):
        reset_user_based_k_means()
    for i in range(cluster_num):
        distance_y = centroid[i][0]
        distance_x = centroid[i][1]
        distance = (distance_y-age)*(distance_y-age) + (distance_x-gtoi)*(distance_x-gtoi)
        if init_distance > distance:
            init_distance = distance
            index = i
    return index

def crawling_part_data(pk):
    cur_page = 1
    if OfficialMapping.objects.filter(lego_set_id=pk):
        set_name = OfficialMapping.objects.get(lego_set_id=pk).id
        while True:
            res = requests.get(url='https://rebrickable.com/api/v3/lego/sets/{}/parts/?page={}&page_size=1000'.format(set_name, cur_page), headers=headers).json()
            parts = res["results"]
            part = parts[0]
            test = SetPart(
                    lego_set_id=pk,
                    part_id=part["part"]["part_num"],
                    color_id=part["color"]["id"],
                    quantity=part["quantity"]
            )
            part_bulk = [
                SetPart(
                    lego_set_id=pk,
                    part_id=part["part"]["part_num"],
                    color_id=part["color"]["id"],
                    quantity=part["quantity"]
                )
                for part in parts
            ]
            SetPart.objects.bulk_create(part_bulk, ignore_conflicts=True)

            if not res["next"]:
                break
            cur_page += 1

# 메서드 정리
# class UserViewSet(viewsets.ViewSet):
#     """
#     Example empty viewset demonstrating the standard
#     actions that will be handled by a router class.

#     If you're using format suffixes, make sure to also include
#     the `format=None` keyword argument for each action.
#     """

#     def list(self, request):
#         pass
#     def create(self, request):
#         pass
#     def retrieve(self, request, pk=None):
#         pass
#     def update(self, request, pk=None):
#         pass
#     def partial_update(self, request, pk=None):
#         pass
#     def destroy(self, request, pk=None):
#         pass

class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10000

class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    pagination_class = SmallPagination

class LegoSetViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    GET params
    name
    tag
    theme
    
    '''
    # queryset = LegoSet.objects.all()
    serializer_class = serializers.LegoSetSerializer2
    pagination_class = SmallPagination

    # 쿼리셋을 word 받아서 스플릿하고 세트명, 태그, 테마 검색해보기
    # 해당하는것 전부 포함시키기
    def get_queryset(self):
        queryset = []
        tmp = set()
        if self.request.query_params.get("name"):
            for word in self.request.query_params["name"].split(' '):
                for legoset in LegoSet.objects.filter(name__contains=word).order_by("-id"):
                    if legoset.id not in tmp:
                        tmp.add(legoset.id)
                        queryset.append(legoset)
            queryset.sort(key=lambda x:-x.id)
            return queryset
        elif self.request.query_params.get("tag"):
            for word in self.request.query_params["tag"].split(' '):
                for legoset in LegoSet.objects.filter(tags__contains=word).order_by("-id"):
                    if legoset.id not in tmp:
                        tmp.add(legoset.id)
                        queryset.append(legoset)
            queryset.sort(key=lambda x:-x.id)
            return queryset
        elif self.request.query_params.get("theme"):
            queryset = LegoSet.objects.filter(theme_id=self.request.query_params["theme"]).order_by("-id")
            return queryset
        return LegoSet.objects.all().order_by("-id")

    def list(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer_data = serializers.LegoSetSerializer(page, many=True).data
            if request.user.is_authenticated:
                user_id = request.user.id
                for legoset in serializer_data:
                    legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user_id) else 0
                    legoset["is_review"] = 1 if Review.objects.filter(lego_set_id=legoset["id"], user_id=user_id) else 0
            else:
                for legoset in serializer_data:
                    legoset["is_like"] = 0
                    legoset["is_review"] = 0
            return self.get_paginated_response(serializer_data)

        serializer_data = serializers.LegoSetSerializer(queryset, many=True).data
        user_id = request.user.id
        if request.user.is_authenticated:
            user_id = request.user.id
            for legoset in serializer_data:
                legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user_id) else 0
                legoset["is_review"] = 1 if Review.objects.filter(lego_set_id=legoset["id"], user_id=user_id) else 0
        else:
            for legoset in serializer_data:
                legoset["is_like"] = 0
                legoset["is_review"] = 0
        user_id = request.user.id

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        user_id = request.user.id
        legoset = get_object_or_404(LegoSet, id=pk)
        serializer_data = serializers.LegoSetSerializer2(legoset).data
        if request.user.is_authenticated:
            serializer_data["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=pk, customuser_id=user_id) else 0
            serializer_data["is_review"] = 1 if Review.objects.filter(lego_set_id=pk, user_id=user_id) else 0
        else:
            serializer_data["is_like"] = 0
            serializer_data["is_review"] = 0
        reviews = serializers.ReviewSerializer(legoset.review_set.all().order_by("-created_at"), many=True).data
        serializer_data["reviews"] = reviews
        return Response(serializer_data)

    def destroy(self, request, pk=None):
        legoset = get_object_or_404(LegoSet, pk=pk)
        if request.user.is_staff or (request.user.is_authenticated and legoset.user.id == request.user.id):
            legoset.delete()
            return Response("삭제 완료")
        return Response("삭제 실패")

class LegoPartViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LegoPart.objects.all()
    serializer_class = serializers.LegoPartSerializer
    pagination_class = SmallPagination

class UserPartViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserPartSerializer
    pagination_class = SmallPagination
    queryset = UserPart.objects.all()

    def list(self, request):
        if request.user.is_authenticated:
            queryset = UserPart.objects.filter(user=request.user)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("로그인이 필요합니다.")

class SetPartViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SetPartSerializer
    queryset = SetPart.objects.all()

    def retrieve(self, request, pk=None):
        queryset = SetPart.objects.filter(lego_set_id=pk)
        if queryset:
            serializer_data = serializers.SetPartSerializer(queryset, many=True).data
            return Response(serializer_data)
        elif OfficialMapping.objects.get(lego_set_id=pk):
            crawling_part_data(pk)
            queryset = SetPart.objects.filter(lego_set_id=pk)
            serializer_data = serializers.SetPartSerializer(queryset, many=True).data
            return Response(serializer_data)
        return Response("")

@api_view(['POST'])
def set_user_category(self):
    categories = self.data.get("categories")
    user = CustomUser.objects.get(id=self.user.id)
    user.categories = categories
    user.save()
    return Response("카테고리 등록 완료")

class CustomLoginView(LoginView):
    def get_response(self):
        user = get_object_or_404(models.CustomUser, username=self.user)
        orginal_response = super().get_response()
        mydata = {
            "nickname": user.nickname,
            "image": user.image,
            "comment": user.comment,
            "age": user.age,
            "gender": user.gender,
            "is_staff": user.is_staff,
            "categories": user.categories,
            # "category_list": user.category_list,
            "status": "success",
            }
        orginal_response.data["user"].update(mydata)
        return orginal_response

class ReviewViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = SmallPagination
    queryset = Review.objects.all().order_by('-id')

    def list(self, request):
        if request.user.is_staff:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("스태프 권한이 필요합니다.")

    def create(self, request):
        if request.user.is_authenticated:
            data = request.data
            user = get_object_or_404(get_user_model(), id=request.user.id)
            legoset = get_object_or_404(LegoSet, id=data["lego_set_id"])
            legoset.review_count += 1
            user.review_count += 1
            with transaction.atomic():
                Review.objects.create(lego_set_id=data["lego_set_id"], user=user, content=data["content"], score=data["score"])
                legoset.save()
                user.save()
        return Response("리뷰 작성 완료")

    def update(self, request, pk=None):
        review = get_object_or_404(Review, pk=pk)
        user_id = request.user_id
        if request.user.is_authenticated and review.user_id == user_id:
            data = request.data
            review.content = data["content"]
            review.score = data["score"]
            return Response("수정 완료")
        return Response("수정 실패")

    def destroy(self, request, pk=None):
        review = get_object_or_404(Review, pk=pk)
        if request.user.is_staff or (request.user.is_authenticated and review.user.id == request.user.id):
            user = get_object_or_404(get_user_model(), id=request.user.id)
            legoset = review.lego_set
            legoset.review_count -= 1
            user.review_count -= 1
            with transaction.atomic():
                legoset.save()
                user.save()
                review.delete()
            return Response("삭제 완료")
        return Response("삭제 실패")

class FollowUserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer
    pagination_class = SmallPagination
    queryset = CustomUser.objects.all()

    def retrieve(self, request, pk=None):
        user = get_object_or_404(get_user_model(), pk=pk)
        followers = user.followers.all()
        page = self.paginate_queryset(followers)
        
        if page is not None:
            serializer = serializers.UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.LegoSetSerializer(followers, many=True)
        return Response(serializer.data)

class FollowingUserViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer
    pagination_class = SmallPagination
    queryset = CustomUser.objects.all()

    def retrieve(self, request, pk=None):
        user = get_object_or_404(get_user_model(), pk=pk)
        followings = user.followings.all()
        page = self.paginate_queryset(followings)

        if page is not None:
            serializer = serializers.UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.LegoSetSerializer(followings, many=True)
        return Response(serializer.data)

class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer
    pagination_class = SmallPagination
    queryset = CustomUser.objects.all().order_by("-date_joined")

    def list(self, request):
        if request.user.is_staff:
            queryset = self.filter_queryset(self.get_queryset())

            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = serializers.UserSerializer2(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.serializers.UserSerializer2(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("접근 실패")

    def retrieve(self, request, pk=None):
        user = get_object_or_404(get_user_model(), id=pk)
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        user = get_object_or_404(get_user_model(), id=pk)
        emailaddress = get_object_or_404(EmailAddress, user_id=pk)
        if request.user.is_authenticated and request.user == user:
            data = request.data
            user.nickname = data["nickname"]
            user.comment = data["comment"]
            user.email = data["email"]
            emailaddress.email = data["email"]
            user.save()
            emailaddress.save()
            return Response("수정 완료")
        elif request.user.is_staff and request.user != user:
            if user.is_staff:
                user.is_staff = False
            else:
                user.is_staff = True
            user.save()
            return Response("권한 변경 성공")
        else:
            return Response("접근 실패")

    def destroy(self, request, pk=None):
        user = get_object_or_404(get_user_model(), id=pk)
        if request.user.is_authenticated and request.user == user:
            user.is_active = False
            user.save()
            return Response("탈퇴 완료")
        elif request.user.is_staff and request.user != user:
            if user.is_active:
                user.is_active = False
                user.save()
                return Response("블럭 성공")
            else:
                user.is_active = True
                user.save()
                return Response("블럭 해제")
        else:
            return Response("접근 실패")

@api_view(['PUT'])
def UpdateUserProfile(self):
    user = self.user
    if user.is_authenticated:
        print(self.data["profile_url"])
        user.image = self.data["profile_url"]
        user.save()
        return Response("프로필 수정 완료")
    return Response("프로필 수정 실패")

class UserLegoSetViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer
    pagination_class = SmallPagination
    queryset = LegoSet.objects.all()

    def retrieve(self, request, pk=None):
        user = request.user
        if user.is_authenticated:
            queryset = LegoSet.objects.filter(user_id=pk)
            page = self.paginate_queryset(queryset)
            serializer_data = serializers.LegoSetSerializer(page, many=True).data
            for legoset in serializer_data:
                legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user.id) else 0
                legoset["is_review"] = 1 if Review.objects.filter(lego_set_id=legoset["id"], user_id=user.id) else 0
            if page is not None:
                return self.get_paginated_response(serializer_data)
            return Response(serializer_data)
        else:
            return Response("로그인이 필요합니다.")

class UserLikeLegoSetViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer
    pagination_class = SmallPagination
    queryset = LegoSet.objects.all()

    def retrieve(self, request, pk=None):
        user = get_object_or_404(get_user_model(), id=pk)
        queryset = user.like_sets.all().order_by('-created_at')
        page = self.paginate_queryset(queryset)
        user_id = request.user.id
        serializer_data = serializers.LegoSetSerializer(page, many=True).data
        for legoset in serializer_data:
            legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user_id) else 0
            legoset["is_review"] = 1 if Review.objects.filter(lego_set_id=legoset["id"], user_id=user_id) else 0
        if page is not None:
            return self.get_paginated_response(serializer_data)

        serializer = serializers.LegoSetSerializer(queryset, many=True)
        return Response(serializer_data)

class LegoSetRankingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer2
    pagination_class = SmallPagination

    def list(self, request):
        queryset = LegoSet.objects.all().order_by("-like_count")
        page = self.paginate_queryset(queryset)
        user = request.user

        if page is not None:
            serializer_data = serializers.LegoSetSerializer(page, many=True).data
            if request.user.is_authenticated:
                user_id = request.user.id
                for legoset in serializer_data:
                    legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user_id) else 0
                    legoset["is_review"] = 1 if Review.objects.filter(lego_set_id=legoset["id"], user_id=user.id) else 0
                return self.get_paginated_response(serializer_data)
            else:
                for legoset in serializer_data:
                    legoset["is_like"] = 0
                    legoset["is_review"] = 0
                return self.get_paginated_response(serializer_data)
            serializer = serializers.LegoSetSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.LegoSetSerializer(queryset, many=True)
        return Response(serializer.data)

class ItemBasedRecommendViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer
    pagination_class = SmallPagination
    queryset = LegoSet.objects.all()
    
    def retrieve(self, request, pk=None):
        legoset = LegoSet.objects.get(pk=pk)
        if legoset.review_count >= recommend_review_num:
            try:
                lego_set_inner_id = knn_item_based.trainset.to_inner_iid(int(pk))
                top_neighbors = knn_item_based.get_neighbors(lego_set_inner_id, k=recommend_num)
                top_neighbors = [LegoSet.objects.get(id=knn_item_based.trainset.to_raw_iid(inner_id)) for inner_id in top_neighbors]
                serializer_data = self.get_serializer(top_neighbors, many=True).data
            except:
                queryset = theme_legoset[legoset.theme.root_id]
                for i in range(len(queryset)):
                    if queryset[i].id == pk:
                        queryset[i], queryset[-1] = queryset[-1], queryset[i]
                        queryset.pop()
                        break
                i = 0
                qeuryset = queryset[:recommend_num]
                while len(queryset) <= recommend_num:
                    if all_legoset_calculated[i].id != pk:
                        queryset.append(all_legoset_calculated[i])
                    i += 1
                queryset = [LegoSet.objects.get(id=legoset.id) for legoset in queryset]
                serializer_data = self.get_serializer(queryset, many=True).data
        else:
            queryset = theme_legoset[legoset.theme.root_id]
            for i in range(len(queryset)):
                if queryset[i].id == pk:
                    queryset[i], queryset[-1] = queryset[-1], queryset[i]
                    queryset.pop()
                    break
            i = 0
            qeuryset = queryset[:recommend_num]
            while len(queryset) <= recommend_num:
                if all_legoset_calculated[i].id != pk:
                    queryset.append(all_legoset_calculated[i])
                i += 1
            queryset = [LegoSet.objects.get(id=legoset.id) for legoset in queryset]
            
            serializer_data = self.get_serializer(queryset, many=True).data
        user = request.user
        if user.is_authenticated:
            for legoset in serializer_data:
                legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user.id) else 0
                legoset["is_review"] = 1 if Review.objects.filter(lego_set_id=legoset["id"], user_id=user.id) else 0
        else:
            for legoset in serializer_data:
                legoset["is_like"] = 0
                legoset["is_review"] = 0
        
        return Response(serializer_data)

class UserBasedRecommendViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer
    queryset = LegoSet.objects.all()

    def list(self, request):
        user = request.user
        if user.is_authenticated:
            if request.user.review_count >= recommend_review_num:
                # 리뷰 작성 안한 설계도 가져온다
                queryset = []
                user = request.user
                user_legoset_set = set()
                for legoset in user.legoset_set.all():
                    user_legoset_set.add(legoset.id)
                for legoset in LegoSet.objects.filter(review_count__gte=10):
                    if legoset.id not in user_legoset_set:
                        queryset.append(legoset)
                predictions = [[knn_user_based.predict(user.id, legoset_id).est, legoset_id] for legoset_id in queryset]
                predictions.sort(key=lambda x: x[0])
                recommend = [legoset for score, legoset in predictions[:recommend_num]]
                serializer_data = serializers.LegoSetSerializer(recommend, many=True).data

                if user.is_authenticated:
                    for legoset in serializer_data:
                        legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user.id) else 0
                        legoset["is_review"] = 1 if Review.objects.filter(lego_set_id=legoset["id"], user_id=user.id) else 0
                else:
                    for legoset in serializer_data:
                        legoset["is_like"] = 0
                        legoset["is_review"] = 0
                return Response(serializer_data)
            else:
                queryset = [LegoSet.objects.get(id=x) for x in cluster_list[get_cluster(user.age, user.gender)]]
                return Response(serializers.LegoSetSerializer(queryset, many=True).data)
        else:
            return Response("로그인이 필요합니다.")

@api_view(['POST'])
def UpdateUserPart(self):
    '''
    {
        "UpdateList": [
            {
                "part_id": String,
                "color_id": Integer,
                "qte": Integer
            }
        ]
    }
    ---
    parameters:
    - name: username
      description: Foobar long description goes here
      required: true
      type: string
      paramType: form
    - name: password
      paramType: form
      required: true
      type: string

    '''
    user = self.user
    # user = CustomUser.objects.get(id=self.user)
    if user.is_authenticated:
        update_d = self.data.get("UpdateList")
        # 유저 보유 데이터 정리하기
        inventory_dict = dict()
        for userpart in UserPart.objects.filter(user=user):
            if not inventory_dict.get(userpart.part_id):
                inventory_dict[userpart.part_id] = dict()

            inventory_dict[userpart.part_id][userpart.color_id] = userpart

        # 갱신리스트
        a = []
        # 삭제리스트
        b = []
        # 생성리스트
        c = []
        # 사용자 요청 데이터들에 대해서 반복문을 돌리며 갱신 혹은 삭제할 것들 확인한다.
        for part in update_d:
            # 유저가 보유하고 있는 아이템이라면
            if inventory_dict.get(part["part_id"]) and inventory_dict[part["part_id"]].get(part["color_id"]):
                tmp = inventory_dict[part["part_id"]][part["color_id"]]
                # 증감 후에도 0보다 크다면
                if tmp.quantity + part["qte"] > 0:
                    # 업데이트리스트에 추가
                    tmp.quantity += part["qte"]
                    a.append(tmp)
                # 0보다 작거나 같으면
                else:
                    # 삭제리스트에 추가
                    b.append(tmp)
            # 유저가 보유하고 있지 않은 아이템이라면
            else:
                if part["qte"] > 0:
                    c.append(UserPart(user=user, part_id=part["part_id"], color_id=part["color_id"], quantity=part["qte"]))
        # 갱신해야하는 값들을 갱신한다
        UserPart.objects.bulk_update(a, ["quantity"])
        # 생성해야하는 값들을 생성한다
        UserPart.objects.bulk_create(c)
        # 삭제해야할 값들을 삭제한다.
        for userpart in b:
            userpart.delete()

    return Response("수정 완료")


@api_view(['POST'])
def UpdateUserPart2(self):
    user = self.user
    print(user)
    print(self.data)
    if user.is_authenticated:
        data = self.data
        UserPart2.objects.create(user=user, part_id=data["part_id"], color_id=data["color_id"])
        print(1)

    return Response("수정 완료")

@api_view(['POST'])
def CreateLegoSet(self):
    '''
    {
        "theme_id": Integer,
        "set_images": String, # ex: "img1|img2"
        "set_name": String,
        "description": String,
        "tags": String, # ex: "tag1|tag2"
        "reference": String,
        "parts": [
            {
                "part_id": String,
                "color_id": Integer,
                "quantity": String
            }
        ]
    }
    '''
    user = self.user
    # user = CustomUser.objects.get(id=self.user)
    if user.is_authenticated:
        data = self.data
        cur_id = LegoSet.objects.all().order_by('-id')[0].id + 1
        lego_set = LegoSet.objects.create(
            id=cur_id,
            user=user,
            theme_id=data["theme_id"],
            name=data["set_name"],
            num_parts=len(data["parts"]),
            images=data["set_images"],
            description=data["description"],
            tags=data["tags"],
            references=data["reference"],
            )
        create_part_list = [
            SetPart(
                lego_set=lego_set,
                part_id=part["part_id"],
                color_id=part["color_id"],
                quantity=part["quantity"]
            )
            for part in data["parts"]
        ]
        SetPart.objects.bulk_create(create_part_list)

    return Response("등록 완료")
def go_to_myhome(request):
    return redirect("http://127.0.0.1:8000/api/swagger/")

@api_view(['POST'])
def like_set(self):
    '''
    {
        "set_id": Integer    # LegoSet.id
    }
    '''
    user = self.user
    if user.is_authenticated:
        lego_set = get_object_or_404(LegoSet, id=self.data["set_id"])
        if user.like_sets.filter(id=lego_set.id):
            with transaction.atomic():
                user.like_sets.remove(lego_set)
                lego_set.like_count -= 1
                lego_set.save()
            return Response("좋아요 취소")
        else:
            with transaction.atomic():
                user.like_sets.add(lego_set)
                lego_set.like_count += 1
                lego_set.save()
            return Response("좋아요")
    else:
        return Response("비 인증 유저")

@api_view(['POST'])
def follow(self):
    '''
    {
        "user_id": Integer    # CustomUser.id
    }
    '''
    user = self.user
    if user.is_authenticated:
        follow_user = get_object_or_404(get_user_model(), id=self.data["user_id"])
        if user.followings.filter(id=follow_user.id):
            user.followings.remove(follow_user)
            return Response("팔로우 취소")
        else:
            user.followings.add(follow_user)
            return Response("팔로우")
    else:
        return Response("비 인증 유저")


@api_view(['GET'])
def crawll(self, idx):
    for i in range(idx, idx + 50):
        if not SetPart.objects.filter(lego_set_id=i):
            print('crawll ' + str(i))
            try:
                crawling_part_data(i)
            except:
                print('fail on ' + str(i))

    
@api_view(['GET'])
def user_parts_registered_by_IoT(self):
    user = self.user
    if user.is_authenticated:
        user_parts = UserPart2.objects.filter(user=user)
        user_part_dict = dict()
        for part in user_parts:
            if user_part_dict.get(part.part_id):
                if user_part_dict[part.part_id].get(part.color_id):
                    user_part_dict[part.part_id][part.color_id]["quantity"] += 1
                else:
                    user_part_dict[part.part_id][part.color_id] = {"part_id": part.part_id, "color_id": part.color_id, "quantity": 1}
            else:
                user_part_dict[part.part_id] = {part.color_id: {"part_id": part.part_id, "color_id": part.color_id, "quantity": 1}}
        # print(user_part_dict)
        res = []
        for part_id, color_dict in user_part_dict.items():
            # print(color_dict)
            for color_id, part in color_dict.items():
                res.append(part)
        return Response(res)
    else:
        return Response("비 인증 유저")

@api_view(['GET'])
def reset_item_based_knn(self):
    global knn_item_based
    user_df = pd.DataFrame(CustomUser.objects.all().values("id", "age", "gender"))
    review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "lego_set_id"))

    ten_user_df = review_df.groupby("user_id").count()
    temp_review_df = review_df.groupby("lego_set_id").count()

    # 10개 이상의 레고작성글에 대한 것
    ten_lego_set = set(temp_review_df[temp_review_df['score']>=10].index)

    # 10개 이상의 리뷰를 남긴 user
    ten_user_set = set(ten_user_df[ten_user_df["score"]>=10].index)

    # 해당 작품에 대한 리뷰가 10개이상이면서 10개 이상 작성자의 정보만 남김
    ten_review_df = review_df[review_df['user_id'].isin(ten_user_set)]
    ten_review_df = ten_review_df[ten_review_df['lego_set_id'].isin(ten_lego_set)]

    ratings_df = ten_review_df[['user_id', 'lego_set_id', 'score']]
    # print(ratings_df)

    # reader => 범위 설정  & 학습 부분
    reader = surprise.Reader(rating_scale=(1, 5))
    review_data = surprise.Dataset.load_from_df(df=ratings_df, reader=reader)
    trainset = review_data.build_full_trainset()

    # 피어슨 유사도로 학습
    sim_options = {'name': 'pearson_baseline', 'user_based': False}
    knn_item_based = surprise.KNNBaseline(k=10, sim_options=sim_options)
    knn_item_based.fit(trainset)
    with open("data/knn_item_based.p", "wb") as f:
        pickle.dump(knn_item_based, f)
    return Response("reset item based knn completed")

@api_view(['GET'])
def reset_item_based_k_means(self):
    global theme_legoset, legoset_theme_root, all_legoset_calculated
    theme_root = dict()
    theme_legoset = dict()
    for theme in Theme.objects.all():
        theme_root[theme.id] = theme.root_id
        theme_legoset[theme.root_id] = dict()
    legoset_theme_root = dict()
    for legoset in LegoSet.objects.all():
        legoset_theme_root[legoset.id] = theme_root[legoset.theme_id]

    a_s = 0
    a_c = 0
    for score in Review.objects.all().values("score"):
        a_s += score["score"]
        a_c += 1
    a = a_s/a_c

    for review in Review.objects.all():
        if theme_legoset.get(theme_root[review.lego_set.theme_id]):
            if theme_legoset[theme_root[review.lego_set.theme_id]].get(review.lego_set_id):
                theme_legoset[theme_root[review.lego_set.theme_id]][review.lego_set_id].append(review.score)
            else:
                theme_legoset[theme_root[review.lego_set.theme_id]][review.lego_set_id] = [review.score]
        else:
            theme_legoset[theme_root[review.lego_set.theme_id]] = {review.lego_set_id: [review.score]}

    all_score = []
    func = lambda x: (len(x) / (len(x) + min_review))*(sum(x)/len(x)) + min_review/(len(x)+min_review)*a
    for root_id in theme_legoset.keys():
        for legoset_id in theme_legoset[root_id].keys():
            theme_legoset[root_id][legoset_id] = func(theme_legoset[root_id][legoset_id])
        for k, v in theme_legoset[root_id].items():
            all_score.append([v, k])
        theme_legoset[root_id] = [LegoSet.objects.get(id=x[1]) for x in sorted([[v, k] for k, v in theme_legoset[root_id].items()], reverse=True)]
    # theme_legoset는 테마 루트아이디를 키로 가지고 그 루트아이디에 속하는 설계도들의 인기도 점수 높은 순으로 반환한다.
    
    all_score.sort(reverse=True)
    all_legoset_calculated = [LegoSet.objects.get(id=x[1]) for x in all_score]

    with open("data/k_means_item_based.p", "wb") as f:
        pickle.dump(theme_legoset, f)
        pickle.dump(legoset_theme_root, f)
        pickle.dump(all_legoset_calculated, f)
    return Response("reset item based k_means completed")

@api_view(['GET'])
def reset_user_based_knn(self):
    global knn_user_based
    user_df = pd.DataFrame(CustomUser.objects.all().values("id", "age", "gender"))
    review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "lego_set_id"))

    ten_user_df = review_df.groupby("user_id").count()
    temp_review_df = review_df.groupby("lego_set_id").count()

    # 10개 이상의 레고작성글에 대한 것
    ten_lego_set = set(temp_review_df[temp_review_df['score']>=10].index)

    # 10개 이상의 리뷰를 남긴 user
    ten_user_set = set(ten_user_df[ten_user_df["score"]>=10].index)

    # 해당 작품에 대한 리뷰가 10개이상이면서 10개 이상 작성자의 정보만 남김
    ten_review_df = review_df[review_df['user_id'].isin(ten_user_set)]
    ten_review_df = ten_review_df[ten_review_df['lego_set_id'].isin(ten_lego_set)]

    ratings_df = ten_review_df[['user_id', 'lego_set_id', 'score']]
    # print(ratings_df)

    # reader => 범위 설정  & 학습 부분
    reader = surprise.Reader(rating_scale=(1, 5))
    review_data = surprise.Dataset.load_from_df(df=ratings_df, reader=reader)
    trainset = review_data.build_full_trainset()

    # 피어슨 유사도로 학습
    sim_options = {'name': 'pearson_baseline', 'user_based': True}
    knn_user_based = surprise.KNNBaseline(k=10, sim_options=sim_options)
    knn_user_based.fit(trainset)
    with open("data/knn_user_based.p", "wb") as f:
        pickle.dump(knn_user_based, f)
        
    return Response("reset user based knn completed")

@api_view(['GET'])
def reset_user_based_k_means(self):
    global centroid, cluster_list
    # user_df = pd.DataFrame(CustomUser.objects.filter(review_count__gte=10))
    user_df = pd.DataFrame(CustomUser.objects.all().values("id", "age", "gender"))
    male_value = 5
    female_value = 0
    min_review = 5

    # gender 값을 정수로 변환
    user_df['gender'] = user_df['gender'].apply(lambda x: male_value*x)

    # kmeans 학습
    kmeans = KMeans(n_clusters=cluster_num, init='k-means++', max_iter=300, random_state=0)
    # print(user_df[["age", "gender"]])
    kmeans.fit(user_df[["age", "gender"]])
    # print('cluster 완료')

    # kmeans.labels_ : 몇번 클러스터인지 라벨링 붙이고 분리했었던 id col을 붙임
    user_df['cluster'] = kmeans.labels_
    review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "lego_set_id"))
    user_df = user_df[user_df['id'].isin(set(review_df['user_id']))]

    user_df = user_df.set_index('id')
    # 리뷰 테이블에 유저 클러스터정보를 조인해서 합쳐준다.
    temp_df = pd.merge(user_df["cluster"], review_df, left_index=True, right_on="user_id")
    temp_df["score"] = temp_df["score"].astype(float)

    # 클러스터의 인덱스에 클러스터 번호에 해당하는 정보만 가져와서 저장한다.
    cluster_list = [temp_df[["lego_set_id", "score"]][temp_df["cluster"]==i] for i in range(cluster_num)]

    for i in range(cluster_num):
        # cluster 각각을 store로 묶는다
        cluster_list[i] = cluster_list[i].groupby('lego_set_id').agg(['sum', 'count', 'mean'])['score']
        cluster_list[i] = cluster_list[i][cluster_list[i]['count']>=5]

        # 각 클러스터별 평균평점을 계산한다.
        a = sum(cluster_list[i]['sum']) / sum(cluster_list[i]['count'])

        # calc 칼럼을 추가하고 거기에 인기도 점수 계산한 값을 넣어준다.
        cluster_list[i]['calc'] = cluster_list[i].apply(lambda x: ((x['count']/(x['count']+min_review))*x['mean'] + (min_review/x['count']+min_review))*a, axis=1)

        # calc 기준으로 내림차순 정렬한다.
        cluster_list[i].sort_values(['calc'], ascending=False, inplace=True)
        cluster_list[i] = cluster_list[i].index

    # centroid -> 저쟁해야하는 값
    centroid = kmeans.cluster_centers_

    with open('data/k_means_user_based.p', 'wb') as f:
        pickle.dump(cluster_list, f)
        pickle.dump(centroid, f)
    return Response("reset user based k_means completed")