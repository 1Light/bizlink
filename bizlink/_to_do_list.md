# Admin

- Use jazzmine
  -Now, user type for admin registery is set to busines sowenr by default, fix it so it says admin

# Login

- remeber me check box, recaptcha, forgot password feature

# Upper navbar

- figure out why the after elemnet s int eh wishlist, account are uppercase

# Shop

- A feature where an owner adds an admin to help with shop

# Signup

- I think it redirects to login even if there is an error
- Display the message registered successfully
- make it so it moves to the exact step in the multi step form the error occurred
- I think the code allows registeration as business owner and customer using the same email, decide if u want to allow that

# Bonus

- Image slider that show 3 images per slide and moves only one per click.
- Tabs beneath the product detail

# Concerns

- Ckeditor u installed bundeles version 4 which has security issues.
- Password change option, email authentication
- I think there is a case where if you create the user from the admin site, you won't be able to login
- currently, the signal only creates a profile for those user created directly on the admin site or the terminal. For the sign up form, i am not using the signal cuz they were never getting called. Instead I am attempting to directly create the user profile in the sign up form during the registeration
- A person might be able to sign up using the same phone number but different cridentials. u cn set the unique=true on it or find another
- wishlist atble uses noremal djangoid. fix it. use shortuuid
- teh social media is howing error, check

# Luxury

- The wishlist count span flickers. work on way to fix that.

# Owner

- Needs an inventory overview where he can update stock quantity
- phone and map suggestion

# Upcoming

- render every product
- create a discount feature
- share feature for product (link)
- banner(contact us)

# Whole frontend

- Shop creation
- Product Creation
- Customer Side
- Inbox

# Later

- Rating
- Inventory
- Social Media Influencer Side
