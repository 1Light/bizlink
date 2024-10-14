from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import *
from django.http import Http404
from .forms import ChatMessageCreateForm
from userauth.models import CustomUser
from django.db.models import Exists, OuterRef

# Create your views here.

def chat(request):
    user = request.user
    # Get all chat groups the user is a member of
    chat_groups = ChatGroup.objects.filter(members=user)

    # Dictionary to store unread message count for each group
    unread_messages_per_group = {}

    # Variable to store the total unread message count across all groups
    total_unread_messages = 0

    # Iterate over each chat group
    for chat_group in chat_groups:
        # Get all messages in the current group where the current user is NOT the author
        chat_messages = GroupMessage.objects.filter(group=chat_group).exclude(author=user)

        # Filter unread messages for the current user
        unread_messages = chat_messages.filter(
            ~Exists(ReadReceipt.objects.filter(message=OuterRef('pk'), user=user))
        )

        # Store the count of unread messages for the current group
        unread_count = unread_messages.count()
        unread_messages_per_group[chat_group.chatGroupId] = unread_count

        # Add the unread count for this group to the total unread messages
        total_unread_messages += unread_count

    # Use a set to collect unique community members across all groups (excluding the logged-in user)
    community_members = set()

    for chat_group in chat_groups:
        # Add all members of the chat group, excluding the logged-in user
        community_members.update(member for member in chat_group.members.all() if member != user)
    
    # Pass chat_groups, community_members, unread_messages_per_group, and total_unread_messages to the template
    return render(request, "chat/chat.html", {
        'chat_groups': chat_groups,
        'community_members': community_members,
        'unread_messages_per_group': unread_messages_per_group,  # Pass unread counts to template
        'total_unread_messages': total_unread_messages,  # Pass total unread message count
    })

def chatroom(request, chatGroupId):
    user = request.user
    # Fetch the chat group
    chat_group = get_object_or_404(ChatGroup, chatGroupId=chatGroupId)

    # Get all messages in the group that were NOT sent by the current user
    chat_messages = chat_group.chat_messages.exclude(author=user)

    # Fetch unread messages for this chat group that the user hasn't read yet
    unread_messages = chat_messages.filter(
        ~Exists(ReadReceipt.objects.filter(message=OuterRef('pk'), user=user))
    )

    # Mark those messages as read by creating a ReadReceipt for each unread message
    for message in unread_messages:
        ReadReceipt.objects.create(message=message, user=user)

    # Find the other members of the chat group (excluding the current user)
    other_chat_user = chat_group.members.exclude(id=user.id).first()  

    # If the request is made with HTMX (to load messages dynamically)
    if request.htmx:
        form = ChatMessageCreateForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            # Render the newly created message using a partial template
            return render(request, "chat/partials/chat_message_p.html", {
                'message': message,
                'user': user,
            })

    # Render the entire chatroom if not using HTMX
    return render(request, "chat/partials/chat_window_p.html", {
        'chat_messages': chat_group.chat_messages.all(),  # All messages for display
        'user': user,
        'form': ChatMessageCreateForm(),
        'chat_group': chat_group,
        'other_chat_user': other_chat_user,
    })

def unread_message_count(request, chatGroupId):
    user = request.user
    chat_group = get_object_or_404(ChatGroup, chatGroupId=chatGroupId)

    # Get all messages in the group that were NOT sent by the current user
    chat_messages = chat_group.chat_messages.exclude(author=user)

    # Fetch unread messages for this chat group that the user hasn't read yet
    unread_messages = chat_messages.filter(
        ~Exists(ReadReceipt.objects.filter(message=OuterRef('pk'), user=user))
    )

    # Mark those messages as read by creating a ReadReceipt for each unread message
    for message in unread_messages:
        ReadReceipt.objects.create(message=message, user=user)

    # Return the count of unread messages as JSON
    return JsonResponse({'unread_count': unread_messages.count()})

def get_or_create_chatroom(request, username):
    user = request.user
    print("I am hereeeeeeeee")

    #if user.username == username:
        #return redirect("chat:chat")
    
    print(username)
    
    other_user = CustomUser.objects.get(username = username)
    my_chatrooms = user.chat_groups.filter(is_private=True)

    if my_chatrooms.exists():

        for chatroom in my_chatrooms:
            if other_user in chatroom.members.all():
                chatroom = chatroom
                break
            else:
                chatroom = ChatGroup.objects.create(is_private=True)
                chatroom.members.add(other_user, user)
            
    else:
        chatroom = ChatGroup.objects.create(is_private=True)
        chatroom.members.add(other_user, user)
    
    return redirect("chat:chatroom", chatroom.chatGroupId)