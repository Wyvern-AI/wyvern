<h1 align="center">Wyvern</h1>

<div align="center">

**Wyvern is a real-time machine learning platform for marketplaces**

[Homepage](https://www.wyvern.ai) | [Docs](https://docs.wyvern.ai) | [Join Us On Slack](https://join.slack.com/t/wyvernai/shared_invite/zt-22nu62m6f-duK46NyhIINsdjKJct1hqg)

</div>

<div align="center">
  <img src="/docs/wyvern_logo.jpg" width="180px" />
</div>

<div align="center">
  <a href="https://www.ycombinator.com/companies/wyvern-ai"><img src="https://badgen.net/badge/Y%20Combinator/S23/orange"/></a>
  <a href="https://join.slack.com/t/wyvernai/shared_invite/zt-22nu62m6f-duK46NyhIINsdjKJct1hqg"><img src="https://badgen.net/badge/join/slack/blue?icon=slack"/></a>
  <a href="https://github.com/Wyvern-AI/wyvern/blob/main/LICENSE"><img src="https://badgen.net/badge/License/Elv2/green?icon=github"/></a>
</div>

## What is Wyvern?

Wyvern is a real-time machine learning platform for marketplaces:

- **Search and Discovery**: Wyvern specializes in bringing use cases like **recommendations and rankings** in-house.
- **Empower the Data Team**: Wyvern is tailored for your data team to independently build and deploy production-grade machine learning pipelines for the e-commerce and marketplace industry, reducing the engineering involvement in the entire process.
- **Orchestration for ML Pipelines**: Wyvern is agnostic to the solutions your pick for your feature sotre, model serving solution, or data warehouse. It automates the process of retrieving data from the feature store and passing data to the model service, as well as logging all the events. It abstracts all the engineering work above away from data scientists, with the goal of enabling data scientists to own the full ML stack, so that they can just focus on defining the request/response schemas of the API, the model, the features the model depends on, the business logic after the model, and finally training the models with the feedback data generated by the ML pipeline.

More about why we built Wyvern can be found [here](https://docs.wyvern.ai/why).

### Wyvern Architecture

![Wyvern Architecture](/docs/wyvern_architecture.png)

Overall, Wyvern gives you a framework to quickly define your real-time ML pipeline. There are a couple of important components as you can see in the architecture:

1. **Retrieval**: Wyvern can connect to and retrieve objects from your search index.
2. **Feature Module**: Wyvern has the built-in support for [feast](https://feast.dev/), an open source feature store. It also supports connecting to the feature store that you would like to use. Moreover, Wyvern provides interfaces for you to define your [batch features](/batch_feature) and [real-time features](/realtime_feature) easily, with the support of feature grouping, feature sharing, features for composite entities and request based features.
3. **Model Module**: Wyvern provides [the model interface](/model_service#define-the-whole-model) that allows you to define your own model in place or call your model service. It provides an interface to define features that your model depends on easily.
4. **Business Logic**: Wyvern makes defining your business logic easy after the model inference. For example, if your want to promote a specific brand of tshirt and move it to the top of the ranking result for the "tshirt" query.
5. **Observability and Event Logging**: All the events in your ML application, including real-time feature, model, business logic, product impression, as well your own custom events, are being automatically logged by Wyvern and data can be piped to your data warehouse. Refer to [Logging Events](/logging_events) for more information.
6. **Training Dataset**: Wyvern provides the feature store serving solution (currently integrated only with feast) to serve all data of the historical batch features and the real-time features that are logged in your data warehouse.

As Wyvern is open sourced, we will bring in more integrations with different feature stores, model serving solutions, search index for retrieval, observability tools, as well as integrations with more data warehouses.

## Quickstart

### Install Wyvern

```
pip install wyvern-ai
```

### Create Wyvern Project

Once Wyvern is installed, run this command to initialize your Wyvern project:

```
wyvern init name_of_your_project
```

Now that the `wyvern init` has set up your initial repository, you should see the following file structure in the generated repository:

```
├── pipelines
│   ├── __init__.py
│   ├── main.py
│   ├── product_ranking
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── ranking_pipline.py
│   │   ├── realtime_features.py
│   │   ├── schemas.py
├── feature-store-python
│   ├── features
│   │   ├── feature_store.yaml
│   │   ├── features.py
│   │   ├── main.py
├── .env
└── .gitignore
```

The generated template code is an [ML pipeline](https://docs.wyvern.ai/ml_pipeline) example for ranking products.

### Run Wyvern Application

#### Pre-requisite

- Redis service

Wyvern uses redis as its index and online feature store. By default, Wyvern connects to the localhost:6379

Your can run this command to install and spin up redis locally

```
wyvern redis
```

#### Run Wyvern

Now cd into the repository that was generated and run:

```
wyvern run
```

Now your service runs on http://0.0.0.0:5001 and the default ranking API schema could be found at [http://0.0.0.0:5001/redoc](http://0.0.0.0:5001/redoc#operation/MyRankingPipeline_api_v1_ranking_post).

#### Make A Request

Assuming you have 24 products and you would like to rank them. Here's a curl request:

```
curl --location 'http://0.0.0.0:5001/api/v1/ranking' \
--header 'Content-Type: application/json' \
--data '{
    "request_id": "test_request_id",
    "query": {"query": "candle"},
    "candidates": [
        {"product_id": "p1"},
        {"product_id": "p2"},
        {"product_id": "p3"},
        {"product_id": "p4"},
        {"product_id": "p5"},
        {"product_id": "p6"},
        {"product_id": "p7"},
        {"product_id": "p8"},
        {"product_id": "p9"},
        {"product_id": "p10"},
        {"product_id": "p11"},
        {"product_id": "p12"},
        {"product_id": "p13"},
        {"product_id": "p14"},
        {"product_id": "p15"},
        {"product_id": "p16"},
        {"product_id": "p17"},
        {"product_id": "p18"},
        {"product_id": "p19"},
        {"product_id": "p20"},
        {"product_id": "p21"},
        {"product_id": "p22"},
        {"product_id": "p23"},
        {"product_id": "p24"}
    ],
    "user_page_size": 8,
    "user_page": 0,
    "candidate_page_size": 24,
    "candidate_page": 0
}'
```

The request sends 24 products to Wyvern. Wyvern ranks these products and returns the 8 products (in descending order) on the first page (`"user_page": 0`).

You should see a response with the products being ordered descendingly by their ranking score.

<details>
<summary>Click to see a response example</summary>

```
{
  "ranked_candidates": [
    {
      "candidate_id": "p9",
      "ranked_score": 43.13991415724884
    },
    {
      "candidate_id": "p18",
      "ranked_score": 42.314880208313376
    },
    {
      "candidate_id": "p17",
      "ranked_score": 41.62010469362527
    },
    {
      "candidate_id": "p3",
      "ranked_score": 40.48391586690772
    },
    {
      "candidate_id": "p19",
      "ranked_score": 39.82504624652922
    },
    {
      "candidate_id": "p24",
      "ranked_score": 39.10042317690844
    },
    {
      "candidate_id": "p11",
      "ranked_score": 38.670359237541945
    },
    {
      "candidate_id": "p21",
      "ranked_score": 37.27313489135458
    }
  ]
}
```

</details>

:tada:Congratulations on making your first Wyvern request!!!

To learn more about how this ML pipeline is built, check out [Wyvern ML Pipeline](https://docs.wyvern.ai/ml_pipeline)

To learn more about Wyvern in general, check out our [documentations](https://docs.wyvern.ai/)

## More Documentations

- [How Wyvern ML Pipeline Works](https://docs.wyvern.ai/ml_pipeline)
- [Wyvern Feature Engineering](https://docs.wyvern.ai/feature_engineering_overview)
