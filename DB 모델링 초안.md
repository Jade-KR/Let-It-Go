DB 모델링 초안

설계도 – 사용한 부품 목록(색상 포함)
유저 – 인벤토리, 회원정보들… 팔로우, 좋아요
레고부품 – id, color(?)
커뮤니티 게시글 - 설계도 ID, 내용, 태그
댓글 - 덧글내용, 작성자ID







- user
  - username, email, age, gender, followers
- user_brick
  - username, brick_id, volume
- brick
  - brick_id, brick_code, brick_color
- lego
  - lego_id, brick_id, volume
- board
  - board_id, lego_id, username, image, title, description, like_users, tags

- review
  - review_id, username, board_id, content, score



LEt it GO



- user
  - username, email, age, gender, followers
- user_brick
  - username, brick_id, brick_color, volume
- brick
  - brick_id
- lego_brick
  - lego_id, brick_id, brick_color, volume
- lego
  - lego_id, username, image, title, description, like_users, tags

- review
  - review_id, username, lego_id, content, score







- 유저
  - 보유한 레고 파트들 볼 수 있어야됨
  - 팔로우한 유저 목록 볼 수 있어야됨
  - 좋아요한 설계도 볼 수 있어야됨
  - 설계도 등록할 수 있어야됨