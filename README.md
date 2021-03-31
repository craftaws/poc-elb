# 프로젝트에 대해서
이 프로젝트는 AWS의 Application Load Balancer 의 여러가지 시나리오 테스트 수행을 위한 것으로, Python 언어로 작성된 CDK 프로젝트 입니다. CDK Pipeline을 구현하고 있어 쉬운 배포 및 지속적인 통합을 통해 추가적인 시나리오 테스트를 할 수 있습니다. ([AWS Developer Blog: CDK Pipelines](https://aws.amazon.com/ko/blogs/developer/cdk-pipelines-continuous-delivery-for-aws-cdk-applications/))

아래 나열된 주제들에 대한 시나리오를 실행해 볼 수 있습니다.
- [custom header 값이 있는 http request 가 ALB 를 통과 했을 때, 연결된 back-end 핸들러에서 custom header 값이 전달되는지](./docs/custom_header.md)

# 프로젝트 배포하기
1. CDK 실행 환경 구성 - aws cli 설치

    ``` bash
    # Installing aws cli: https://docs.aws.amazon.com/cli/  latest/userguide/install-cliv2-linux. html#cliv2-linux-install
    $ curl "https://awscli.amazonaws.com/   awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    $ unzip awscliv2.zip
    $ sudo ./aws/install

    $ sudo npm install -g npm && sudo npm install -g aws-cdk
    $ cdk --version
    ```

2. 파이선 가상 실행환경

    Python AWS CDK applications require Python 3.6 or later.
    To activate a virtualenv:
    ``` bash
    $ python -m venv .env
    $ source .env/bin/activate
    ```
    
    To install the required dependencies:
    ``` bash
    $ pip install --upgrade pip && pip install -r requirements.txt
    ```

3. 환경변수 생성
    secret manager 에 아래와 같은 환경변수가 입력되어 있어야 합니다.
    - stack_name
    - pipeline_name
    - github_owner
    - github_repo
    - github_branch
    - connection_arn

4. example command to execute cdk project

    ``` bash
    $ cdk -c secret_name=my_secret -c region=ap-northeast-2 synth
    $ cdk -c secret_name=my_secret -c region=ap-northeast-2 deploy
    ```