from django.db import models
import re													
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, postData):
        pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode() # create the hash
        return self.create(
            first_name=postData['first_name'], 
            last_name=postData['last_name'], 
            email=postData['email'], 
            password=pw_hash
        )

    # Checking login 
    def authenticate(self, email, password):
        user_with_email = self.filter(email = email)
        if not user_with_email: # we quering for all users with this email, and if its empty list:
            return False
        user = user_with_email[0] # if we do have user with that email in our system:
        return bcrypt.checkpw(password.encode(), user.password.encode()) # checkpw returns True of False

    def validator(self, postData):												
        errors = {}																										
        # NAME VALIDATION 	
        if len(postData['first_name']) < 2:											
            errors['first_name'] = 'First name should be at least 2 characters long.'	
        if not postData['first_name'].isalpha() and postData['first_name'] != '':
            errors['first_name'] = 'First name must containt only letters.'
        if len(postData['last_name']) < 2:										
            errors['last_name'] = 'Last name should be at least 2 characters long.'
        if not postData['last_name'].isalpha() and postData['first_name'] != '':
            errors['last_name'] = 'Last name must containt only letters.'
        # EMAIL VALIDATION
        if len(postData['email']) < 1:
            errors['email'] = "Email cannot be blank."
        if not EMAIL_REGEX.match(postData['email']): 
            errors['email'] = "Email is not valid."
        result =  self.filter(email = postData['email'])
        if len(result) > 0:
            errors['email'] = "Email is already registered."
        # PASSWORD VALIDATION
        if len(postData['password']) < 3:
            errors['password'] = 'Password required, should be at least 8 characters long.'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Confirmation didn't match the password"
        return errors


# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length = 255)										
    last_name = models.CharField(max_length = 255)																			
    email = models.TextField()
    password = models.TextField()
    #themes
    #posts
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)									
    objects = UserManager()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Theme(models.Model):
    name = models.CharField(max_length = 100)
    poster = models.ForeignKey(User, related_name='themes', on_delete=models.CASCADE, null = True)
    #posts
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self.name[:30]


class Post(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField()
    theme = models.ForeignKey(Theme, related_name='posts', on_delete=models.CASCADE, null = True)
    poster = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, null = True)
    created_at = models.DateTimeField(auto_now_add = True)  								
    updated_at = models.DateTimeField(auto_now = True)	

    def __str__(self):
        return self.title[:30]