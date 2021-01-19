#Muss nicht extra Loopen sondern kann mit Queryset ein
#anderes Queryset filtern.
user = User.objects.get(username="foo")
user_stores = user.stores.all()

store_events = StoreEvent.objects.filter(store__in=user_stores).order_by('store__name', '-date')



Create a Blank Django Project
https://www.codingforentrepreneurs.com/blog/create-a-blank-django-project/