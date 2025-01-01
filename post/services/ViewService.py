from django.core.exceptions import ObjectDoesNotExist
from ..models import Post
from ..serializers import CreatePostsSerilizer  , PostSerializerPartialUpdate , PostRetrieve , ReadPostSerilizer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import logging
from django.core.cache import cache
logger = logging.getLogger(__name__)

class ReadCachservice:
    pass

class ReadViewService:
    @staticmethod
    def Read_post(self , request):
            posts = PostModel.objects.all()
            if posts == []:
                logger.warning("No posts found")
                return Response([], status=status.HTTP_204_NO_CONTENT)

            serializer = ReadPostSerilizer(posts, many=True , context={'request': request})
            data = serializer.data
            for post in data:
                if post.get("image"):
                    post["image"] = request.build_absolute_uri(post["image"])
            cache.set("list_key",data, 60 * 15)
            return data
    @staticmethod
    def ReadPosts(self , request):
        cached_data = cache.get("list_key")
        if cached_data is not None:
            response =  Response(data=cached_data, status=status.HTTP_200_OK)
            return response
        data = ReadViewService.Read_post(self , request)
        return  Response(data)


    @staticmethod
    def retrieve(self, request, pk):
        try:
            product = get_object_or_404(PostModel, pk=pk)
            serializer = PostRetrieve(product , context={"request":request})
            data = serializer.data
            return Response(data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            logger.warning(f"Post with ID {pk} not found")
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
class ChangesViewService:
    @staticmethod
    def update_cache(request):
        cache.delete("list_key")
        products = PostModel.objects.all()
        serializer = ReadPostSerilizer(products, many=True, context={'request': request})
        data = serializer.data
        cache.set("list_key", data, 60 * 15)

    @staticmethod
    def CreatePost(self , request):
        logger.info("Received POST request to create a new post")

        try:
            data = request.data
            serializer = CreatePostsSerilizer(data=data)

            if serializer.is_valid():
                logger.info("Validated data for new post creation")

                user = request.user
                logger.info(f"Associated user ID: {user.id}")

                data['author'] = user.id
                serializer.save()
                logger.info("New post created successfully")
                ChangesViewService.update_cache(request)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.error(f"Validation failed for post creation: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(f"Error in CreatePost: {str(e)}")
            return Response({"error": "An error occurred while creating the post"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def PartialUpdate(self , request , pk):
        logger.info(f"Received PATCH request to update post with ID: {pk}")

        try:
            post = get_object_or_404(PostModel, pk=pk)
            logger.info(f"Retrieved post with ID: {post.postId}")

            serializer = PostSerializerPartialUpdate(post, data=request.data)

            if serializer.is_valid():
                logger.info("Validated data for partial update")
                serializer.save()
                logger.info("Partial update completed successfully")
                ChangesViewService.update_cache(request)

                return Response(serializer.data)
            else:
                logger.error(f"Validation failed for partial update: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            logger.warning(f"Post with ID {pk} not found")
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"Error in PartialUpdate: {str(e)}")
            return Response({"error": "An error occurred while updating the post"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def Delete(self , request , pk ):
        logger.info(f"Received DELETE request to remove post with ID: {pk}")

        try:
            post = get_object_or_404(PostModel, pk=pk)
            logger.info(f"Deleting post with ID: {post.postId}")
            post.delete()
            logger.info("Post deletion completed successfully")
            ChangesViewService.update_cache(request)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            logger.warning(f"Attempted to delete non-existent post with ID {pk}")
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"Error in Delete: {str(e)}")
            return Response({"error": "An error occurred while deleting the post"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LikePosts:
    @staticmethod
    def like(request , pk ):
        logger.info(f"Received LIKE request for post ID: {pk}")

        try:
            post = get_object_or_404(PostModel, pk=pk)
            logger.info(f"Retrieved post with ID: {post.postId}")

            user = request.user
            logger.info(f"Associated user ID: {user.id}")

            if user in post.likes.all():
                logger.info(f"Removing like for user {user.id} on post {post.postId}")
                post.likes.remove(user)
                logger.info("Like removed successfully")
                return Response("Removed like.", status=status.HTTP_201_CREATED)
            else:
                logger.info(f"Adding like for user {user.id} on post {post.postId}")
                post.likes.add(user)
                logger.info("Like added successfully")
                return Response("Added like.", status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:
            logger.warning(f"Post with ID {pk} not found")
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception(f"Error in like method: {str(e)}")
            return Response({"error": "An error occurred while processing the like"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
