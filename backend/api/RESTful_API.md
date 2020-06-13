# RESTful API

## themes

경로: api/Themes

메소드 GET

요청이 들어오면 페이지네이션 된 테마 리스트를 반환합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page(INT)    |     F     |
| page_size(INT) |     F     |

출력:

```json
{
    "count": INT(총 theme 개수),
    "next": string(다음페이지 Url),
    "previous": string(이전페이지 Url),
    "results": [
        {
            "id": 1,
            "parent_id": INT(부모 테마 아이디),
            "name": string(테마 이름)
        }
    ]
}
```

메소드 POST

요청이 들어오면 테마를 작성합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
| parent_id(INT) |     F     |
|  name(string)  |     T     |

경로: api/Themes/{id}

메소드 GET

요청이 들어오면 id에 해당하는 Theme 정보를 반환합니다.

출력:

```json
{
    "id": 1,
    "parent_id": INT(부모 테마 아이디),
    "name": string(테마 이름)
}
```

메소드 PUT

요청이 들어오면 id에 해당하는 Theme 정보를 수정합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
| parent_id(INT) |     F     |
|  name(string)  |     T     |

메소드 DELETE

요청이 들어오면 id에 해당하는 Theme 정보를 삭제합니다.

## LegoSet

경로: api/LegoSet

메소드: GET

요청이 들어오면 세트명, 태그, 테마를 검색한 결과를 반환합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page(INT)    |     F     |
| page_size(INT) |     F     |
|  name(string)  |     F     |
|  tag(string)   |     F     |
| theme(string)  |     F     |

출력:

```json
{
    "count": INT(총 설계도 개수),
    "next": string(다음페이지 Url),
    "previous": string(이전페이지 Url),
    "results": [
        {
            "id": INT(설계도 id),
            "name": string(설계도 이름),
            "nickname": string(설계도 제작자 이름),
            "images": string(|로 구분된 이미지 주소),
            "review_count": INT(설계도에 작성된 리뷰 개수),
            "like_count": INT(설계도를 좋아요 한 사람의 수),
            "is_like": INT(요청을 보낸 유저의 좋아요 여부 0/1),
            "is_review": INT(요청을 보낸 유저의 리뷰작성 여부 0/1)
        }
    ]
}
```

경로: api/LegoSet/{id}

메소드: GET

요청이 들어오면 pk에 해당하는 설계도 정보를 반환합니다.

```json
{
    "id": INT(설계도 id),
    "name": string(설계도 이름),
    "nickname": string(설계도 제작자 이름),
    "images": string(|로 구분된 이미지 주소),
    "review_count": INT(설계도에 작성된 리뷰 개수),
    "like_count": INT(설계도를 좋아요 한 사람의 수),
    "is_like": INT(요청을 보낸 유저의 좋아요 여부 0/1),
    "is_review": INT(요청을 보낸 유저의 리뷰작성 여부 0/1)
}
```

메소드: DELETE

요청이 들어오면 pk에 해당하는 설계도를 삭제합니다.

## LegoPart

경로: api/LegoPart

메소드: GET

요청이 들어오면 서버에 등록된 레고 부품정보를 반환합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page(INT)    |     F     |
| page_size(INT) |     F     |

출력:

```json
{
    "count": INT(총 부품 종류 개수),
    "next": string(다음페이지 Url),
    "previous": string(이전페이지 Url),
    "results": [
        {
            "id": string(레고 부품 id),
            "category": INT(레고 부품의 카테고리 id),
            "name": string(레고 부품 이름),
            "image": string(이미지 주소)
        }
    ]
]
```

경로: api/LegoPart/{id}

메소드: GET

요청이 들어오면 id에 해당하는 부품 정보를 반환합니다.

출력:

```json
{
    "id": string(레고 부품 id),
    "category": INT(레고 부품의 카테고리 id),
    "name": string(레고 부품 이름),
    "image": string(이미지 주소)
}
```

## UserPart

경로: api/UserPart

메소드: GET

요청이 들어오면 요청한 유저가 가지고 있는 부품 리스트를 반환합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page(INT)    |     F     |
| page_size(INT) |     F     |

출력:

```json
{
    "count": INT(총 부품 종류 개수),
    "next": string(다음페이지 Url),
    "previous": string(이전페이지 Url),
    "results": [
        {
            "user_id": INT(user의 id),
            "part_id": INT(part의 id),
            "color_id": INT(color의 id),
            "quantity": INT(유저의 해당 부품 보유량),
            "image": string(이미지 주소),
            "rgb": string(rgb 정보)
        }
    ]
]
```

## UserSet

경로: api/UserSet

메소드: GET

요청이 들어오면 요청을 한 유저가 보유한 설계도 정보를 반환합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page(INT)    |     F     |
| page_size(INT) |     F     |

출력:

```json
{
    "count": INT(총 부품 종류 개수),
    "next": string(다음페이지 Url),
    "previous": string(이전페이지 Url),
    "results": [
        {
            "legoset_id": INT(설계도의 id),
            "quantity": INT(설계도 보유 갯수),
            "image": string(설계도 이미지 주소),
            "name": string(설계도 이름),
            "user_nickname": string(설계도 작성자 닉네임),
            "review_count": INT(설계도에 작성된 리뷰 개수),
            "like_count": INT(설계도를 좋아요 한 사람의 수),
            "is_like": INT(요청을 보낸 유저의 좋아요 여부 0/1),
            "is_review": INT(요청을 보낸 유저의 리뷰작성 여부 0/1)
        }
    ]
]
```

## SetPart

경로: api/SetPart/{id}

메소드: GET

요청이 들어오면 id에 해당하는 설계도의 부품 리스트를 반환합니다.

출력:

```json
[
    {
        "lego_set_id": 1,
        "part_id": "132a",
        "color_id": 7,
        "quantity": 4
    }
]
```

## Set_User_category

경로: api/set_user_category

메소드: POST

요청이 들어오면 요청을 보낸 유저의 |로 구분된 카테고리를 입력합니다.



입력:

|        인자        | 필수 여부 |
| :----------------: | :-------: |
| categories(string) |     T     |

## Review

경로: api/Review

메소드: GET

요청이 들어오면 권한이 있을 경우 전체 리뷰 리스트를 반환합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page(INT)    |     F     |
| page_size(INT) |     F     |

출력:

```json
[
    {
        "id": INT(리뷰 id),
	    "user_id": string(리뷰 작성자 id),	
        "nickname": string(리뷰 작성자 nickname),
        "content": string(리뷰 내용),
        "score": INT(리뷰 평점),
        "user_image": string(리뷰 작성자의 프로필이미지 url),
        "updated_at": datetime(리뷰 최종 수정 시간),
    }
]
```

메소드: POST

요청이 들어오면 권한이 있을 경우 리뷰를 작성합니다.

입력:

| 인자            | 필수 여부 |
| --------------- | --------- |
| content(string) | T         |
| score(INT)      | T         |

경로: api/Review/{id}

메소드: PUT

요청이 들어오면 권한이 있을 경우 리뷰를 수정합니다.

입력:

| 인자            | 필수 여부 |
| --------------- | --------- |
| content(string) | T         |
| score(INT)      | T         |

메소드: DELETE

요청이 들어오면 권한이 있을 경우 리뷰를 삭제합니다.

## Follower

경로: api/Follower/{id}

메소드: GET

요청이 들어오면 id에 해당하는 유저를 팔로우 한 유저들을 반환합니다.

출력:

```json
[
    {
        "id": INT(유저 id),
        "nickname": string(유저 닉네임),
        "image": string(유저의 프로필 이미지 url)
    }
]
```

## Following

경로: api/Following/{id}

메소드: GET

요청이 들어오면 id에 해당하는 유저가 팔로우 한 유저 목록을 반환합니다.

출력:

```json
[
    {
        "id": INT(유저 id),
        "nickname": string(유저 닉네임),
        "image": string(유저의 프로필 이미지 url)
    }
]
```

## User

경로: api/User

메소드: GET

요청이 들어오면 권한이 있을 경우 유저 리스트를 반환합니다.

출력:

```json
[
    {
        "id": INT(유저 id),
        "nickname": string(유저 닉네임),
        "image": string(유저의 프로필 이미지 url)
    }
]
```

경로: api/User/{id}

메소드: GET

요청이 들어오면 id에 해당하는 유저의 정보를 반환합니다.

출력:

```json
{
    "id": INT(유저 id),
    "nickname": string(유저 닉네임),
    "image": string(유저의 프로필 이미지 url),
    "comment": string(유저의 프로필 한마디)
}
```

메소드: PUT

요청이 들어오면 권한이 있을 경우 id에 해당하는 유저의 정보를 변경합니다.

입력:

|       인자       | 필수 여부 |
| :--------------: | :-------: |
| nickname(string) |     F     |
| comment(string)  |     F     |
|  email(string)   |     F     |

메소드: DELETE

요청이 들어오면 권한이 있을 경우 요청한 id에 해당하는 유저의 상태를 변경합니다.

블럭, 블럭해제 등

## UpdateUserProfile

경로: api/UpdateUserProfile

메소드: PUT

요청이 들어오면 해당 유저의 프로필 정보를 변경합니다.

입력:

|        인자         | 필수 여부 |
| :-----------------: | :-------: |
| profile_url(string) |     T     |

## UserLegoSet

경로: api/UserLegoSet/{id}

메소드: GET

요청이 들어오면 요청을 보낸 유저가 입력한 설계도를 반환합니다.

출력:

```json
[
    { 
        "id": INT(설계도 id),
        "name": string(설계도 이름),
        "nickname": string(설계도 작성자 닉네임),
        "images": string(|로 구분된 image url),
        "review_count": INT(해당 설계도에 작성된 리뷰 개수),
        "like_count": INT(해당 설계도를 좋아요 한 사람의 수),
       	"is_like": INT(요청을 보낸 유저의 좋아요 여부 0/1),
        "is_review": INT(요청을 보낸 유저의 리뷰작성 여부 0/1)
    }
]           
```

## UserLikeLegoSet

경로: api/UserLikeLegoSet/{id}

메소드: GET

요청이 들어오면 id에 해당하는 유저가 좋아요 한 설계도를 반환합니다.

출력:

```json
[
    { 
        "id": INT(설계도 id),
        "name": string(설계도 이름),
        "nickname": string(설계도 작성자 닉네임),
        "images": string(|로 구분된 image url),
        "review_count": INT(해당 설계도에 작성된 리뷰 개수),
        "like_count": INT(해당 설계도를 좋아요 한 사람의 수),
       	"is_like": INT(요청을 보낸 유저의 좋아요 여부 0/1),
        "is_review": INT(요청을 보낸 유저의 리뷰작성 여부 0/1)
    }
]           
```

## LegoSetRanking

경로: api/LegoSetRanking

메소드: GET

요청이 들어오면 좋아요 수가 가장 많은 레고 순으로 설계도를 반환합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page(INT)    |     F     |
| page_size(INT) |     F     |

출력:

```json
{
    "count": INT(총 부품 종류 개수),
    "next": string(다음페이지 Url),
    "previous": string(이전페이지 Url),
    "results": [
        {
            "id": INT(설계도 id),
            "name": string(설계도 이름),
            "nickname": string(설계도 작성자 닉네임),
            "images": string(|로 구분된 image url),
            "review_count": INT(해당 설계도에 작성된 리뷰 개수),
            "like_count": INT(해당 설계도를 좋아요 한 사람의 수),
            "is_like": INT(요청을 보낸 유저의 좋아요 여부 0/1),
            "is_review": INT(요청을 보낸 유저의 리뷰작성 여부 0/1)
        }
    ]
}
```

## ItemBasedRecommend

경로: api/ItemBasedRecommend/{id}

메소드: GET

아이템(설계도) 기반으로 추천을 해 주는 API입니다.
입력한 설계도의 리뷰 개수가 충분하면(recommend_review_num 이상)
knn 알고리즘을 적용한 추천을 하고
충분하지 않으면 k-means 알고리즘을 적용한 추천을 합니다.

출력:

```json
[
    {
        "id": INT(설계도 id),
        "name": string(설계도 이름),
        "nickname": string(설계도 작성자 닉네임),
        "images": string(|로 구분된 image url),
        "review_count": INT(해당 설계도에 작성된 리뷰 개수),
        "like_count": INT(해당 설계도를 좋아요 한 사람의 수),
        "is_like": INT(요청을 보낸 유저의 좋아요 여부 0/1),
        "is_review": INT(요청을 보낸 유저의 리뷰작성 여부 0/1)
    }
]
```

## UserBasedRecommend

경로: api/UserBasedRecommend

메소드: GET

유저 기반으로 추천을 해 주는 API입니다.
요청한 유저의 리뷰 개수가 충분하면(recommend_review_num 이상)
knn 알고리즘을 적용한 추천을 하고
충분하지 않으면 k-means 알고리즘을 적용한 추천을 합니다.

입력:

|      인자      | 필수 여부 |
| :------------: | :-------: |
|   page(INT)    |     F     |
| page_size(INT) |     F     |

출력:

```json
[
    {
        "id": INT(설계도 id),
        "name": string(설계도 이름),
        "nickname": string(설계도 작성자 닉네임),
        "images": string(|로 구분된 image url),
        "review_count": INT(해당 설계도에 작성된 리뷰 개수),
        "like_count": INT(해당 설계도를 좋아요 한 사람의 수),
        "is_like": INT(요청을 보낸 유저의 좋아요 여부 0/1),
        "is_review": INT(요청을 보낸 유저의 리뷰작성 여부 0/1)
    }
]
```

## UpdateUserPart

경로: api/UpdateUserPart

메소드: POST

유저가 부품id, color_id, qte를 입력하면 보유한 부품 인벤토리를 입력에 맞게 변경시킵니다.

입력:

```json
{
    "UpdateList": [
        {
            "part_id": String,
            "color_id": Integer,
            "qte": Integer(증감시킬 개수)
        }
    ]
}
```

## UpdateUserPart2

경로: api/UpdateUserPart2

메소드: POST

레고 마스터(레고 자동 분류 AI &IoT)기기에서 식별된 부품을 서버로 전송하는 API 입니다.

입력:

```json
{
    "part_id": String,
    "color_id": Integer
}
```

## CreateLegoSet

경로: api/CreateLegoSet

메소드: POST

입력된 정보를 바탕으로 새로운 설계도를 등록합니다.

입력:

```json
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
	],
	"sub_sets": [
        
    ]
}
```

## like_set

경로: api/like_set

메소드: POST

요청을 보낸 유저가 입력한 설계도를 좋아요 혹은 좋아요 해제 하도록 합니다.

입력:

```json
{
    "set_id": Integer    # LegoSet.id
}
```

## follow

경로: api/follow

메소드: POST

요청을 보낸 유저가 입력한 유저를 팔로우 혹은 팔로우 해제 하도록 합니다.

입력:

```json
{
    "user_id": Integer    # CustomUser.id
}
```

## user_parts_registered_by_IoT

경로: api/user_parts_registered_by_IoT

메소드: GET

IoT 기기에서 식별된 부품들을 유저에게 전송하는 API입니다.

서버에 등록된 부품을 part_id, color_id, quantity 리스트로 반환해 줍니다.

출력:

```json
[
    {
        "part_id": INT,
        "color_id": INT,
        "quantity": INT
    }
]
```

## reset_item_based_knn

경로: api/reset_item_based_knn

메소드: GET

아이템 기반 추천에 사용될 knn 모델을 재학습시킵니다.

## reset_item_based_k_means

경로: api/reset_item_based_k_means

메소드: GET

아이템 기반 추천에 사용될 k-means 모델을 재학습시킵니다.



## reset_user_based_knn

경로: api/reset_user_based_knn

메소드: GET

유저 기반 추천에 사용될 knn 모델을 재학습시킵니다.

## reset_user_based_k_means

경로: api/reset_user_based_k_means

메소드: GET

유저 기반 추천에 사용될 k-means 모델을 재학습시킵니다.

## update_user_set_inventory

경로: api/update_user_set_inventory

메소드: POST

add_set에 설계도 아이디를 입력하면 해당 설계도에 필요한 부품을 유저가 모두 보유하고 있을 경우 이를 제거하고 해당 설계도의 보유 갯수를 1 증가시킵니다.

sub_set에 설계도 아이디를 입력하면 유저가 해당 설계도를 보유하고 있을 경우 그 설계도에 필요한 부품을 인벤토리에 추가한 후 해당 설계도의 보유 갯수를 1 감소시킵니다.

입력:

```json
{
    add_set: 1,
    sub_set: 21
}
```

## update_user_set_inventory2

경로: api/update_user_set_inventory2

메소드: POST

요청이 들어오면 레고 마스터(레고 분류기)로부터 입력된 정보들을 모두 제거합니다.