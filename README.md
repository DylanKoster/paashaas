<a name="readme-top"></a>

<div align="center">

[![Contributors](https://img.shields.io/badge/Contributors-4-green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/graphs/contributors)
[![Pull Requests](https://img.shields.io/badge/Pull%20Requests--green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/pulls)
[![Branches](https://img.shields.io/badge/Branches--green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/pulls)
[![Issues](https://img.shields.io/badge/Issues--green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/issues)
[![Insight](https://img.shields.io/badge/Insight--green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/pulse/monthly)

</div>
<br />
<div align="center">
    <div style="font-size: 75px; line-height: 1.2;">Paas-Haas</div>
    <div style="font-size: 20px;">Platform as a Service - Handling and Storage</div>
    <br/>
    <p align="center">
    <strong>Paas-Haas</strong> is a powerful Platform-as-a-Service solution designed to simplify inventory management deployment. With a streamlined configuration-based setup, users can automatically deploy their system to AWS with minimal effort. Leveraging AWS Lambda for a fully serverless architecture, along with DynamoDB and Simple Email Service, Paas-Haas offers a scalable, efficient, and hassle-free way to manage inventory systems in the cloud.
    </p>
    <br />
    <br />
    <a href="https://github.com/DylanKoster/paashaas"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/DylanKoster/paashaas/">View Demo</a>
    ·
    <a href="https://github.com/DylanKoster/paashaas/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/DylanKoster/paashaas/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#techstack">TechStack</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

## About The Project

In retail, efficient inventory management is critical to ensuring smooth operations and meeting customer demand. The PaaS-HaaS (Platform as a Service: Handling and Storage) system is a comprehensive back-end solution designed to support stores in managing and monitoring stock levels in real-time. By integrating an API and a robust database, PaaS-HaaS provides seamless tracking, and updating of inventory across multiple retail locations.

PaaS-HaaS simplifies the management of goods by automating the monitoring of stock levels, and offering actionable insights for better decision-making. PaaS-HaaS allows store managers and administrators to retrieve up-to-date information on product availability, and inventory status directly through a well-structured API.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How It Works

1. **Assignment Submission**: A student submits their assignment through the platform.
2. **AI Analysis**: The submission is processed by our LLM, which examines the code for potential improvements.
3. **Review Assignment**: The analyzed submission is then assigned to another student for review.
4. **Guided Review**: The reviewing student receives the LLM's suggestions, aiding them in providing constructive feedback.
5. **Feedback Delivery**: The review is sent back to the original student, helping them learn and improve their work based on peer and AI-assisted feedback.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Benefits

- **For Teachers**: Streamlined assignment management and enhanced student engagement.
- **For Students**: Improved learning outcomes through constructive peer feedback and AI-guided review processes.
- **Quality Feedback**: Higher quality and more insightful reviews lead to better learning experiences.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## TechStack

These are all the services that were used to for this project.

<div align="left">

[![AWS Lambda][Lambda]][Lambda-url]
[![DynamoDB][DynamoDB]][DynamoDB-url]
[![AWS SAM][SAM]][SAM-url]
[![SES][SES]][SES-url]


</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

This section provides instructions on settup up the whole platform on aws from you local device. By following these simple steps all the aws services will be setup automatically.

### Prerequisites

An version of python have to be isntalled on your device, preferabally python version 3.13 or newer. This can be donwloaded from [here](https://www.python.org/downloads/).
Apart from python AWS SAM should be installed on your device for running the automatic deployment. SAM can be donwloaded from [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/DylanKoster/paashaas.git
   ```
2. Navigate to the project directory
   ```sh
   cd paashaas
   ```
3. (Optional) Create a virtual enivornment to store the requirements. 
   ```sh
   python -m venv venv
   venv/Scripts/activate
   ```
4. Install all the requirements.
    ```
    pip install -r requirements.txt
    ```
5. Fill in all configurations in config/example_config.yaml.
6. Run the configuration file to build and deploy the platform to AWS.
    ```
    python paashaas.py config/example_config.yaml
    ```

And that's it! The PaaS-HaaS inventory managment system should now be up and running in AWS. Open the AWS console [here](https://aws.amazon.com/console/) to see if everything was setup correctly.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

We would like to express our gratitude to the following individuals and organizations for their support and contributions to this project:

- The [template](https://github.com/othneildrew/Best-README-Template) for this README
- We used the [OpenAI API](https://openai.com/index/openai-api/) to generate the feedback hints.
- Paul for his guidance and insightful feedback throughout the development process.
- The UVA for their valuable resources.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Lambda]: https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white
[Lambda-url]: https://aws.amazon.com/lambda/

[DynamoDB]: https://img.shields.io/badge/DynamoDB-4053D6?style=for-the-badge&logo=amazon-dynamodb&logoColor=white
[DynamoDB-url]: https://aws.amazon.com/dynamodb/

[SAM]: https://img.shields.io/badge/AWS%20SAM-1D72B8?style=for-the-badge&logo=amazonaws&logoColor=white
[SAM-url]: https://aws.amazon.com/serverless/sam/

[SES]: https://img.shields.io/badge/AWS%20SES-232F3E?style=for-the-badge&logo=amazonses&logoColor=white
[SES-url]: https://aws.amazon.com/ses/

