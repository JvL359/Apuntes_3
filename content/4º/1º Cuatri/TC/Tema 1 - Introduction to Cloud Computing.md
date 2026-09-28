---
estado: pendiente de revisión
---

### I. Introduction to Cloud Computing

#### 1. Definition and main characteristics

> **Cloud Computing** is a model that enables ubiquitous, convenient and on-demand network access to a shared pool of configurable computing resources. These resources include networks, servers, storage, applications and services, and can be provisioned or released rapidly with minimal management effort or interaction with the provider.

> Its defining characteristics are:

- A **pool of shared resources** accessible over a network.
- Ubiquitous access.
- On-demand, self-service consumption.
- Rapid elasticity.
- Measured service usage.

#### 2. Brief history

> The idea of computing as a utility can be traced to John McCarthy in the 1960s. Important later milestones include Salesforce in 1999, the launch of AWS S3 and EC2 in 2006, and Google Cloud and Microsoft Azure in 2009.

> The growth of cloud platforms was driven by large-scale e-commerce needs: operating reliable, scalable and cost-effective data centers for rapid growth led to common platforms, API-based services and the possibility of offering that infrastructure to other organizations. The launch of S3 and EC2 popularized the idea of the Internet as an operating system.

### II. Cloud Service and Deployment Models

#### 1. Main service models

> Service models distribute responsibility between the customer and the cloud provider. As we move from **IaaS** to **SaaS**, the provider manages a progressively larger part of the stack.

| Model | Provider delivers and manages | Customer responsibility |
| --- | --- | --- |
| **IaaS** | Compute resources such as virtual machines, storage and networking; facilities and hardware infrastructure. | Operating system, application server, application software, data and user management. |
| **PaaS** | Hardware and platform resources needed to develop and deploy applications, including the operating system and application server. | Application code, data and user management. |
| **SaaS** | The complete cloud-based application stack, including maintenance, updates and bug fixes. | Use of the application and user management. |

> **IaaS** removes the need to manage a physical data center, but the customer still configures and maintains operating systems and applications. **PaaS** provides the environment for developing, running and managing applications, while customers retain their code, data and applications. **SaaS** is ready to use, commonly through a web browser, without installing or maintaining the application locally.

#### 2. Other service models

> **CaaS** (*Container as a Service*) provides and manages the hardware and software resources required to develop and deploy applications using containers. The customer writes the code and manages data and applications, but not the underlying container infrastructure or platform.

> **FaaS** (*Function as a Service*), also called *serverless*, provides a platform for building applications as simple event-triggered functions without managing or scaling infrastructure directly.

#### 3. Deployment models

> Cloud deployments can be organized as **public**, **semi-private**, **private**, **hybrid**, **community** or **multi-cloud**. In a private cloud, the customer acts as its own cloud service provider. Hybrid deployments combine different environments, whereas multi-cloud uses services from more than one cloud provider.

#### 4. Benefits and challenges

| Benefits | Challenges |
| --- | --- |
| Agility and elasticity | Security and privacy |
| Scalability and increased reliability | Regulatory requirements and interoperability |
| Reduced in-house IT needs and access to multiple services | Organizational challenges |
| Cost considerations between CAPEX and OPEX | Performance |

### III. Technology Enablers

#### 1. Data centers

> A **data center** is a physical facility that hosts computer systems and their associated components to store, process, manage and distribute large volumes of data. It includes hardware, a physical location, support infrastructure and staff.

> Common types are enterprise, colocation, managed, cloud and edge data centers. A cloud data center requires physical security, power, climate control, network connectivity, fire-suppression systems and sound server organization.

#### 2. Virtualization

> **Virtualization** creates a virtual version of a technology resource, such as a server, storage device or network resource. It partitions physical computing resources into virtual machines (VMs), improving hardware utilization and enabling agile resource creation.

> Its practical advantages include more flexible management of hardware upgrades, incidents and VM relocation, together with a simpler and more homogeneous data-center infrastructure.

##### 2.1. Server virtualization and hypervisors

> Server virtualization is implemented by a **hypervisor**, software that creates and runs VMs. It treats CPU, memory and storage as a resource pool that can be reallocated between existing or new VMs, and schedules VM resources against the physical hardware.

> Each VM receives its allocated resources and runs a guest operating system and applications. When a guest OS issues a privileged instruction involving shared hardware, the hypervisor intercepts and performs the operation on its behalf. This provides strong VM isolation and encapsulation while keeping the guest software unaware of the underlying mediation.

| Hypervisor type | Location and implications |
| --- | --- |
| **Type 1** | Runs directly on physical hardware, with VMs above it. It can provide higher availability, security and performance. |
| **Type 2** | Runs on top of an existing operating system, does not control the underlying hardware directly and is less performant than Type 1. |

##### 2.2. Network virtualization and SDN

> **Network virtualization** supports VM networking through vNICs, vSwitches, overlays, routing, isolation and mobility. It provides each tenant with a private virtual network on shared infrastructure and makes network services such as firewalls, load balancers, VPNs and routers available in software through **NFV**.

> It enables networks to be provisioned in seconds, improves scalability, supports micro-segmentation and per-VM firewalls, and simplifies operations through logically centralized control. It can:

- Divide one physical network into independent logical networks for different tenants.
- Provide network-like functionality to an OS partition.
- Abstract hardware network resources into software services.
- Combine several physical networks into one logical, software-based network.

> **Software Defined Networks** (SDN) separate the control plane from the data plane. Combined with network virtualization, this decoupling enables automation and orchestration in cloud architectures.

##### 2.3. Storage virtualization

> **Storage virtualization** presents a logical view of physical storage resources to a host. It treats disks, optical media and other enterprise storage as one pool.

> It can use a network-based SAN approach with Fiber Channel or iSCSI for block-based virtualization, or NAS for file-based virtualization. Cloud platforms commonly offer block-, file- and object-based storage.

> **Software Defined Storage** separates the software that performs storage operations from the physical hardware. Typically it runs on x86 servers, turns them into storage devices, aggregates cost-effective resources and scales out across a server cluster.

#### 3. Containers and orchestration

> A **container** is an isolated runtime instance of an application, defined by its filesystem, configuration and metadata. A container image is a lightweight, standalone, immutable and executable software package containing the code, runtime, system tools, libraries and settings required by the application. The image becomes a container at runtime.

> Containers are a form of operating-system-level virtualization. A container runtime such as Docker, Podman, CRI-O or `containerd` pulls images from a registry, manages their lifecycle and runs the containers on the host.

> Containers provide isolation and encapsulation, but are lighter than VMs because they include only the software needed by the deployed application: they do not need virtual hardware or a separate OS kernel.

> La diferencia estructural es relevante: cada VM empaqueta la aplicación, sus binarios y librerías y un **guest OS** sobre el hypervisor; los contenedores empaquetan únicamente la aplicación y sus binarios/librerías sobre un container engine que comparte el host OS y la infraestructura.

> A **container orchestration platform** manages container lifecycles in large, dynamic environments. Kubernetes is an open-source, production-grade platform that automates:

- Container deployment and scale-out/scale-in.
- Communication with other containers and external systems.
- Load balancing and service discovery.
- Health monitoring and zero-downtime upgrades.
- Resource allocation and storage management.

> Without orchestration, large microservices architectures become difficult to manage.

### IV. Cloud Platforms

#### 1. Platforms and evaluation criteria

> Major public cloud platforms include AWS, Google Cloud, Microsoft Azure and Alibaba Cloud. Examples of private cloud platforms are VMware, OpenStack and OpenShift Virtualization.

> When comparing platforms, consider their APIs, IAM capabilities, availability zones, fault tolerance and failover, elasticity, migration support, monitoring, logging, tracing and the services provided.

### V. Automation, Orchestration and DevOps

#### 1. Automation and orchestration

> Cloud environments are complex, large, heterogeneous and constantly changing, so automation is essential both for providers and customers. It covers resource creation and deployment, workload monitoring and accounting, lifecycle management, scaling, monitoring and self-healing.

> Declarative, intent-based automation is preferred. **Orchestration** coordinates all subsystems required to deploy, upgrade, scale and operate a service.

#### 2. Infrastructure as Code and DevOps

> **Infrastructure as Code** (IaC) treats virtualized infrastructure like application software. It improves agility when setting up or cloning environments, keeps configurations consistent through version control and reduces manual effort.

> **DevOps** integrates application development and operations to improve agility, efficiency and quality. It requires automation across the entire workflow: development, testing, deployment and operation.

### VI. Cloud Security

#### 1. Cloud-specific risks

> Cloud computing introduces or increases risks because its overall architecture and management systems are complex. This expands the potential attack surface and raises the likelihood of exploitable configuration errors.

> Shared infrastructure also creates multi-tenant isolation risks: software or hardware defects and misconfigurations can disrupt isolation. In addition, management systems are Internet-facing and legal aspects must be considered.

#### 2. Security practices

> Cloud security requires general IT security practices together with measures suited to the selected service and deployment models:

- Use MFA for access control.
- Apply least privilege and separation of duties.
- Assign roles to groups rather than individual users.
- Encrypt data in transit and at rest.
- Encrypt network communications with HTTPS or IPsec, and use network isolation and IDS/IPS.
- Apply a Zero Trust security model.
- Maintain proper logging and monitoring.

### VII. Final Summary

> Cloud Computing provides on-demand access to shared, configurable resources with rapid provisioning and elastic consumption. IaaS, PaaS, SaaS, CaaS and FaaS differ primarily in how they distribute management responsibilities between provider and customer.

> Data centers, high-speed networking and virtualization enable cloud platforms. Hypervisors, virtual networking, storage virtualization, containers and orchestration abstract physical resources into manageable services. Automation, IaC and DevOps make this infrastructure repeatable and scalable, while security depends on appropriate model selection, strong isolation, least privilege, encryption and continuous monitoring.
