from dataclasses import dataclass
import json
import traceback, os
from typing import Any, Dict, Union

class DuplicateResponseException(Exception):
    pass

@dataclass(frozen=True)
class ContentType:
    textPlain: str = "text/plain"
    textHtml: str = "text/html"
    textCss: str = "text/css"
    textJavaScript: str = "text/javascript"
    applicationJson: str = "application/json"
    applicationXml: str = "application/xml"
    imageJpeg: str = "image/jpeg"
    imagePng: str = "image/png"
    imageGif: str = "image/gif"
    imageSvgXml: str = "image/svg+xml"
    audioMpeg: str = "audio/mpeg"
    audioOgg: str = "audio/ogg"
    videoMp4: str = "video/mp4"
    videoWebm: str = "video/webm"
    applicationOctetStream: str = "application/octet-stream"
    applicationPdf: str = "application/pdf"
    applicationZip: str = "application/zip"
    applicationXWwwFormUrlencoded: str = "application/x-www-form-urlencoded"
    multipartFormData: str = "multipart/form-data"
    multipartByteranges: str = "multipart/byteranges"

class Response:
    status_code: int = None
    contentType: str = None
    body: bytes = None
    
    def _is_body_init(self):
        if self.body is not None:
            raise DuplicateResponseException("Duplicate response is not allowed!")

    def json(self, json_object: Any):
        self._is_body_init()
        try:
            resp_obj = json.dumps(json_object)
        except:
            traceback.print_exc()
            return None
        
        # we set the the contentType here
        self.contentType =  ContentType.applicationJson
        # set the response body here
        self.body = resp_obj.encode()
    
    def template(self,template):
        self._is_body_init()
        with open("views/" + template , "rb") as f:
            views_content = f.read()
            
        # set the content type
        self.contentType =  ContentType.textHtml
        # set body
        self.body = views_content

    
def make_response(resp_object: Union[str, Response])-> str:
    if isinstance(resp_object, Response):
        response = (
            f"HTTP/1.1 {resp_object.status_code} OK\r\n"
            f"Content-Type: {resp_object.contentType}\r\n"
            f"Content-Length: {len(resp_object.body)}\r\n"
            "\r\n"
        )
        return response.encode() + resp_object.body
    elif isinstance(resp_object, str) or isinstance(resp_object, bytes):
        response = (
            f"HTTP/1.1 {200} OK\r\n"
            f"Content-Type: {ContentType.textPlain}\r\n"
            f"Content-Length: {len(resp_object)}\r\n"
            "\r\n"
            f"{resp_object}"
        )
        return response.encode()
    else:
        raise TypeError("Route Handler must have a return type of str or Response")
