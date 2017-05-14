import PIL as pillow
from PIL import ImageFont, Image, ImageDraw,ImageOps

import facebook
import requests
import textwrap
import json
from settings import FACEBOOK_SECRET_KEY, FACEBOOK_APP_ID, FB_ACCESS_TOKEN_URL, OUTPUT_PATH, IMAGE_SOURCE_PATH, \
    QUOTE_FILE_PATH


def get_fb_token():
    """
            Generate a FB access token for a user to allow publish_action permission to allow the facebook app with FACEBOOK_APP_ID as app id to post on his wall after the user grants permissions

               Extended description of function.

                  Parameters
                       ----------

                  Returns
                       -------
                       ACCESS TOKEN
                           It uses the FACEBOOK_SECRET_KEY and FACEBOOK_APP_ID to ask the user for an access token to post on his behalf and returns the access token
    """
    client_secret = FACEBOOK_SECRET_KEY
    app_id = FACEBOOK_APP_ID
    payload = {'grant_type': 'client_credentials', 'client_id': app_id, 'client_secret': client_secret}
    file = requests.post(FB_ACCESS_TOKEN_URL, params=payload)
    json_data = json.loads(file.text)
    result = json_data["access_token"]
    return result


def convertQuoteToImage():
    """
        Convert a text quote into an image.

           Extended description of function.

              Parameters
                   ----------

                   Returns
                   -------
                   Image Path
                       It converts the first quote from my quotes text file  into a high quality image. It ensures the proper alignment of each line of the quote in the image and make sure that it doesn't cross image boundary.

        """
    line = 'None'
    with open(QUOTE_FILE_PATH) as f:
        line = f.readline()
    with open(QUOTE_FILE_PATH, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(QUOTE_FILE_PATH, 'w') as fout:
        fout.writelines(data[1:])

    source_img = Image.open(IMAGE_SOURCE_PATH).convert("RGBA")
    font = ImageFont.truetype("Arial.ttf", 70)
    w, h = source_img.size
    img = Image.new("RGBA", (1024, 1024), (120, 20, 20))
    w, h = img.size
    draw = ImageDraw.Draw(img)
    lines = textwrap.wrap(line, width=27)
    y_text = 100
    # used to break long quote into multiple lines so as to dynamcally ensure that it NEVER crosses the boundary of the image created
    for l in lines:
        #print(l)
        #get each line of quote ad add it to image in a center aligned format
        f, height = font.getsize(l)
        draw.text(((w - f) / 2, y_text), l, font=font)
        y_text += height
    source_img.paste(img, (0, 0))
    # save in new file
    img.save(OUTPUT_PATH, "JPEG")
    tempImg=ImageOps.expand(Image.open(OUTPUT_PATH), border=30, fill='yellow')
    tempImg.save(OUTPUT_PATH)
    image = open(OUTPUT_PATH, 'rb')
    return image


def makeQuoteFile():
    """
        Make a quotes text file from the TheySaidSo Api

           Extended description of function.

              Parameters
                   ----------

                   Returns
                   -------
                   Void
                       It creates a text file with 100(it can be changed) different quotes from the mentioned API
    """
    response = requests.get("https://talaikis.com/api/quotes/",
                            headers={
                                "Content-Type": "application/x-www-form-urlencoded",
                                "Accept": "application/json"
                            }
                            )
    data = response.json()
    with open(QUOTE_FILE_PATH, "w") as file:
        for item in data:
            file.write(item['quote'] + '\n')


def maintainQuoteFile():
    """
    Maintain the quotes in the text file. This function is not being used but can be used/modified yo add more logic on how to handle thw quotes file

       Extended description of function.

          Parameters
               ----------

               Returns
               -------
               Void
                   It maintains the that unique quotes are always there in the text file

    """
    response = requests.get("https://talaikis.com/api/quotes/",
                            headers={
                                "Content-Type": "application/x-www-form-urlencoded",
                                "Accept": "application/json"
                            }
                            )
    #print(response.content)
    data = response.json()
    with open(QUOTE_FILE_PATH, "r") as f2:
        content = f2.readlines()
    with open(QUOTE_FILE_PATH, "r+") as file:
        for item in data:
            if not item['quote'] + '\n' in content:
                file.write(item['quote'] + '\n')


def postImageOnFacebook(img):
    """
           Post an image on Facebook.

           Extended description of function.

           Parameters
           ----------
           arg1 : img (open(/path/to/the/image/to/be/posted) in 'rb' mode)
               Quote which is to be posted

           Returns
           -------
           Void
               It just posts an image on Facebook

    """

    oauth_access_token = get_fb_token()
    graph = facebook.GraphAPI(oauth_access_token)
    #graph = facebook.GraphAPI('TO TEST IT , HERE ENTER THE USER ACCESS TOKEN FROM GRAPH API EXPLORER with publish_action permission ')
    graph.put_photo(image=img, message='Look at this cool photo!')
    return


def postContentAsImage():
    """
        Convert quote to image and then post an image post on Facebook.

        Extended description of function.

        Parameters
        ----------

        Returns
        -------
        Void
            It coverts a quote to image and just posts an image post on Facebook

    """
    # maintainQuoteFile()
    #makeQuoteFile()
    img = convertQuoteToImage()
    postImageOnFacebook(img)

    # First put the quote into image
    # Then post it onto Fb
    return


postContentAsImage()
