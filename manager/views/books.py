from imports import *


def books(request):
    if request.session.get('isloggedin', False):
        data['view']="books"
        data['username']=request.session.get("username")
        data['collections']=Collection.objects.all()
        data['books']=Book.objects.all()
        data['authors']=Author.objects.all()
        template = loader.get_template('manager_books.html')
        context = {
        'data': data
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect("login")


def createbook(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            name=request.POST.get("name")
            description=request.POST.get("description")
            authorid=request.POST.get("authorid")
            isbn=request.POST.get("isbn")
            publishdate=request.POST.get("publishdate")

            book=processBook(name,description,authorid,isbn,publishdate)
            if book.id!=None:
                data={}
                data['status']="ok"
                data['message']="book created successfully"
            else:
                data={}
                data['message']="unable to create book"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../books")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../books")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def updatebook(request):
    if request.session.get('isloggedin', False):
        if request.method == "POST":
            bookid = request.POST.get("id")
            name=request.POST.get("name")
            description=request.POST.get("description")
            authorid=request.POST.get("authorid")
            isbn=request.POST.get("isbn")
            publishdate=request.POST.get("publishdate")

            book=processBook(name,description,authorid,isbn,publishdate,bookid)
            if book.id!=None:
                data={}
                data['status']="ok"
                data['message']="book updated successfully"
            else:
                data={}
                data['message']="unable to update book"
                data['status']="failed"
            context = {
                'data': data
                }
            return HttpResponseRedirect("../books")
        else:
            data={}
            data['message']="invalid method POST required"
            data['status']="failed"
            context = {
            'data': data
            }
            return HttpResponseRedirect("../books")

    else:
        data={}
        data['message']="admin not loggedin"
        data['status']="failed"
        context = {
        'data': data
        }
        return HttpResponseRedirect("login")


def deletebook(request,id):
    if request.session.get('isloggedin', False):
        if id is None:
            bookid=request.GET['id']
        else:
            bookid=id
        book=Book.objects.get(id=bookid)
        book.delete()
        return HttpResponseRedirect("../../books")
    else:
        return HttpResponseRedirect("login")


def listbook(request):
    if request.session.get('isloggedin', False):
        data={}
        offset=request.GET['offset']
        limit=request.GET['limit']
        pager="LIMIT "+offset+","+limit
        media=Book.objects.raw("SELECT api_author.name as author,* from api_books,api_author WHERE api_book.authorid=api_author.id "+pager)
        data={}
        data['total']= Book.objects.count()
        data['rows']=booksToJson(media)
        return JsonResponse(data)
    else:
        request.session['isloggedin']=False
        return HttpResponseRedirect("login")

def processBook(name,description,authorid,isbn,publishdate,bookid=None):
    if bookid==None:
        book = Book.objects.create(name=name, description=description, authorid=authorid, isbn=isbn,
                               publishdate=publishdate, createdate=timezone.now())
    else:
        book = Book.objects.get(id=bookid)
        book.name = name
        book.description = description
        book.authorid = authorid
        book.isbn = isbn
        book.publishdate = publishdate
        book.save()

    return book