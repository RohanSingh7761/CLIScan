import google.generativeai as genai
import PIL.Image
API_KEY = 'AIzaSyB6lnyP8r-7x0pX89HrKjxgr5NlKhjoWOc'
genai.configure(api_key=API_KEY)


def TextResponse(value , stream = False):
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(value,stream=stream)
        if stream:
            return response
        else:
            return response.text
    except Exception as e:
        print(f'{type(e).__name__}: {e}')


def TextPlusImageResponse(image , stream=False):
    img = PIL.Image.open(image)
    model = genai.GenerativeModel('gemini-pro-vision')
    try:
        response = model.generate_content(img , stream=stream)
        if stream:
            return response
        else:
            return response.text
    except Exception as e:
        print(f'{type(e).__name__}: {e}')

class Response:
    def __init__(self) -> None:
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.model.start_chat(history=[])


    def Chat(self,request,stream):
        try:
            response = self.chat.send_message(request, stream=stream)
            if stream:
                return response
            else:
                return response.text
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
            
    @property
    def history(self):
        for message in self.chat.history:
            yield f'**{message.role}**: {message.parts[0].text}'




if __name__ == "__main__":
    stream_bool = True
    # answer = TextResponse("What is the meaning of life?" , stream_bool)
    # answer = TextPlusImageResponse('image.png',stream_bool)

    object = Response()
    answer = object.Chat(request = "Hi gemini , My name is rjdp .",stream=stream_bool)

    if stream_bool:
        for chunk in answer:
            print(chunk.text)
    else:
        print(answer)
