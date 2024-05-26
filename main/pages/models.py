from django.db import models

class Book(models.Model):
    element_id = models.CharField(max_length=100)
    neo4j_id = models.IntegerField()
    avg_age = models.IntegerField()
    avg_book_rating = models.FloatField()
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20)
    image_url = models.URLField()
    publisher = models.CharField(max_length=100)
    year_of_publication = models.IntegerField()
    category_id = models.IntegerField()
    category = models.CharField(max_length=100)
    description = models.TextField()

class Person(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

  

class Add(models.Model):
  
    category_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    userid = models.IntegerField(default=0)


class catagories(models.Model):

    category_id = models.IntegerField()
    category_name = models.CharField(max_length=100)
    userid = models.IntegerField(default=0)



class BookVisited(models.Model):
  
    bookId = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    userid = models.IntegerField(default=0)




class BookLike(models.Model):
    bookId = models.IntegerField()
    liked = models.BooleanField(default=False)
    userid = models.IntegerField(default=0)


class getvisited (models.Model):
    Gid = models.IntegerField()
    Gage = models.IntegerField()
    Gyear = models.IntegerField()
   


class agee(models.Model):
    Gid = models.IntegerField()
    Gage = models.IntegerField()
    Gyear = models.IntegerField()
   

