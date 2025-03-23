<a name="readme-top"></a>

<div align="center">

[![Contributors](https://img.shields.io/badge/Contributors-4-green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/graphs/contributors)
[![Pull Requests](https://img.shields.io/badge/Pull%20Requests--green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/pulls)
[![Branches](https://img.shields.io/badge/Branches--green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/branches)
[![Issues](https://img.shields.io/badge/Issues--green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/issues)
[![Insight](https://img.shields.io/badge/Insight--green.svg?style=for-the-badge)](https://github.com/DylanKoster/paashaas/pulse/monthly)

<pre>
 ______   ________   ________   ______             ___   ___   ________   ________   ______      
/_____/\ /_______/\ /_______/\ /_____/\           /__/\ /__/\ /_______/\ /_______/\ /_____/\     
\   _ \ \\    _  \ \\    _  \ \\  ___\/_   _______\  \ \\  \ \\    _  \ \\    _  \ \\  ___\/_    
 \ (_) \ \\  (_)  \ \\  (_)  \ \\ \/___/\ /______/\\  \/_\  \ \\  (_)  \ \\  (_)  \ \\ \/___/\   
  \  ___\/ \   __  \ \\   __  \ \\_____\ \\______\/ \   ___  \ \\   __  \ \\   __  \ \\_____\ \  
   \ \ \    \  \ \  \ \\  \ \  \ \ /____\ \          \  \ \\  \ \\  \ \  \ \\  \ \  \ \ /____\ \ 
    \_\/     \__\/\__\/ \__\/\__\/ \_____\/           \__\/ \__\/ \__\/\__\/ \__\/\__\/ \_____\/
</pre>

</div>
<div align="center">
    <h3>Platform as a Service - Handling and Storage</h3>
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

## Available endpoints

#### **Store Management**
- **GET `/stores/`**  
  Retrieve a list of all stores.
  
- **GET `/stores/{store_id}`**  
  Retrieve a specific store by its ID.
  
- **POST `/stores/`**  
  Create a new store.
  
- **PUT `/stores/{store_id}`**  
  Update an existing store's details by its ID.

#### **Item Management**
- **POST `/stores/{store_id}/items/`**  
  Create a new item for a specific store.
  
- **GET `/stores/{store_id}/items/`**  
  Retrieve all items in a specific store.

- **GET `/stores/{store_id}/items/{item_id}`**  
  Retrieve a specific item by its ID within a store.

- **PUT `/stores/{store_id}/items/{item_id}`**  
  Update the details of a specific item by its ID within a store.

#### **Order Management**
- **POST `/stores/{store_id}/orders/`**  
  Create a new order for a specific store.
  
- **GET `/stores/{store_id}/orders/`**  
  Retrieve all orders for a specific store.
  
- **GET `/stores/{store_id}/orders/{order_id}`**  
  Retrieve a specific order by its ID within a store.
  
- **PUT `/stores/{store_id}/orders/{order_id}`**  
  Update an existing order's details by its ID within a store.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How It Works

**1. Configure Your Project:**  
Start by filling out a simple configuration file to define your inventory management system.

**2. Automated Setup:**  
Once the configuration file is complete, the platform uses AWS SAM (Serverless Application Model) to automatically generate and set up all necessary services.

**3. One-Command Deployment:**  
With a single script, your entire application is build and deployed to AWS. There's no need to manage servers or handle complex infrastructure manually.

**4. Serverless Architecture:**  
Your application runs fully serverless using AWS Lambda. It leverages DynamoDB for data storage and Amazon SES (Simple Email Service) for notifications.

**5. Cloud-Native Scalability:**  
Everything lives in the cloud, so your system scales automatically. When it's time for an update, just run the deployment script again—your new version goes live instantly with zero downtime.

**6. Customize Anytime:**  
Need to change something? Simply edit the configuration file and adjust settings to fit your needs. No infrastructure rework required.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Benefits

**Fast & Effortless Deployment**  
Deploy your inventory management system to AWS with just a single script—no manual setup or server provisioning required.

**Fully Serverless**  
Built entirely on AWS Lambda, DynamoDB, and Amazon SES, the platform eliminates the need for managing or maintaining servers, reducing overhead and complexity.

**Cloud-Native Scalability**  
Thanks to its cloud-native architecture, the system automatically scales with your workload, whether you're handling ten items or ten thousand.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## TechStack

These are all the services that were used to for this project.

<div align="left">

[![AWS Lambda][Lambda]][Lambda-url]
[![DynamoDB][DynamoDB]][DynamoDB-url]
[![AWS SAM][SAM]][SAM-url]
[![SES][SES]][SES-url]
[![IAM][IAM]][IAM-url]

</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

This section provides instructions on settup up the whole platform on aws from you local device. By following these simple steps all the aws services will be setup automatically.

### Prerequisites

An version of python have to be installed on your device, preferabally python version 3.13 or newer. This can be donwloaded from [here](https://www.python.org/downloads/).
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
- Paul for his guidance and insightful feedback throughout the development process.
- The UVA for their valuable resources.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[Lambda]: https://img.shields.io/badge/AWS%20Lambda-FF9900?style=for-the-badge&logo=awslambda&logoColor=white
[Lambda-url]: https://aws.amazon.com/lambda/

[DynamoDB]: https://img.shields.io/badge/DynamoDB-4053D6?style=for-the-badge&logo=amazon-dynamodb&logoColor=white
[DynamoDB-url]: https://aws.amazon.com/dynamodb/

[SAM]: https://img.shields.io/badge/AWS%20SAM-1D72B8?style=for-the-badge&logo=amazonsam&logoColor=white
[SAM-url]: https://aws.amazon.com/serverless/sam/

[SES]: https://img.shields.io/badge/AWS%20SES-232F3E?style=for-the-badge&logo=amazonses&logoColor=white
[SES-url]: https://aws.amazon.com/ses/

[IAM]: https://img.shields.io/badge/AWS%20IAM-14a86b?style=for-the-badge&logo=amazoniam&logoColor=white
[IAM-url]: https://aws.amazon.com/iam/

