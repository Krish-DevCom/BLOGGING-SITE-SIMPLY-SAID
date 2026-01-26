from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Blog
from .serializers import BlogSerializer

@api_view(['GET', 'POST'])
def blog_list(request):
    if request.method == 'GET':
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    serializer = BlogSerializer(blog)
    return Response(serializer.data)

@api_view(['POST'])
def toggle_like(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
        return Response({"status": "unliked", "like_count": blog.likes.count()})
    blog.likes.add(request.user)
    return Response({"status": "liked", "like_count": blog.likes.count()})

@api_view(['POST'])
def toggle_star(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user in blog.stars.all():
        blog.stars.remove(request.user)
        return Response({"status": "unstarred"})
    blog.stars.add(request.user)
    return Response({"status": "starred"})

@api_view(['POST'])
def toggle_bookmark(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.user in blog.bookmarks.all():
        blog.bookmarks.remove(request.user)
        return Response({"status": "unbookmarked"})
    blog.bookmarks.add(request.user)
    return Response({"status": "bookmarked"})