import requests
from collections import Counter

def displayUserInfo(users): 
    #users is a list of json objects, each json object represents a user
    for user in users:
        name = user["name"]
        email = user["email"]
        print("Name: ", name, " Email: ", email)

def countUserPosts(userPosts):
    #userPosts is a list of json objects, each json object holds info about a user's post
    
    #creating a list of userIDs from userPosts to pass to Counter class
    user_ids = [post['userId'] for post in userPosts]

    #Using Counter to count the number of posts for each user
    users_posts_count = Counter(user_ids)
    print("Number of posts for each user: ", users_posts_count)

    return users_posts_count

def usersWithMostPosts(usersPostsCount, n):
    #usersPostCount = Counter object with user:post_counts as key value pair
    # n = number of users with highest posts required

    highestPostsUsers = usersPostsCount.most_common(n)
    print("Users with most posts: ", highestPostsUsers)


#accessing user information
userdata_response = requests.get("https://jsonplaceholder.typicode.com/users")
user_data = userdata_response.json()

#accessing user post information
userposts_response = requests.get("https://jsonplaceholder.typicode.com/posts")
user_posts_data = userposts_response.json()

#Displaying user information
displayUserInfo(user_data)

#Number of posts for each user
usersPostsCounter = countUserPosts(user_posts_data)

#users with most posts: 
usersWithMostPosts(usersPostsCounter, 5)