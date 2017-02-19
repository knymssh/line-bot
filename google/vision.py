# coding:utf-8
# !/usr/bin/python

# Copyright 2016 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import base64
import os

from vendor.googleapiclient import discovery
from vendor.oauth2client.service_account import ServiceAccountCredentials

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'
GOOGLE_APPLICATION_CREDENTIALS = {
    "type": "service_account" # 色々省略。GoogleDeveloperConsoleから認証情報もらってきてください。
}


def get_image_text(image):
    request = get_vision_service().images().annotate(body={
        'requests': {
            'image': {
                'content': base64.b64encode(image)
            },
            'features': [
                {"type": "FACE_DETECTION", "maxResults": 5},
                {"type": "LABEL_DETECTION", "maxResults": 5},
                {"type": "TEXT_DETECTION", "maxResults": 5},
                {"type": "LANDMARK_DETECTION", "maxResults": 5},
                {"type": "LOGO_DETECTION", "maxResults": 5},
                {"type": "SAFE_SEARCH_DETECTION", "maxResults": 5}
            ],
            'imageContext': {
                'languageHints': [
                    "ja",
                    "en"
                ]
            }
        },
    })
    response = request.execute()

    annotation = response['responses'][0].get('safeSearchAnnotation')
    if annotation.get("adult") == "POSSIBLE" or annotation.get("adult") == "LIKELY" or annotation.get(
            "adult") == "VERY_LIKELY":
        return u"えっちなのはいけないと思います！"
    if annotation.get("medical") == "POSSIBLE" or annotation.get("medical") == "LIKELY" or annotation.get(
            "adult") == "VERY_LIKELY":
        return u"そういうのはちょっと、、"
    if annotation.get("spoof") == "POSSIBLE" or annotation.get("spoof") == "LIKELY" or annotation.get(
            "adult") == "VERY_LIKELY":
        return u"詐欺にかけようったってそうはいきません！？"
    if annotation.get("violence") == "POSSIBLE" or annotation.get("violence") == "LIKELY" or annotation.get(
            "adult") == "VERY_LIKELY":
        return u"あっ、暴力はダメです！ダメです！ぎゃー！"

    text = u""
    annotations = response['responses'][0].get('labelAnnotations')
    if annotations is not None:
        text = text + u'多分こんな感じの写真だと思います。' + os.linesep
        for annotation in annotations:
            text = text + u'[ ' + annotation.get("description") + u' ]' + os.linesep
        text = text + os.linesep

    annotations = response['responses'][0].get('textAnnotations')
    if annotations is not None:
        text = text + u"こんな文字が写ってますよね。" + os.linesep
        for annotation in annotations:
            text = text + u'[ ' + annotation.get("description") + u' ]' + os.linesep
        text = text + os.linesep

    annotations = response['responses'][0].get('faceAnnotations')
    if annotations is not None:
        text = text + str(len(annotations)) + u"人写ってるのが分かりました！" + os.linesep
        count = 1
        for annotation in annotations:
            text = text + str(count) + u'人目は'
            if annotation.get("joyLikelihood") == "POSSIBLE" or annotation.get("joyLikelihood") == "LIKELY" or annotation.get("joyLikelihood") == "VERY_LIKELY":
                text = text + u"楽しそう!" + os.linesep
            elif annotation.get("sorrowLikelihood") == "POSSIBLE" or annotation.get("sorrowLikelihood") == "LIKELY" or annotation.get("sorrowLikelihood") == "VERY_LIKELY":
                text = text + u"悲しそう、、!" + os.linesep
            elif annotation.get("angerLikelihood") == "POSSIBLE" or annotation.get("angerLikelihood") == "LIKELY" or annotation.get("angerLikelihood") == "VERY_LIKELY":
                text = text + u"怒ってます？" + os.linesep
            elif annotation.get("surpriseLikelihood") == "POSSIBLE" or annotation.get("surpriseLikelihood") == "LIKELY" or annotation.get("surpriseLikelihood") == "VERY_LIKELY":
                text = text + u"驚いてる!!" + os.linesep
            elif annotation.get("underExposedLikelihood") == "POSSIBLE" or annotation.get("underExposedLikelihood") == "LIKELY" or annotation.get("underExposedLikelihood") == "VERY_LIKELY":
                text = text + u"あれ、露出不足ですかね。" + os.linesep
            elif annotation.get("blurredLikelihood") == "POSSIBLE" or annotation.get("blurredLikelihood") == "LIKELY" or annotation.get("blurredLikelihood") == "VERY_LIKELY":
                text = text + u"ピンボケだ >_<" + os.linesep
            elif annotation.get("headwearLikelihood") == "POSSIBLE" or annotation.get("headwearLikelihood") == "LIKELY" or annotation.get("headwearLikelihood") == "VERY_LIKELY":
                text = text + u"帽子かぶってます？" + os.linesep
            else:
                text = text + u"普通？" + os.linesep
            count += 1
        text = text + os.linesep

    annotations = response['responses'][0].get('landmarkAnnotations')
    if annotations is not  None:
        text = text + u"おっ、多分この場所ですよね！" + os.linesep
        for annotation in annotations:
            text = text + u'[ ' + annotation.get("description") + u' ]' + os.linesep
        text = text + os.linesep

    annotations = response['responses'][0].get('logoAnnotations')
    if annotations is not None:
        text = text + u"あっ、知ってますよこのロゴ。" + os.linesep
        for annotation in annotations:
            text = text + u'[ ' + annotation.get("description") + u' ]' + os.linesep
        text = text + os.linesep

    print text
    return text


def get_vision_service():
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(GOOGLE_APPLICATION_CREDENTIALS)
    return discovery.build('vision', 'v1', credentials=credentials,
                           discoveryServiceUrl=DISCOVERY_URL)
