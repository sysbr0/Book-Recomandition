
from neo4j import GraphDatabase
from .models import Book
from .models import Add 
from .models import catagories
from .models import BookVisited
from .models import BookLike
from django.db.models import Max
from .models import getvisited
from .models import agee
from .models import Person
from django.shortts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from myapp.models import CustomUser
# Create your views here.

def index(request) :
  
    neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    check = "heart_plus"
    

   
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    
    latest_categories = Add.objects.values('category_id') \
                                   .annotate(latest_date=Max('created_at')) \
                                   .order_by('-latest_date')[:5]
    # last getegories to aray ORDER BY rand()
    latest_category_ids = [category['category_id'] for category in latest_categories]

    
    category_ids = []

    # Append to the qury 
    category_ids.extend(latest_category_ids)
    cypher_query2 = (
        "MATCH (b:Book) RETURN b  LIMIT 1"
    )
   

    books1 = []
    books2 = []
    
    with driver.session() as session:
     
        result2 = session.run(cypher_query2)
        for record in result2:
            book_data = record['b']
            # Process book data as needed
            book = Book(
                element_id=book_data['<elementId>'],
                neo4j_id=book_data['<id>'],
                avg_age=book_data['AvgOfAge'],
                avg_book_rating=book_data['AvgOfbookRating'],
                author=book_data['Book-Author'],
                title=book_data['Book-Title'],
                isbn=book_data['ISBN'],
                image_url=book_data['Image-URL-L'],
                publisher=book_data['Publisher'],
                year_of_publication=book_data['Year-Of-Publication'],
                category_id=book_data['catagoryid'],
                category=book_data['category'],
                description=book_data['description']
            )
            books2.append(book)
            if BookLike.objects.filter(bookId=book.isbn, liked=True).exists():
                check = "kid_star"
  


    return  render(request, 'pages/bookCard.html' ,  {'books1': books1, 'books2': books2 , 'check' : check})


def about(request) : 
    neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    
    categories = []
    category_counts = {}

    # Define the userid for filtering
    user_id = request.user.id if request.user.is_authenticated else None  #log into

    # Fetch data filtered by userid
    data = Add.objects.filter(userid=user_id)  # data all category where userid matches

    for i in data:
        id = i.category_id

        with driver.session() as session:
            result = session.run('MATCH (n:Category {categoryId: $id}) RETURN n', id=id)

            for record in result:
                category = record['n']  # get the category node from neo4j
                category_id = category['categoryId']  # in neo4j
                category_name = category['name']  # in neo4j take the name
                
                # Count the occurrences of each category
                if category_name in category_counts:  # if the category name is in the dictionary check 
                    category_counts[category_name] += 1  # if exist add 1
                else:
                    category_counts[category_name] = 1  
                    # if not exist set 1

                # Create a category object and append it to the categories list
                category_obj = catagories(  # initialize the category object, 
                    category_id=category_id,  # the form to append data 
                    category_name=category_name
                )
                categories.append(category_obj)  # append to the empty list

    # Convert the category counts dictionary to a list of lists
    category_counts_list = [[category, count] for category, count in category_counts.items()]

    categoriess = [item[0] for item in category_counts_list]
    amounts = [item[1] for item in category_counts_list]

    books = []  # categories
    books_counts = {}
    ages = []
    age_counts = {}
    visited = BookVisited.objects.filter(userid=user_id)  # visited book filtered by userid

    for i in visited:
        id = str(i.bookId)

        with driver.session() as session:
            result1 = session.run('MATCH (n:Book {ISBN: $id}) RETURN n', id=id)

            for recordd in result1:
                book = recordd['n']  # Get the category node from neo4j
                date = book['Year-Of-Publication']  # in neo4j
                age = book['AvgOfAge']  # in neo4j take the name
                age0 = age[0]
                age1 = age[1]
                age = (int(age1) * 1 + int(age0) * 10)

                # Count the occurrences of each category
                if int(date) in books_counts:  # if the category name is in the dictionary check
                    books_counts[int(date)] += 1  # if exist add 1
                else:
                    books_counts[int(date)] = 1  # if not exist add 1

                if age in age_counts:  # if the category name is in the dictionary check
                    age_counts[age] += 1  # if exist add 1
                else:
                    age_counts[age] = 1  # if not exist add 1

                # Create a category object and append it to the categories list
                book_obj = getvisited(  # initialize the category object, categories is the class in model to append data
                    Gage=age,  # the form to append data
                    Gyear=date
                )
                books.append(book_obj)  # append to the empty list
                age_obj = agee(
                    Gage=age,
                    Gyear=date
                )
                ages.append(age_obj)

    # Convert the category counts dictionary to a list of lists
    book_counts_list = [[book, count] for book, count in books_counts.items()]
    age_counts_list = [[book, count] for book, count in age_counts.items()]

    dates = [item[0] for item in book_counts_list]
    conts = [item[1] for item in book_counts_list]

    agees = [item[0] for item in age_counts_list]
    agecount = [item[1] for item in age_counts_list]

    likedBook = []
    like = BookLike.objects.filter(userid=user_id)  # filter liked books by userid

    for i in like:
        if i.liked:
            bookid = i.bookId
            bookidstring = str(bookid)

            with driver.session() as session:
                result1 = session.run('MATCH (n:Book {ISBN: $bookidstring}) RETURN n', bookidstring=bookidstring)

                for record in result1:
                    book_data = record['n']

                    book = Book(
                        element_id=book_data['<elementId>'],
                        neo4j_id=book_data['<id>'],
                        avg_age=book_data['AvgOfAge'],
                        avg_book_rating=book_data['AvgOfbookRating'],
                        author=book_data['Book-Author'],
                        title=book_data['Book-Title'],
                        isbn=book_data['ISBN'],
                        image_url=book_data['Image-URL-L'],
                        publisher=book_data['Publisher'],
                        year_of_publication=book_data['Year-Of-Publication'],
                        category_id=book_data['catagoryid'],
                        category=book_data['category'],
                        description=book_data['description']
                    )

                    likedBook.append(book)

    return render(request, 'pages/chart.html', {
        'data': book_counts_list,
        'book': categories,
        'list': category_counts_list,
        'categoriess': categoriess,
        'amounts': amounts,
        'dates': dates,
        'conts': conts,
        'agees': agees,
        'agecount': agecount,
        'likedBook': likedBook
    })

def chart1(request):
    # Connect to Neo4j
    neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
    graph = Graph(neo4j_uri, auth=(neo4j_username, neo4j_password))

    # Query Neo4j to get category counts
    query = """
    MATCH (c:Category)<-[:BELONGS_TO]-(a:Add)
    RETURN c.name AS category, COUNT(a) AS count
    """
    category_counts = graph.run(query).data()

    # Calculate total count
    total_count = sum(category['count'] for category in category_counts)

    # Calculate percentages
    for category in category_counts:
        category['percentage'] = (category['count'] / total_count) * 100

    # Pass category names and percentages to the template
    return render(request, 'pages/chart1.html', {'category_counts': category_counts})




def like_post(request):
    id = request.user.id if request.user.is_authenticated else None
    number = request.GET.get('isbnnumber')



    try:
        liked_entry = BookLike.objects.get(bookId=number)
        # Number exists, modify the associated post_id
        liked_entry.liked = not liked_entry.liked
        liked_entry.save()
    except BookLike.DoesNotExist:
        # Number doesn't exist, create a new entry
       
        like = BookLike(bookId= int(number),liked =True  , userid = id )

        like.save()

    
   
       



    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



def navbar(request):
    social_media_links = [
    
         {
            'platform': 'instagram',
            'url': 'https://www.instagram.com/your_instagram_username',
            'icon_class': 'fab fa-instagram fa-lg',
        },
        {
            'platform': 'youtube',
            'url': 'https://www.youtube.com/your_youtube_channel',
            'icon_class': 'fab fa-youtube fa-lg',
        },
        {
            'platform': 'facebook',
            'url': 'https://www.facebook.com/your_facebook_page',
            'icon_class': 'fab fa-facebook fa-lg',
        },
        {
            'platform': 'email',
            'url': 'mailto:your_email@example.com',
            'icon_class': 'fa-solid fa-envelope',
        },
        {
            'platform': 'whatsapp',
            'url': 'https://wa.me/your_whatsapp_number',
            'icon_class': 'fab fa-whatsapp fa-lg',
        },
    
      
    ]
    menu =[ 
    

          {
          'name': 'facebook',
            'link': 'https://www.facebook.com/your_facebook_page'
        },
          {
          'name': 'facebook',
            'link': 'https://www.facebook.com/your_facebook_page'
        },
          {
          'name': 'facebook',
            'link': 'https://www.facebook.com/your_facebook_page'
        },
          {
          'name': 'facebook',
            'link': 'https://www.facebook.com/your_facebook_page'
        },
    
     ]
    
    email = request.user.email if request.user.is_authenticated else None
    print(email)



    return render(request, 'base/navbar.html', {'social_media_links': social_media_links, 'menu': menu , 'email': email})


def index2(request) :
     books = [
        {
            'ISBN': '195153448',
            'title': 'Classical Mythology',
            'author': 'Mark P. O. Morford',
            'year_of_publication': '2002',
            'publisher': 'Oxford University Press',
            'image_url': 'http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg'
        },
        {
            'ISBN': '2005018',
            'title': 'Clara Callan',
            'author': 'Richard Bruce Wright',
            'year_of_publication': '2001',
            'publisher': 'HarperFlamingo Canada',
            'image_url': 'http://images.amazon.com/images/P/0002005018.01.LZZZZZZZ.jpg'
        },

             ]
     return  render(request, 'pages/bk.html' ,{'books': books})  
@login_required
def navbar2(request) :
     
     
     return  render(request, 'base/navbar2.html' )

def indix(request) :
      books = [
        {
            'ISBN': '195153448',
            'title': 'Classical Mythology',
            'author': 'Mark P. O. Morford',
            'year_of_publication': '2002',
            'publisher': 'Oxford University Press',
            'image_url': 'http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg'
        },
        {
            'ISBN': '2005018',
            'title': 'Clara Callan',
            'author': 'Richard Bruce Wright',
            'year_of_publication': '2001',
            'publisher': 'HarperFlamingo Canada',
            'image_url': 'http://images.amazon.com/images/P/0002005018.01.LZZZZZZZ.jpg'
        },
        
        # Add more books similarly
             ]
      

      latest_categories = Add.objects.values('category_id')\
                                   .annotate(latest_date=Max('created_at'))\
                                   .order_by('-latest_date')[:5]
      return  render(request, 'pages/index.html',{'books': books , 'latest_categories' : latest_categories} )



def book_list(request):
  


    # Connect to Neo4j
    neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
   
    cypher_query_all = (
    "MATCH (b:Book) RETURN b LIMIT 1")

     
    with driver.session() as session:
        result = session.run(cypher_query_all)
        books1 = []
        for record in result:
            book_data = record['b']
            book = Book(
                element_id=book_data['<elementId>'],
                neo4j_id=book_data['<id>'],
                avg_age=book_data['AvgOfAge'],
                avg_book_rating=book_data['AvgOfbookRating'],
                author=book_data['Book-Author'],
                title=book_data['Book-Title'],
                isbn=book_data['ISBN'],
                image_url=book_data['Image-URL-L'],
                publisher=book_data['Publisher'],
                year_of_publication=book_data['Year-Of-Publication'],
                category_id=book_data['catagoryid'],
                category=book_data['category'],
                description=book_data['description']
            )
            books1.append(book)
    
    return render(request, 'pages/bookdetail.html', {'books1': books1})

    


def filter(request):
   


    driver = GraphDatabase.driver("neo4j+s://db7beccf.databases.neo4j.io", auth=("neo4j", "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"))
    with driver.session() as session:
        result = session.run("""
        MATCH (b:Book)
        RETURN b """)
        books = [record['b'] for record in result]




    return render(request, 'pages/index2.html', {'books': books})

@login_required
def fatch(request):
    users = CustomUser.objects.all()
 
    





    
    id = request.user.id if request.user.is_authenticated else None

    print(id)
    neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    
   
    email = request.user.email if request.user.is_authenticated else None



    latest_categories = Add.objects.filter(userid=id) \
                               .values('category_id') \
                               .annotate(latest_date=Max('created_at')) \
                               .order_by('-latest_date')[:5]
    # last getegories to aray
    latest_category_ids = [category['category_id'] for category in latest_categories]

    
    category_ids = []

    # Append to the qury 
    category_ids.extend(latest_category_ids)
    cypher_query2 = (
        "MATCH (b:Book) RETURN b ORDER BY rand() LIMIT 25"
    )
    cypher_query1 = (
        "MATCH (c:Category)<-[:BELONGS_TO]-(book:Book) "
        "WHERE c.categoryId IN $categoryIds "
        "RETURN c, book "
        "ORDER BY RAND() "
        "LIMIT 250"
    )

    books1 = []
    books2 = []
    
    with driver.session() as session:
        result1 = session.run(
            cypher_query1,
            {"categoryIds": category_ids}
        )
        for record in result1:
            book_data = record['book']
            category_data = record['c']
            book = Book(
                element_id=book_data['<elementId>'],
                neo4j_id=book_data['<id>'],
                avg_age=book_data['AvgOfAge'],
                avg_book_rating=book_data['AvgOfbookRating'],
                author=book_data['Book-Author'],
                title=book_data['Book-Title'],
                isbn=book_data['ISBN'],
                image_url=book_data['Image-URL-L'],
                publisher=book_data['Publisher'],
                year_of_publication=book_data['Year-Of-Publication'],
                category_id=book_data['catagoryid'],
                category=book_data['category'],
                description=book_data['description']
            )
            books1.append(book)
        
        result2 = session.run(cypher_query2)
        for record in result2:
            book_data = record['b']
            # Process book data as needed
            book = Book(
                element_id=book_data['<elementId>'],
                neo4j_id=book_data['<id>'],
                avg_age=book_data['AvgOfAge'],
                avg_book_rating=book_data['AvgOfbookRating'],
                author=book_data['Book-Author'],
                title=book_data['Book-Title'],
                isbn=book_data['ISBN'],
                image_url=book_data['Image-URL-L'],
                publisher=book_data['Publisher'],
                year_of_publication=book_data['Year-Of-Publication'],
                category_id=book_data['catagoryid'],
                category=book_data['category'],
                description=book_data['description']
            )
            books2.append(book)

    return render(request, "pages/template.html", {'books1': books1, 'books2': books2 , 'email' : email , 'users': users})



# not alll thwe work hers

def userbooks(request , id):

    user = id 
    user1 = get_object_or_404(CustomUser, id=user)
    print(user1)

    neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    
    email = request.user.email if request.user.is_authenticated else None



    latest_categories = Add.objects.filter(userid=user) \
                               .values('category_id') \
                               .annotate(latest_date=Max('created_at')) \
                               .order_by('-latest_date')[:5]
    # last getegories to aray
    latest_category_ids = [category['category_id'] for category in latest_categories]

    
    category_ids = []

    # Append to the qury 
    category_ids.extend(latest_category_ids)
   
    cypher_query1 = (
        "MATCH (c:Category)<-[:BELONGS_TO]-(book:Book) "
        "WHERE c.categoryId IN $categoryIds "
        "RETURN c, book "
        "ORDER BY RAND() "
        "LIMIT 250"
    )

    books1 = []

    
    with driver.session() as session:
        result1 = session.run(
            cypher_query1,
            {"categoryIds": category_ids}
        )
        for record in result1:
            book_data = record['book']
            category_data = record['c']
            book = Book(
                element_id=book_data['<elementId>'],
                neo4j_id=book_data['<id>'],
                avg_age=book_data['AvgOfAge'],
                avg_book_rating=book_data['AvgOfbookRating'],
                author=book_data['Book-Author'],
                title=book_data['Book-Title'],
                isbn=book_data['ISBN'],
                image_url=book_data['Image-URL-L'],
                publisher=book_data['Publisher'],
                year_of_publication=book_data['Year-Of-Publication'],
                category_id=book_data['catagoryid'],
                category=book_data['category'],
                description=book_data['description']
            )
            books1.append(book)
        
        


   

 

    return render(request , "pages/userbook.html" ,  {"user" : books1 ,  'email' : email })



def bookdt(request):

  


    # Connect to Neo4j
    neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
   
    cypher_query_all = (
    "MATCH (b:Book) RETURN b LIMIT 1")

     
    with driver.session() as session:
        result = session.run(cypher_query_all)
        books1 = []
        for record in result:
            book_data = record['b']
            book = Book(
                element_id=book_data['<elementId>'],
                neo4j_id=book_data['<id>'],
                avg_age=book_data['AvgOfAge'],
                avg_book_rating=book_data['AvgOfbookRating'],
                author=book_data['Book-Author'],
                title=book_data['Book-Title'],
                isbn=book_data['ISBN'],
                image_url=book_data['Image-URL-L'],
                publisher=book_data['Publisher'],
                year_of_publication=book_data['Year-Of-Publication'],
                category_id=book_data['catagoryid'],
                category=book_data['category'],
                description=book_data['description']
            )
            books1.append(book)
    
    return render(request, 'pages/bookdetail.html', {'books1': books1})

def bk(request, iso):
    # Connect to Neo4j
    neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))

    cypher_query = (
        "MATCH (b:Book {ISO: $iso}) RETURN b LIMIT 1"
    )
    with driver.session() as session:
        result = session.run(cypher_query, iso=iso)
        books1 = []
        for record in result:
            book_data = record['b']
            book = Book(
                element_id=book_data['<elementId>'],
                neo4j_id=book_data['<id>'],
                avg_age=book_data['AvgOfAge'],
                avg_book_rating=book_data['AvgOfbookRating'],
                author=book_data['Book-Author'],
                title=book_data['Book-Title'],
                isbn=book_data['ISBN'],
                image_url=book_data['Image-URL-L'],
                publisher=book_data['Publisher'],
                year_of_publication=book_data['Year-Of-Publication'],
                category_id=book_data['catagoryid'],
                category=book_data['category'],
                description=book_data['description']
            )
            books1.append(book)
    return render(request, 'pages/bk.html', {'books1': books1, "title": iso})





def bk_detail(request, iso , cid):

    neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
    neo4j_username = "neo4j"
    neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
    cypher_query1 = (
    "MATCH (c:Category {categoryId: $cid})<-[:BELONGS_TO]-(book:Book) "
    "RETURN c, book ")
    books1 = []
    books2 = []
    check = "heart_plus"

    id = request.user.id if request.user.is_authenticated else None
    
    dataInside = Add(category_id=cid , userid =id)
    dataInside.save()

    isoinside = BookVisited(bookId= int(iso), userid = id)
    isoinside.save()
        
        
    with driver.session() as session:
        result1 = session.run(cypher_query1,cid=cid)
        for record in result1:
            book_data = record['book']
            category_data = record['c']
            book = Book(
                element_id=book_data['<elementId>'],
                neo4j_id=book_data['<id>'],
                avg_age=book_data['AvgOfAge'],
                avg_book_rating=book_data['AvgOfbookRating'],
                author=book_data['Book-Author'],
                title=book_data['Book-Title'],
                isbn=book_data['ISBN'],
                image_url=book_data['Image-URL-L'],
                publisher=book_data['Publisher'],
                year_of_publication=book_data['Year-Of-Publication'],
                category_id=book_data['catagoryid'],
                category=book_data['category'],
                description=book_data['description']
            )
            books2.append(book)
        
        result2 = session.run("MATCH (b:Book {ISBN: $iso}) RETURN b LIMIT 1", iso=iso)
        for record in result2:
            book_data = record['b']
            # Process book data as needed
            book = Book(
                element_id=book_data['<elementId>'],
                neo4j_id=book_data['<id>'],
                avg_age=book_data['AvgOfAge'],
                avg_book_rating=book_data['AvgOfbookRating'],
                author=book_data['Book-Author'],
                title=book_data['Book-Title'],
                isbn=book_data['ISBN'],
                image_url=book_data['Image-URL-L'],
                publisher=book_data['Publisher'],
                year_of_publication=book_data['Year-Of-Publication'],
                category_id=book_data['catagoryid'],
                category=book_data['category'],
                description=book_data['description']
            )
            books1.append(book)
            if BookLike.objects.filter(bookId=book.isbn, liked=True).exists():
                check = "kid_star"


    return render(request, "pages/bk_detail.html", {"books1": books1 , 'books2' : books2 , 'check' : check})

def form(request):

    id = request.user.id if request.user.is_authenticated else None
    category_id = request.POST.get('category')

    dataIn = Add(category_id = category_id , userid =id)
    dataIn.save()

    print(category_id)

    x = 14
    books = [
        {
            'category_id':100,
            'title': 'Classical Mythology',
            'author': 'Mark P. O. Morford',
            'year_of_publication': '2002',
            'publisher': 'Oxford University Press',
            'image_url': 'http://images.amazon.com/images/P/0195153448.01.LZZZZZZZ.jpg'
        }, ]
    

    return render(request, "pages/form.html",{"books" : books}) 


def account(request):
    return render(request, "pages/account.html")

def creteaccount(request):

  
  #  username = request.GET.get('username')
  #  email = request.GET.get('email')
   # email = request.GET.get('email')
  #  password = request.GET.get('password')
  #  passwordVerify = request.GET.get('verify')
  #  print(email)
  #  if len(str(password)) < 5 :
   #      messages.error(request, "Password must be at least 6 characters long.")
         
   # if password != passwordVerify:

   #    messages.error(request, "Passwords do not match.")
   #    return render(request, 'pages/account.html')

  #  if not Person.objects.filter(email=email).exists():
                    
   #        user = Person(name = username, email =email, password = password)
    #       user.save()
    #       messages.success(request, "Account created successfully.")
    #       return redirect('fatch')
   # else :
             
       #   messages.error(request, "email already exists.")
                      
    
   
      
    return render(request, 'pages/account.html')


def login_view(request):
 #  request.method == 'POST': request.POST.get('username') request.POST.get('password')
     #username = "sabir@gmail.com"
   #   password = "12345678"
    #  u= ""
    #  user = authenticate(request, email=username, password=password)
    #  if user is not None:
          
       #    print("sucsessfly")
       #    login(request, user)
        #   messages.success(request, "You have successfully logged in.")
        #   u = user.name
        #   print(user.name)
        #   return redirect('fatch')  # Redirect to a home or another desired page
     # else:
    #   messages.error(request, "Invalid username or password.")

     return render(request, 'pages/login.html' , )


def login_view(request):
    #if request.method == 'POST':
    #    email = request.POST.get('email')
     #    password = request.POST.get('password')
     #    user = authenticate(request, username=email, password=password)
      #  if user is not None:
       #      login(request, user, backend='myapp.backends.PersonAuthenticationBackend')  # Specify the custom backend
       #      return redirect('pages/profile')
      #   else:
       #      messages.error(request, "Invalid email or password.")
     return render(request, 'pages/login.html')

def profile_view(request):
   #  user = request.user
   #  person = Person.objects.get(email=user.email)
    return render(request, 'pages/profile.html')


def admincharts(request) :
        neo4j_uri = "neo4j+s://db7beccf.databases.neo4j.io"
        neo4j_username = "neo4j"
        neo4j_password = "jd_4C_lKNmyXaYci_ZtTYmXIi4aWHZ-Hbu_B5qhET-s"
        driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_username, neo4j_password))
            
        categories = []
        category_counts = {}
 
        data = Add.objects.all() # data all catagory 
 

        # Dictionary to store category counts bookId
       

        for i in data: 
            id = i.category_id

            with driver.session() as session:
                result = session.run('MATCH (n:Category {categoryId : $id}) RETURN n', id=id)

                for record in result:
                 
                    category = record['n'] # Get the category node from neo4j
                    category_id = category['categoryId'] #in new4j
                    category_name = category['name'] #in new4j take the name 
                  
                    # Count the occurrences of each category
                    if category_name in category_counts: #if the category name is in the dictionary check 
                        category_counts[category_name] += 1 # if exist add 1
                    else:
                        category_counts[category_name] = 1 # if not exist add 1

                    # Create a category object and append it to the categories list
                    category_obj = catagories( #initlize the catagory object  catagories is the class in model to append data 
                        category_id=category_id, #the form to apend data 
                        category_name=category_name
                    )
                    categories.append(category_obj) # append to the empty list

        # Convert the category counts dictionary to a list of lists
        category_counts_list = [[category, count] for category, count in category_counts.items()]


        categoriess = [item[0] for item in category_counts_list]
        amounts = [item[1] for item in category_counts_list]


      
        books = [] #categories
        books_counts = {}
 
        ages =[]
        age_counts = {}
        visited = BookVisited.objects.all() # visted book 

        # Dictionary to store category counts bookId
       

        for i in visited: 
            id = str(i.bookId)
            

            with driver.session() as session:
                result1 = session.run('MATCH (n:Book {ISBN : $id}) RETURN n', id=id)
               

                for recordd in result1:
                   
                    book = recordd['n'] # Get the category node from neo4j
                    date = book['Year-Of-Publication'] #in new4j
                    age = book['AvgOfAge'] #in new4j take the name 
                    age0= age[0]
                    age1= age[1]
                    age= (int(age1)*1 + int(age0)*10)
                    


                    # Count the occurrences of each category
                    if int(date) in books_counts: #if the category name is in the dictionary check 
                        books_counts[int(date)] += 1 # if exist add 1
                    else:
                        books_counts[int(date)] = 1 # if not exist add 1


                

                    if age in age_counts: #if the category name is in the dictionary check 
                        age_counts[age] += 1 # if exist add 1
                    else:
                        age_counts[age] = 1 # if not exist add 1
                        
                        

                    # Create a category object and append it to the categories list
                    book_obj = getvisited( #initlize the catagory object  catagories is the class in model to append data 
                     Gage=age, #the form to apend data 
                        Gyear=date
                    )
                    books.append(book_obj) # append to the empty list
                    age_obj = agee(
                        Gage=age,
                        Gyear=date
                    )
                    ages.append(age_obj)
        # Convert the category counts dictionary to a list of lists
        book_counts_list = [[book, count] for book, count in books_counts.items()]
        age_counts_list = [[book, count] for book, count in age_counts.items()]


        dates = [item[0] for item in book_counts_list]
        conts = [item[1] for item in book_counts_list]
  

        agees = [item[0] for item in age_counts_list]
        agecount = [item[1] for item in age_counts_list]
        likedBook = []
        like = BookLike.objects.all()
        for i in like :
            if i.liked ==True :
            
                    bookid = i.bookId
                    bookidstring = str(bookid)

                    
                    with driver.session() as session:
                        result1 = session.run('MATCH (n:Book {ISBN : $bookidstring}) RETURN n',bookidstring=bookidstring)
                    
                    
                        for record in result1:
                            book_data = record['n']
                            
                            book = Book(
                                element_id=book_data['<elementId>'],
                                neo4j_id=book_data['<id>'],
                                avg_age=book_data['AvgOfAge'],
                                avg_book_rating=book_data['AvgOfbookRating'],
                                author=book_data['Book-Author'],
                                title=book_data['Book-Title'],
                                isbn=book_data['ISBN'],
                                image_url=book_data['Image-URL-L'],
                                publisher=book_data['Publisher'],
                                year_of_publication=book_data['Year-Of-Publication'],
                                category_id=book_data['catagoryid'],
                                category=book_data['category'],
                                description=book_data['description']
                            
                                )
                    
                            likedBook.append(book)
                        print("hhiid")
                        print(likedBook)
                                    
            
  





        
        return  render(request, 'admin/chart.html' , {'data' : book_counts_list , 'book': categories , 'list' : category_counts_list ,'categoriess':categoriess ,'amounts' : amounts , 'dates' :dates , 'conts': conts,'agees' :agees ,'agecount':agecount ,'likedBook' : likedBook})
 