
content=""

for i in range(32, 1200):
    user = CustomUser.objects.filter(id=i)
    random_number = randint(1,100)
    lego_set_id = 1872
    if(user[0].age<27):
        if(random_number<=3):
            Review.objects.create(user_id=i, content=content, lego_set_id=lego_set_id, score=randint(4,5))
    elif(user[0].age>26 and user[0].age<35):
        if(random_number<=4):
            Review.objects.create(user_id=i, content=content, lego_set_id=lego_set_id, score=randint(4,5))
    elif(user[0].age>34 and user[0].age<43):
        if(random_number<=8):
            Review.objects.create(user_id=i, content=content, lego_set_id=lego_set_id, score=randint(4,5))
    elif(user[0].age>42 and user[0].age<53):
        if(random_number<=1):
            Review.objects.create(user_id=i, content=content, lego_set_id=lego_set_id, score=randint(4,5))
    else:
        if(random_number<=0):
            Review.objects.create(user_id=i, content=content, lego_set_id=lego_set_id, score=randint(4,5))