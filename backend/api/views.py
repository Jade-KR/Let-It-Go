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

API_key = '08d368a0e1830b9fec088091be154133'
headers = {
    'Authorization': 'key ' + API_key,
    'Accept': 'application/json'
}

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
    max_page_size = 50

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
                return self.get_paginated_response(serializer_data)
            else:
                for legoset in serializer_data:
                    legoset["is_like"] = 0
                    legoset["is_review"] = 0
                return self.get_paginated_response(serializer_data)

        serializer = serializers.LegoSetSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        legoset = get_object_or_404(LegoSet, id=pk)
        serializer_data = serializers.LegoSetSerializer2(legoset).data
        if request.user.is_authenticated and UserLikeLegoSet.objects.filter(legoset_id=pk, customuser_id=request.user.id):
            serializer_data["is_like"] = 1
        else:
            serializer_data["is_like"] = 0
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
            # crawling_part_data(pk)
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
            "category_list": user.category_list,
            "status": "success",
            }
        orginal_response.data["user"].update(mydata)
        return orginal_response

class ReviewViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ReviewSerializer
    pagination_class = SmallPagination
    queryset = Review.objects.all()

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
    queryset = CustomUser.objects.all()

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

    def retrieve(self, request, pk=None):
        queryset = LegoSet.objects.filter(user_id=pk)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = serializers.LegoSetSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.LegoSetSerializer(queryset, many=True)
        return Response(serializer.data)

class UserLikeLegoSetViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer
    pagination_class = SmallPagination

    def retrieve(self, request, pk=None):
        user = get_object_or_404(get_user_model(), id=pk)
        queryset = user.like_sets.all().order_by('-created_at')
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = serializers.LegoSetSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.LegoSetSerializer(queryset, many=True)
        return Response(serializer.data)

class LegoSetRankingViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer2
    pagination_class = SmallPagination

    def list(self, request):
        queryset = LegoSet.objects.all().order_by("-like_count")
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer_data = serializers.LegoSetSerializer(page, many=True).data
            if request.user.is_authenticated:
                user_id = request.user.id
                for legoset in serializer_data:
                    legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user_id) else 0
                return self.get_paginated_response(serializer_data)
            else:
                for legoset in serializer_data:
                    legoset["is_like"] = 0
                return self.get_paginated_response(serializer_data)
            serializer = serializers.LegoSetSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.LegoSetSerializer(queryset, many=True)
        return Response(serializer.data)

class FollowingUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.LegoSetSerializer2
    pagination_class = SmallPagination
    
    def list(self, request):
        if request.user.is_authenticated:
            queryset = UserPart.objects.filter(user=request.user)

        queryset = LegoSet.objects.all().order_by("-like_count")
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer_data = serializers.LegoSetSerializer(page, many=True).data
            if request.user.is_authenticated:
                user_id = request.user.id
                for legoset in serializer_data:
                    legoset["is_like"] = 1 if UserLikeLegoSet.objects.filter(legoset_id=legoset["id"], customuser_id=user_id) else 0
                return self.get_paginated_response(serializer_data)
            else:
                for legoset in serializer_data:
                    legoset["is_like"] = 0
                return self.get_paginated_response(serializer_data)
            serializer = serializers.LegoSetSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.LegoSetSerializer(queryset, many=True)
        return Response(serializer.data)


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
    """
    {
		"part_id": "10066pr0001",
		"color_id": 1,
		"qte": 5
	}

    """
    user = self.user
    if user.is_authenticated:
        data = self.data
        UserPart2.objects.create(user=user, part_id=data["part_id"], color_id=data["color_id"])
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
        res = []
        for part_id, color_dict in user_part_dict.items():
            for color_id, part in color_dict.items():
                res.append(part)
        return Response(res)
    else:
        return Response("비 인증 유저")