from blog.models import Bb

for bb in Bb.objects.all():
    print(bb.title)
    
