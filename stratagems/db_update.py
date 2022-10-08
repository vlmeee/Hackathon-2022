from news.models import News
from news.process_news import determine_role


news = News.objects.all()
for i in news:
    if i.role is None:
        print(i.role)
        new_role = determine_role(i.text)
        if new_role is not None:
            print(new_role)
            News.objects.filter(pk=i.pk).update(role=new_role)
