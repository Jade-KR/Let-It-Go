from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, Theme, LegoSet, OfficialMapping, Category, Review, LegoPart, Color, UserPart, SetPart
from api import models, serializers
from rest_framework import viewsets, mixins
from rest_framework.schemas import AutoSchema
from rest_framework.decorators import api_view, action, authentication_classes, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model

class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50

class ThemeViewSet(viewsets.ModelViewSet):
    queryset = Theme.objects.all()
    serializer_class = serializers.ThemeSerializer
    pagination_class = SmallPagination

class LegoSetViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LegoSet.objects.all()
    serializer_class = serializers.LegoSetSerializer
    pagination_class = SmallPagination

class LegoPartViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = LegoPart.objects.all()
    serializer_class = serializers.LegoPartSerializer
    pagination_class = SmallPagination

class UserPartViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.UserPartSerializer
    
    def list(self, request):
        queryset = UserPart.objects.filter(user_id=1)#request.user.id)

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def UpdateUserPart(self):
    user = CustomUser.objects.get(id=1)
    if user.is_authenticated:
        update_d = self.data.get("UpdateList")
        # 요청 들어온 데이터 정리하기
        # update_dict = dict()
        # for update_part in self.data.get("LegoList"):
        #     if update_dict.get(update_part["part_id"]):
        #         if update_dict[update_part["part_id"]].get(update_part["color_id"]):
        #             update_dict[update_part["part_id"]][update_part["color_id"]] += update_part["qte"]
        #         else:
        #             update_dict[update_part["part_id"]][update_part["color_id"]] = update_part["qte"]
        #     else:
        #         update_dict[update_part["part_id"]] = {update_part["color_id"]: update_part["qte"]}
        
        # 유저 보유 데이터 정리하기
        inventory_dict = dict()
        for userpart in UserPart.objects.filter(user=user):
            inventory_dict[userpart.part_id] = {userpart.color_id: userpart}
        
        # 갱신리스트
        a = []
        # 삭제리스트
        b = []

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
                    a.append(UserPart.objects.create(user=user, part_id=part["part_id"], color_id=part["color_id"], quantity=part["qte"]))

        # 갱신해야하는 값들을 갱신한다
        UserPart.objects.bulk_update(a, ["quantity"])

        # 삭제해야할 값들을 삭제한다.
        for userpart in b:
            userpart.delete()

    return Response("수정 완료")
