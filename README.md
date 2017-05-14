# jugnoo
Documentation for quotePoster API

This API provides a feature to fetch 100 post from the TheySaidSo Famous Quotes API to populate a text file and post a unique quote from it on your facebook account.

Productivity : 
Instead of writing quotes daily and converting them into an image manually, this API saves a lot of this manual effort and posts a text quote to facebook by automatically converting it to an image. Also, there is no need to track what quotes you have previously posted as here once the quote is posted, it is deleted from the text file that is used to create the post image.

To be able to use this API we need to run the following commands to download these: 

For MAC user:

brew install pip3

Now in pip3,

pip3 install facebook-sdk

pip3 install requests

pip3 install pillow

pip3 install textwrap


Now go to terminal and go to the path where the file ‘jugnoo.py’ is stored and then run command python3 jugnoo.py


Key Functions :
postAsImage() : This function is called to post one quote from a textfile to your facebook account after converting it to an image.

makeQuoteFile()  : This function is to be executed once ONLY to get a lists from a quotes API(TheySaidSo) in our case to populate the quotes text file with new quotes. Make sure not to run it again as it might fetch a quote that has already been used by you and deleted!

postImageOnFacebook(image) : This take an open image file as an argument and post this image on your facebook wall. This function uses the facebook GraphAPI and requires you to pass the access token as argument. The user needs to provide an access token after granting permissions to use it.
Currently we can get the access token from https://developers.facebook.com/tools/explorer/ by clicking on Get Token->Get User Access Token and specifically granting it the “publish_actions” permissions. Copy it and paste it in the facebook.GraphApi() function’s argument. Ideally we should generate a oauth_access_token and pass it as argument to the facebook.GraphApi() function



convertQuoteToImage() : This function reads the quotes file created in the makeQuoteFile() function. It reads the first quote from the file, then deletes that quote so that now the 2nd quote in the file becomes the first quote for further posts. Once the quote is obtained as a string, various PIL API features transform that text quote to a image and returns the open image file to be processed further. It ensures the proper alignment of each line of the quote in the image and make sure that it doesn't cross image boundary.


