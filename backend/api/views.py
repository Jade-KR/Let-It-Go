from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, Theme, LegoSet, OfficialMapping, Category, Review, LegoPart, Color, UserPart, UserPart2, SetPart, UserLikeLegoSet, UserSet
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
# 추천할 아이템 개수
recommend_num = 10
# 콜드스타트 기준 리뷰 개수
recommend_review_num = 10
# 성별정보 수치화
male_value = 5
female_value = 0
# 리뷰를 평가하기 위해 필요한 최소 리뷰 개수(의미있는 리뷰 개수)
min_review = 5
# user_based knn 알고리즘에서 적용할 클러스터 개수
cluster_num = 4
# 남성에 해당하는 값
male_value = 5
# 여성에 해당하는 값
female_value = 0
# user category에 존재시 값
exist_value = 10
# user category에 존재 안할 시 값
nonexist_value = 0
# 존재하는 user category
category_list = ["건축물", "장난감", "공상과학", "레이싱", "클래식", "창작품", "게임", "히어로", "공룡"]

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

def get_cluster(age, gender, categories):
    if not categories:
        categories = ''
    gtoi = female_value if gender else male_value
    category_set = set(categories.split('|'))

    index = -1
    init_distance = 9999999
    if cluster_num != len(centroid):
        reset_user_based_k_means()
    for i in range(cluster_num):
        distance = (centroid[i][0] - age)**2 + (centroid[i][1] - gtoi)**2
        for j in range(2, 11):
            distance += (centroid[i][j] - (exist_value if category_list[j-2] in category_set else nonexist_value))**2
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
        '''
        요청이 들어오면 설계도 리스트를 반환합니다.
        '''
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
        '''
        요청이 들어오면 pk에 해당하는 설계도 정보를 반환합니다.
        '''
        user_id = request.user.id
        legoset = get_object_or_404(LegoSet, id=pk)
        serializer_data = serializers.LegoSetSerializer2(legoset).data
        # set_quantity
        if request.user.is_authenticated:
            serializer_data["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=pk, customuser_id=user_id) else 0
            serializer_data["is_review"] = 1 if Review.objects.filter(lego_set_id=pk, user_id=user_id) else 0
            serializer_data["set_quantity"] = UserSet.objects.get(user_id=user_id, legoset_id=legoset.id).quantity if UserSet.objects.filter(user_id=user_id, legoset_id=legoset.id) else 0
        else:
            serializer_data["is_like"] = 0
            serializer_data["is_review"] = 0
            serializer_data["set_quantity"] = 0
        reviews = serializers.ReviewSerializer(legoset.review_set.all().order_by("-created_at"), many=True).data
        serializer_data["reviews"] = reviews
        return Response(serializer_data)

    def destroy(self, request, pk=None):
        '''
        요청이 들어오면 권한이 있을 경우 pk에 해당하는 설계도를 삭제합니다.
        '''
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
        '''
        요청이 들어오면 요청한 유저가 가지고 있는 부품 리스트를 반환합니다.
        '''
        if request.user.is_authenticated:
            queryset = UserPart.objects.filter(user=request.user)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("비 인증 유저")

class UserSetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserSetSerializer
    pagination_class = SmallPagination
    queryset = UserPart.objects.all()

    def list(self, request):
        '''
        요청이 들어오면 요청을 한 유저가 작성한 설계도 리스트를 반환합니다.
        '''
        user = request.user
        if user.is_authenticated:
            queryset = UserSet.objects.filter(user=user)
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response("비 인증 유저")

class SetPartViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.SetPartSerializer
    queryset = SetPart.objects.all()

    def retrieve(self, request, pk=None):
        '''
        요청이 들어오면 pk에 해당하는 설계도의 부품 리스트를 반환합니다.
        '''
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
    '''
    요청이 들어오면 요청을 보낸 유저의 카테고리 정보를 입력합니다.
    '''
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
        '''
        요청이 들어오면 권한이 있을 경우 전체 리뷰 리스트를 반환합니다.
        '''
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
        '''
        요청이 들어오면 권한이 있을 경우 입력한 정보를 바탕으로 리뷰를 작성합니다.
        '''
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
        '''
        요청이 들어오면 권한이 있을 경우 pk에 해당하는 리뷰를 수정합니다.
        '''
        review = get_object_or_404(Review, pk=pk)
        user_id = request.user.id
        if request.user.is_authenticated and review.user_id == user_id:
            data = request.data
            review.content = data["content"]
            review.score = data["score"]
            review.save()
            return Response("수정 완료")
        return Response("수정 실패")

    def destroy(self, request, pk=None):
        '''
        요청이 들어오면 권한이 있을 경우 pk에 해당하는 리뷰를 삭제합니다.
        '''
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
        '''
        요청이 들어오면 pk에 해당하는 유저를 팔로우 한 유저들을 반환합니다.
        '''
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
        '''
        요청이 들어오면 pk에 해당하는 유저가 팔로우 한 유저 목록을 반환합니다.
        '''
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
        '''
        요청이 들어오면 권한이 있을 경우 유저 리스트를 반환합니다.
        '''
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
        '''
        요청이 들어오면 pk에 해당하는 유저의 정보를 반환합니다.
        '''
        user = get_object_or_404(get_user_model(), id=pk)
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        '''
        요청이 들어오면 권한이 있을 경우
        pk에 해당하는 유저의 정보를 변경합니다.
        '''
        user = get_object_or_404(get_user_model(), id=pk)
        emailaddress = get_object_or_404(EmailAddress, user_id=pk)
        if request.user.is_authenticated and request.user == user:
            data = request.data
            if EmailAddress.objects.filter(email=data["email"]) and EmailAddress.objects.get(email=data["email"]).user_id != user.id:
                return Response("이미 존재하는 이메일입니다.")
            else:
                user.nickname = data["nickname"]
                user.comment = data["comment"]
                user.email = data["email"]
                emailaddress.email = data["email"]
                user.save()
                emailaddress.save()
                return Response("수정 완료")
        elif request.user.is_staff and request.user != user:
            if user.is_superuser:
                return Response("접근 실패")
            if user.is_staff:
                user.is_staff = False
            else:
                user.is_staff = True
            user.save()
            return Response("권한 변경 성공")
        else:
            return Response("접근 실패")

    def destroy(self, request, pk=None):
        '''
        요청이 들어오면 권한이 있을 경우
        요청한 pk에 해당하는 유저의 상태를 변경합니다.
        블럭, 블럭해제 등
        '''
        user = get_object_or_404(get_user_model(), id=pk)
        if request.user.is_authenticated and request.user == user:
            user.is_active = False
            user.save()
            return Response("탈퇴 완료")
        elif request.user.is_staff and request.user != user:
            if user.is_superuser:
                return Response("접근 실패")
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
    '''
    요청이 들어오면 해당 유저의 프로필 정보를 변경합니다.
    '''
    user = self.user
    if user.is_authenticated:
        user.image = self.data["profile_url"]
        user.save()
        return Response("프로필 수정 완료")
    return Response("프로필 수정 실패")

class UserLegoSetViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer
    pagination_class = SmallPagination
    queryset = LegoSet.objects.all()
    
    def retrieve(self, request, pk=None):
        '''
        요청이 들어오면 요청을 보낸 유저가 입력한 설계도를 반환합니다.
        '''
        user = request.user
        if user.is_authenticated:
            queryset = LegoSet.objects.filter(user_id=pk).order_by('-created_at')
            page = self.paginate_queryset(queryset)
            serializer_data = serializers.LegoSetSerializer(page, many=True).data
            for legoset in serializer_data:
                legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user.id) else 0
                legoset["is_review"] = 1 if Review.objects.filter(lego_set_id=legoset["id"], user_id=user.id) else 0
            if page is not None:
                return self.get_paginated_response(serializer_data)
            return Response(serializer_data)
        else:
            return Response("비 인증 유저")

class UserLikeLegoSetViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer
    pagination_class = SmallPagination
    queryset = LegoSet.objects.all()

    def retrieve(self, request, pk=None):
        '''
        요청이 들어오면 pk에 해당하는 유저가 좋아요 한 설계도를 반환합니다.
        '''
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
        '''
        요청이 들어오면 좋아요 수가 가장 많은 레고 순으로 설계도를 반환합니다.
        '''
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
        '''
        아이템(설계도) 기반으로 추천을 해 주는 API입니다.
        입력한 설계도의 리뷰 개수가 충분하면(recommend_review_num 이상)
        knn 알고리즘을 적용한 추천을 하고
        충분하지 않으면 k-means 알고리즘을 적용한 추천을 합니다.
        '''
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
                while len(queryset) < recommend_num:
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
    pagination_class = SmallPagination
    queryset = LegoSet.objects.all()

    def list(self, request):
        '''
        유저 기반으로 추천을 해 주는 API입니다.
        요청한 유저의 리뷰 개수가 충분하면(recommend_review_num 이상)
        knn 알고리즘을 적용한 추천을 하고
        충분하지 않으면 k-means 알고리즘을 적용한 추천을 합니다.
        '''
        user = request.user
        if user.is_authenticated:
            if request.user.review_count >= recommend_review_num:
                # 리뷰 작성 안한 설계도 가져온다
                queryset = []
                user = request.user
                user_legoset_set = set()
                for legoset in user.legoset_set.all():
                    user_legoset_set.add(legoset.id)
                for legoset in LegoSet.objects.filter(review_count__gte=min_review):
                    if legoset.id not in user_legoset_set:
                        queryset.append(legoset)
                predictions = [[knn_user_based.predict(user.id, legoset_id).est, legoset_id] for legoset_id in queryset]
                predictions.sort(key=lambda x: x[0])
                queryset = [LegoSet.objects.get(id=legoset.id) for score, legoset in predictions]
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer_data = serializers.LegoSetSerializer(page, many=True).data
                else:
                    serializer_data = serializers.LegoSetSerializer(queryset, many=True).data
            else:
                queryset = [LegoSet.objects.get(id=legoset_id) for legoset_id in cluster_list[get_cluster(user.age, user.gender, user.categories)]]
                page = self.paginate_queryset(queryset)
                if page is not None:
                    serializer_data = serializers.LegoSetSerializer(page, many=True).data
                else:
                    serializer_data = serializers.LegoSetSerializer(queryset, many=True).data
            for legoset in serializer_data:
                legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user.id) else 0
                legoset["is_review"] = 1 if Review.objects.filter(lego_set_id=legoset["id"], user_id=user.id) else 0
            return self.get_paginated_response(serializer_data)
        else:
            return Response("비 인증 유저")

@api_view(['POST'])
def UpdateUserPart(self):
    '''
    유저가 부품id, color_id, qte를 입력하면 보유한 부품 인벤토리를
    입력에 맞게 변경시킵니다.
    {
        "UpdateList": [
            {
                "part_id": String,
                "color_id": Integer,
                "qte": Integer(증감시킬 개수)
            }
        ]
    }
    '''
    user = self.user
    # user = CustomUser.objects.get(id=self.user)
    if user.is_authenticated:
        update_d = self.data.get("UpdateList")
        if update_d:
            # 유저 보유 데이터 정리하기
            inventory_dict = dict()
            for userpart in UserPart.objects.filter(user=user):
                if not inventory_dict.get(userpart.part_id):
                    inventory_dict[userpart.part_id] = dict()

                inventory_dict[userpart.part_id][userpart.color_id] = userpart

            # 갱신리스트
            u = []
            # 삭제리스트
            d = []
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
                        u.append(tmp)
                    # 0보다 작거나 같으면
                    else:
                        # 삭제리스트에 추가
                        d.append(tmp)
                # 유저가 보유하고 있지 않은 아이템이라면
                else:
                    if part["qte"] > 0:
                        c.append(UserPart(user=user, part_id=part["part_id"], color_id=part["color_id"], quantity=part["qte"]))
            
            with transaction.atomic():
                # 갱신해야하는 값들을 갱신한다
                UserPart.objects.bulk_update(u, ["quantity"])
                # 생성해야하는 값들을 생성한다
                UserPart.objects.bulk_create(c)
                # 삭제해야할 값들을 삭제한다.
                for userpart in d:
                    userpart.delete()
                return Response("수정 완료")
            return Response("수정 실패 - 오류")
        return Response("UpdateList: [{part_id, color_id, qte}]를 입력하세요")
    return Response("비 인증 유저")

@api_view(['POST'])
def UpdateUserPart2(self):
    '''
    IoT에서 식별된 부품을 서버로 전송하는 API 입니다.
    {
        part_id: integer,
        color_id: integer
    }
    '''
    user = self.user
    if user.is_authenticated:
        data = self.data
        UserPart2.objects.create(user=user, part_id=data["part_id"], color_id=data["color_id"])
    return Response("수정 완료")

@api_view(['POST'])
def CreateLegoSet(self):
    '''
    입력된 정보를 바탕으로 새로운 설계도를 등록합니다.
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
    return redirect("https://k02d1081.p.ssafy.io")

@api_view(['POST'])
def like_set(self):
    '''
    요청을 보낸 유저가 입력한 설계도를 좋아요 혹은 좋아요 해제 하도록 합니다.
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
    요청을 보낸 유저가 입력한 유저를 팔로우 혹은 팔로우 해제 하도록 합니다.
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
    '''
    idx ~ idx+50까지의 레고셋 설계도에 대해서 파트 정보를 수집합니다.
    '''
    for i in range(idx, idx + 50):
        if not SetPart.objects.filter(lego_set_id=i):
            print('crawll ' + str(i))
            try:
                crawling_part_data(i)
            except:
                print('fail on ' + str(i))
    
@api_view(['GET'])
def user_parts_registered_by_IoT(self):
    '''
    IoT 기기에서 식별된 부품들을 유저에게 전송하는 API입니다.
    서버에 등록된 부품을 part_id, color_id, quantity 리스트로 반환해 줍니다.
    '''
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
        res = []
        for part_id, color_dict in user_part_dict.items():
            for color_id, part in color_dict.items():
                res.append(part)
        return Response(res)
    else:
        return Response("비 인증 유저")

@api_view(['GET'])
def reset_item_based_knn(self):
    '''
    아이템 기반 추천에 사용될 knn 모델을 재학습시킵니다.
    '''
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
    '''
    아이템 기반 추천에 사용될 k-means 모델을 재학습시킵니다.
    '''
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
    '''
    유저 기반 추천에 사용될 knn 모델을 재학습시킵니다.
    '''
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
    '''
    유저 기반 추천에 사용될 k-means 모델을 재학습시킵니다.
    '''
    global centroid, cluster_list
    user_df = pd.DataFrame(CustomUser.objects.all().values("id", "age", "gender", "categories", "review_count"))
    user_df = user_df[user_df["review_count"] >= min_review]
    # None값을 ""로 변경
    user_df["categories"] = user_df["categories"].fillna("")
    # 각 태그가 존재하면 exist_value, 없으면 nonexist_value
    user_df["건축물"] = user_df["categories"].apply(lambda x: exist_value if "건축물" in x else nonexist_value)
    user_df["장난감"] = user_df["categories"].apply(lambda x: exist_value if "장난감" in x else nonexist_value)
    user_df["공상과학"] = user_df["categories"].apply(lambda x: exist_value if "공상과학" in x else nonexist_value)
    user_df["레이싱"] = user_df["categories"].apply(lambda x: exist_value if "레이싱" in x else nonexist_value)
    user_df["클래식"] = user_df["categories"].apply(lambda x: exist_value if "클래식" in x else nonexist_value)
    user_df["창작품"] = user_df["categories"].apply(lambda x: exist_value if "창작품" in x else nonexist_value)
    user_df["게임"] = user_df["categories"].apply(lambda x: exist_value if "게임" in x else nonexist_value)
    user_df["히어로"] = user_df["categories"].apply(lambda x: exist_value if "히어로" in x else nonexist_value)
    user_df["공룡"] = user_df["categories"].apply(lambda x: exist_value if "공룡" in x else nonexist_value)

    # gender 값을 정수로 변환
    user_df['gender'] = user_df['gender'].apply(lambda x: male_value*x)

    # kmeans 학습
    kmeans = KMeans(n_clusters=cluster_num, init='k-means++', max_iter=300, random_state=0)

    kmeans.fit(user_df[["age", "gender", "건축물", "장난감", "공상과학", "레이싱", "클래식", "창작품", "게임", "히어로", "공룡"]])

    # kmeans.labels_ : 몇번 클러스터인지 라벨링 붙이고 분리했었던 id col을 붙임
    user_df['cluster'] = kmeans.labels_
    review_df = pd.DataFrame(Review.objects.all().values("user_id", "score", "lego_set_id"))
    user_df = user_df[user_df['id'].isin(set(review_df['user_id']))]
    # a = [0]*10
    # for val in user_df['cluster']:
    #     a[val] += 1
    # print(a)
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
        a = sum(cluster_list[i]['sum']) / sum(cluster_list[i]['count']) if sum(cluster_list[i]['count']) else 0.0

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

@api_view(['POST'])
def update_user_set_inventory(self):
    '''
    입력
    add_set: legoset_id 입력 시 부품 인벤토리 확인 후 부품 제거하고 설계도 인벤토리에 추가
    sub_set: legoset_id 입력 시 설계도 인벤토리 확인 후 설계도 1개 감소하고 부품 인벤토리에 추가
    {
        add_set: 1
        sub_set: 21
    }
    '''
    user = self.user
    if user.is_authenticated:
        # 유저가 보유한 재고 딕셔너리 만들기
        inventory_dict = dict()
        for userpart in UserPart.objects.filter(user=user):
            if not inventory_dict.get(userpart.part_id):
                inventory_dict[userpart.part_id] = dict()
            inventory_dict[userpart.part_id][userpart.color_id] = userpart
        
        # 생성리스트
        c = []
        # 갱신리스트
        u = []
        # 삭제리스트
        d = []

        if self.data.get("add_set"):
            legoset_id = self.data.get("add_set")
            # UserSet.objects.create(user=user, legoset_id=legoset_id, quantity=1)
            # 부품 모두 보유하고 있는지 확인하기
            # 재고 이동 가능 여부 확인하기
            chk = True
            # 유저가 보유한 재고와 설계도 부품 비교하기
            for setpart in get_object_or_404(LegoSet, pk=legoset_id).setpart_set.all():
                # 유저가 보유하고 있는 아이템이라면
                if inventory_dict.get(setpart.part_id) and inventory_dict[setpart.part_id].get(setpart.color_id):
                    tmp = inventory_dict[setpart.part_id][setpart.color_id]
                    # 감소 후에도 0보다 크다면
                    if tmp.quantity - setpart.quantity > 0:
                        # 업데이트리스트에 추가
                        tmp.quantity -= setpart.quantity
                        u.append(tmp)
                    # 0이면
                    elif tmp.quantity - setpart.quantity == 0:
                        # 삭제리스트에 추가
                        d.append(tmp)
                    else:
                        # 재고 처리 불가능한 상태이므로 리턴하기
                        chk = False
                        break
                else:
                    chk = False
                    break

            # 재고 처리 가능하다면
            if chk:                
                with transaction.atomic():
                    # 갱신해야할 값들 갱신
                    UserPart.objects.bulk_update(u, ["quantity"])
                    # 삭제해야할 값들 삭제
                    for userpart in d:
                        userpart.delete()
                    # 인벤토리에 설계도 추가
                    userset_q = user.userset_set.filter(legoset_id=legoset_id)
                    if userset_q:
                        userset = userset_q[0]
                        userset.quantity += 1
                        userset.save()
                    else:
                        UserSet.objects.create(user=user, legoset_id=legoset_id, quantity=1)
                    return Response("갱신 완료")
                return Response("갱신 실패 - 처리 오류")
            return Response("갱신 실패 - 재고 부족")
        if self.data.get("sub_set"):
            legoset_id = self.data.get("sub_set")
            userset_q = user.userset_set.filter(legoset_id=legoset_id)
            if userset_q:
                userset = userset_q[0]
                
                # 설계도의 부품들 중복 합쳐주기
                setpart_dict = dict()
                for setpart in get_object_or_404(LegoSet, id=legoset_id).setpart_set.all():
                    if setpart_dict.get(setpart.part_id):
                        if setpart_dict[setpart.part_id].get(setpart.color_id):
                            setpart_dict[setpart.part_id][setpart.color_id] += setpart.quantity
                        else:
                            setpart_dict[setpart.part_id][setpart.color_id] = setpart.quantity
                    else:
                        setpart_dict[setpart.part_id] = {setpart.color_id: setpart.quantity}

                with transaction.atomic():
                    userset.quantity -= 1
                    if userset.quantity:
                        userset.save()
                    else:
                        userset.delete()
                    for part_id, color_dict in setpart_dict.items():
                        for color_id, quantity in  color_dict.items():
                            # 유저가 보유하고 있는 아이템이라면 갱신리스트에 추가
                            if inventory_dict.get(part_id) and inventory_dict[part_id].get(color_id):
                                tmp = inventory_dict[part_id][color_id]
                                tmp.quantity += setpart.quantity
                                u.append(tmp)
                            # 아니면 생성리스트에 추가
                            else:
                                c.append(UserPart(user=user, part_id=part_id, color_id=color_id, quantity=quantity))
                    # 생성할 것들 생성
                    UserPart.objects.bulk_create(c)
                    # 갱신할 것들 갱신
                    UserPart.objects.bulk_update(u, ["quantity"])
                    return Response("갱신 완료")
                return Response("갱신 실패 - 처리 오류")
            return Response("갱신 실패 - 재고 부족")
        return Response("add_set 혹은 sub_set를 입력하세요")
    else:
        return Response("비 인증 유저")

@api_view(['POST'])
def update_user_set_inventory2(self):
    user = self.user
    UserPart2.objects.filter(user=user).delete()
    return Response("초기화 완료")