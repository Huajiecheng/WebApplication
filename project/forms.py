from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms import ClearableFileInput
from project.models import Restaurant, Entry, Review, ReviewImage, AddressProfile

MAX_UPLOAD_SIZE = 2500000

#from forms-example
class LoginForm(forms.Form):
    username = forms.CharField(max_length = 20, widget= forms.TextInput(attrs={'id':'id_username'}))
    password = forms.CharField(max_length = 200, widget = forms.PasswordInput(attrs={'id':'id_password'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid username/password")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

#from forms-example
class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=20, widget= forms.TextInput(attrs={'id':'id_first_name'}))
    last_name  = forms.CharField(max_length=20, widget= forms.TextInput(attrs={'id':'id_last_name'}))
    email      = forms.CharField(max_length=50,
                                 widget = forms.EmailInput(attrs={'id':'id_email'}))
    username   = forms.CharField(max_length = 20,widget= forms.TextInput(attrs={'id':'id_username'}))
    password1  = forms.CharField(max_length = 200, 
                                 label='Password', 
                                 widget = forms.PasswordInput(attrs={'id':'id_password'}))
    password2  = forms.CharField(max_length = 200, 
                                 label='Confirm password',  
                                 widget = forms.PasswordInput(attrs={'id':'id_confirm_password'}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super().clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary'
        return username
'''
states_choices = ("Alabama", "Alaska", "Arizona", "Arkansas", "California", 
                  "Colorado", "Connecticut", "Delaware", "District Of Columbia", 
                  "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", 
                  "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
                  "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
                  "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
                  "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
                  "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
                  "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
                  "West Virginia", "Wisconsin", "Wyoming")

'''
states_choices = ((1, "Alabama"), (2, "Alaska"), (3, "Arizona"), (4, "Arkansas"), (5, "California"), (6, "Colorado"),
                (7, "Connecticut"), (8, "Delaware"), (9, "District Of Columbia"),
                (10, "Florida"), (11, "Georgia"), (12, "Hawaii"), (13, "Idaho"), (14, "Illinois"), 
                (15, "Indiana"), (16, "Iowa"), (17, "Kansas"), (18, "Kentucky"), (19, "Louisiana"), (20,  "Maine"),
                (21, "Maryland"), (22, "Massachusetts"), (23, "Michigan"), (24, "Minnesota"), (25, "Mississippi"),
                (26, "Missouri"), (27, "Montana"), (28, "Nebraska"), (29, "Nevada"), (30, "New Hampshire"),
                (31, "New Jersey"), (32, "New Mexico"), (34, "New York"), (35, "North Carolina"), (36, "North Dakota"),
                (36, "Ohio"), (37, "Oklahoma"), (38, "Oregon"), (39, "Pennsylvania"), (40, "Rhode Island"), (41, "South Carolina"),
                (42, "South Dakota"), (43, "Tennessee"), (44, "Texas"), (45, "Utah"), (46, "Vermont"), (47, "Virginia"),
                (48, "Washington"), (49, "West Virginia"), (50, "Wisconsin"), (51, "Wyoming"))

class ProfileAddressForm(forms.ModelForm):

    state = forms.ChoiceField(choices=states_choices, required=True)
    class Meta:
        model = AddressProfile
        fields = ('picture', 'postal_code', 'state', 'street_1', 'street_2')
    def clean_picture(self):
        picture = self.cleaned_data['picture']
        if not picture:
            return picture
        if not picture or not hasattr(picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture
    def clean_state(self):
        state = self.cleaned_data['state']
        if not state:
            raise forms.ValidationError('You must choose a state')
        return state
    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if not postal_code or not postal_code.isdigit():
            raise forms.ValidationError('You must enter a valid postal code')
        if int(postal_code) > 99999 or int(postal_code) < 10000:
            raise forms.ValidationError('You must enter a valid postal code')
        
        return postal_code
    def street_1(self):
        street_1 = self.cleaned_data['street_1']
        if not street_1:
            raise forms.ValidationError('You must enter a valid street address')
        return street_1

class AddressForm(forms.ModelForm):
    state = forms.ChoiceField(choices=states_choices, required=True)
    class Meta:
        model = AddressProfile
        fields = ('postal_code', 'state', 'street_1', 'street_2')
    def clean_state(self):
        state = self.cleaned_data['state']
        if not state:
            raise forms.ValidationError('You must choose a state')
        return state
    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        if not postal_code or not postal_code.isdigit():
            raise forms.ValidationError('You must enter a valid postal code')
        if int(postal_code) > 99999 or int(postal_code) < 10000:
            raise forms.ValidationError('You must enter a valid postal code')
        
        return postal_code
    def street_1(self):
        street_1 = self.cleaned_data['street_1']
        if not street_1:
            raise forms.ValidationError('You must enter a valid street address')
        return street_1

class CreateRestaurant(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'description', 'location', 'photo', 'deliveryTime')
    def clean_photo(self):
        picture = self.cleaned_data['photo']
        if not picture:
            return picture
        if not picture or not hasattr(picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture

class CreateEntry(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('name', 'price', 'description', 'entry_type')
    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError('You must enter a name for this entry')
        return name
    def clean_price(self):
        price = self.cleaned_data['price']
        if not price:
            raise forms.ValidationError('You must enter a price for this entry')
        if price < 0:
            raise forms.ValidationError('You must enter a positive float as price')
        return price
    def clean_description(self):
        description = self.cleaned_data['description']
        if not description:
            raise forms.ValidationError('You must enter a description for this entry')
        return description


class CreateReview(forms.ModelForm):
    rating_choices = ((1,1),(2,2),(3,3),(4,4),(5,5))
    rating = forms.MultipleChoiceField(choices=rating_choices, widget=forms.CheckboxSelectMultiple())
    class Meta:
        model=Review
        fields = ('review_text',)
    def clean_rating(self):
        if len(self.cleaned_data['rating']) != 1:
            raise forms.ValidationError("Select one score.")
        return self.cleaned_data['rating'][0]


class CreateReviewImage(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model = ReviewImage
        fields = ('image',)
    def clean_image(self):
        picture = self.cleaned_data['image']
        if not picture:
            return picture
        if not picture or not hasattr(picture, 'content_type'):
            raise forms.ValidationError('You must upload a picture')
        if not picture.content_type or not picture.content_type.startswith('image'):
            raise forms.ValidationError('File type is not image')
        if picture.size > MAX_UPLOAD_SIZE:
            raise forms.ValidationError('File too big (max size is {0} bytes)'.format(MAX_UPLOAD_SIZE))
        return picture