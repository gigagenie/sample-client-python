# Sample Client Python
본 프로젝트는 GiGA Genie Inside(이하, G-INSIDE) API의 규격(grpc, REST)에 맞추어 개발된 
Python 샘플 클라이언트입니다.


## GiGA Genie Inside
GiGA Genie Inside(이하, G-INSIDE)는 3rd party 개발자가 자신들의 제품(단말 장치, 서비스, 앱 등)에 KT의 AI Platform인 
'기가지니'를 올려서 음성인식과 자연어로 제어하고 기가지니가 제공하는 서비스(생활비서, 뮤직, 라디오 등)를 사용할 수 있도록 해줍니다.
G-INSIDE는 기가지니가 탑재된 제품을 개발자들이 쉽게 만들 수 있도록 개발 도구와 문서, 샘플 소스 등 개발에 필요한 리소스를 제공합니다.


## Sample client Python 개요

Sample Client에 구현되어있는 기능은 다음과 같습니다.
* 디바이스 키 인증
* 음성/Text를 이용한 대화
    * 마이크(mic) 제어
    * ServiceM RPC command 일부 지원
        >해당 command는 Cloud AI Platform에서 제공하는 API로 G-API 스펙은 별도 공간을 통해 오픈 예정입니다.

다른 언어의 샘플은 https://github.com/gigagenie 에서 확인할 수 있습니다.


## 배포 패키지 구성

* README.md: this file
* agent.config: 본 배포판 실행을 위한 서버와 키 정보(키 발급 후 수정 필요)
* requirements.txt: 본 배포판에서 사용되는 Python 라이브러리
* **run_enter.py**: 본 배포판을 CLI로 실행하는 파일
* **run_curses.py**: 본 배포판을 텍스트 모드 디스플레이 형태로 실행하는 파일
* proto/: grpc proto 파일
* agent/: Client 구현을 위해 필요한 라이브러리 및 모듈
    * _audio.py: 마이크 기능 및 pyaudio 라이브러리를 이용한 오디오 출력 모듈
    * _player.py: Vlc와 Wave 라이브러리를 이용한 출력 player 모듈
    * _authorize.py: UUID 등록 및 확인 모듈
    * regist.py: GINSIDE 계정 키의 UUID 확인
    * **service.py**: ServiceM RPC command 기능
    * grpc_channel.py: grpc 채널 연결 기능
    

# Prerequisites

## 인사이드 디바이스 키 발급
1. API Link(https://apilink.kt.co.kr) 에서 회원가입 
2. 사업 제휴 신청 및 디바이스 등록 (Console > GiGA Genie > 인사이드 디바이스 등록)
3. 디바이스 등록 완료 후 My Device에서 등록한 디바이스 정보 및 개발키 발급 확인 (Console > GiGA Genie > My Device)
4. 발급된 개발키를 agent.config 파일에 등록하여 개발 서버 연동 및 테스트


## 개발 환경

* OS: Ubuntu, Mac OS X 지원
* Python version: 2.x, 3.x 지원

# Quick Start

## 1. 오디오 모듈 및 pip 설치
### - Ubuntu
    $ sudo apt-get install libasound-dev
    $ sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
    $ sudo apt-get install python-pip
    $ sudo apt-get install vlc
    
### - Mac OS X
    $ brew remove portaudio
    $ brew install portaudio
    $ sudo easy_install pip
    $ brew cask install vlc
  
## 2. 필요한 파이썬 라이브러리 설치
    $ pip install -r requirements.txt

## 3. 클라이언트 키 정보 설정
발급받은 인사이드 디바이스 키 정보를 입력 

    $ vi agent.config
    
    [client]
    client_type: GINSIDE
    client_id: YOUR_CLIENT_ID
    client_key: YOUR_CLIENT_KEY
    client_secret: YOUR_CLIENT_SECRET

## 4. 실행 !!!
    $ python run_enter.py
    
   or
   
    $ python run_curses.py

    

## 5. 로그 확인
    $ tail -f run.log

# Tip

gRPC protocol python stub 소스(gigagenieM_pb2.py, gigagenieM_pb2_grpc.py)을 다시 만들고 싶다면?

    $ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/gigagenieM.proto


# License

sample-client-python is licensed under the [Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0)

Sample Client Python은 아래의 오픈소스 라이브러리를 사용합니다.
* gRPC : Apache License 2.0 (https://github.com/grpc/grpc/blob/master/LICENSE)
* protobuf : New BSD License (https://github.com/protocolbuffers/protobuf/blob/master/LICENSE)

