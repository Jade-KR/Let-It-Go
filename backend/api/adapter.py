from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.nickname = data.get('nickname')
        user.image = data.get('image')
        user.comment = data.get('comment')
        user.age = data.get('age')
        user.gender = data.get('gender')
        user.save()
        return user