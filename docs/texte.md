Il y à plusieur endpoint classé  sur (Payments API
Get Channels
get
Get Networks
get
Get Rates
get
Get Account
get
Resolve Bank Account
post
Widget Quote
post
Get Crypto Channels
get
Sends
Submit Send Request
post
Accept Send Request
post
Deny Send Request
post
Fail Send Pending Liquidity
post
Lookup Send
get
Lookup Send by sequenceId
get
List Sends
get
Receives
Submit Receive Request
post
Accept Receive Request
post
Deny Receive Request
post
Cancel Receive
post
Refund Receive
post
Lookup Receive
get
Lookup Receive by sequenceId
get
List Receives
get
Fees
Get Fee Config
post
Webhooks
Create Webhook
post
Update Webhook
put
Remove Webhook
del
List Webhooks
get
Crypto Sends
Lookup Crypto Send by sequenceId
get
Submit Crypto Send Request
post
List Crypto Sends
get
Wallets as a Service
Vaults

Transactions

Fiat Wallets

RFQ
Check Eligibility
post
Execute Auto Convert
post
Create RFQ
post
Accept RFQ
post
Reject RFQ
post
Get RFQ by ID
get
List RFQs
get
Get Conversion By ID
get
List Conversions
get
Virtual Accounts
Get Onboarding Status
get
List Virtual Accounts
get
Get Virtual Account by ID
get
Simulate Deposit (Sandbox only)
post
Receive Accounts - Latin America
Create Receive Account
post
Get Receive Account
get
Powered by ) la page    : Get Channels

# Get Channels

Retrieve all supported payment ramps (Bank Transfer, Mobile Money, E-Wallets transfers)

This endpoint that enables the ability to see a list of all <Glossary>channels</Glossary> and their status as well as determine which countries and currencies are currently supported.

> 🚧 Always filter by status!
>
> Payment Channels in Africa do not have perfect uptime. Each channel has a status attached to enable dynamic availability. It is a recommended best practice to dynamic disable/filter out any channels with an "inactive" status.
>
> if you're using the channels endpoint for the widget integration, be sure to filter by `widgetStatus` field on the channels response.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/channels": {
      "get": {
        "summary": "Get Channels",
        "description": "Retrieve all supported payment ramps (Bank Transfer, Mobile Money, E-Wallets transfers)",
        "operationId": "get-channels",
        "parameters": [
          {
            "name": "country",
            "in": "query",
            "description": "Specific country (ISO 3166-2) to retrieve channels for.",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "[\n{\n \"id\": \"7844f392-1421-47df-8a90-cbf7096b0441\",\n \"max\": 5000000,\n \"currency\": \"NGN\",\n \"countryCurrency\": \"NGN\",\n \"status\": \"active\",\n \"widgetStatus\": \"active\",\n \"feeLocal\": 185.2,\n \"createdAt\": \"2022-08-09T11:41:25.696Z\",\n \"vendorId\": \"7844f392-1421-47df-8a90-cbf7096b0441\",\n \"country\": \"NG\",\n \"feeUSD\": 1.2,\n \"min\": 0,\n \"channelType\": \"bank\",\n \"rampType\": \"withdraw\",\n \"apiStatus\": \"active\",\n \"settlementType\": \"instant\",\n \"estimatedSettlementTime\": 60,\n \"updatedAt\": \"2022-08-09T11:41:25.696Z\",\n \"balancer\": {},\n \"widgetMin\":100,\n \"widgetMax\":10000,\n \"countryMin\":0,\n \"countryMax\":10000,\n}\n]"
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "id": "7844f392-1421-47df-8a90-cbf7096b0441",
                    "max": 5000000,
                    "currency": "NGN",
                    "countryCurrency": "NGN",
                    "status": "active",
                    "widgetStatus": "active",
                    "feeLocal": 2.3,
                    "vendorId": "7844f392-1421-47df-8a90-cbf7096b0441",
                    "createdAt": "2022-08-09T11:41:25.696Z",
                    "country": "NG",
                    "feeUSD": 0.5,
                    "min": 0,
                    "channelType": "bank",
                    "apiStatus": "active",
                    "rampType": "withdraw",
                    "settlementType": "instant",
                    "estimatedSettlementTime": 60,
                    "updatedAt": "2022-08-09T11:41:25.696Z",
                    "balancer": {}
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```Get Networks

# Get Networks

Retrieve all supported end financial interfaces (Banks, Mobile Money Networks, E-Wallets)

A network is a company, bank, or service that the end-user interfaces financially with. There can be multiple channels linked to a network.

An example is MTN Ghana (Mobile Money / TelCo network), Stanbic Bank Kenya (Traditional Bank Account), etc.

Get Networks endpoint will allow a selection of the Bank, Mobile Network, or end service that a user actually receives/sends money from.

Upon selection of Channel and Network our system will know exactly how to route the transaction so it can reach its destination.

> 🚧 Always filter by status!
>
> Networks in Africa do not have perfect uptime. Each network has a status attached to enable dynamic availability. It is a recommended best practice to dynamic disable/filter out any networks with an "inactive" status.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/networks": {
      "get": {
        "summary": "Get Networks",
        "description": "Retrieve all supported end financial interfaces (Banks, Mobile Money Networks, E-Wallets)",
        "operationId": "get-networks",
        "parameters": [
          {
            "name": "country",
            "in": "query",
            "description": "Specific country(ISO 3166-2) to retrieve networks for.",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "[\n{\n \"id\": \"b0804b93-5899-4ccf-b13b-7d93981f36fd\",\n \"code\": \"063\",\n \"updatedAt\": \"2022-12-18T23:54:55.380Z\",\n \"status\": \"active\",\n \"createdAt\": \"2022-12-18T23:54:55.380Z\",\n \"accountNumberType\": \"bank\",\n \"country\": \"NG\",\n \"name\": \"Diamond Bank\",\n \"channelIds\": [\"81018280-e320-4c81-db2f-6f6d6cy239d8\"],\n \"countryAccountNumberType\": \"NGBANK\"\n}\n]"
                  }
                },
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "id": {
                        "type": "string",
                        "example": "b0804b93-5899-4ccf-b13b-7d93981f36fd"
                      },
                      "code": {
                        "type": "string",
                        "example": "063"
                      },
                      "updatedAt": {
                        "type": "string",
                        "example": "2022-12-18T23:54:55.380Z"
                      },
                      "status": {
                        "type": "string",
                        "example": "active"
                      },
                      "createdAt": {
                        "type": "string",
                        "example": "2022-12-18T23:54:55.380Z"
                      },
                      "accountNumberType": {
                        "type": "string",
                        "example": "bank"
                      },
                      "country": {
                        "type": "string",
                        "example": "NG"
                      },
                      "name": {
                        "type": "string",
                        "example": "Diamond Bank"
                      },
                      "channelIds": {
                        "type": "array",
                        "items": {
                          "type": "string",
                          "example": "81018280-e320-4c81-db2f-6f6d6cy239d8"
                        }
                      },
                      "countryAccountNumberType": {
                        "type": "string",
                        "example": "NGBANK"
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "id": "b0804b93-5899-4ccf-b13b-7d93981f36fd",
                    "code": "063",
                    "updatedAt": "2022-12-18T23:54:55.380Z",
                    "status": "active",
                    "channelIds": [
                      "81018280-e320-4c81-db2f-6f6d6cy239d8"
                    ],
                    "createdAt": "2022-12-18T23:54:55.380Z",
                    "accountNumberType": "bank",
                    "country": "NG",
                    "name": "Diamond Bank",
                    "countryAccountNumberType": "NGBANK"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```Get Rates

# Get Rates

Retrieve rates for supported countries

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/rates": {
      "get": {
        "summary": "Get Rates",
        "description": "Retrieve rates for supported countries",
        "operationId": "get-rates",
        "parameters": [
          {
            "name": "currency",
            "in": "query",
            "description": "ISO 4217 Currency Code",
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"rates\": [\n        {\n            \"buy\": 13.23,\n            \"sell\": 10.83,\n            \"locale\": \"GH\",\n            \"rateId\": \"cedi\",\n            \"code\": \"GHS\",\n            \"updatedAt\": \"2023-12-05T11:35:44.140Z\"\n        },\n        {\n            \"buy\": 608.14,\n            \"sell\": 595.84,\n            \"locale\": \"CM\",\n            \"rateId\": \"franc\",\n            \"code\": \"XAF\",\n            \"updatedAt\": \"2023-12-05T11:35:47.455Z\"\n        },\n        {\n            \"buy\": 153.4,\n            \"sell\": 153.4,\n            \"locale\": \"KE\",\n            \"rateId\": \"kenyan-shilling\",\n            \"code\": \"KES\",\n            \"updatedAt\": \"2023-12-05T11:35:51.281Z\"\n        },\n        {\n            \"buy\": 608.5,\n            \"sell\": 521.2,\n            \"locale\": \"NG\",\n            \"rateId\": \"naira\",\n            \"code\": \"NGN\",\n            \"updatedAt\": \"2023-12-05T11:36:13.499Z\"\n        }\n    ]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "rates": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "buy": {
                            "type": "number",
                            "example": 13.23,
                            "default": 0
                          },
                          "sell": {
                            "type": "number",
                            "example": 10.83,
                            "default": 0
                          },
                          "locale": {
                            "type": "string",
                            "example": "GH"
                          },
                          "rateId": {
                            "type": "string",
                            "example": "cedi"
                          },
                          "code": {
                            "type": "string",
                            "example": "GHS"
                          },
                          "updatedAt": {
                            "type": "string",
                            "example": "2023-12-05T11:35:44.140Z"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "partnerId": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01",
                    "buy": 569.48,
                    "marginLock": "absolute",
                    "buyBase": 567.18,
                    "locale": "NG",
                    "rateId": "naira",
                    "createdAt": "2021-12-03T05:15:08.340Z",
                    "sell": 558.08,
                    "code": "NGN",
                    "sellMargin": -10,
                    "updatedAt": "2021-12-30T09:13:54.544Z",
                    "sellBase": 568.08,
                    "buyMargin": 2.3,
                    "id": "57ec1c37d9ca050fc56ae67a9378ca90c2e195ed"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```Get Account

# Get Account

Retrieve information about accounts, including available balance.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/account": {
      "get": {
        "summary": "Get Account",
        "description": "Retrieve information about accounts, including available balance.",
        "operationId": "get-account",
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"accounts\": [\n        {\n            \"available\": 237735.2,\n            \"currency\": \"USD\",\n            \"currencyType\": \"fiat\"\n        }\n    ]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "accounts": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "available": {
                            "type": "number",
                            "example": 237735.2,
                            "default": 0
                          },
                          "currency": {
                            "type": "string",
                            "example": "USD"
                          },
                          "currencyType": {
                            "type": "string",
                            "example": "fiat"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"code\": \"InternalServerError\",\n  \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "accounts": [
                      {
                        "available": 237735.2,
                        "currency": "USD",
                        "currencyType": "fiat"
                      }
                    ]
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```Resolve Bank Account

# Resolve Bank Account

Validate a bank account before sending.

> 📘 Only available in select countries
>
> Due to limitations and variation of technology across the continent, only a handful of countries will support this endpoint.
>
> **Currently only required for Nigeria**

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/details/bank": {
      "post": {
        "summary": "Resolve Bank Account",
        "description": "Validate a bank account before sending.",
        "operationId": "resolve-bank-account",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "accountNumber",
                  "networkId"
                ],
                "properties": {
                  "accountNumber": {
                    "type": "string",
                    "description": "Bank Account Number for Recipient"
                  },
                  "networkId": {
                    "type": "string",
                    "description": "Unique identifier of selected network."
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"accountNumber\": \"0123456789\",\n  \"accountName\": \"Emmanuel Doe\",\n  \"accountBank\": \"Access Bank\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "accountNumber": {
                      "type": "string",
                      "example": "0123456789"
                    },
                    "accountName": {
                      "type": "string",
                      "example": "Emmanuel Doe"
                    },
                    "accountBank": {
                      "type": "string",
                      "example": "Access Bank"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```Widget Quote

# Widget Quote

Gets a quote for a widget transaction

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/widget/quote": {
      "post": {
        "summary": "Widget Quote",
        "description": "Gets a quote for a widget transaction",
        "operationId": "widget-quote",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "currency": {
                    "type": "string",
                    "description": "Local currency user is buying tokens with"
                  },
                  "localAmount": {
                    "type": "integer",
                    "description": "Total amount of local currency user is wanting to buy of tokens. This should only be used for BUY transactionType",
                    "format": "int32"
                  },
                  "cryptoAmount": {
                    "type": "number",
                    "description": "Total amount of crypto currency user is wanting to sell of tokens. This should only be used for SELL transactionType",
                    "format": "float"
                  },
                  "coin": {
                    "type": "string",
                    "description": "The type of coin/token that the user is wanting to buy"
                  },
                  "network": {
                    "type": "string",
                    "description": "The network of the coin/token that the user is wanting to buy"
                  },
                  "channelId": {
                    "type": "string",
                    "description": "The channelId of the payment method that the user is wanting to use. This will be retrieved from the getChannels API"
                  },
                  "transactionType": {
                    "type": "string",
                    "description": "Type of the transaction wanting to be conducted by the user. This will be 'Buy' or 'Sell'"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"currency\": \"NGN\",\n    \"coin\": \"USDC\",\n    \"cryptoAmount\": 100,\n    \"network\": \"ERC20\",\n    \"channelId\": \"d01e48c1-8ada-408b-8bee-c62090cfb24a\",\n    \"transactionType\": \"Sell\",\n    \"fiatReceived\": 153430.08,\n    \"convertedAmount\": 159823,\n    \"rateLocal\": 1598.23,\n    \"serviceFeeLocal\": 1598.23,\n    \"serviceFeeUSD\": 1,\n    \"partnerFeeLocal\": 4794.69,\n    \"partnerFeeUSD\": 3,\n    \"paymentMethod\": \"p2p\",\n    \"settlement\": \"instant\",\n    \"updatedAt\": \"2024-12-09T11:46:23.325Z\",\n    \"expireAt\": \"2024-12-09T11:56:23.325Z\",\n    \"transactionLimitMin\": 10000,\n    \"transactionLimitMax\": 500000,\n    \"cryptoMaxLimit\": 312.85,\n    \"cryptoMinLimit\": 6.26\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "coin": {
                      "type": "string",
                      "example": "USDC"
                    },
                    "cryptoAmount": {
                      "type": "integer",
                      "example": 100,
                      "default": 0
                    },
                    "network": {
                      "type": "string",
                      "example": "ERC20"
                    },
                    "channelId": {
                      "type": "string",
                      "example": "d01e48c1-8ada-408b-8bee-c62090cfb24a"
                    },
                    "transactionType": {
                      "type": "string",
                      "example": "Sell"
                    },
                    "fiatReceived": {
                      "type": "number",
                      "example": 153430.08,
                      "default": 0
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 159823,
                      "default": 0
                    },
                    "rateLocal": {
                      "type": "number",
                      "example": 1598.23,
                      "default": 0
                    },
                    "serviceFeeLocal": {
                      "type": "number",
                      "example": 1598.23,
                      "default": 0
                    },
                    "serviceFeeUSD": {
                      "type": "integer",
                      "example": 1,
                      "default": 0
                    },
                    "partnerFeeLocal": {
                      "type": "number",
                      "example": 4794.69,
                      "default": 0
                    },
                    "partnerFeeUSD": {
                      "type": "integer",
                      "example": 3,
                      "default": 0
                    },
                    "paymentMethod": {
                      "type": "string",
                      "example": "p2p"
                    },
                    "settlement": {
                      "type": "string",
                      "example": "instant"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2024-12-09T11:46:23.325Z"
                    },
                    "expireAt": {
                      "type": "string",
                      "example": "2024-12-09T11:56:23.325Z"
                    },
                    "transactionLimitMin": {
                      "type": "integer",
                      "example": 10000,
                      "default": 0
                    },
                    "transactionLimitMax": {
                      "type": "integer",
                      "example": 500000,
                      "default": 0
                    },
                    "cryptoMaxLimit": {
                      "type": "number",
                      "example": 312.85,
                      "default": 0
                    },
                    "cryptoMinLimit": {
                      "type": "number",
                      "example": 6.26,
                      "default": 0
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```     Get Crypto Channels

# Get Crypto Channels

Retrieve supported widget crypto currencies. 

Each currency contains an array of supported networks and their status.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/channels/crypto": {
      "get": {
        "summary": "Get Crypto Channels",
        "description": "Retrieve supported widget crypto currencies. \n\nEach currency contains an array of supported networks and their status.",
        "operationId": "crypto-channels",
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"channels\": [\n        {\n            \"code\": \"USDC\",\n            \"resources\": [\n                {\n                    \"type\": \"file_url\",\n                    \"content\": \"https://f.hubspotusercontent30.net/hubfs/9304636/PDF/centre-whitepaper.pdf\",\n                    \"id\": \"WHITEPAPER\"\n                }\n            ],\n            \"zones\": [\n                \"stablecoins\"\n            ],\n            \"updatedAt\": \"2024-12-06T07:13:13.561Z\",\n            \"networks\": {\n                \"XLM\": {\n                    \"nativeAsset\": \"XLM\",\n                    \"chainCurrencyId\": \"USDC\",\n                    \"addressRegex\": \"^G[A-Z2-7]{55}$\",\n                    \"requiresMemo\": true,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n                    ],\n                    \"explorerUrl\": \"https://blockchair.com/stellar/transaction/__TX_HASH__\",\n                    \"name\": \"Stellar\",\n                    \"enabled\": true,\n                    \"network\": \"XLM\"\n                },\n                \"SOL\": {\n                    \"nativeAsset\": \"SOL\",\n                    \"chainCurrencyId\": \"USDC\",\n                    \"addressRegex\": \"^[1-9A-HJ-NP-Za-km-z]{32,44}$\",\n                    \"requiresMemo\": false,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n                    ],\n                    \"explorerUrl\": \"https://explorer.solana.com/tx/__TX_HASH__\",\n                    \"name\": \"Solana\",\n                    \"enabled\": true,\n                    \"network\": \"SOL\"\n                },\n                \"CELO\": {\n                    \"nativeAsset\": \"CELO\",\n                    \"chainCurrencyId\": \"USDC\",\n                    \"addressRegex\": \"^(0x)[0-9A-Fa-f]{40}$\",\n                    \"requiresMemo\": false,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n                    ],\n                    \"explorerUrl\": \"https://celoscan.io/tx/__TX_HASH__\",\n                    \"name\": \"Celo\",\n                    \"enabled\": true,\n                    \"network\": \"CELO\"\n                },\n                \"ERC20\": {\n                    \"nativeAsset\": \"ETH\",\n                    \"chainCurrencyId\": \"USDC\",\n                    \"addressRegex\": \"^(0x)[0-9A-Fa-f]{40}$\",\n                    \"requiresMemo\": false,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n                    ],\n                    \"explorerUrl\": \"https://etherscan.io/tx/__TX_HASH__\",\n                    \"name\": \"Ethereum\",\n                    \"enabled\": true,\n                    \"network\": \"ERC20\"\n                },\n                \"BASE\": {\n                    \"nativeAsset\": \"OP\",\n                    \"chainCurrencyId\": \"USDC\",\n                    \"addressRegex\": \"^(0x)[0-9A-Fa-f]{40}$\",\n                    \"requiresMemo\": false,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n                    ],\n                    \"explorerUrl\": \"https://basescan.org/tx/__TX_HASH__\",\n                    \"name\": \"Base\",\n                    \"enabled\": true,\n                    \"network\": \"BASE\"\n                }\n            },\n            \"createdAt\": \"2024-12-06T07:13:13.561Z\",\n            \"isUTXOBased\": false,\n            \"description\": \"USDC is a stablecoin, pegged 1:1 to the US$. Created by Circle & Coinbase, each USDC unit in circulation is backed by $1 held in reserve, consisting of a mix of cash and short-term U.S. Treasury bonds.<br /><br />Join the USDC ecosystem and enjoy the benefits of stability and peace of mind as you make digital transactions with confidence! 🛡️\",\n            \"id\": \"usd-coin\",\n            \"name\": \"USD Coin\",\n            \"defaultNetwork\": \"ERC20\",\n            \"enabled\": false,\n            \"buyMinLocal\": {\n                \"XAF\": 5000,\n                \"ZAR\": 100,\n                \"ZMW\": 200,\n                \"NGN\": 10000,\n                \"KES\": 1000,\n                \"TZS\": 2500,\n                \"RWF\": 10000,\n                \"MWK\": 2000,\n                \"UGX\": 15000,\n                \"BWP\": 150\n            },\n            \"buyMaxLocal\": {\n                \"XAF\": 500000,\n                \"ZAR\": 5000,\n                \"ZMW\": 10000,\n                \"NGN\": 500000,\n                \"KES\": 50000,\n                \"TZS\": 5000000,\n                \"RWF\": 500000,\n                \"MWK\": 1000000,\n                \"UGX\": 400000,\n                \"BWP\": 5000\n            },\n            \"sellMinLocal\": {\n                \"ZAR\": 100,\n                \"MWK\": 2000,\n                \"BWP\": 150,\n                \"XOF\": 5000,\n                \"UGX\": 15000,\n                \"ZMW\": 200,\n                \"XAF\": 5000,\n                \"KES\": 1000,\n                \"NGN\": 10000,\n                \"TZS\": 2500,\n                \"RWF\": 10000\n            },\n            \"sellMaxLocal\": {\n                \"ZAR\": 5000,\n                \"MWK\": 1000000,\n                \"BWP\": 5000,\n                \"XOF\": 200000,\n                \"UGX\": 400000,\n                \"ZMW\": 10000,\n                \"XAF\": 500000,\n                \"KES\": 50000,\n                \"NGN\": 500000,\n                \"TZS\": 5000000,\n                \"RWF\": 500000\n            }\n        },\n        {\n            \"code\": \"SOL\",\n            \"resources\": [\n                {\n                    \"type\": \"file_url\",\n                    \"content\": \"https://solana.com/solana-whitepaper.pdf\",\n                    \"id\": \"WHITEPAPER\"\n                }\n            ],\n            \"zones\": [],\n            \"updatedAt\": \"2024-12-06T07:13:13.562Z\",\n            \"networks\": {\n                \"SOL\": {\n                    \"nativeAsset\": \"SOL\",\n                    \"chainCurrencyId\": \"SOL\",\n                    \"addressRegex\": \"^[1-9A-HJ-NP-Za-km-z]{32,44}$\",\n                    \"requiresMemo\": false,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n                    ],\n                    \"explorerUrl\": \"https://explorer.solana.com/tx/__TX_HASH__\",\n                    \"name\": \"solana\",\n                    \"enabled\": true,\n                    \"network\": \"SOL\"\n                }\n            },\n            \"createdAt\": \"2024-12-06T07:13:13.562Z\",\n            \"isUTXOBased\": false,\n            \"description\": \"Solana is an open-source project leveraging blockchain's permissionless nature to deliver highly functional decentralised finance (DeFi) solutions.<br /><br />Launched in 2020 by the Solana Foundation in Geneva, Solana enables seamless, secure, and inclusive financial opportunities. SOL coin plays a pivotal role, facilitating transactions and fuelling the Solana ecosystem's growth. ☀️\",\n            \"id\": \"solana\",\n            \"name\": \"Solana\",\n            \"defaultNetwork\": \"SOL\",\n            \"enabled\": false,\n            \"buyMinLocal\": {\n                \"XAF\": 5000,\n                \"ZAR\": 100,\n                \"ZMW\": 200,\n                \"NGN\": 10000,\n                \"KES\": 1000,\n                \"TZS\": 2500,\n                \"RWF\": 10000,\n                \"MWK\": 2000,\n                \"UGX\": 15000,\n                \"BWP\": 150\n            },\n            \"buyMaxLocal\": {\n                \"XAF\": 500000,\n                \"ZAR\": 5000,\n                \"ZMW\": 10000,\n                \"NGN\": 500000,\n                \"KES\": 50000,\n                \"TZS\": 5000000,\n                \"RWF\": 500000,\n                \"MWK\": 1000000,\n                \"UGX\": 400000,\n                \"BWP\": 5000\n            },\n            \"sellMinLocal\": {\n                \"ZAR\": 100,\n                \"MWK\": 2000,\n                \"BWP\": 150,\n                \"XOF\": 5000,\n                \"UGX\": 15000,\n                \"ZMW\": 200,\n                \"XAF\": 5000,\n                \"KES\": 1000,\n                \"NGN\": 10000,\n                \"TZS\": 2500,\n                \"RWF\": 10000\n            },\n            \"sellMaxLocal\": {\n                \"ZAR\": 5000,\n                \"MWK\": 1000000,\n                \"BWP\": 5000,\n                \"XOF\": 200000,\n                \"UGX\": 400000,\n                \"ZMW\": 10000,\n                \"XAF\": 500000,\n                \"KES\": 50000,\n                \"NGN\": 500000,\n                \"TZS\": 5000000,\n                \"RWF\": 500000\n            }\n        },\n        {\n            \"code\": \"ETH\",\n            \"resources\": [\n                {\n                    \"type\": \"url\",\n                    \"content\": \"https://ethereum.org/en/whitepaper/\",\n                    \"id\": \"WHITEPAPER\"\n                }\n            ],\n            \"zones\": [\n                \"eth-ecosystem\"\n            ],\n            \"updatedAt\": \"2024-12-06T07:13:13.544Z\",\n            \"networks\": {\n                \"ERC20\": {\n                    \"nativeAsset\": \"ETH\",\n                    \"chainCurrencyId\": \"ETH\",\n                    \"addressRegex\": \"^(0x)[0-9A-Fa-f]{40}$\",\n                    \"requiresMemo\": false,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n                    ],\n                    \"explorerUrl\": \"https://etherscan.io/tx/__TX_HASH__\",\n                    \"name\": \"Ethereum\",\n                    \"enabled\": true,\n                    \"network\": \"ERC20\"\n                }\n            },\n            \"createdAt\": \"2024-12-06T07:13:13.544Z\",\n            \"isUTXOBased\": false,\n            \"description\": \"This groundbreaking, decentralised blockchain was introduced in 2015 alongside it’s native cryptocurrency, Ether (ETH).<br /><br />Ethereum enhanced the blockchain space by introducing smart contracts. These self-executing agreements enable developers to build decentralised applications (dApps) on its platform. Experience a world where trust is automated, transparent, and accessible. 🤝\",\n            \"id\": \"ethereum\",\n            \"name\": \"Ethereum\",\n            \"defaultNetwork\": \"ERC20\",\n            \"enabled\": false,\n            \"buyMinLocal\": {\n                \"XAF\": 5000,\n                \"ZAR\": 100,\n                \"ZMW\": 200,\n                \"NGN\": 10000,\n                \"KES\": 1000,\n                \"TZS\": 2500,\n                \"RWF\": 10000,\n                \"MWK\": 2000,\n                \"UGX\": 15000,\n                \"BWP\": 150\n            },\n            \"buyMaxLocal\": {\n                \"XAF\": 500000,\n                \"ZAR\": 5000,\n                \"ZMW\": 10000,\n                \"NGN\": 500000,\n                \"KES\": 50000,\n                \"TZS\": 5000000,\n                \"RWF\": 500000,\n                \"MWK\": 1000000,\n                \"UGX\": 400000,\n                \"BWP\": 5000\n            },\n            \"sellMinLocal\": {\n                \"ZAR\": 100,\n                \"MWK\": 2000,\n                \"BWP\": 150,\n                \"XOF\": 5000,\n                \"UGX\": 15000,\n                \"ZMW\": 200,\n                \"XAF\": 5000,\n                \"KES\": 1000,\n                \"NGN\": 10000,\n                \"TZS\": 2500,\n                \"RWF\": 10000\n            },\n            \"sellMaxLocal\": {\n                \"ZAR\": 5000,\n                \"MWK\": 1000000,\n                \"BWP\": 5000,\n                \"XOF\": 200000,\n                \"UGX\": 400000,\n                \"ZMW\": 10000,\n                \"XAF\": 500000,\n                \"KES\": 50000,\n                \"NGN\": 500000,\n                \"TZS\": 5000000,\n                \"RWF\": 500000\n            }\n        },\n        {\n            \"code\": \"USDT\",\n            \"resources\": [\n                {\n                    \"type\": \"url\",\n                    \"content\": \"https://tether.to/en/whitepaper/\",\n                    \"id\": \"WHITEPAPER\"\n                }\n            ],\n            \"zones\": [\n                \"stablecoins\"\n            ],\n            \"updatedAt\": \"2024-12-06T07:13:13.545Z\",\n            \"networks\": {\n                \"SOL\": {\n                    \"chainCurrencyId\": \"USDT\",\n                    \"nativeAsset\": \"SOL\",\n                    \"addressRegex\": \"^[1-9A-HJ-NP-Za-km-z]{32,44}$\",\n                    \"requiresMemo\": false,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n                    ],\n                    \"explorerUrl\": \"https://explorer.solana.com/tx/__TX_HASH__\",\n                    \"name\": \"Solana\",\n                    \"enabled\": true,\n                    \"network\": \"SOL\"\n                },\n                \"CELO\": {\n                    \"chainCurrencyId\": \"USDT\",\n                    \"nativeAsset\": \"CELO\",\n                    \"addressRegex\": \"^(0x)[0-9A-Fa-f]{40}$\",\n                    \"requiresMemo\": false,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n                    ],\n                    \"explorerUrl\": \"https://celoscan.io/tx/__TX_HASH__\",\n                    \"name\": \"Celo\",\n                    \"enabled\": true,\n                    \"network\": \"CELO\"\n                },\n                \"POLYGON\": {\n                    \"chainCurrencyId\": \"USDT\",\n                    \"nativeAsset\": \"MATIC\",\n                    \"addressRegex\": \"^(0x)[0-9A-Fa-f]{40}$\",\n                    \"requiresMemo\": false,\n                    \"activities\": [\n                        \"SEND\",\n                        \"RECEIVE\"\n      

[Message truncated - exceeded 50,000 character limit]





Sends :  Submit Send Request

# Submit Send Request

Submit a send request. This will lock in a rate and await approval.

<br />

> ⚠️ Updated Terminology
>
> Payments are now called Sends. These Send endpoints replace the legacy Payments endpoints. The functionality remains identical, only the terminology has changed. Legacy payment endpoints are deprecated but will continue to  work. We recommend migrating to these new `/send` endpoints for future compatibility.

> 📘 Amount in USD or local currency
>
> The `amount` field and the `localAmount` field are interchangeable in the request body. **Either one is required, but not both**. Specifying the USD `amount` will then calculate an amount in local currency based on the partner rates, while specifying a `localAmount` in the local currency will fix this amount for the user while calculating the USD amount from the rates. The `convertedAmount` in the response body indicates the amount in local currency that has either been fixed or calculated.

> 🚧 Ten Minute Expiry
>
> Send requests have ten minutes to be accepted or will automatically mark itself as expired.

> 📘 Force Accept
>
> Setting `forceAccept` field to `true` allows you to skip the accept send request and your send would start processing once you submit send request.

<br />

> 📘 Channel Note
>
> You can now use `channelType` as an alternative to specifying a channelId in your Submit Send API Request.
>
> When using `channelType` you're required to pass the `country` and `currency` in the send request
>
> When you provide a `channelType`, `country` and `currency`  the system will automatically select an appropriate active channel for your transaction.
>
> Available Channel Types:
>
> * momo
> * bank (P2P and EFT channel types should be passed in as bank)

<br />

<Recipe slug="submit-your-first-payment-request" title="Submit your first Send Request" />

<Recipe slug="recipe-title" title="Submit your first  Send Request in Latin America" />

# LATAM Send Fields

When sending send transactions to LATAM currencies, additional fields are required beyond the standard request body. This document outlines the currency-specific fields per currency.

***

## MXN — Mexico

No extra fields required. Ensure `destination.accountNumber` is a valid **18-digit CLABE** number.

***

## ARS — Argentina

| Field           | Location      | Required | Description                                      |
| --------------- | ------------- | -------- | ------------------------------------------------ |
| `accountNumber` | `destination` | Yes      | CVU or CBU — must be exactly **22 digits**       |
| `cuit`          | request root  | Yes      | Argentine tax ID — must be exactly **11 digits** |

***

## BRL — Brazil

| Field        | Location      | Required | Description                                                          |
| ------------ | ------------- | -------- | -------------------------------------------------------------------- |
| `pixKeyType` | `destination` | Yes      | Pix key type — one of: `CPF`, `CNPJ`, `EMAIL`, `PHONE`, `RANDOM_KEY` |

**Pix key format by type (`destination.accountNumber`):**

| `pixKeyType` | Expected format            |
| ------------ | -------------------------- |
| `CPF`        | 11 digits                  |
| `CNPJ`       | 14 digits                  |
| `EMAIL`      | Valid email address        |
| `PHONE`      | 10–11 digits               |
| `RANDOM_KEY` | UUID format (contains `-`) |

***

## COP — Colombia

| Field                  | Location     | Required | Description                                               |
| ---------------------- | ------------ | -------- | --------------------------------------------------------- |
| `identificationType`   | request root | Yes      | Document type code (see table below)                      |
| `identificationNumber` | request root | Yes      | Document number                                           |
| `accountType`          | request root | No       | Account type code — defaults to `ch` (savings) if omitted |

**`accountType` values:**

| Value | Description               |
| ----- | ------------------------- |
| `cc`  | Checking account          |
| `ch`  | Savings account (default) |
| `dp`  | Electronic deposit        |

**`identificationType` values:**

| Value | Description                 |
| ----- | --------------------------- |
| `cc`  | Citizenship ID              |
| `nit` | Tax ID                      |
| `ce`  | Foreigner ID                |
| `pa`  | Passport                    |
| `ppt` | Temporary Protection Permit |
| `ti`  | Identity Card               |
| `rc`  | Civil Registry              |
| `te`  | Foreigner Card              |
| `die` | Foreign ID Document         |
| `nd`  | No Document                 |

<Recipe slug="recipe-title" title="Submit your first Payment Request in Latin America" />

<br />

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/send": {
      "post": {
        "summary": "Submit Send Request",
        "description": "Submit a send request. This will lock in a rate and await approval.",
        "operationId": "submit-payment",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "sequenceId",
                  "reason",
                  "sender",
                  "destination",
                  "customerUID",
                  "customerType",
                  "forceAccept"
                ],
                "properties": {
                  "channelId": {
                    "type": "string",
                    "description": "The identifier of the specific channel to execute payment through"
                  },
                  "sequenceId": {
                    "type": "string",
                    "description": "Represents a unique id for the transaction from your end"
                  },
                  "amount": {
                    "type": "integer",
                    "description": "Amount in USD to transact",
                    "format": "int32"
                  },
                  "localAmount": {
                    "type": "integer",
                    "description": "The amount in local currency to transact",
                    "format": "int32"
                  },
                  "reason": {
                    "type": "string",
                    "description": "The reason for the withdrawal. See guide for supported payment reasons"
                  },
                  "sender": {
                    "type": "object",
                    "description": "Sender KYC details",
                    "properties": {
                      "name": {
                        "type": "string",
                        "description": "Sender's Full Name.   Required only if `customerType` is retail."
                      },
                      "country": {
                        "type": "string",
                        "description": "Sender's country in ISO 3166. Required only if `customerType` is retail."
                      },
                      "phone": {
                        "type": "string",
                        "description": "Sender's Phone Number in E.164 format."
                      },
                      "address": {
                        "type": "string",
                        "description": "Sender's Address. Required only if `customerType` is retail."
                      },
                      "dob": {
                        "type": "string",
                        "description": "Sender's DOB (mm/dd/yyyy). Required only if `customerType` is retail."
                      },
                      "email": {
                        "type": "string",
                        "description": "Sender's Email Address. Required only for certain channels that require sender email."
                      },
                      "idNumber": {
                        "type": "string",
                        "description": "Sender's national ID number. Required only if `customerType` is retail."
                      },
                      "idType": {
                        "type": "string",
                        "description": "Type of ID. Required only if `customerType` is retail."
                      },
                      "businessId": {
                        "type": "string",
                        "description": "Sender business id. Required only if `customerType` is institution."
                      },
                      "businessName": {
                        "type": "string",
                        "description": "Sender business id. Required only if `customerType` is institution."
                      },
                      "additionalIdType": {
                        "type": "string",
                        "description": "Sender's additional ID type. Required only if `customerType` is retail and sender country is Nigeria"
                      },
                      "additionalIdNumber": {
                        "type": "string",
                        "description": "Sender's additional ID number. Required only if `customerType` is retail and sender country is Nigeria"
                      }
                    }
                  },
                  "destination": {
                    "type": "object",
                    "description": "Destination and Recipient Details",
                    "required": [
                      "accountNumber",
                      "accountType",
                      "networkId",
                      "accountName"
                    ],
                    "properties": {
                      "accountNumber": {
                        "type": "string",
                        "description": "Destination account number"
                      },
                      "accountType": {
                        "type": "string",
                        "description": "Account type",
                        "enum": [
                          "bank",
                          "momo"
                        ]
                      },
                      "networkId": {
                        "type": "string",
                        "description": "Network ID"
                      },
                      "accountBank": {
                        "type": "string"
                      },
                      "networkName": {
                        "type": "string"
                      },
                      "country": {
                        "type": "string"
                      },
                      "accountName": {
                        "type": "string"
                      },
                      "phoneNumber": {
                        "type": "string"
                      },
                      "branch": {
                        "type": "string",
                        "description": "Bank Branch Name. This is in the code field in the network"
                      },
                      "branchCode": {
                        "type": "string",
                        "description": "Bank branch code. This is in the code field in the network"
                      }
                    }
                  },
                  "forceAccept": {
                    "type": "boolean",
                    "description": "Specify whether or not you want to skip the accept payment step",
                    "default": false,
                    "enum": [
                      true,
                      false
                    ]
                  },
                  "customerType": {
                    "type": "string",
                    "description": "Determines the type of validation that is performed on the sender. If value is `institution`, the sender request object will be validated to ensure it includes `businessName` and `businessId` parameter. If the value is `retail`, the sender request object will be validated to ensure it includes `name`, `phone`, `email`, `country`, `address`, `dob`, `idNumber` and `idType`.",
                    "default": "retail",
                    "enum": [
                      "retail",
                      "institution"
                    ]
                  },
                  "customerUID": {
                    "type": "string",
                    "description": "Unique identifier for the customer"
                  },
                  "channelType": {
                    "type": "string",
                    "enum": [
                      "momo",
                      "bank"
                    ]
                  },
                  "country": {
                    "type": "string",
                    "description": "Country ISO 3166 code e.g. NG, KE, CI. This field is only required when using `channelType`"
                  },
                  "currency": {
                    "type": "string",
                    "description": "Currency code e.g. NGN, KES, XAF, XOF. This field is only required when using `channelType`"
                  },
                  "directSettlement": {
                    "type": "boolean",
                    "default": "false"
                  },
                  "settlementInfo": {
                    "type": "object",
                    "properties": {
                      "cryptoCurrency": {
                        "type": "string",
                        "description": "USDT, USDC, CUSD, etc"
                      },
                      "cryptoNetwork": {
                        "type": "string",
                        "description": "SOL, ERC20, TRC20, etc"
                      },
                      "cryptoAmount": {
                        "type": "number",
                        "description": "Amount of crypto to send"
                      },
                      "refundAddress": {
                        "type": "string"
                      }
                    },
                    "description": "Only required when `directSettlement` is true"
                  }
                }
              },
              "examples": {
                "Request Example": {
                  "value": {
                    "id": "12",
                    "channelId": "12fghj20-a0oikjs2",
                    "sequenceId": "123",
                    "currency": "GHS",
                    "country": "GH",
                    "amount": 500,
                    "reason": "entertainment",
                    "convertedAmount": 20000,
                    "status": "created",
                    "rate": 14,
                    "sender": {
                      "name": "John Doe",
                      "country": "United States",
                      "phone": "+1293019990",
                      "address": "20019 Giantlane Or.",
                      "dob": "19/10/2002",
                      "email": "john.doe@yellowcard.io",
                      "idNumber": "12345",
                      "idType": "license"
                    },
                    "destination": {
                      "accountName": "Json Bourne",
                      "accountNumber": "1111111111",
                      "accountType": "bank",
                      "networkId": "28sh203-18272-1aks2-1233ma"
                    },
                    "createdAt": "2022-12-18T23:54:55.380Z",
                    "updatedAt": "2022-12-18T23:54:55.380Z",
                    "expiresAt": "2023-02-02T09:40:48.628Z"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": {
                      "id": "12",
                      "channelId": "12",
                      "sequenceId": "123",
                      "currency": "GHS",
                      "country": "GH",
                      "amount": 500,
                      "reason": "entertainment",
                      "forceAccept": true,
                      "directSettlement": false,
                      "convertedAmount": 20000,
                      "partnerId": "partner-id",
                      "requestSource": "api",
                      "attempt": 1,
                      "status": "created",
                      "rate": 14,
                      "fiatWallet": "USD",
                      "sender": {
                        "name": "Justin",
                        "country": "United States",
                        "phone": "+12514218828",
                        "address": "1404 Attwater Dr.",
                        "dob": "02/01/1997",
                        "email": "justin@yellowcard.io",
                        "idNumber": "12345",
                        "idType": "license"
                      },
                      "destination": {
                        "accountName": "Elom",
                        "accountNumber": "123",
                        "accountType": "bank",
                        "networkId": "012"
                      },
                      "createdAt": "2022-12-18T23:54:55.380Z",
                      "updatedAt": "2022-12-18T23:54:55.380Z",
                      "expiresAt": "2023-02-02T09:40:48.628Z"
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "example": "12"
                    },
                    "channelId": {
                      "type": "string",
                      "example": "12"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "123"
                    },
                    "currency": {
                      "type": "string",
                      "example": "GHS"
                    },
                    "country": {
                      "type": "string",
                      "example": "GH"
                    },
                    "amount": {
                      "type": "integer",
                      "example": 500,
                      "default": 0
                    },
                    "reason": {
                      "type": "string",
                      "example": "entertainment"
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 20000,
                      "default": 0
                    },
                    "status": {
                      "type": "string",
                      "example": "created"
                    },
                    "rate": {
                      "type": "integer",
                      "example": 14,
                      "default": 0
                    },
                    "sender": {
                      "type": "object",
                      "properties": {
                        "name": {
                          "type": "string",
                          "example": "Justin"
                        },
                        "country": {
                          "type": "string",
                          "example": "United States"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+12514218828"
                        },
                        "address": {
                          "type": "string",
                          "example": "1404 Attwater Dr."
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "email": {
                          "type": "string",
                          "example": "justin@yellowcard.io"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "12345"
                        },
                        "idType": {
                          "type": "string",
                          "example": "license"
                        }
                      }
                    },
                    "destination": {
                      "type": "object",
                      "properties": {
                        "accountName": {
                          "type": "string",
                          "example": "Elom"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "123"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        },
                        "networkId": {
                          "type": "string",
                          "example": "012"
                        }
                      }
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2022-12-18T23:54:55.380Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2022-12-18T23:54:55.380Z"
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-02-02T09:40:48.628Z"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```   Accept Send Request

# Accept Send Request

Accept a send request for execution.

<br />

> ⚠️ Updated Terminology
>
> Payments are now called Sends. These Send endpoints replace the legacy Payments endpoints. The functionality remains identical, only the terminology has changed. Legacy payment endpoints are deprecated but will continue to  work. We recommend migrating to these new `/send` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/send/{id}/accept": {
      "post": {
        "summary": "Accept Payment Request",
        "description": "Accept a payment request for execution.",
        "operationId": "accept-payment-request",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique Send Identifier",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"currency\": \"NGN\",\n    \"rate\": 679.91,\n    \"status\": \"process\",\n    \"createdAt\": \"2023-03-21T17:01:46.746Z\",\n    \"sequenceId\": \"64ajhfba-aHbv-4b96-v28d-5h8a19c2aa8c\",\n    \"country\": \"NG\",\n    \"reason\": \"other\",\n    \"sender\": {\n        \"country\": \"Nigeria\",\n        \"address\": \"12 John Street, Lagos\",\n        \"idType\": \"12\",\n        \"phone\": \"+12514218828\",\n        \"dob\": \"02/01/1997\",\n        \"name\": \"John Smith\",\n        \"idNumber\": \"12\",\n        \"email\": \"justin@yellowcard.io\"\n    },\n    \"convertedAmount\": 60000,\n    \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n    \"expiresAt\": \"2023-03-21T17:11:46.729Z\",\n    \"updatedAt\": \"2023-03-21T17:02:28.733Z\",\n    \"amount\": 88.25,\n    \"destination\": {\n        \"networkName\": \"Stanbic Ibtc Bank\",\n        \"networkId\": \"3d4d08c1-4811-4fee-9349-a302328e55c1\",\n        \"accountNumber\": \"0760349371\",\n        \"accountName\": \"Héloïse D'arban\",\n        \"accountType\": \"bank\"\n    },\n    \"id\": \"0d72f565-f617-534c-871d-c055ee28c544\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "rate": {
                      "type": "number",
                      "example": 679.91,
                      "default": 0
                    },
                    "status": {
                      "type": "string",
                      "example": "process"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2023-03-21T17:01:46.746Z"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "64ajhfba-aHbv-4b96-v28d-5h8a19c2aa8c"
                    },
                    "country": {
                      "type": "string",
                      "example": "NG"
                    },
                    "reason": {
                      "type": "string",
                      "example": "other"
                    },
                    "sender": {
                      "type": "object",
                      "properties": {
                        "country": {
                          "type": "string",
                          "example": "Nigeria"
                        },
                        "address": {
                          "type": "string",
                          "example": "12 John Street, Lagos"
                        },
                        "idType": {
                          "type": "string",
                          "example": "12"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+12514218828"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "name": {
                          "type": "string",
                          "example": "John Smith"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "12"
                        },
                        "email": {
                          "type": "string",
                          "example": "justin@yellowcard.io"
                        }
                      }
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 60000,
                      "default": 0
                    },
                    "channelId": {
                      "type": "string",
                      "example": "fe8f4989-3bf6-41ca-9621-ffe2bc127569"
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-03-21T17:11:46.729Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-03-21T17:02:28.733Z"
                    },
                    "amount": {
                      "type": "number",
                      "example": 88.25,
                      "default": 0
                    },
                    "destination": {
                      "type": "object",
                      "properties": {
                        "networkName": {
                          "type": "string",
                          "example": "Stanbic Ibtc Bank"
                        },
                        "networkId": {
                          "type": "string",
                          "example": "3d4d08c1-4811-4fee-9349-a302328e55c1"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "0760349371"
                        },
                        "accountName": {
                          "type": "string",
                          "example": "Héloïse D'arban"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        }
                      }
                    },
                    "id": {
                      "type": "string",
                      "example": "0d72f565-f617-534c-871d-c055ee28c544"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "deprecated": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "sender": {
                      "name": "j",
                      "country": "N",
                      "phone": "+12514218828",
                      "address": "12dsa",
                      "dob": "02/01/1997",
                      "email": "justin@yellowcard.io",
                      "idNumber": "12",
                      "idType": "12"
                    },
                    "destination": {
                      "accountName": "Héloïse D'arban",
                      "accountNumber": "0760349371",
                      "accountType": "bank",
                      "networkId": "5f1af11b-305f-4420-8fce-65ed2725a409"
                    },
                    "channelId": "fe8f4989-3bf6-41ca-9621-ffe2bc127569",
                    "sequenceId": "wseks28asdasd",
                    "amount": 50,
                    "currency": "NGN",
                    "country": "NG",
                    "reason": "other",
                    "partnerId": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01",
                    "id": "9ae480ef-71cc-4ba3-9eb8-6970a8d707aa",
                    "status": "created",
                    "convertedAmount": 20026,
                    "rate": 400.52,
                    "expiresAt": "2023-02-02T09:40:48.628Z",
                    "createdAt": "2023-02-02T09:30:48.629Z",
                    "updatedAt": "2023-02-02T09:30:48.629Z"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```   Deny Send Request

# Deny Send Request

Deny a send request.

<br />

> ⚠️ Updated Terminology
>
> Payments are now called Sends. These Send endpoints replace the legacy Payments endpoints. The functionality remains identical, only the terminology has changed. Legacy payment endpoints are deprecated but will continue to  work. We recommend migrating to these new `/send` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/send/{id}/deny": {
      "post": {
        "summary": "Deny Payment Request",
        "description": "Deny a payment request.",
        "operationId": "deny-payment-request",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique Send Identifier",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"currency\": \"NGN\",\n    \"rate\": 679.91,\n    \"status\": \"denied\",\n    \"createdAt\": \"2023-03-21T17:02:50.380Z\",\n    \"sequenceId\": \"6hajhfba-aHbv-4b96-v28d-5h8a19c2aa8c\",\n    \"country\": \"NG\",\n    \"reason\": \"other\",\n    \"sender\": {\n        \"country\": \"Nigeria\",\n        \"address\": \"12 John Street, Lagos\",\n        \"idType\": \"12\",\n        \"phone\": \"+12514218828\",\n        \"dob\": \"02/01/1997\",\n        \"name\": \"John Smith\",\n        \"idNumber\": \"12\",\n        \"email\": \"justin@yellowcard.io\"\n    },\n    \"convertedAmount\": 60000,\n    \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n    \"expiresAt\": \"2023-03-21T17:12:50.370Z\",\n    \"updatedAt\": \"2023-03-21T17:03:04.373Z\",\n    \"amount\": 88.25,\n    \"destination\": {\n        \"networkName\": \"Stanbic Ibtc Bank\",\n        \"networkId\": \"3d4d08c1-4811-4fee-9349-a302328e55c1\",\n        \"accountNumber\": \"0760349371\",\n        \"accountName\": \"Héloïse D'arban\",\n        \"accountType\": \"bank\"\n    },\n    \"id\": \"a2d094ec-5b45-56b1-83dd-5f83f91bebca\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "rate": {
                      "type": "number",
                      "example": 679.91,
                      "default": 0
                    },
                    "status": {
                      "type": "string",
                      "example": "denied"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2023-03-21T17:02:50.380Z"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "6hajhfba-aHbv-4b96-v28d-5h8a19c2aa8c"
                    },
                    "country": {
                      "type": "string",
                      "example": "NG"
                    },
                    "reason": {
                      "type": "string",
                      "example": "other"
                    },
                    "sender": {
                      "type": "object",
                      "properties": {
                        "country": {
                          "type": "string",
                          "example": "Nigeria"
                        },
                        "address": {
                          "type": "string",
                          "example": "12 John Street, Lagos"
                        },
                        "idType": {
                          "type": "string",
                          "example": "12"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+12514218828"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "name": {
                          "type": "string",
                          "example": "John Smith"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "12"
                        },
                        "email": {
                          "type": "string",
                          "example": "justin@yellowcard.io"
                        }
                      }
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 60000,
                      "default": 0
                    },
                    "channelId": {
                      "type": "string",
                      "example": "fe8f4989-3bf6-41ca-9621-ffe2bc127569"
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-03-21T17:12:50.370Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-03-21T17:03:04.373Z"
                    },
                    "amount": {
                      "type": "number",
                      "example": 88.25,
                      "default": 0
                    },
                    "destination": {
                      "type": "object",
                      "properties": {
                        "networkName": {
                          "type": "string",
                          "example": "Stanbic Ibtc Bank"
                        },
                        "networkId": {
                          "type": "string",
                          "example": "3d4d08c1-4811-4fee-9349-a302328e55c1"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "0760349371"
                        },
                        "accountName": {
                          "type": "string",
                          "example": "Héloïse D'arban"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        }
                      }
                    },
                    "id": {
                      "type": "string",
                      "example": "a2d094ec-5b45-56b1-83dd-5f83f91bebca"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "deprecated": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "sender": {
                      "name": "j",
                      "country": "N",
                      "phone": "+12514218828",
                      "address": "12dsa",
                      "dob": "02/01/1997",
                      "email": "justin@yellowcard.io",
                      "idNumber": "12",
                      "idType": "12"
                    },
                    "destination": {
                      "accountName": "Héloïse D'arban",
                      "accountNumber": "0760349371",
                      "accountType": "bank",
                      "networkId": "5f1af11b-305f-4420-8fce-65ed2725a409"
                    },
                    "channelId": "fe8f4989-3bf6-41ca-9621-ffe2bc127569",
                    "sequenceId": "wseks28asdasd",
                    "amount": 50,
                    "currency": "NGN",
                    "country": "NG",
                    "reason": "other",
                    "partnerId": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01",
                    "id": "9ae480ef-71cc-4ba3-9eb8-6970a8d707aa",
                    "status": "created",
                    "convertedAmount": 20026,
                    "rate": 400.52,
                    "expiresAt": "2023-02-02T09:40:48.628Z",
                    "createdAt": "2023-02-02T09:30:48.629Z",
                    "updatedAt": "2023-02-02T09:30:48.629Z"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```     Fail Send Pending Liquidity

#  Fail Send Pending Liquidity

Fail a send request that is stuck because of liquidity.

<br />

> ⚠️ Updated Terminology
>
> Payments are now called Sends. These Send endpoints replace the legacy Payments endpoints. The functionality remains identical, only the terminology has changed. Legacy payment endpoints are deprecated but will continue to  work. We recommend migrating to these new `/send` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/payments/{id}/fail-pending-liquidity": {
      "post": {
        "summary": " Fail Send Pending Liquidity",
        "description": "Fail a send request that is stuck because of liquidity.",
        "operationId": "deny-payment-request-1",
        "parameters": [
          {
            "in": "path",
            "name": "id",
            "schema": {
              "type": "string"
            },
            "required": true,
            "description": "Unique Send Identifier"
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n  \"currency\": \"NGN\",\n  \"status\": \"failed\",\n  \"sequenceId\": \"6hajhfba-aHbv-4b96-v28d-5h8a19c2aa8c\",\n  \"country\": \"NG\",\n  \"reason\": \"other\",\n  \"sender\": {\n    \"country\": \"Nigeria\",\n    \"address\": \"12 John Street, Lagos\",\n    \"idType\": \"12\",\n    \"phone\": \"+12514218828\",\n    \"dob\": \"02/01/1997\",\n    \"name\": \"John Smith\",\n    \"idNumber\": \"12\",\n    \"email\": \"justin@yellowcard.io\"\n  },\n  \"convertedAmount\": 60000,\n  \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n  \"expiresAt\": \"2023-03-21T17:12:50.370Z\",\n  \"updatedAt\": \"2023-03-21T17:03:04.373Z\",\n  \"amount\": 88.25,\n  \"destination\": {\n    \"networkName\": \"Stanbic Ibtc Bank\",\n    \"networkId\": \"3d4d08c1-4811-4fee-9349-a302328e55c1\",\n    \"accountNumber\": \"0760349371\",\n    \"accountName\": \"Héloïse D'arban\",\n    \"accountType\": \"bank\"\n  },\n  \"id\": \"a2d094ec-5b45-56b1-83dd-5f83f91bebca\",\n  \"partnerFeeAmountLocal\": 0,\n  \"partnerFeeAmountUSD\": 0,\n  \"tier0Active\": false,\n  \"fiatSettlement\" false\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "status": {
                      "type": "string",
                      "example": "denied"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "6hajhfba-aHbv-4b96-v28d-5h8a19c2aa8c"
                    },
                    "country": {
                      "type": "string",
                      "example": "NG"
                    },
                    "reason": {
                      "type": "string",
                      "example": "other"
                    },
                    "sender": {
                      "type": "object",
                      "properties": {
                        "country": {
                          "type": "string",
                          "example": "Nigeria"
                        },
                        "address": {
                          "type": "string",
                          "example": "12 John Street, Lagos"
                        },
                        "idType": {
                          "type": "string",
                          "example": "12"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+12514218828"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "name": {
                          "type": "string",
                          "example": "John Smith"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "12"
                        },
                        "email": {
                          "type": "string",
                          "example": "justin@yellowcard.io"
                        }
                      }
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 60000,
                      "default": 0
                    },
                    "channelId": {
                      "type": "string",
                      "example": "fe8f4989-3bf6-41ca-9621-ffe2bc127569"
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-03-21T17:12:50.370Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-03-21T17:03:04.373Z"
                    },
                    "amount": {
                      "type": "number",
                      "example": 88.25,
                      "default": 0
                    },
                    "destination": {
                      "type": "object",
                      "properties": {
                        "networkName": {
                          "type": "string",
                          "example": "Stanbic Ibtc Bank"
                        },
                        "networkId": {
                          "type": "string",
                          "example": "3d4d08c1-4811-4fee-9349-a302328e55c1"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "0760349371"
                        },
                        "accountName": {
                          "type": "string",
                          "example": "Héloïse D'arban"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        }
                      }
                    },
                    "id": {
                      "type": "string",
                      "example": "a2d094ec-5b45-56b1-83dd-5f83f91bebca"
                    },
                    "fiatWallet": {
                      "type": "boolean"
                    },
                    "fiatSettlement": {
                      "type": "boolean"
                    },
                    "tier0Active": {
                      "type": "boolean"
                    },
                    "partnerFeeAmountUSD": {
                      "type": "number"
                    },
                    "partnerFeeAmountLocal": {
                      "type": "number"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          }
        },
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "id": "a2d094ec-5b45-56b1-83dd-5f83f91bebca"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```    Lookup Send

# Lookup Send

Retrieve information about a specific send

<br />

> ⚠️ Updated Terminology
>
> Payments are now called Sends. These Send endpoints replace the legacy Payments endpoints. The functionality remains identical, only the terminology has changed. Legacy payment endpoints are deprecated but will continue to  work. We recommend migrating to these new `/send` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/send/{id}": {
      "get": {
        "summary": "Lookup Payment",
        "description": "Retrieve information about a specific payment",
        "operationId": "lookup-payment",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique Send Identifier",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"sender\": {\n    \"name\": \"james\",\n    \"country\": \"NG\",\n    \"phone\": \"+12514218828\",\n    \"address\": \"Home office, address1\",\n    \"dob\": \"02/01/1997\",\n    \"email\": \"justin@yellowcard.io\",\n    \"idNumber\": \"12910293821\",\n    \"idType\": \"passport\"\n  },\n  \"destination\": {\n    \"accountName\": \"Héloïse D'arban\",\n    \"accountNumber\": \"0760349371\",\n    \"accountType\": \"bank\",\n    \"networkId\": \"5f1af11b-305f-4420-8fce-65ed2725a409\"\n  },\n  \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n  \"sequenceId\": \"7707c304-4583-4077-9531-de3f7616659c\",\n  \"amount\": 50,\n  \"currency\": \"NGN\",\n  \"country\": \"NG\",\n  \"reason\": \"other\",\n  \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n  \"id\": \"9ae480ef-71cc-4ba3-9eb8-6970a8d707aa\",\n  \"status\": \"complete\",\n  \"sessionId\": \"0192102837711029102930\",\n  \"convertedAmount\": 20026,\n  \"rate\": 400.52,\n  \"expiresAt\": \"2023-02-02T09:40:48.628Z\",\n  \"createdAt\": \"2023-02-02T09:30:48.629Z\",\n  \"updatedAt\": \"2023-02-02T09:30:48.629Z\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "sender": {
                      "type": "object",
                      "properties": {
                        "name": {
                          "type": "string",
                          "example": "james"
                        },
                        "country": {
                          "type": "string",
                          "example": "NG"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+12514218828"
                        },
                        "address": {
                          "type": "string",
                          "example": "Home office, address1"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "email": {
                          "type": "string",
                          "example": "justin@yellowcard.io"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "12910293821"
                        },
                        "idType": {
                          "type": "string",
                          "example": "passport"
                        }
                      }
                    },
                    "destination": {
                      "type": "object",
                      "properties": {
                        "accountName": {
                          "type": "string",
                          "example": "Héloïse D'arban"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "0760349371"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        },
                        "networkId": {
                          "type": "string",
                          "example": "5f1af11b-305f-4420-8fce-65ed2725a409"
                        }
                      }
                    },
                    "channelId": {
                      "type": "string",
                      "example": "fe8f4989-3bf6-41ca-9621-ffe2bc127569"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "7707c304-4583-4077-9531-de3f7616659c"
                    },
                    "amount": {
                      "type": "integer",
                      "example": 50,
                      "default": 0
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "country": {
                      "type": "string",
                      "example": "NG"
                    },
                    "reason": {
                      "type": "string",
                      "example": "other"
                    },
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "id": {
                      "type": "string",
                      "example": "9ae480ef-71cc-4ba3-9eb8-6970a8d707aa"
                    },
                    "status": {
                      "type": "string",
                      "example": "complete"
                    },
                    "sessionId": {
                      "type": "string",
                      "example": "0192102837711029102930"
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 20026,
                      "default": 0
                    },
                    "rate": {
                      "type": "number",
                      "example": 400.52,
                      "default": 0
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-02-02T09:40:48.628Z"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2023-02-02T09:30:48.629Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-02-02T09:30:48.629Z"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "sender": {
                      "name": "j",
                      "country": "N",
                      "phone": "+12514218828",
                      "address": "12dsa",
                      "dob": "02/01/1997",
                      "email": "justin@yellowcard.io",
                      "idNumber": "12",
                      "idType": "12"
                    },
                    "destination": {
                      "accountName": "Héloïse D'arban",
                      "accountNumber": "0760349371",
                      "accountType": "bank",
                      "networkId": "5f1af11b-305f-4420-8fce-65ed2725a409"
                    },
                    "channelId": "fe8f4989-3bf6-41ca-9621-ffe2bc127569",
                    "sequenceId": "wseks28asdasd",
                    "amount": 50,
                    "currency": "NGN",
                    "country": "NG",
                    "reason": "other",
                    "partnerId": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01",
                    "id": "9ae480ef-71cc-4ba3-9eb8-6970a8d707aa",
                    "status": "created",
                    "convertedAmount": 20026,
                    "rate": 400.52,
                    "expiresAt": "2023-02-02T09:40:48.628Z",
                    "createdAt": "2023-02-02T09:30:48.629Z",
                    "updatedAt": "2023-02-02T09:30:48.629Z"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```   Lookup Send by sequenceId

# Lookup Send by sequenceId

Retrieve information about a specific send using its sequenceId property

<br />

> ⚠️ Updated Terminology
>
> Payments are now called Sends. These Send endpoints replace the legacy Payments endpoints. The functionality remains identical, only the terminology has changed. Legacy payment endpoints are deprecated but will continue to  work. We recommend migrating to these new `/send` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/payments/sequence-id/{id}": {
      "get": {
        "summary": "Lookup Payment by sequenceId",
        "description": "Retrieve information about a specific payment using its sequenceId property",
        "operationId": "lookup-payment-by-sequenceid",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique Payment sequenceId property",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n  \"sender\": {\n    \"name\": \"james\",\n    \"country\": \"NG\",\n    \"phone\": \"+12514218828\",\n    \"address\": \"Home office, address1\",\n    \"dob\": \"02/01/1997\",\n    \"email\": \"justin@yellowcard.io\",\n    \"idNumber\": \"12910293821\",\n    \"idType\": \"passport\"\n  },\n  \"destination\": {\n    \"accountName\": \"Héloïse D'arban\",\n    \"accountNumber\": \"0760349371\",\n    \"accountType\": \"bank\",\n    \"networkId\": \"5f1af11b-305f-4420-8fce-65ed2725a409\"\n  },\n  \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n  \"sequenceId\": \"7707c304-4583-4077-9531-de3f7616659c\",\n  \"amount\": 50,\n  \"currency\": \"NGN\",\n  \"country\": \"NG\",\n  \"reason\": \"other\",\n  \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n  \"id\": \"9ae480ef-71cc-4ba3-9eb8-6970a8d707aa\",\n  \"status\": \"complete\",\n  \"sessionId\": \"0192102837711029102930\",\n  \"convertedAmount\": 20026,\n  \"rate\": 400.52,\n  \"expiresAt\": \"2023-02-02T09:40:48.628Z\",\n  \"createdAt\": \"2023-02-02T09:30:48.629Z\",\n  \"updatedAt\": \"2023-02-02T09:30:48.629Z\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "sender": {
                      "type": "object",
                      "properties": {
                        "name": {
                          "type": "string",
                          "example": "james"
                        },
                        "country": {
                          "type": "string",
                          "example": "NG"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+12514218828"
                        },
                        "address": {
                          "type": "string",
                          "example": "Home office, address1"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "email": {
                          "type": "string",
                          "example": "justin@yellowcard.io"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "12910293821"
                        },
                        "idType": {
                          "type": "string",
                          "example": "passport"
                        }
                      }
                    },
                    "destination": {
                      "type": "object",
                      "properties": {
                        "accountName": {
                          "type": "string",
                          "example": "Héloïse D'arban"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "0760349371"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        },
                        "networkId": {
                          "type": "string",
                          "example": "5f1af11b-305f-4420-8fce-65ed2725a409"
                        }
                      }
                    },
                    "channelId": {
                      "type": "string",
                      "example": "fe8f4989-3bf6-41ca-9621-ffe2bc127569"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "7707c304-4583-4077-9531-de3f7616659c"
                    },
                    "amount": {
                      "type": "integer",
                      "example": 50,
                      "default": 0
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "country": {
                      "type": "string",
                      "example": "NG"
                    },
                    "reason": {
                      "type": "string",
                      "example": "other"
                    },
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "id": {
                      "type": "string",
                      "example": "9ae480ef-71cc-4ba3-9eb8-6970a8d707aa"
                    },
                    "status": {
                      "type": "string",
                      "example": "complete"
                    },
                    "sessionId": {
                      "type": "string",
                      "example": "0192102837711029102930"
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 20026,
                      "default": 0
                    },
                    "rate": {
                      "type": "number",
                      "example": 400.52,
                      "default": 0
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-02-02T09:40:48.628Z"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2023-02-02T09:30:48.629Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-02-02T09:30:48.629Z"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "sender": {
                      "name": "j",
                      "country": "N",
                      "phone": "+12514218828",
                      "address": "12dsa",
                      "dob": "02/01/1997",
                      "email": "justin@yellowcard.io",
                      "idNumber": "12",
                      "idType": "12"
                    },
                    "destination": {
                      "accountName": "Héloïse D'arban",
                      "accountNumber": "0760349371",
                      "accountType": "bank",
                      "networkId": "5f1af11b-305f-4420-8fce-65ed2725a409"
                    },
                    "channelId": "fe8f4989-3bf6-41ca-9621-ffe2bc127569",
                    "sequenceId": "wseks28asdasd",
                    "amount": 50,
                    "currency": "NGN",
                    "country": "NG",
                    "reason": "other",
                    "partnerId": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01",
                    "id": "9ae480ef-71cc-4ba3-9eb8-6970a8d707aa",
                    "status": "created",
                    "convertedAmount": 20026,
                    "rate": 400.52,
                    "expiresAt": "2023-02-02T09:40:48.628Z",
                    "createdAt": "2023-02-02T09:30:48.629Z",
                    "updatedAt": "2023-02-02T09:30:48.629Z"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```       List Sends

# List Sends

Get a list of send requests

<br />

> ⚠️ Updated Terminology
>
> Payments are now called Sends. These Send endpoints replace the legacy Payments endpoints. The functionality remains identical, only the terminology has changed. Legacy payment endpoints are deprecated but will continue to  work. We recommend migrating to these new `/send` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/sends": {
      "get": {
        "summary": "List Payments",
        "description": "Get a list of payment requests",
        "operationId": "list-payments",
        "parameters": [
          {
            "name": "endDate",
            "in": "query",
            "description": "a date string in ISO format (_2023-02-13T10:08:57.307Z_)",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "startDate",
            "in": "query",
            "description": "a date string in ISO format (_2023-02-13T10:08:57.307Z_)",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "startAt",
            "in": "query",
            "description": "a number indicating the where the pagination should start from",
            "schema": {
              "type": "integer",
              "format": "int32"
            }
          },
          {
            "name": "perPage",
            "in": "query",
            "description": "a number indicating the number of items per page",
            "schema": {
              "type": "integer",
              "format": "int32",
              "default": 100
            }
          },
          {
            "name": "rangeBy",
            "in": "query",
            "description": "a string indicating the field to which the start and end date are applied - either 'createdAt' or 'updatedAt'",
            "schema": {
              "type": "string",
              "default": "createdAt"
            }
          },
          {
            "name": "sortBy",
            "in": "query",
            "description": "a string indicating the field on which to sort by - either 'createdAt' or 'updatedAt'",
            "schema": {
              "type": "string",
              "default": "createdAt"
            }
          },
          {
            "name": "orderBy",
            "in": "query",
            "description": "a string indicating how to order the results - either 'asc' or 'desc'",
            "schema": {
              "type": "string",
              "default": "desc"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"payments\": [\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 488.25,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-15T13:01:08.386Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"country\": \"NG\",\n            \"convertedAmount\": 9765,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-15T13:11:08.386Z\",\n            \"updatedAt\": \"2023-02-15T13:11:11.662Z\",\n            \"amount\": 20,\n            \"id\": \"f39aa0a6-5006-5559-9424-dc72876f0561\"\n        },\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 487.85,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-16T15:13:17.808Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"country\": \"NG\",\n            \"convertedAmount\": 9757,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-16T15:23:17.808Z\",\n            \"updatedAt\": \"2023-02-16T15:24:12.982Z\",\n            \"amount\": 20,\n            \"id\": \"5073fa46-59aa-5b82-9349-b415e323cc8e\"\n        },\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 488.25,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-15T13:01:06.506Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"country\": \"NG\",\n            \"convertedAmount\": 9765,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-15T13:11:06.505Z\",\n            \"updatedAt\": \"2023-02-15T13:11:08.847Z\",\n            \"amount\": 20,\n            \"id\": \"843479b1-a0fc-5090-90de-f9787a04cad0\"\n        },\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 487.85,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-16T15:12:50.518Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"country\": \"NG\",\n            \"convertedAmount\": 9757,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-16T15:22:50.518Z\",\n            \"updatedAt\": \"2023-02-16T15:23:11.048Z\",\n            \"amount\": 20,\n            \"id\": \"19582e7e-f960-5c6f-8688-f1a4c2c36a5d\"\n        },\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 487.21,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-23T14:12:43.187Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"sequenceId\": \"test2-c1f913cc-156c-4e60-bd71-887bf4f52287\",\n            \"country\": \"NG\",\n            \"convertedAmount\": 9744.2,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-23T14:22:43.187Z\",\n            \"updatedAt\": \"2023-02-23T14:23:53.887Z\",\n            \"amount\": 20,\n            \"id\": \"f51c7b43-140d-51f0-ac5e-841ce3d95160\"\n        }\n      ]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "payments": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "partnerId": {
                            "type": "string",
                            "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                          },
                          "currency": {
                            "type": "string",
                            "example": "NGN"
                          },
                          "rate": {
                            "type": "number",
                            "example": 488.25,
                            "default": 0
                          },
                          "status": {
                            "type": "string",
                            "example": "expired"
                          },
                          "createdAt": {
                            "type": "string",
                            "example": "2023-02-15T13:01:08.386Z"
                          },
                          "source": {
                            "type": "object",
                            "properties": {
                              "accountNumber": {
                                "type": "string",
                                "example": "1111111111"
                              },
                              "networkId": {
                                "type": "string",
                                "example": "6df48502-1ebe-473f-be17-e2cae4dd67ee"
                              },
                              "accountType": {
                                "type": "string",
                                "example": "bank"
                              }
                            }
                          },
                          "country": {
                            "type": "string",
                            "example": "NG"
                          },
                          "convertedAmount": {
                            "type": "integer",
                            "example": 9765,
                            "default": 0
                          },
                          "recipient": {
                            "type": "object",
                            "properties": {
                              "country": {
                                "type": "string",
                                "example": "Nigeria"
                              },
                              "address": {
                                "type": "string",
                                "example": "Home Address"
                              },
                              "idType": {
                                "type": "string",
                                "example": "license"
                              },
                              "phone": {
                                "type": "string",
                                "example": "+2349092916898"
                              },
                              "dob": {
                                "type": "string",
                                "example": "02/01/1997"
                              },
                              "name": {
                                "type": "string",
                                "example": "John Doe"
                              },
                              "idNumber": {
                                "type": "string",
                                "example": "314159"
                              },
                              "email": {
                                "type": "string",
                                "example": "john.doe@yellowcard.io"
                              }
                            }
                          },
                          "channelId": {
                            "type": "string",
                            "example": "fe8f4989-3bf6-41ca-9621-ffe2bc127569"
                          },
                          "expiresAt": {
                            "type": "string",
                            "example": "2023-02-15T13:11:08.386Z"
                          },
                          "updatedAt": {
                            "type": "string",
                            "example": "2023-02-15T13:11:11.662Z"
                          },
                          "amount": {
                            "type": "integer",
                            "example": 20,
                            "default": 0
                          },
                          "id": {
                            "type": "string",
                            "example": "f39aa0a6-5006-5559-9424-dc72876f0561"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "text/plain": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InvalidInput\",\n    \"message\": \"invalid startDate passed in request\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InvalidInput"
                    },
                    "message": {
                      "type": "string",
                      "example": "invalid startDate passed in request"
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```         Receives  :Submit Receive Request

# Submit Receive Request

Submit a receive request. This will lock in a rate and await approval.

<br />

> ⚠️ Updated Terminology
>
> Collections are now called Receives. These `/receive` endpoints replace the legacy `/collections` endpoints. The functionality remains identical, only the terminology has changed. Legacy collections endpoints are deprecated but will continue to  work. We recommend migrating to these new `/receive` endpoints for future compatibility.

> 📘 Amount in USD or local currency
>
> The `amount` field and the `localAmount` field are interchangeable in the request body. **Either one is required, but not both.** Specifying the USD `amount` will then calculate an amount in local currency based on the partner rates, while specifying a `localAmount` in the local currency will fix this amount for the user while calculating the USD amount from the rates. The `convertedAmount` in the response body indicates the amount in local currency that has either been fixed or calculated.

> 🚧 Ten minutes expiry
>
> Receive requests have ten minutes to be accepted or will automatically mark itself as expired.

> 📘 Force Accept
>
> Setting `forceAccept` field to `true` allows you to skip the accept receive request and your collection would start processing once you submit collection request.
>
> **Note**:  You should expect the `bankInfo` object for bank channel type if `forceAccept` is `true`,  Also keep in mind force accept for bank channel type adds a bit more latency to your submit receive request.
>
> When the channel  selected requires a redirect for the receive to be made and the `forceAccept` value is set to `true`, then the `redirectUrl` field is required and the request will fail if it is not provided.
>
> **Note**: the `redirectUrl`has to be a valid url with the `http://` or `https://` scheme included.

> 📘 Channel Note
>
> You can now use `channelType` as an alternative to specifying a channelId in your Submit Receive API request.
>
> When using `channelType` you're required to pass the `country` and `currency` in the send request
>
> When you provide a `channelType`, `country` and `currency`  the system will automatically select an appropriate active channel for your transaction.
>
> Available Channel Types:
>
> * momo
> * bank (P2P and EFT channel types should be passed in as bank)

<Recipe slug="submit-your-first-collection-request" title="Submit your first receive request" />

<Recipe slug="submit-your-first-collection-request-in-latin-america" title="Submit your first Receive Request in Latin America" />

<br />

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/receive": {
      "post": {
        "summary": "Submit Receive Request",
        "description": "Submit a receive request. This will lock in a rate and await approval.",
        "operationId": "submit-collection-request",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "channelId",
                  "sequenceId",
                  "customerUID",
                  "customerType"
                ],
                "properties": {
                  "channelId": {
                    "type": "string",
                    "description": "The identifier of the specific channel to execute payment through"
                  },
                  "sequenceId": {
                    "type": "string",
                    "description": "Represents a unique id for the transaction from your end"
                  },
                  "amount": {
                    "type": "integer",
                    "description": "Amount in USD to transact",
                    "format": "int32"
                  },
                  "localAmount": {
                    "type": "integer",
                    "description": "The amount in local currency to transact",
                    "format": "int32"
                  },
                  "recipient": {
                    "properties": {
                      "name": {
                        "type": "string",
                        "description": "Recipient's full name.  Required only if `customerType` is retail."
                      },
                      "country": {
                        "type": "string",
                        "description": "Recipient's country in ISO 3166 format. Example, NG, CM, GH. https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes.   Required only if `customerType` is retail."
                      },
                      "address": {
                        "type": "string",
                        "description": "Recipient's address.   Required only if `customerType` is retail."
                      },
                      "dob": {
                        "type": "string",
                        "description": "Recipient's date of birth (mm/dd/yyyy).   Required only if `customerType` is retail."
                      },
                      "email": {
                        "type": "string",
                        "description": "Recipient's email address.   Required for both `customerType` is `retail` and `institution`."
                      },
                      "idNumber": {
                        "type": "string",
                        "description": "Recipient's ID number.   Required only if `customerType` is retail."
                      },
                      "idType": {
                        "type": "string",
                        "description": "Recipient's identity document type.   Required only if `customerType` is retail."
                      },
                      "additionalIdType": {
                        "type": "string",
                        "description": "Recipient's additional ID type.   Required only if `customerType` is retail and recipient country is NG"
                      },
                      "additionalIdNumber": {
                        "type": "string",
                        "description": "Recipient's additional ID number.   Required only if `customerType` is retail and recipient country is NG"
                      },
                      "phone": {
                        "type": "string",
                        "description": "Recipient's phone number.   Required only if `customerType` is retail."
                      },
                      "businessId": {
                        "type": "string",
                        "description": "Recipient's business id. Required only if `customerType` is institution."
                      },
                      "businessName": {
                        "type": "string",
                        "description": "Recipient's business name. Required only if `customerType` is institution."
                      }
                    },
                    "type": "object",
                    "description": "Recipient's KYC details"
                  },
                  "source": {
                    "properties": {
                      "accountType": {
                        "type": "string",
                        "description": "The type of account ('bank' or 'momo')"
                      },
                      "accountNumber": {
                        "type": "string",
                        "description": "For momo account type, Mobile money phone number of the Recipient. In the sandbox environment use 1111111111 simulate a success source and 0000000000 for a failure source for both \"momo\" and \"bank\". Please note that the account number is not required for bank receives in production"
                      },
                      "networkId": {
                        "type": "string",
                        "description": "The identifier of the specific network to execute payment through (not required for bank receives)"
                      }
                    },
                    "required": [
                      "accountType"
                    ],
                    "type": "object",
                    "description": "Source account details"
                  },
                  "forceAccept": {
                    "type": "boolean",
                    "description": "Specify whether or not you want to skip the accept collection step",
                    "default": false
                  },
                  "customerType": {
                    "type": "string",
                    "description": "Determines the type of validation that is performed on the recipient. If value is `institution`, the recipient request object will be validated to ensure it includes `businessName` and `businessId` parameter. If the value is `retail`, the recipient request object will be validated to ensure it includes `name`, `phone`, `email`, `country`, `address`, `dob`, `idNumber` and `idType`",
                    "default": "retail",
                    "enum": [
                      "retail",
                      "institution"
                    ]
                  },
                  "redirectUrl": {
                    "type": "string",
                    "description": "This is used to determine where the customer is redirected to after a transaction is initiated for channels that require redirect. This param is required if the selected channel requires redirect and forceAccept is set to true."
                  },
                  "customerUID": {
                    "type": "string",
                    "description": "Unique identifier for the customer"
                  },
                  "country": {
                    "type": "string",
                    "description": "Country ISO 3166 code e.g. NG, KE, CI. This field is only required when using `channelType`"
                  },
                  "currency": {
                    "type": "string",
                    "description": "Currency code e.g. NGN, KES, XAF, XOF. This field is only required when using `channelType`"
                  },
                  "channelType": {
                    "type": "string",
                    "enum": [
                      "bank",
                      "momo"
                    ]
                  },
                  "directSettlement": {
                    "type": "boolean",
                    "default": "false"
                  },
                  "settlementInfo": {
                    "type": "object",
                    "properties": {
                      "walletAddress": {
                        "type": "string",
                        "description": "Crypto payout destination wallet address"
                      },
                      "cryptoCurrency": {
                        "type": "string",
                        "description": "USDC, USDT, CUSD, etc."
                      },
                      "cryptoNetwork": {
                        "type": "string",
                        "description": "SOL, ERC20, TRC20"
                      },
                      "walletTag": {
                        "type": "string",
                        "description": "only required for USDC - XLM destination addresses"
                      }
                    },
                    "description": "Only required when `directSettlement` is true"
                  }
                }
              },
              "examples": {
                "Request Example": {
                  "value": {
                    "recipient": {
                      "name": "John Doe",
                      "country": "Nigeria",
                      "phone": "+2349092916898",
                      "address": "Home Address",
                      "dob": "02/01/1997",
                      "email": "john.doe@yellowcard.io",
                      "idNumber": "314159",
                      "idType": "license"
                    },
                    "source": {
                      "accountType": "bank",
                      "accountNumber": "1111111111",
                      "networkId": "6df48502-1ebe-473f-be17-e2cae4dd67ee"
                    },
                    "channelId": "fe8f4989-3bf6-41ca-9621-ffe2bc127569",
                    "sequenceId": "97f7c7f2-f7bb-450c-8f6d-1bd70766d26d",
                    "amount": 20,
                    "currency": "NGN",
                    "country": "Nigeria",
                    "reason": "other"
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": {
                      "recipient": {
                        "name": "John Doe",
                        "country": "Nigeria",
                        "phone": "+12514218828",
                        "address": "Home Address",
                        "dob": "02/01/1997",
                        "email": "john.doe@yellowcard.io",
                        "idNumber": "314159",
                        "idType": "license"
                      },
                      "source": {
                        "accountNumber": "0000000000",
                        "accountType": "momo",
                        "networkId": "995eb625-e23b-4d0b-bd90-18ce44cc17a3"
                      },
                      "channelId": "79da4d6e-1c42-4aac-ae7d-422730528f96",
                      "sequenceId": "93f7c7f9-f2bb-450c-8f6d-1bd70766d36d",
                      "amount": 1000,
                      "currency": "XAF",
                      "country": "CM",
                      "partnerId": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01",
                      "apiKey": "533fc4c3eaeb2a8f297a740ea178d830",
                      "id": "7a1f2622-29b0-4e23-bb7e-bfc9883b78fa",
                      "status": "created",
                      "convertedAmount": 569480,
                      "rate": 569.48,
                      "serviceFeeAmountLocal": 6000,
                      "serviceFeeAmountUSD": 5,
                      "partnerFeeAmountLocal": 3000,
                      "partnerFeeAmountUSD": 2,
                      "fiatWallet": "USD",
                      "requestSource": "api",
                      "directSettlement": false,
                      "expiresAt": "2023-02-02T13:50:06.298Z",
                      "createdAt": "2023-02-02T13:50:06.298Z",
                      "updatedAt": "2023-02-02T13:50:06.298Z"
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "recipient": {
                      "type": "object",
                      "properties": {
                        "name": {
                          "type": "string",
                          "example": "John Doe"
                        },
                        "country": {
                          "type": "string",
                          "example": "Nigeria"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+12514218828"
                        },
                        "address": {
                          "type": "string",
                          "example": "Home Address"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "email": {
                          "type": "string",
                          "example": "john.doe@yellowcard.io"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "314159"
                        },
                        "idType": {
                          "type": "string",
                          "example": "license"
                        }
                      }
                    },
                    "source": {
                      "type": "object",
                      "properties": {
                        "accountNumber": {
                          "type": "string",
                          "example": "0000000000"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "momo"
                        },
                        "networkId": {
                          "type": "string",
                          "example": "995eb625-e23b-4d0b-bd90-18ce44cc17a3"
                        }
                      }
                    },
                    "channelId": {
                      "type": "string",
                      "example": "79da4d6e-1c42-4aac-ae7d-422730528f96"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "93f7c7f9-f2bb-450c-8f6d-1bd70766d36d"
                    },
                    "amount": {
                      "type": "integer",
                      "example": 1000,
                      "default": 0
                    },
                    "currency": {
                      "type": "string",
                      "example": "XAF"
                    },
                    "country": {
                      "type": "string",
                      "example": "CM"
                    },
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "apiKey": {
                      "type": "string",
                      "example": "533fc4c3eaeb2a8f297a740ea178d830"
                    },
                    "id": {
                      "type": "string",
                      "example": "7a1f2622-29b0-4e23-bb7e-bfc9883b78fa"
                    },
                    "status": {
                      "type": "string",
                      "example": "created"
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 569480,
                      "default": 0
                    },
                    "rate": {
                      "type": "number",
                      "example": 569.48,
                      "default": 0
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-02-02T13:50:06.298Z"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2023-02-02T13:50:06.298Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-02-02T13:50:06.298Z"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n   \"code\": \"PaymentValidationError\",\n   \"message\": \"amount must be between 0 and 1000\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "PaymentValidationError"
                    },
                    "message": {
                      "type": "string",
                      "example": "amount must be between 0 and 1000"
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```   Accept Receive Request

# Accept Receive Request

Accept a receive request for execution.

<br />

> ⚠️ Updated Terminology
>
> Collections are now called Receives. These `/receive` endpoints replace the legacy `/collections` endpoints. The functionality remains identical, only the terminology has changed. Legacy collections endpoints are deprecated but will continue to  work. We recommend migrating to these new `/receive` endpoints for future compatibility.

> 📘 Channel Note
>
> When the channel id selected requires a redirect for the receive to be made then the `redirectUrl` field is required and the request will fail if it is not provided in the request to submit receive api. Currently only South African Receive channel requires a `redirectUrl`
>
> **Note**: the `redirectUrl`has to be a valid url with the `http://` or `https://` scheme included.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/receive/{id}/accept": {
      "post": {
        "summary": "Accept Collection Request",
        "description": "Accept a collection request for execution.",
        "operationId": "accept-collection-request",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique Receive Identifier",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"currency\": \"NGN\",\n    \"rate\": 487.89,\n    \"bankInfo\": {\n        \"name\": \"PAGA\",\n        \"accountNumber\": \"01234567890\",\n        \"accountName\": \"Ken Adams\"\n    },\n    \"status\": \"processing\",\n    \"createdAt\": \"2023-02-06T13:31:20.108Z\",\n    \"source\": {\n        \"accountNumber\": \"1111111111\",\n        \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n        \"accountType\": \"bank\"\n    },\n    \"sequenceId\": \"11f4c7f2-f7bb-450c-4s6d-1bd70766d26d\",\n    \"country\": \"NG\",\n    \"reference\": \"JJ8094861\",\n    \"convertedAmount\": 9757.8,\n    \"recipient\": {\n        \"country\": \"Nigeria\",\n        \"address\": \"Home Address\",\n        \"idType\": \"license\",\n        \"phone\": \"+2349092916898\",\n        \"dob\": \"02/01/1997\",\n        \"name\": \"John Doe\",\n        \"idNumber\": \"314159\",\n        \"email\": \"john.doe@yellowcard.io\"\n    },\n    \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n    \"expiresAt\": \"2023-02-06T13:41:20.108Z\",\n    \"updatedAt\": \"2023-02-06T13:31:48.802Z\",\n    \"amount\": 20,\n    \"id\": \"805b2317-0da9-42b9-89fb-e14e3fe12dd8\",\n    \"depositId\": \"47069e2d-b225-4155-9028-2607fe3346bb\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "rate": {
                      "type": "number",
                      "example": 487.89,
                      "default": 0
                    },
                    "bankInfo": {
                      "type": "object",
                      "properties": {
                        "name": {
                          "type": "string",
                          "example": "PAGA"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "01234567890"
                        },
                        "accountName": {
                          "type": "string",
                          "example": "Ken Adams"
                        }
                      }
                    },
                    "status": {
                      "type": "string",
                      "example": "processing"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2023-02-06T13:31:20.108Z"
                    },
                    "source": {
                      "type": "object",
                      "properties": {
                        "accountNumber": {
                          "type": "string",
                          "example": "1111111111"
                        },
                        "networkId": {
                          "type": "string",
                          "example": "6df48502-1ebe-473f-be17-e2cae4dd67ee"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        }
                      }
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "11f4c7f2-f7bb-450c-4s6d-1bd70766d26d"
                    },
                    "country": {
                      "type": "string",
                      "example": "NG"
                    },
                    "reference": {
                      "type": "string",
                      "example": "JJ8094861"
                    },
                    "convertedAmount": {
                      "type": "number",
                      "example": 9757.8,
                      "default": 0
                    },
                    "recipient": {
                      "type": "object",
                      "properties": {
                        "country": {
                          "type": "string",
                          "example": "Nigeria"
                        },
                        "address": {
                          "type": "string",
                          "example": "Home Address"
                        },
                        "idType": {
                          "type": "string",
                          "example": "license"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+2349092916898"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "name": {
                          "type": "string",
                          "example": "John Doe"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "314159"
                        },
                        "email": {
                          "type": "string",
                          "example": "john.doe@yellowcard.io"
                        }
                      }
                    },
                    "channelId": {
                      "type": "string",
                      "example": "fe8f4989-3bf6-41ca-9621-ffe2bc127569"
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-02-06T13:41:20.108Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-02-06T13:31:48.802Z"
                    },
                    "amount": {
                      "type": "integer",
                      "example": 20,
                      "default": 0
                    },
                    "id": {
                      "type": "string",
                      "example": "805b2317-0da9-42b9-89fb-e14e3fe12dd8"
                    },
                    "depositId": {
                      "type": "string",
                      "example": "47069e2d-b225-4155-9028-2607fe3346bb"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"PaymentExpired\",\n    \"message\": \"Collection request expired\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "PaymentExpired"
                    },
                    "message": {
                      "type": "string",
                      "example": "Collection request expired"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "404",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"CollectionNotFoundError\",\n    \"message\": \"\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "CollectionNotFoundError"
                    },
                    "message": {
                      "type": "string",
                      "example": ""
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false,
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {},
              "examples": {
                "Request Example": {
                  "value": {
                    "partnerId": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01",
                    "currency": "NGN",
                    "rate": 487.89,
                    "bankInfo": {
                      "name": "PAGA",
                      "accountNumber": "01234567890",
                      "accountName": "Ken Adams"
                    },
                    "status": "processing",
                    "createdAt": "2023-02-06T13:31:20.108Z",
                    "source": {
                      "accountNumber": "1111111111",
                      "networkId": "6df48502-1ebe-473f-be17-e2cae4dd67ee",
                      "accountType": "bank"
                    },
                    "sequenceId": "11f4c7f2-f7bb-450c-4s6d-1bd70766d26d",
                    "country": "NG",
                    "reference": "JJ8094861",
                    "convertedAmount": 9757.8,
                    "recipient": {
                      "country": "Nigeria",
                      "address": "Home Address",
                      "idType": "license",
                      "phone": "+2349092916898",
                      "dob": "02/01/1997",
                      "name": "John Doe",
                      "idNumber": "314159",
                      "email": "john.doe@yellowcard.io"
                    },
                    "channelId": "fe8f4989-3bf6-41ca-9621-ffe2bc127569",
                    "expiresAt": "2023-02-06T13:41:20.108Z",
                    "updatedAt": "2023-02-06T13:31:48.802Z",
                    "amount": 20,
                    "id": "805b2317-0da9-42b9-89fb-e14e3fe12dd8",
                    "depositId": "47069e2d-b225-4155-9028-2607fe3346bb"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```     Deny Receive Request

# Deny Receive Request

Deny a receive request.

<br />

> ⚠️ Updated Terminology
>
> Collections are now called Receives. These `/receive` endpoints replace the legacy `/collections` endpoints. The functionality remains identical, only the terminology has changed. Legacy collections endpoints are deprecated but will continue to  work. We recommend migrating to these new `/receive` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/receive/{id}/deny": {
      "post": {
        "summary": "Deny Collection Request",
        "description": "Deny a collection request.",
        "operationId": "deny-collection-request",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique Receive Identifier",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"currency\": \"NGN\",\n    \"rate\": 767.21,\n    \"status\": \"denied\",\n    \"createdAt\": \"2023-03-21T17:03:18.336Z\",\n    \"source\": {\n        \"accountNumber\": \"1111111111\",\n        \"networkId\": \"3d4d08c1-4811-4fee-9349-a302328e55c1\",\n        \"accountType\": \"bank\"\n    },\n    \"sequenceId\": \"3hfgk3c5-hhvb-76gc-462d-1bd707h6d46d\",\n    \"country\": \"NG\",\n    \"convertedAmount\": 60000,\n    \"recipient\": {\n        \"country\": \"Nigeria\",\n        \"address\": \"Home Address\",\n        \"idType\": \"license\",\n        \"phone\": \"+2349092916898\",\n        \"dob\": \"02/01/1997\",\n        \"name\": \"John Doe\",\n        \"idNumber\": \"314159\",\n        \"email\": \"john.doe@yellowcard.io\"\n    },\n    \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n    \"expiresAt\": \"2023-03-21T17:13:18.330Z\",\n    \"updatedAt\": \"2023-03-21T17:03:33.499Z\",\n    \"amount\": 78.21,\n    \"refundRetry\": 0,\n    \"id\": \"d55bd8b2-c530-5afa-8c44-2b61a159fed0\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "rate": {
                      "type": "number",
                      "example": 767.21,
                      "default": 0
                    },
                    "status": {
                      "type": "string",
                      "example": "denied"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2023-03-21T17:03:18.336Z"
                    },
                    "source": {
                      "type": "object",
                      "properties": {
                        "accountNumber": {
                          "type": "string",
                          "example": "1111111111"
                        },
                        "networkId": {
                          "type": "string",
                          "example": "3d4d08c1-4811-4fee-9349-a302328e55c1"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        }
                      }
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "3hfgk3c5-hhvb-76gc-462d-1bd707h6d46d"
                    },
                    "country": {
                      "type": "string",
                      "example": "NG"
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 60000,
                      "default": 0
                    },
                    "recipient": {
                      "type": "object",
                      "properties": {
                        "country": {
                          "type": "string",
                          "example": "Nigeria"
                        },
                        "address": {
                          "type": "string",
                          "example": "Home Address"
                        },
                        "idType": {
                          "type": "string",
                          "example": "license"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+2349092916898"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "name": {
                          "type": "string",
                          "example": "John Doe"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "314159"
                        },
                        "email": {
                          "type": "string",
                          "example": "john.doe@yellowcard.io"
                        }
                      }
                    },
                    "channelId": {
                      "type": "string",
                      "example": "fe8f4989-3bf6-41ca-9621-ffe2bc127569"
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-03-21T17:13:18.330Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-03-21T17:03:33.499Z"
                    },
                    "amount": {
                      "type": "number",
                      "example": 78.21,
                      "default": 0
                    },
                    "refundRetry": {
                      "type": "integer",
                      "example": 0,
                      "default": 0
                    },
                    "id": {
                      "type": "string",
                      "example": "d55bd8b2-c530-5afa-8c44-2b61a159fed0"
                    }
                  }
                }
              }
            }
          },
          "404": {
            "description": "404",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"CollectionNotFoundError\",\n    \"message\": \"\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "CollectionNotFoundError"
                    },
                    "message": {
                      "type": "string",
                      "example": ""
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```    Cancel Receive

# Cancel Receive

Cancel receive request while it's pending or processing.

<br />

> ⚠️ Updated Terminology
>
> Collections are now called Receives. These `/receive` endpoints replace the legacy `/collections` endpoints. The functionality remains identical, only the terminology has changed. Legacy collections endpoints are deprecated but will continue to  work. We recommend migrating to these new `/receive` endpoints for future compatibility.

> 🚧 Cancellation status
>
> You can only cancel a receive when it's in `pending` or `processing` state.  If we receive the collection after it's cancelled a refund is triggered for the receive.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/receive/{id}/cancel": {
      "post": {
        "summary": "Cancel Collection",
        "description": "Cancel collection request while it's pending or processing.",
        "operationId": "cancel-collection",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique receive identifier",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"currency\": \"NGN\",\n    \"rate\": 486.3,\n    \"bankInfo\": {\n        \"name\": \"PAGA\",\n        \"accountNumber\": \"01234567890\",\n        \"accountName\": \"Ken Adams\"\n    },\n    \"status\": \"cancelled\",\n    \"createdAt\": \"2023-02-24T23:36:28.692Z\",\n    \"source\": {\n        \"accountNumber\": \"5678987667\",\n        \"accountType\": \"bank\"\n    },\n    \"sequenceId\": \"53f7c7f9-f2bb-450c-8f6d-1vd707s66d30c\",\n    \"country\": \"NG\",\n    \"reference\": \"JJ0487919\",\n    \"convertedAmount\": 4863,\n    \"recipient\": {\n        \"country\": \"Nigeria\",\n        \"address\": \"Home Address\",\n        \"idType\": \"license\",\n        \"phone\": \"+2349092916898\",\n        \"dob\": \"02/01/1997\",\n        \"name\": \"John Doe\",\n        \"idNumber\": \"314159\",\n        \"email\": \"john.doe@yellowcard.io\"\n    },\n    \"channelId\": \"af944f0c-ba70-47c7-86dc-1bad5a6ab4e4\",\n    \"expiresAt\": \"2023-02-24T23:46:28.691Z\",\n    \"updatedAt\": \"2023-02-24T23:39:46.013Z\",\n    \"amount\": 10,\n    \"refundRetry\": 0,\n    \"id\": \"58cadfdc-8264-59eb-90c6-cd9e969305aa\",\n    \"depositId\": \"19b2dad8-2fd1-4b5a-b621-bb37cd9e755b\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "rate": {
                      "type": "number",
                      "example": 486.3,
                      "default": 0
                    },
                    "bankInfo": {
                      "type": "object",
                      "properties": {
                        "name": {
                          "type": "string",
                          "example": "PAGA"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "01234567890"
                        },
                        "accountName": {
                          "type": "string",
                          "example": "Ken Adams"
                        }
                      }
                    },
                    "status": {
                      "type": "string",
                      "example": "cancelled"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2023-02-24T23:36:28.692Z"
                    },
                    "source": {
                      "type": "object",
                      "properties": {
                        "accountNumber": {
                          "type": "string",
                          "example": "5678987667"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        }
                      }
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "53f7c7f9-f2bb-450c-8f6d-1vd707s66d30c"
                    },
                    "country": {
                      "type": "string",
                      "example": "NG"
                    },
                    "reference": {
                      "type": "string",
                      "example": "JJ0487919"
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 4863,
                      "default": 0
                    },
                    "recipient": {
                      "type": "object",
                      "properties": {
                        "country": {
                          "type": "string",
                          "example": "Nigeria"
                        },
                        "address": {
                          "type": "string",
                          "example": "Home Address"
                        },
                        "idType": {
                          "type": "string",
                          "example": "license"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+2349092916898"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "name": {
                          "type": "string",
                          "example": "John Doe"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "314159"
                        },
                        "email": {
                          "type": "string",
                          "example": "john.doe@yellowcard.io"
                        }
                      }
                    },
                    "channelId": {
                      "type": "string",
                      "example": "af944f0c-ba70-47c7-86dc-1bad5a6ab4e4"
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-02-24T23:46:28.691Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-02-24T23:39:46.013Z"
                    },
                    "amount": {
                      "type": "integer",
                      "example": 10,
                      "default": 0
                    },
                    "refundRetry": {
                      "type": "integer",
                      "example": 0,
                      "default": 0
                    },
                    "id": {
                      "type": "string",
                      "example": "58cadfdc-8264-59eb-90c6-cd9e969305aa"
                    },
                    "depositId": {
                      "type": "string",
                      "example": "19b2dad8-2fd1-4b5a-b621-bb37cd9e755b"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"PaymentInvalidState\",\n    \"message\": \"collection is not in processing/pending state.\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "PaymentInvalidState"
                    },
                    "message": {
                      "type": "string",
                      "example": "collection is not in processing/pending state."
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"Internal Server Error\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "Internal Server Error"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```    Refund Receive

# Refund Receive

Refund cash received from customer

<br />

> ⚠️ Updated Terminology
>
> Collections are now called Receives. These `/receive` endpoints replace the legacy `/collections` endpoints. The functionality remains identical, only the terminology has changed. Legacy collections endpoints are deprecated but will continue to  work. We recommend migrating to these new `/receive` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/receive/{id}/refund": {
      "post": {
        "summary": "Refund collection",
        "description": "Refund cash collected from customer",
        "operationId": "refund-collection",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique receive Identifier (id returned on Submit Receive request)",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"currency\": \"NGN\",\n    \"rate\": 486.3,\n    \"bankInfo\": {\n        \"name\": \"PAGA\",\n        \"accountNumber\": \"01234567890\",\n        \"accountName\": \"Ken Adams\"\n    },\n    \"status\": \"pending_refund\",\n    \"createdAt\": \"2023-02-24T19:54:43.784Z\",\n    \"source\": {\n        \"accountNumber\": \"1111111111\",\n        \"accountType\": \"bank\"\n    },\n    \"sequenceId\": \"53f7c7f9-f2bb-450c-8f6d-1bd70766d36c\",\n    \"country\": \"NG\",\n    \"reference\": \"JJ6208921\",\n    \"convertedAmount\": 4863,\n    \"recipient\": {\n        \"country\": \"Nigeria\",\n        \"address\": \"Home Address\",\n        \"idType\": \"license\",\n        \"phone\": \"+2349092916898\",\n        \"dob\": \"02/01/1997\",\n        \"name\": \"John Doe\",\n        \"idNumber\": \"314159\",\n        \"email\": \"john.doe@yellowcard.io\"\n    },\n    \"channelId\": \"af944f0c-ba70-47c7-86dc-1bad5a6ab4e4\",\n    \"expiresAt\": \"2023-02-24T20:04:43.781Z\",\n    \"updatedAt\": \"2023-02-24T19:57:42.161Z\",\n    \"amount\": 10,\n    \"refundRetry\": 0,\n    \"id\": \"70fde235-4c7e-5784-9133-9b676e411e30\",\n    \"depositId\": \"d99d5cba-222a-404f-a27e-2858e4ecb2ce\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "rate": {
                      "type": "number",
                      "example": 486.3,
                      "default": 0
                    },
                    "bankInfo": {
                      "type": "object",
                      "properties": {
                        "name": {
                          "type": "string",
                          "example": "PAGA"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "01234567890"
                        },
                        "accountName": {
                          "type": "string",
                          "example": "Ken Adams"
                        }
                      }
                    },
                    "status": {
                      "type": "string",
                      "example": "pending_refund"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2023-02-24T19:54:43.784Z"
                    },
                    "source": {
                      "type": "object",
                      "properties": {
                        "accountNumber": {
                          "type": "string",
                          "example": "1111111111"
                        },
                        "accountType": {
                          "type": "string",
                          "example": "bank"
                        }
                      }
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "53f7c7f9-f2bb-450c-8f6d-1bd70766d36c"
                    },
                    "country": {
                      "type": "string",
                      "example": "NG"
                    },
                    "reference": {
                      "type": "string",
                      "example": "JJ6208921"
                    },
                    "convertedAmount": {
                      "type": "integer",
                      "example": 4863,
                      "default": 0
                    },
                    "recipient": {
                      "type": "object",
                      "properties": {
                        "country": {
                          "type": "string",
                          "example": "Nigeria"
                        },
                        "address": {
                          "type": "string",
                          "example": "Home Address"
                        },
                        "idType": {
                          "type": "string",
                          "example": "license"
                        },
                        "phone": {
                          "type": "string",
                          "example": "+2349092916898"
                        },
                        "dob": {
                          "type": "string",
                          "example": "02/01/1997"
                        },
                        "name": {
                          "type": "string",
                          "example": "John Doe"
                        },
                        "idNumber": {
                          "type": "string",
                          "example": "314159"
                        },
                        "email": {
                          "type": "string",
                          "example": "john.doe@yellowcard.io"
                        }
                      }
                    },
                    "channelId": {
                      "type": "string",
                      "example": "af944f0c-ba70-47c7-86dc-1bad5a6ab4e4"
                    },
                    "expiresAt": {
                      "type": "string",
                      "example": "2023-02-24T20:04:43.781Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2023-02-24T19:57:42.161Z"
                    },
                    "amount": {
                      "type": "integer",
                      "example": 10,
                      "default": 0
                    },
                    "refundRetry": {
                      "type": "integer",
                      "example": 0,
                      "default": 0
                    },
                    "id": {
                      "type": "string",
                      "example": "70fde235-4c7e-5784-9133-9b676e411e30"
                    },
                    "depositId": {
                      "type": "string",
                      "example": "d99d5cba-222a-404f-a27e-2858e4ecb2ce"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"PaymentInvalidState\",\n    \"message\": \"collection is not in complete/cancelled/refund_failed state.\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "PaymentInvalidState"
                    },
                    "message": {
                      "type": "string",
                      "example": "collection is not in complete/cancelled/refund_failed state."
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "text/plain": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"Internal Server Error\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "Internal Server Error"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```     Lookup Receive

# Lookup Receive

Retrieve information about a specific receive request

<br />

> ⚠️ Updated Terminology
>
> Collections are now called Receives. These `/receive` endpoints replace the legacy `/collections` endpoints. The functionality remains identical, only the terminology has changed. Legacy collections endpoints are deprecated but will continue to  work. We recommend migrating to these new `/receive` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/receive/{id}": {
      "get": {
        "summary": "Lookup Collection",
        "description": "Retrieve information about a specific collection request",
        "operationId": "lookup-collection",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique Receive Identifier",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"currency\": \"NGN\",\n    \"rate\": 487.89,\n    \"bankInfo\": {\n        \"name\": \"PAGA\",\n        \"accountNumber\": \"1234567890\",\n        \"accountName\": \"Ken Adams\"\n    },\n    \"status\": \"complete\",\n    \"createdAt\": \"2023-02-06T13:31:20.108Z\",\n\t   \"source\": {\n\t\t  \"accountBank\": \"Access Bank\",\n  \t\t\"accountName\": \"OLUWATOBILOBA JAMES FALOLA\",\n\t\t  \"accountNumber\": \"9876543210\",\n\t\t  \"accountType\": \"bank\",\n       \"networkId\" \"93f7c7f9-f2bb-450c-8f6d-1bd70766d3850\"\n\t\t },\n    \"sequenceId\": \"11f4c7f2-f7bb-450c-4s6d-1bd70766d26d\",\n    \"country\": \"NG\",\n    \"reference\": \"JJ8094861\",\n    \"convertedAmount\": 9757.8,\n    \"recipient\": {\n        \"country\": \"Nigeria\",\n        \"address\": \"Home Address\",\n        \"idType\": \"license\",\n        \"phone\": \"+2348192039281\",\n        \"dob\": \"02/01/1987\",\n        \"name\": \"John Doe\",\n        \"idNumber\": \"29012938110\",\n        \"email\": \"john.doe@yellowcard.io\"\n    },\n    \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n    \"expiresAt\": \"2023-02-06T13:41:20.108Z\",\n    \"updatedAt\": \"2023-02-06T13:31:48.802Z\",\n    \"amount\": 20,\n    \"id\": \"805b2317-0da9-42b9-89fb-e14e3fe12dd8\",\n    \"depositId\": \"47069e2d-b225-4155-9028-2607fe3346bb\"\n}"
                  }
                }
              }
            }
          },
          "404": {
            "description": "404",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"CollectionNotFoundError\",\n    \"message\": \"\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "CollectionNotFoundError"
                    },
                    "message": {
                      "type": "string",
                      "example": ""
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```        Lookup Receive by sequenceId

# Lookup Receive by sequenceId

Retrieve information about a specific receive request using its sequenceId property

<br />

> ⚠️ Updated Terminology
>
> Collections are now called Receives. These `/receive` endpoints replace the legacy `/collections` endpoints. The functionality remains identical, only the terminology has changed. Legacy collections endpoints are deprecated but will continue to  work. We recommend migrating to these new `/receive` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/receive/sequence-id/{id}": {
      "get": {
        "summary": "Lookup Collection by sequenceId",
        "description": "Retrieve information about a specific collection request using its sequenceId property",
        "operationId": "lookup-collection-by-sequenceid",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "description": "Unique Receive sequenceId property",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"currency\": \"NGN\",\n    \"rate\": 487.89,\n    \"bankInfo\": {\n        \"name\": \"PAGA\",\n        \"accountNumber\": \"1234567890\",\n        \"accountName\": \"Ken Adams\"\n    },\n    \"status\": \"complete\",\n    \"createdAt\": \"2023-02-06T13:31:20.108Z\",\n\t   \"source\": {\n\t\t  \"accountBank\": \"Access Bank\",\n  \t\t\"accountName\": \"OLUWATOBILOBA JAMES FALOLA\",\n\t\t  \"accountNumber\": \"9876543210\",\n\t\t  \"accountType\": \"bank\",\n       \"networkId\" \"93f7c7f9-f2bb-450c-8f6d-1bd70766d3850\"\n\t\t },\n    \"sequenceId\": \"11f4c7f2-f7bb-450c-4s6d-1bd70766d26d\",\n    \"country\": \"NG\",\n    \"reference\": \"JJ8094861\",\n    \"convertedAmount\": 9757.8,\n    \"recipient\": {\n        \"country\": \"Nigeria\",\n        \"address\": \"Home Address\",\n        \"idType\": \"license\",\n        \"phone\": \"+2348192039281\",\n        \"dob\": \"02/01/1987\",\n        \"name\": \"John Doe\",\n        \"idNumber\": \"29012938110\",\n        \"email\": \"john.doe@yellowcard.io\"\n    },\n    \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n    \"expiresAt\": \"2023-02-06T13:41:20.108Z\",\n    \"updatedAt\": \"2023-02-06T13:31:48.802Z\",\n    \"amount\": 20,\n    \"id\": \"805b2317-0da9-42b9-89fb-e14e3fe12dd8\",\n    \"depositId\": \"47069e2d-b225-4155-9028-2607fe3346bb\"\n}"
                  }
                }
              }
            }
          },
          "404": {
            "description": "404",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"CollectionNotFoundError\",\n    \"message\": \"\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "CollectionNotFoundError"
                    },
                    "message": {
                      "type": "string",
                      "example": ""
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```  List Receives

# List Receives

Get a list of receive requests

<br />

> ⚠️ Updated Terminology
>
> Collections are now called Receives. These `/receive` endpoints replace the legacy `/collections` endpoints. The functionality remains identical, only the terminology has changed. Legacy collections endpoints are deprecated but will continue to  work. We recommend migrating to these new `/receive` endpoints for future compatibility.

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/receives": {
      "get": {
        "summary": "List Collection",
        "description": "Get a list of collection requests",
        "operationId": "list-collections",
        "parameters": [
          {
            "name": "endDate",
            "in": "query",
            "description": "a date string in ISO format (_2023-02-13T10:08:57.307Z_)",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "startDate",
            "in": "query",
            "description": "a date string in ISO format (_2023-02-13T10:08:57.307Z_)",
            "schema": {
              "type": "string"
            }
          },
          {
            "name": "startAt",
            "in": "query",
            "description": "a number indicating the where the pagination should start from",
            "schema": {
              "type": "integer",
              "format": "int32"
            }
          },
          {
            "name": "perPage",
            "in": "query",
            "description": "a number indicating the number of items per page",
            "schema": {
              "type": "integer",
              "format": "int32",
              "default": 100
            }
          },
          {
            "name": "rangeBy",
            "in": "query",
            "description": "a string indicating the field to which the start and end date are applied - either 'createdAt' or 'updatedAt'",
            "schema": {
              "type": "string",
              "default": "createdAt"
            }
          },
          {
            "name": "sortBy",
            "in": "query",
            "description": "a string indicating the field on which to sort by - either 'createdAt' or 'updatedAt'",
            "schema": {
              "type": "string",
              "default": "createdAt"
            }
          },
          {
            "name": "orderBy",
            "in": "query",
            "description": "a string indicating how to order the results - either 'asc' or 'desc'",
            "schema": {
              "type": "string",
              "default": "desc"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"collections\": [\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 488.25,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-15T13:01:08.386Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"country\": \"NG\",\n            \"convertedAmount\": 9765,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-15T13:11:08.386Z\",\n            \"updatedAt\": \"2023-02-15T13:11:11.662Z\",\n            \"amount\": 20,\n            \"id\": \"f39aa0a6-5006-5559-9424-dc72876f0561\"\n        },\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 487.85,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-16T15:13:17.808Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"country\": \"NG\",\n            \"convertedAmount\": 9757,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-16T15:23:17.808Z\",\n            \"updatedAt\": \"2023-02-16T15:24:12.982Z\",\n            \"amount\": 20,\n            \"id\": \"5073fa46-59aa-5b82-9349-b415e323cc8e\"\n        },\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 488.25,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-15T13:01:06.506Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"country\": \"NG\",\n            \"convertedAmount\": 9765,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-15T13:11:06.505Z\",\n            \"updatedAt\": \"2023-02-15T13:11:08.847Z\",\n            \"amount\": 20,\n            \"id\": \"843479b1-a0fc-5090-90de-f9787a04cad0\"\n        },\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 487.85,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-16T15:12:50.518Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"country\": \"NG\",\n            \"convertedAmount\": 9757,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-16T15:22:50.518Z\",\n            \"updatedAt\": \"2023-02-16T15:23:11.048Z\",\n            \"amount\": 20,\n            \"id\": \"19582e7e-f960-5c6f-8688-f1a4c2c36a5d\"\n        },\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"currency\": \"NGN\",\n            \"rate\": 487.21,\n            \"status\": \"expired\",\n            \"createdAt\": \"2023-02-23T14:12:43.187Z\",\n            \"source\": {\n                \"accountNumber\": \"1111111111\",\n                \"networkId\": \"6df48502-1ebe-473f-be17-e2cae4dd67ee\",\n                \"accountType\": \"bank\"\n            },\n            \"sequenceId\": \"test2-c1f913cc-156c-4e60-bd71-887bf4f52287\",\n            \"country\": \"NG\",\n            \"convertedAmount\": 9744.2,\n            \"recipient\": {\n                \"country\": \"Nigeria\",\n                \"address\": \"Home Address\",\n                \"idType\": \"license\",\n                \"phone\": \"+2349092916898\",\n                \"dob\": \"02/01/1997\",\n                \"name\": \"John Doe\",\n                \"idNumber\": \"314159\",\n                \"email\": \"john.doe@yellowcard.io\"\n            },\n            \"channelId\": \"fe8f4989-3bf6-41ca-9621-ffe2bc127569\",\n            \"expiresAt\": \"2023-02-23T14:22:43.187Z\",\n            \"updatedAt\": \"2023-02-23T14:23:53.887Z\",\n            \"amount\": 20,\n            \"id\": \"f51c7b43-140d-51f0-ac5e-841ce3d95160\"\n        }\n      ]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "collections": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "partnerId": {
                            "type": "string",
                            "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                          },
                          "currency": {
                            "type": "string",
                            "example": "NGN"
                          },
                          "rate": {
                            "type": "number",
                            "example": 488.25,
                            "default": 0
                          },
                          "status": {
                            "type": "string",
                            "example": "expired"
                          },
                          "createdAt": {
                            "type": "string",
                            "example": "2023-02-15T13:01:08.386Z"
                          },
                          "source": {
                            "type": "object",
                            "properties": {
                              "accountNumber": {
                                "type": "string",
                                "example": "1111111111"
                              },
                              "networkId": {
                                "type": "string",
                                "example": "6df48502-1ebe-473f-be17-e2cae4dd67ee"
                              },
                              "accountType": {
                                "type": "string",
                                "example": "bank"
                              }
                            }
                          },
                          "country": {
                            "type": "string",
                            "example": "NG"
                          },
                          "convertedAmount": {
                            "type": "integer",
                            "example": 9765,
                            "default": 0
                          },
                          "recipient": {
                            "type": "object",
                            "properties": {
                              "country": {
                                "type": "string",
                                "example": "Nigeria"
                              },
                              "address": {
                                "type": "string",
                                "example": "Home Address"
                              },
                              "idType": {
                                "type": "string",
                                "example": "license"
                              },
                              "phone": {
                                "type": "string",
                                "example": "+2349092916898"
                              },
                              "dob": {
                                "type": "string",
                                "example": "02/01/1997"
                              },
                              "name": {
                                "type": "string",
                                "example": "John Doe"
                              },
                              "idNumber": {
                                "type": "string",
                                "example": "314159"
                              },
                              "email": {
                                "type": "string",
                                "example": "john.doe@yellowcard.io"
                              }
                            }
                          },
                          "channelId": {
                            "type": "string",
                            "example": "fe8f4989-3bf6-41ca-9621-ffe2bc127569"
                          },
                          "expiresAt": {
                            "type": "string",
                            "example": "2023-02-15T13:11:08.386Z"
                          },
                          "updatedAt": {
                            "type": "string",
                            "example": "2023-02-15T13:11:11.662Z"
                          },
                          "amount": {
                            "type": "integer",
                            "example": 20,
                            "default": 0
                          },
                          "id": {
                            "type": "string",
                            "example": "f39aa0a6-5006-5559-9424-dc72876f0561"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "text/plain": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InvalidInput\",\n    \"message\": \"invalid startDate passed in request\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InvalidInput"
                    },
                    "message": {
                      "type": "string",
                      "example": "invalid startDate passed in request"
                    }
                  }
                }
              }
            }
          },
          "500": {
            "description": "500",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"InternalServerError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```



Webhook

Create Webhook

# Create Webhook

Create a webhook for a given transaction state, or for all states.

<TutorialTile backgroundColor="#018FF4" emoji="🦉" id="68305ea472c2850041213d00" link="https://docs.yellowcard.engineering/v1.0.2/recipes/working-with-webhooks" slug="working-with-webhooks" title="Working with webhooks" />

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/webhooks": {
      "post": {
        "summary": "Create Webhook",
        "description": "Create a webhook for a given transaction state, or for all states.",
        "operationId": "create-webhook",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "url"
                ],
                "properties": {
                  "url": {
                    "type": "string",
                    "description": "The URL to which the event will be posted to."
                  },
                  "state": {
                    "type": "string",
                    "description": "The transaction status event that this webhook will be activated for. If omitted, the webhook will receive all events."
                  },
                  "active": {
                    "type": "boolean",
                    "description": "Whether this webhook is currently active or not. Defaults to `true` if omitted.",
                    "default": true
                  }
                }
              },
              "examples": {
                "Request Example": {
                  "value": {
                    "url": "https://test.sample.com/webhook/test",
                    "state": "collection.complete",
                    "active": true
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"url\": \"https://test.sample.com/webhook/test\",\n    \"state\": \"collection.complete\",\n    \"active\": true,\n    \"createdAt\": \"2022-12-14T11:56:09.617Z\",\n    \"updatedAt\": \"2022-12-14T11:56:09.617Z\",\n    \"id\": \"4fb49434-077e-49dd-ac41-74f58c3c779c\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "url": {
                      "type": "string",
                      "example": "https://test.sample.com/webhook/test"
                    },
                    "state": {
                      "type": "string",
                      "example": "collection.complete"
                    },
                    "active": {
                      "type": "boolean",
                      "example": true,
                      "default": true
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2022-12-14T11:56:09.617Z"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2022-12-14T11:56:09.617Z"
                    },
                    "id": {
                      "type": "string",
                      "example": "4fb49434-077e-49dd-ac41-74f58c3c779c"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```


Update Webhook

# Update Webhook

Update the fields of a given webhook.

<TutorialTile backgroundColor="#018FF4" emoji="🦉" id="68305ea472c2850041213d00" link="https://docs.yellowcard.engineering/v1.0.2/recipes/webhooks" slug="webhooks" title="Webhooks" />

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/webhooks": {
      "put": {
        "summary": "Update Webhook",
        "description": "Update the fields of a given webhook.",
        "operationId": "update-webhook",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "required": [
                  "id"
                ],
                "properties": {
                  "id": {
                    "type": "string",
                    "description": "The unique ID of the webhook to be updated."
                  },
                  "url": {
                    "type": "string",
                    "description": "The URL to which the event will be posted to."
                  },
                  "state": {
                    "type": "string",
                    "description": "The transaction status event that this webhook will be activated for. An undefined state will receive all events."
                  },
                  "active": {
                    "type": "boolean",
                    "description": "Whether this webhook is currently active or not."
                  }
                }
              },
              "examples": {
                "Request Example": {
                  "value": {
                    "id": "4fb49434-077e-49dd-ac41-74f58c3c779c",
                    "active": false
                  }
                }
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n    \"active\": false,\n    \"updatedAt\": \"2022-09-01T13:21:12.858Z\",\n    \"createdAt\": \"2022-09-01T13:15:25.441Z\",\n    \"id\": \"4fb49434-077e-49dd-ac41-74f58c3c779c\",\n    \"url\": \"https://test.sample.com/webhook/test\",\n    \"state\": \"payment.created\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "partnerId": {
                      "type": "string",
                      "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                    },
                    "active": {
                      "type": "boolean",
                      "example": false,
                      "default": true
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2022-09-01T13:21:12.858Z"
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2022-09-01T13:15:25.441Z"
                    },
                    "id": {
                      "type": "string",
                      "example": "4fb49434-077e-49dd-ac41-74f58c3c779c"
                    },
                    "url": {
                      "type": "string",
                      "example": "https://test.sample.com/webhook/test"
                    },
                    "state": {
                      "type": "string",
                      "example": "payment.created"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```


Remove Webhook

# Remove Webhook

Remove a given webhook.

<TutorialTile backgroundColor="#018FF4" emoji="🦉" id="68305ea472c2850041213d00" link="https://docs.yellowcard.engineering/v1.0.2/recipes/webhooks" slug="webhooks" title="Webhooks" />

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/webhooks/{id}": {
      "delete": {
        "summary": "Remove Webhook",
        "description": "Remove a given webhook.",
        "operationId": "remove-webhook",
        "parameters": [
          {
            "in": "path",
            "name": "id",
            "schema": {
              "type": "string"
            },
            "required": true,
            "description": "The unique ID of the webhook to be removed."
          }
        ],
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {}
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```

List Webhooks

# List Webhooks

List all webhooks associated with your account.

<TutorialTile backgroundColor="#018FF4" emoji="🦉" id="68305ea472c2850041213d00" link="https://docs.yellowcard.engineering/v1.0.2/recipes/working-with-webhooks" slug="working-with-webhooks" title="Working with webhooks" />

# OpenAPI definition

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "yellow-cards-payment-api",
    "version": "1.0.23"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "components": {
    "securitySchemes": {
      "sec0": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "x-bearer-format": ""
      },
      "sec1": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "security": [
    {
      "sec0": [],
      "sec1": []
    }
  ],
  "paths": {
    "/webhooks": {
      "get": {
        "summary": "List Webhooks",
        "description": "List all webhooks associated with your account.",
        "operationId": "list-webhooks",
        "responses": {
          "200": {
            "description": "200",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"webhooks\": [\n        {\n            \"partnerId\": \"9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01\",\n            \"active\": true,\n            \"updatedAt\": \"2022-01-19T10:18:46.903Z\",\n            \"createdAt\": \"2022-01-19T10:18:46.903Z\",\n            \"url\": \"https://o1lce324xh.execute-api.eu-west-2.amazonaws.com/staging/webhook/test\",\n            \"id\": \"860ba0db-5012-4ebc-98ee-d88278ead198\",\n            \"state\": \"COLLECTION.FAILED\"\n        }\n    ]\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "webhooks": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "partnerId": {
                            "type": "string",
                            "example": "9ecf5248-17e7-4a2b-b5a8-3bd58ff0fe01"
                          },
                          "active": {
                            "type": "boolean",
                            "example": true,
                            "default": true
                          },
                          "updatedAt": {
                            "type": "string",
                            "example": "2022-01-19T10:18:46.903Z"
                          },
                          "createdAt": {
                            "type": "string",
                            "example": "2022-01-19T10:18:46.903Z"
                          },
                          "url": {
                            "type": "string",
                            "example": "https://o1lce324xh.execute-api.eu-west-2.amazonaws.com/staging/webhook/test"
                          },
                          "id": {
                            "type": "string",
                            "example": "860ba0db-5012-4ebc-98ee-d88278ead198"
                          },
                          "state": {
                            "type": "string",
                            "example": "COLLECTION.FAILED"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "400": {
            "description": "400",
            "content": {
              "application/json": {
                "examples": {
                  "Result": {
                    "value": "{\n    \"code\": \"BadRequestError\",\n    \"message\": \"something went wrong\"\n}"
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "BadRequestError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                }
              }
            }
          }
        },
        "deprecated": false
      }
    }
  },
  "x-readme": {
    "headers": [],
    "explorer-enabled": true,
    "proxy-enabled": true
  },
  "x-readme-fauxas": true
}
```









Create Vault

# Create Vault

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/vaults": {
      "post": {
        "summary": "Create Vault",
        "tags": [
          "Vaults"
        ],
        "responses": {
          "201": {
            "description": "Create Vault",
            "headers": {
              "Date": {
                "schema": {
                  "type": "string"
                }
              },
              "Content-Length": {
                "schema": {
                  "type": "integer"
                }
              },
              "Connection": {
                "schema": {
                  "type": "string"
                }
              },
              "Server": {
                "schema": {
                  "type": "string"
                }
              },
              "CF-Ray": {
                "schema": {
                  "type": "integer"
                }
              },
              "CF-Cache-Status": {
                "schema": {
                  "type": "string"
                }
              },
              "Access-Control-Allow-Origin": {
                "schema": {
                  "type": "string"
                }
              },
              "Set-Cookie": {
                "schema": {
                  "type": "string"
                }
              },
              "Strict-Transport-Security": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-credentials": {
                "schema": {
                  "type": "boolean"
                }
              },
              "x-amz-apigw-id": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-requestid": {
                "schema": {
                  "type": "integer"
                }
              },
              "x-amzn-trace-id": {
                "schema": {
                  "type": "string"
                }
              },
              "X-Hiring": {
                "schema": {
                  "type": "string"
                }
              },
              "Vary": {
                "schema": {
                  "type": "string"
                }
              },
              "expect-ct": {
                "schema": {
                  "type": "string"
                }
              },
              "referrer-policy": {
                "schema": {
                  "type": "string"
                }
              },
              "x-content-type-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-frame-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-xss-protection": {
                "schema": {
                  "type": "integer"
                }
              }
            },
            "content": {
              "application/json": {
                "examples": {
                  "Created": {
                    "summary": "Created",
                    "value": {
                      "id": "vaultinternal-uuid-239292",
                      "vaultLabel": "Main Treasury Vault",
                      "partnerId": "partneruuid-00293"
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "example": "vaultinternal-uuid-239292"
                    },
                    "vaultLabel": {
                      "type": "string",
                      "example": "Main Treasury Vault"
                    },
                    "partnerId": {
                      "type": "string",
                      "example": "partneruuid-00293"
                    }
                  }
                }
              }
            }
          }
        },
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "default": "",
                    "description": "Vault name for identification"
                  }
                },
                "required": [
                  "name"
                ]
              },
              "examples": {
                "": {
                  "summary": "",
                  "value": {
                    "name": "Main Treasury Vault"
                  }
                }
              }
            }
          }
        },
        "x-readme": {}
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```


Get Vaults

# Get Vaults

This is a GET request and it is used to "get" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).

A successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data.

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/vaults": {
      "get": {
        "summary": "Get Vaults",
        "tags": [
          "Vaults"
        ],
        "responses": {
          "200": {
            "description": "Get Vaults",
            "headers": {
              "Date": {
                "schema": {
                  "type": "string"
                }
              },
              "Transfer-Encoding": {
                "schema": {
                  "type": "string"
                }
              },
              "Connection": {
                "schema": {
                  "type": "string"
                }
              },
              "Content-Encoding": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-requestid": {
                "schema": {
                  "type": "integer"
                }
              },
              "access-control-allow-origin": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amz-apigw-id": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-trace-id": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-credentials": {
                "schema": {
                  "type": "boolean"
                }
              },
              "cf-cache-status": {
                "schema": {
                  "type": "string"
                }
              },
              "Strict-Transport-Security": {
                "schema": {
                  "type": "string"
                }
              },
              "expect-ct": {
                "schema": {
                  "type": "string"
                }
              },
              "referrer-policy": {
                "schema": {
                  "type": "string"
                }
              },
              "x-content-type-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-frame-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-xss-protection": {
                "schema": {
                  "type": "integer"
                }
              },
              "X-Hiring": {
                "schema": {
                  "type": "string"
                }
              },
              "Set-Cookie": {
                "schema": {
                  "type": "string"
                }
              },
              "Server": {
                "schema": {
                  "type": "string"
                }
              },
              "CF-RAY": {
                "schema": {
                  "type": "integer"
                }
              }
            },
            "content": {
              "application/json": {
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": {
                      "vaults": [
                        {
                          "vaultLabel": "Collection Test Vault",
                          "createdAt": "2025-10-31T13:06:27.143Z",
                          "vaultAccountId": "436403",
                          "partnerId": "7882e37a-51c7-4e6f-80cc-4d9ca99e39ae",
                          "id": "ec96d00e-67d3-4da0-8022-cf267f7e67e5",
                          "updatedAt": "2025-10-31T13:07:35.313Z"
                        },
                        {
                          "updatedAt": "2025-10-31T13:40:18.897Z",
                          "vaultLabel": "Address Vault",
                          "id": "9f4b8b2d-0b90-4176-8f51-d04df121bc04",
                          "vaultAccountId": "436404",
                          "createdAt": "2025-10-31T13:21:21.807Z",
                          "partnerId": "7882e37a-51c7-4e6f-80cc-4d9ca99e39ae"
                        }
                      ]
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "vaults": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "name": {
                            "type": "string",
                            "example": "Collection Test Vault"
                          },
                          "createdAt": {
                            "type": "string",
                            "example": "2025-10-31T13:06:27.143Z"
                          },
                          "partnerId": {
                            "type": "string",
                            "example": "7882e37a-51c7-4e6f-80cc-4d9ca99e39ae"
                          },
                          "id": {
                            "type": "string",
                            "example": "ec96d00e-67d3-4da0-8022-cf267f7e67e5"
                          },
                          "updatedAt": {
                            "type": "string",
                            "example": "2025-10-31T13:07:35.313Z"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "description": "This is a GET request and it is used to \"get\" data from an endpoint. There is no request body for a GET request, but you can use query parameters to help specify the resource you want data on (e.g., in this request, we have `id=1`).\n\nA successful GET response will have a `200 OK` status, and should include some kind of response body - for example, HTML web content or JSON data."
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```


Get Vault by ID

# Get Vault by ID

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/vaults/{id}": {
      "get": {
        "summary": "Get Vault by ID",
        "tags": [
          "Vaults"
        ],
        "responses": {
          "200": {
            "description": "Get Vault by ID",
            "headers": {
              "Date": {
                "schema": {
                  "type": "string"
                }
              },
              "Transfer-Encoding": {
                "schema": {
                  "type": "string"
                }
              },
              "Connection": {
                "schema": {
                  "type": "string"
                }
              },
              "Content-Encoding": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-requestid": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-origin": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amz-apigw-id": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-trace-id": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-credentials": {
                "schema": {
                  "type": "boolean"
                }
              },
              "cf-cache-status": {
                "schema": {
                  "type": "string"
                }
              },
              "Strict-Transport-Security": {
                "schema": {
                  "type": "string"
                }
              },
              "expect-ct": {
                "schema": {
                  "type": "string"
                }
              },
              "referrer-policy": {
                "schema": {
                  "type": "string"
                }
              },
              "x-content-type-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-frame-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-xss-protection": {
                "schema": {
                  "type": "integer"
                }
              },
              "X-Hiring": {
                "schema": {
                  "type": "string"
                }
              },
              "Set-Cookie": {
                "schema": {
                  "type": "string"
                }
              },
              "Server": {
                "schema": {
                  "type": "string"
                }
              },
              "CF-RAY": {
                "schema": {
                  "type": "integer"
                }
              }
            },
            "content": {
              "application/json": {
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": {
                      "id": "5bb1b7ce-508c-4acc-9e49-44d9ec572a6a",
                      "vaultLabel": "Address vault",
                      "partnerId": "06b3054b-1ac5-42c6-8687-d2195c1f0e4b",
                      "assets": [
                        {
                          "id": "PYUSD_ERC20",
                          "available": "0",
                          "pending": "0"
                        },
                        {
                          "id": "SOL_SOL",
                          "available": "2.2",
                          "pending": "0"
                        },
                        {
                          "id": "USDC_SOL",
                          "available": "100",
                          "pending": "0"
                        }
                      ]
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "example": "5bb1b7ce-508c-4acc-9e49-44d9ec572a6a"
                    },
                    "name": {
                      "type": "string",
                      "example": "Address vault"
                    },
                    "partnerId": {
                      "type": "string",
                      "example": "06b3054b-1ac5-42c6-8687-d2195c1f0e4b"
                    },
                    "assets": {
                      "type": "array",
                      "items": {
                        "type": "object",
                        "properties": {
                          "id": {
                            "type": "string",
                            "example": "PYUSD_ERC20"
                          },
                          "available": {
                            "type": "string",
                            "example": "0"
                          },
                          "pending": {
                            "type": "string",
                            "example": "0"
                          },
                          "depositAddress": {
                            "type": "string"
                          }
                        }
                      }
                    }
                  }
                }
              }
            }
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "description": "This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.\n\nA successful POST request typically returns a `200 OK` or `201 Created` response code.",
        "parameters": [
          {
            "in": "path",
            "name": "id",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Get Asset Config

# Get Asset Config

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.

List of Supported Stablecoins by Network:

**USDC**

* USDC\_XLM
* USDC\_SOL
* USDC\_CELO
* USDC\_ERC20
* USDC\_BASE

**USDT**

* USDT\_SOL
* USDT\_CELO
* USDT\_POLYGON
* USDT\_TRC20

**CUSD**

* CUSD\_CELO

**PYUSD**

* PYUSD\_SOL
* PYUSD\_ERC20

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/vaults/config": {
      "get": {
        "summary": "Get Asset Config",
        "tags": [
          "Vaults"
        ],
        "responses": {
          "200": {
            "description": "OK",
            "headers": {
              "Date": {
                "schema": {
                  "type": "string"
                }
              },
              "Transfer-Encoding": {
                "schema": {
                  "type": "string"
                }
              },
              "Connection": {
                "schema": {
                  "type": "string"
                }
              },
              "Content-Encoding": {
                "schema": {
                  "type": "string"
                }
              },
              "CF-Ray": {
                "schema": {
                  "type": "integer"
                }
              },
              "CF-Cache-Status": {
                "schema": {
                  "type": "string"
                }
              },
              "Access-Control-Allow-Origin": {
                "schema": {
                  "type": "string"
                }
              },
              "Set-Cookie": {
                "schema": {
                  "type": "string"
                }
              },
              "Strict-Transport-Security": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-credentials": {
                "schema": {
                  "type": "boolean"
                }
              },
              "x-amz-apigw-id": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-requestid": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-trace-id": {
                "schema": {
                  "type": "string"
                }
              },
              "X-Hiring": {
                "schema": {
                  "type": "string"
                }
              },
              "Vary": {
                "schema": {
                  "type": "string"
                }
              },
              "expect-ct": {
                "schema": {
                  "type": "string"
                }
              },
              "referrer-policy": {
                "schema": {
                  "type": "string"
                }
              },
              "x-content-type-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-frame-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-xss-protection": {
                "schema": {
                  "type": "integer"
                }
              },
              "Server": {
                "schema": {
                  "type": "string"
                }
              }
            },
            "content": {
              "application/json": {
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": [
                      {
                        "code": "USDC",
                        "resources": [
                          {
                            "type": "file_url",
                            "content": "https://f.hubspotusercontent30.net/hubfs/9304636/PDF/centre-whitepaper.pdf",
                            "id": "WHITEPAPER"
                          }
                        ],
                        "zones": [
                          "stablecoins"
                        ],
                        "updatedAt": "2024-12-06T07:13:13.561Z",
                        "networks": {
                          "XLM": {
                            "nativeAsset": "XLM",
                            "chainCurrencyId": "USDC",
                            "addressRegex": "^G[A-Z2-7]{55}$",
                            "requiresMemo": true,
                            "activities": [
                              "SEND",
                              "RECEIVE"
                            ],
                            "explorerUrl": "https://blockchair.com/stellar/transaction/__TX_HASH__",
                            "name": "Stellar",
                            "enabled": true,
                            "network": "XLM"
                          },
                          "SOL": {
                            "nativeAsset": "SOL",
                            "chainCurrencyId": "USDC",
                            "addressRegex": "^[1-9A-HJ-NP-Za-km-z]{32,44}$",
                            "requiresMemo": false,
                            "activities": [
                              "SEND",
                              "RECEIVE"
                            ],
                            "explorerUrl": "https://explorer.solana.com/tx/__TX_HASH__",
                            "name": "Solana",
                            "enabled": true,
                            "network": "SOL"
                          },
                          "CELO": {
                            "nativeAsset": "CELO",
                            "chainCurrencyId": "USDC",
                            "addressRegex": "^(0x)[0-9A-Fa-f]{40}$",
                            "requiresMemo": false,
                            "activities": [
                              "SEND",
                              "RECEIVE"
                            ],
                            "explorerUrl": "https://celoscan.io/tx/__TX_HASH__",
                            "name": "Celo",
                            "enabled": true,
                            "network": "CELO"
                          },
                          "ERC20": {
                            "nativeAsset": "ETH",
                            "chainCurrencyId": "USDC",
                            "addressRegex": "^(0x)[0-9A-Fa-f]{40}$",
                            "requiresMemo": false,
                            "activities": [
                              "SEND",
                              "RECEIVE"
                            ],
                            "explorerUrl": "https://etherscan.io/tx/__TX_HASH__",
                            "name": "Ethereum",
                            "enabled": true,
                            "network": "ERC20"
                          },
                          "BASE": {
                            "nativeAsset": "OP",
                            "chainCurrencyId": "USDC",
                            "addressRegex": "^(0x)[0-9A-Fa-f]{40}$",
                            "requiresMemo": false,
                            "activities": [
                              "SEND",
                              "RECEIVE"
                            ],
                            "explorerUrl": "https://basescan.org/tx/__TX_HASH__",
                            "name": "Base",
                            "enabled": true,
                            "network": "BASE"
                          }
                        },
                        "createdAt": "2024-12-06T07:13:13.561Z",
                        "isUTXOBased": false,
                        "description": "USDC is a stablecoin, pegged 1:1 to the US$. Created by Circle & Coinbase, each USDC unit in circulation is backed by $1 held in reserve, consisting of a mix of cash and short-term U.S. Treasury bonds.<br /><br />Join the USDC ecosystem and enjoy the benefits of stability and peace of mind as you make digital transactions with confidence! 🛡️",
                        "id": "usd-coin",
                        "name": "USD Coin",
                        "defaultNetwork": "ERC20"
                      }
                    ]
                  }
                },
                "schema": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "code": {
                        "type": "string",
                        "example": "USDC"
                      },
                      "resources": {
                        "type": "array",
                        "items": {
                          "type": "object",
                          "properties": {
                            "type": {
                              "type": "string",
                              "example": "file_url"
                            },
                            "content": {
                              "type": "string",
                              "example": "https://f.hubspotusercontent30.net/hubfs/9304636/PDF/centre-whitepaper.pdf"
                            },
                            "id": {
                              "type": "string",
                              "example": "WHITEPAPER"
                            }
                          }
                        }
                      },
                      "zones": {
                        "type": "array",
                        "items": {
                          "type": "string",
                          "example": "stablecoins"
                        }
                      },
                      "updatedAt": {
                        "type": "string",
                        "example": "2024-12-06T07:13:13.561Z"
                      },
                      "networks": {
                        "type": "object",
                        "properties": {
                          "XLM": {
                            "type": "object",
                            "properties": {
                              "nativeAsset": {
                                "type": "string",
                                "example": "XLM"
                              },
                              "chainCurrencyId": {
                                "type": "string",
                                "example": "USDC"
                              },
                              "addressRegex": {
                                "type": "string",
                                "example": "^G[A-Z2-7]{55}$"
                              },
                              "requiresMemo": {
                                "type": "boolean",
                                "example": true,
                                "default": true
                              },
                              "activities": {
                                "type": "array",
                                "items": {
                                  "type": "string",
                                  "example": "SEND"
                                }
                              },
                              "explorerUrl": {
                                "type": "string",
                                "example": "https://blockchair.com/stellar/transaction/__TX_HASH__"
                              },
                              "name": {
                                "type": "string",
                                "example": "Stellar"
                              },
                              "enabled": {
                                "type": "boolean",
                                "example": true,
                                "default": true
                              },
                              "network": {
                                "type": "string",
                                "example": "XLM"
                              }
                            }
                          },
                          "SOL": {
                            "type": "object",
                            "properties": {
                              "nativeAsset": {
                                "type": "string",
                                "example": "SOL"
                              },
                              "chainCurrencyId": {
                                "type": "string",
                                "example": "USDC"
                              },
                              "addressRegex": {
                                "type": "string",
                                "example": "^[1-9A-HJ-NP-Za-km-z]{32,44}$"
                              },
                              "requiresMemo": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "activities": {
                                "type": "array",
                                "items": {
                                  "type": "string",
                                  "example": "SEND"
                                }
                              },
                              "explorerUrl": {
                                "type": "string",
                                "example": "https://explorer.solana.com/tx/__TX_HASH__"
                              },
                              "name": {
                                "type": "string",
                                "example": "Solana"
                              },
                              "enabled": {
                                "type": "boolean",
                                "example": true,
                                "default": true
                              },
                              "network": {
                                "type": "string",
                                "example": "SOL"
                              }
                            }
                          },
                          "CELO": {
                            "type": "object",
                            "properties": {
                              "nativeAsset": {
                                "type": "string",
                                "example": "CELO"
                              },
                              "chainCurrencyId": {
                                "type": "string",
                                "example": "USDC"
                              },
                              "addressRegex": {
                                "type": "string",
                                "example": "^(0x)[0-9A-Fa-f]{40}$"
                              },
                              "requiresMemo": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "activities": {
                                "type": "array",
                                "items": {
                                  "type": "string",
                                  "example": "SEND"
                                }
                              },
                              "explorerUrl": {
                                "type": "string",
                                "example": "https://celoscan.io/tx/__TX_HASH__"
                              },
                              "name": {
                                "type": "string",
                                "example": "Celo"
                              },
                              "enabled": {
                                "type": "boolean",
                                "example": true,
                                "default": true
                              },
                              "network": {
                                "type": "string",
                                "example": "CELO"
                              }
                            }
                          },
                          "ERC20": {
                            "type": "object",
                            "properties": {
                              "nativeAsset": {
                                "type": "string",
                                "example": "ETH"
                              },
                              "chainCurrencyId": {
                                "type": "string",
                                "example": "USDC"
                              },
                              "addressRegex": {
                                "type": "string",
                                "example": "^(0x)[0-9A-Fa-f]{40}$"
                              },
                              "requiresMemo": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "activities": {
                                "type": "array",
                                "items": {
                                  "type": "string",
                                  "example": "SEND"
                                }
                              },
                              "explorerUrl": {
                                "type": "string",
                                "example": "https://etherscan.io/tx/__TX_HASH__"
                              },
                              "name": {
                                "type": "string",
                                "example": "Ethereum"
                              },
                              "enabled": {
                                "type": "boolean",
                                "example": true,
                                "default": true
                              },
                              "network": {
                                "type": "string",
                                "example": "ERC20"
                              }
                            }
                          },
                          "BASE": {
                            "type": "object",
                            "properties": {
                              "nativeAsset": {
                                "type": "string",
                                "example": "OP"
                              },
                              "chainCurrencyId": {
                                "type": "string",
                                "example": "USDC"
                              },
                              "addressRegex": {
                                "type": "string",
                                "example": "^(0x)[0-9A-Fa-f]{40}$"
                              },
                              "requiresMemo": {
                                "type": "boolean",
                                "example": false,
                                "default": true
                              },
                              "activities": {
                                "type": "array",
                                "items": {
                                  "type": "string",
                                  "example": "SEND"
                                }
                              },
                              "explorerUrl": {
                                "type": "string",
                                "example": "https://basescan.org/tx/__TX_HASH__"
                              },
                              "name": {
                                "type": "string",
                                "example": "Base"
                              },
                              "enabled": {
                                "type": "boolean",
                                "example": true,
                                "default": true
                              },
                              "network": {
                                "type": "string",
                                "example": "BASE"
                              }
                            }
                          }
                        }
                      },
                      "createdAt": {
                        "type": "string",
                        "example": "2024-12-06T07:13:13.561Z"
                      },
                      "isUTXOBased": {
                        "type": "boolean",
                        "example": false,
                        "default": true
                      },
                      "description": {
                        "type": "string",
                        "example": "USDC is a stablecoin, pegged 1:1 to the US$. Created by Circle & Coinbase, each USDC unit in circulation is backed by $1 held in reserve, consisting of a mix of cash and short-term U.S. Treasury bonds.<br /><br />Join the USDC ecosystem and enjoy the benefits of stability and peace of mind as you make digital transactions with confidence! 🛡️"
                      },
                      "id": {
                        "type": "string",
                        "example": "usd-coin"
                      },
                      "name": {
                        "type": "string",
                        "example": "USD Coin"
                      },
                      "defaultNetwork": {
                        "type": "string",
                        "example": "ERC20"
                      }
                    }
                  }
                }
              }
            }
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "description": "This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.\n\nA successful POST request typically returns a `200 OK` or `201 Created` response code."
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Generate Address

# Generate Address

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/addresses": {
      "post": {
        "summary": "Generate Address",
        "tags": [
          "Vaults"
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "address": {
                      "type": "string",
                      "example": "0xbebfA3cE1BA1d9385e9D53A1B1d71ECeB80245E4"
                    },
                    "token": {
                      "type": "string",
                      "example": "USDT_POLYGON"
                    },
                    "vaultId": {
                      "type": "string",
                      "example": "vault_internal_uuid"
                    }
                  }
                },
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": {
                      "address": "0xbebfA3cE1BA1d9385e9D53A1B1d71ECeB80245E4",
                      "token": "USDT_POLYGON",
                      "vaultId": "vault_internal_uuid"
                    }
                  }
                }
              }
            },
            "description": "OK"
          },
          "400": {
            "description": "Generate Address",
            "headers": {
              "Date": {
                "schema": {
                  "type": "string"
                }
              },
              "Content-Length": {
                "schema": {
                  "type": "integer"
                }
              },
              "Connection": {
                "schema": {
                  "type": "string"
                }
              },
              "CF-RAY": {
                "schema": {
                  "type": "integer"
                }
              },
              "x-amzn-requestid": {
                "schema": {
                  "type": "integer"
                }
              },
              "access-control-allow-origin": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amz-apigw-id": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-trace-id": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-credentials": {
                "schema": {
                  "type": "boolean"
                }
              },
              "cf-cache-status": {
                "schema": {
                  "type": "string"
                }
              },
              "Strict-Transport-Security": {
                "schema": {
                  "type": "string"
                }
              },
              "expect-ct": {
                "schema": {
                  "type": "string"
                }
              },
              "referrer-policy": {
                "schema": {
                  "type": "string"
                }
              },
              "x-content-type-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-frame-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-xss-protection": {
                "schema": {
                  "type": "integer"
                }
              },
              "X-Hiring": {
                "schema": {
                  "type": "string"
                }
              },
              "Set-Cookie": {
                "schema": {
                  "type": "string"
                }
              },
              "Server": {
                "schema": {
                  "type": "string"
                }
              }
            },
            "content": {
              "application/json": {
                "examples": {
                  "Bad Request": {
                    "summary": "Bad Request",
                    "value": {
                      "code": "ValidationError",
                      "message": "invalid token supplied"
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "ValidationError"
                    },
                    "message": {
                      "type": "string",
                      "example": "invalid token supplied"
                    }
                  }
                }
              }
            }
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "token": {
                    "type": "string",
                    "default": "",
                    "description": "A combination of crypto currency network pair for asset. e,g, USDC_SOL "
                  },
                  "vaultId": {
                    "type": "string",
                    "default": ""
                  }
                },
                "required": [
                  "token",
                  "vaultId"
                ]
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Get Fee

# Get Fee

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/sends/fee": {
      "post": {
        "summary": "Get Fee",
        "tags": [
          "Transactions"
        ],
        "responses": {
          "200": {
            "description": "Get Fee",
            "headers": {
              "Date": {
                "schema": {
                  "type": "string"
                }
              },
              "Content-Length": {
                "schema": {
                  "type": "integer"
                }
              },
              "Connection": {
                "schema": {
                  "type": "string"
                }
              },
              "Server": {
                "schema": {
                  "type": "string"
                }
              },
              "CF-Ray": {
                "schema": {
                  "type": "integer"
                }
              },
              "CF-Cache-Status": {
                "schema": {
                  "type": "string"
                }
              },
              "Access-Control-Allow-Origin": {
                "schema": {
                  "type": "string"
                }
              },
              "Set-Cookie": {
                "schema": {
                  "type": "string"
                }
              },
              "Strict-Transport-Security": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-credentials": {
                "schema": {
                  "type": "boolean"
                }
              },
              "x-amz-apigw-id": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-requestid": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-trace-id": {
                "schema": {
                  "type": "string"
                }
              },
              "X-Hiring": {
                "schema": {
                  "type": "string"
                }
              },
              "Vary": {
                "schema": {
                  "type": "string"
                }
              },
              "expect-ct": {
                "schema": {
                  "type": "string"
                }
              },
              "referrer-policy": {
                "schema": {
                  "type": "string"
                }
              },
              "x-content-type-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-frame-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-xss-protection": {
                "schema": {
                  "type": "integer"
                }
              }
            },
            "content": {
              "application/json": {
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": {
                      "gasFee": 4.1342
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "gasFee": {
                      "type": "number",
                      "example": 4.1342,
                      "default": 0
                    },
                    "gasToken": {
                      "type": "string"
                    }
                  }
                }
              }
            }
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "description": "This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.\n\nA successful POST request typically returns a `200 OK` or `201 Created` response code.",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "token": {
                    "type": "string",
                    "description": "The stablecoin and network combination used for sending (e.g. USDC_SOL, USDT_TRC20). Determines which blockchain fee to calculate."
                  }
                },
                "required": [
                  "token"
                ]
              },
              "examples": {
                "New Example": {
                  "summary": "New Example",
                  "value": {
                    "token": "USDT_TRC20"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Create Send Transaction

# Create Send Transaction

Initiate a send transaction from vault.

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/sends": {
      "post": {
        "summary": "Create Send Transaction",
        "tags": [
          "Transactions"
        ],
        "responses": {
          "201": {
            "description": "Create Send Transaction",
            "headers": {
              "Date": {
                "schema": {
                  "type": "string"
                }
              },
              "Content-Length": {
                "schema": {
                  "type": "integer"
                }
              },
              "Connection": {
                "schema": {
                  "type": "string"
                }
              },
              "CF-RAY": {
                "schema": {
                  "type": "integer"
                }
              },
              "x-amzn-requestid": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-origin": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amz-apigw-id": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-trace-id": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-credentials": {
                "schema": {
                  "type": "boolean"
                }
              },
              "cf-cache-status": {
                "schema": {
                  "type": "string"
                }
              },
              "Set-Cookie": {
                "schema": {
                  "type": "string"
                }
              },
              "Strict-Transport-Security": {
                "schema": {
                  "type": "string"
                }
              },
              "expect-ct": {
                "schema": {
                  "type": "string"
                }
              },
              "referrer-policy": {
                "schema": {
                  "type": "string"
                }
              },
              "x-content-type-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-frame-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-xss-protection": {
                "schema": {
                  "type": "integer"
                }
              },
              "X-Hiring": {
                "schema": {
                  "type": "string"
                }
              },
              "Server": {
                "schema": {
                  "type": "string"
                }
              }
            },
            "content": {
              "application/json": {
                "examples": {
                  "Created": {
                    "summary": "Created",
                    "value": {
                      "id": "f16f278b-1313-50eb-a511-46ed296c68ec",
                      "sequenceId": "14d7ca44-afad-4d08-97d2-e98de10dfaf-04",
                      "partnerId": "06b3054b-1ac5-42c6-8687-d2195c1f0e4b",
                      "amount": 10,
                      "networkFee": 0,
                      "token": "USDT_TRC20",
                      "countryCode": "NG",
                      "type": "send",
                      "status": "created",
                      "destinationAddress": "9343af1f-cca4-448c-b460-b178c6dbe34f",
                      "destinationType": "INTERNAL",
                      "destinationVaultId": "9343af1f-cca4-448c-b460-b178c6dbe34f",
                      "sourceAddress": "15f62532-a28d-42fd-9997-cdc2876cce13",
                      "sourceVaultId": "15f62532-a28d-42fd-9997-cdc2876cce13",
                      "createdAt": 1761868420068,
                      "updatedAt": 1761868420068
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "description": "id"
                    },
                    "sequenceId": {
                      "type": "string"
                    },
                    "partnerId": {
                      "type": "string"
                    },
                    "amount": {
                      "type": "integer"
                    },
                    "networkFee": {
                      "type": "integer"
                    },
                    "token": {
                      "type": "string"
                    },
                    "currency": {
                      "type": "string"
                    },
                    "network": {
                      "type": "string"
                    },
                    "type": {
                      "type": "string"
                    },
                    "status": {
                      "type": "string"
                    },
                    "destinationAddress": {
                      "type": "string"
                    },
                    "destinationType": {
                      "type": "string"
                    },
                    "destinationVaultId": {
                      "type": "string"
                    },
                    "sourceAddress": {
                      "type": "string"
                    },
                    "sourceVaultId": {
                      "type": "string"
                    },
                    "createdAt": {
                      "type": "string",
                      "format": "date-time"
                    },
                    "updatedAt": {
                      "type": "string",
                      "format": "date-time"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "ValidationError"
                    },
                    "message": {
                      "type": "string",
                      "example": "vault id not found"
                    }
                  }
                },
                "examples": {
                  "Bad Request": {
                    "summary": "Bad Request",
                    "value": {
                      "code": "ValidationError",
                      "message": "vault id not found"
                    }
                  }
                }
              }
            },
            "description": "Bad Request"
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "token": {
                    "type": "string",
                    "description": "The stablecoin identifier to transfer (e.g. USDT_TRC20, USDC_SOL)."
                  },
                  "vaultId": {
                    "type": "string",
                    "description": "The unique ID of the originating vault from which funds will be withdrawn.\nUSD_BALANCE is also acceptable here, to transfer from USD float balance to destination vault."
                  },
                  "amount": {
                    "type": "integer",
                    "description": "The transfer amount."
                  },
                  "sequenceId": {
                    "type": "string",
                    "description": "A unique client-generated reference used to ensure idempotency and prevent duplicate transfers."
                  },
                  "destination": {
                    "type": "object",
                    "properties": {
                      "type": {
                        "type": "string",
                        "description": "INTERNAL is used when transferring from one vault to another vault.\nEXTERNAL is used when transferring to external wallet addresses.\nUSD_BALANCE is used when topping up USD Float balance from a vault.",
                        "default": "INTERNAL",
                        "enum": [
                          "USD_BALANCE",
                          "INTERNAL",
                          "EXTERNAL"
                        ]
                      },
                      "address": {
                        "type": "string",
                        "description": "The blockchain wallet address."
                      },
                      "vaultId": {
                        "type": "string",
                        "description": "The internal vault ID to transfer funds to. Only required if INTERNAL."
                      }
                    },
                    "required": [
                      "type",
                      "address"
                    ],
                    "description": "The destination details for the transfer. The structure varies depending on transfer type (on-chain, internal vault, etc.)."
                  },
                  "countryCode": {
                    "type": "string",
                    "description": "Recipient country code. e.g. NG",
                    "default": "NG"
                  },
                  "travelRuleData": {
                    "type": "string",
                    "description": "Travel rule data based on travel rule config for recipient country code."
                  }
                },
                "required": [
                  "token",
                  "vaultId",
                  "amount",
                  "sequenceId",
                  "destination",
                  "countryCode",
                  "travelRuleData"
                ]
              },
              "examples": {
                "New Example": {
                  "summary": "New Example",
                  "value": {
                    "token": "USDT_TRC20",
                    "vaultId": "ec96d00e-67d3-4da0-8022-cf267f7e67e5",
                    "amount": 15,
                    "countryCode": "NG",
                    "sequenceId": "14d7ca44-afad-4d08-97d2-e98de10dfaf-22",
                    "destination": {
                      "type": "EXTERNAL",
                      "address": "TP8iP5xDUaSu92gViDEaz2Ps6aAinRn6iX"
                    }
                  }
                }
              }
            }
          }
        },
        "description": "Initiate a send transaction from vault."
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Get Transactions

# Get Transactions

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/sends": {
      "get": {
        "summary": "Get Transactions",
        "tags": [
          "Transactions"
        ],
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": {
                      "transactions": [
                        {
                          "id": "7166cbdf-2f31-52df-a945-c503779577d1",
                          "sequenceId": "fe0d2370-3611-4497-a31d-33062ff449d2",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "b0f6911f62f765966d1775e3a2dd88416bf69ca11779c963890cd842b1c9023c",
                          "externalId": "837fc557-89e0-4751-a432-b0fa13646ee0",
                          "amount": "25.00",
                          "networkFee": "3.08424",
                          "token": "USDT_TRC20",
                          "currency": "USDT",
                          "network": "TRC20",
                          "type": "send",
                          "status": "complete",
                          "destinationType": "INTERNAL",
                          "sourceAddress": "TMSkxBZpzhEQJHtSoz9QLwTf75LbVsC3ar",
                          "destinationAddress": "a0c829c9-ce1f-4123-9b1d-096b475c3b09",
                          "destinationTag": "",
                          "sourceVaultId": "f9fa9aef-449e-46af-a677-3eabda0d1598",
                          "destinationVaultId": "a0c829c9-ce1f-4123-9b1d-096b475c3b09",
                          "apiKey": "4111b96e14fc39039bb4e4540f2cf670",
                          "countryCode": "NG",
                          "travelRuleData": {},
                          "error": "",
                          "createdAt": "2026-02-22T19:15:49.082Z",
                          "updatedAt": "2026-02-22T19:16:30.347Z"
                        },
                        {
                          "id": "7dc5ece9-92b7-5b0c-b0a3-aae0cb9e2f19",
                          "sequenceId": "7c78d0bc-0846-4777-8932-dab484446721",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "2d90c363d0944089d87802c34db526a9f4661e0302820a533d522bdb35746e08",
                          "externalId": "2b8b915c-e44e-4e0b-9599-5297f9035bb8",
                          "amount": "1.00",
                          "networkFee": "5.88924",
                          "token": "USDT_TRC20",
                          "currency": "USDT",
                          "network": "TRC20",
                          "type": "send",
                          "status": "complete",
                          "destinationType": "INTERNAL",
                          "sourceAddress": "TMSkxBZpzhEQJHtSoz9QLwTf75LbVsC3ar",
                          "destinationAddress": "a0c829c9-ce1f-4123-9b1d-096b475c3b09",
                          "destinationTag": "",
                          "sourceVaultId": "f9fa9aef-449e-46af-a677-3eabda0d1598",
                          "destinationVaultId": "a0c829c9-ce1f-4123-9b1d-096b475c3b09",
                          "apiKey": "4111b96e14fc39039bb4e4540f2cf670",
                          "countryCode": "NG",
                          "travelRuleData": {},
                          "error": "",
                          "createdAt": "2026-02-22T19:10:50.124Z",
                          "updatedAt": "2026-02-22T19:11:33.215Z"
                        },
                        {
                          "id": "12fcf8d7-6011-58c8-ae72-0e15acb68982",
                          "sequenceId": "14d7ca44-afad-4d08-97d2-e98de10dfaf-60",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "114a3567f326f63c2097b6d3578890ba461d523f1502b89081aca9cece5faa83",
                          "externalId": "4b81fe94-7324-5903-9989-ab60765eae77",
                          "amount": "45.00",
                          "networkFee": "2.73945",
                          "token": "USDT_TRC20",
                          "currency": "USDT",
                          "network": "TRC20",
                          "type": "send",
                          "status": "complete",
                          "destinationType": "EXTERNAL",
                          "sourceAddress": "TMSkxBZpzhEQJHtSoz9QLwTf75LbVsC3ar",
                          "destinationAddress": "TP8iP5xDUaSu92gViDEaz2Ps6aAinRn6iX",
                          "destinationTag": "",
                          "sourceVaultId": "f9fa9aef-449e-46af-a677-3eabda0d1598",
                          "destinationVaultId": "",
                          "apiKey": "90c0cce7fb5cb8820f516fe7afe447fc",
                          "countryCode": "NG",
                          "travelRuleData": {
                            "firstName": "James",
                            "lastName": "Falola"
                          },
                          "error": "",
                          "createdAt": "2026-01-14T11:44:14.444Z",
                          "updatedAt": "2026-01-14T11:46:51.530Z"
                        },
                        {
                          "id": "6c6cc1a1-a26d-568c-ab14-9286f7a100b5",
                          "sequenceId": "c177b17e-99d4-52cf-b7cc-d7d4c8b7fcfc",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "",
                          "externalId": "c177b17e-99d4-52cf-b7cc-d7d4c8b7fcfc",
                          "amount": "200.00",
                          "networkFee": "",
                          "token": "USDT_TRC20",
                          "currency": "USDT",
                          "network": "TRC20",
                          "type": "receive",
                          "status": "complete",
                          "destinationType": "INTERNAL",
                          "sourceAddress": "TP8iP5xDUaSu92gViDEaz2Ps6aAinRn6iX",
                          "destinationAddress": "TMSkxBZpzhEQJHtSoz9QLwTf75LbVsC3ar",
                          "destinationTag": "",
                          "sourceVaultId": "",
                          "destinationVaultId": "",
                          "apiKey": "",
                          "countryCode": "",
                          "travelRuleData": {},
                          "error": "",
                          "createdAt": "2026-01-14T11:43:50.880Z",
                          "updatedAt": "2026-01-14T11:43:50.880Z"
                        },
                        {
                          "id": "02924fda-f5ac-52db-a873-eb98b899bdad",
                          "sequenceId": "14d7ca44-afad-4d08-97d2-e98de10dfaf-59",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "",
                          "externalId": "",
                          "amount": "20.00",
                          "networkFee": "0.00",
                          "token": "USDT_TRC20",
                          "currency": "USDT",
                          "network": "TRC20",
                          "type": "send",
                          "status": "failed",
                          "destinationType": "EXTERNAL",
                          "sourceAddress": "TMSkxBZpzhEQJHtSoz9QLwTf75LbVsC3ar",
                          "destinationAddress": "TP8iP5xDUaSu92gViDEaz2Ps6aAinRn6iX",
                          "destinationTag": "",
                          "sourceVaultId": "f9fa9aef-449e-46af-a677-3eabda0d1598",
                          "destinationVaultId": "",
                          "apiKey": "90c0cce7fb5cb8820f516fe7afe447fc",
                          "countryCode": "NG",
                          "travelRuleData": {
                            "firstName": "James",
                            "lastName": "Falola"
                          },
                          "error": "insufficient TRX balance for gas fee. required: 4.2294, available: 0",
                          "createdAt": "2026-01-14T11:34:32.991Z",
                          "updatedAt": "2026-01-14T11:34:35.374Z"
                        },
                        {
                          "id": "ed91e1fc-d5b3-509d-9a81-8a776da772a5",
                          "sequenceId": "14d7ca44-afad-4d08-97d2-e98de10dfaf-58",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "",
                          "externalId": "",
                          "amount": "20.00",
                          "networkFee": "0.00",
                          "token": "USDT_TRC20",
                          "currency": "USDT",
                          "network": "TRC20",
                          "type": "send",
                          "status": "failed",
                          "destinationType": "EXTERNAL",
                          "sourceAddress": "TL39TM5ZJjhRuv5pZYEcBaRrhAXGbJFM8Q",
                          "destinationAddress": "TP8iP5xDUaSu92gViDEaz2Ps6aAinRn6iX",
                          "destinationTag": "",
                          "sourceVaultId": "a0c829c9-ce1f-4123-9b1d-096b475c3b09",
                          "destinationVaultId": "",
                          "apiKey": "90c0cce7fb5cb8820f516fe7afe447fc",
                          "countryCode": "NG",
                          "travelRuleData": {
                            "firstName": "James",
                            "lastName": "Falola"
                          },
                          "error": "insufficient TRX balance for gas fee. required: 4.2294, available: 0",
                          "createdAt": "2026-01-14T11:32:24.575Z",
                          "updatedAt": "2026-01-14T11:32:27.133Z"
                        },
                        {
                          "id": "ea64fe8f-6656-5d61-b30f-52a6ecdd407f",
                          "sequenceId": "14d7ca44-afad-4d08-97d2-e98de10dfaf-56",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "",
                          "externalId": "",
                          "amount": "20.00",
                          "networkFee": "0.00",
                          "token": "USDT_TRC20",
                          "currency": "USDT",
                          "network": "TRC20",
                          "type": "send",
                          "status": "failed",
                          "destinationType": "EXTERNAL",
                          "sourceAddress": "TL39TM5ZJjhRuv5pZYEcBaRrhAXGbJFM8Q",
                          "destinationAddress": "TP8iP5xDUaSu92gViDEaz2Ps6aAinRn6iX",
                          "destinationTag": "",
                          "sourceVaultId": "a0c829c9-ce1f-4123-9b1d-096b475c3b09",
                          "destinationVaultId": "",
                          "apiKey": "90c0cce7fb5cb8820f516fe7afe447fc",
                          "countryCode": "NG",
                          "travelRuleData": {
                            "firstName": "James",
                            "lastName": "Falola"
                          },
                          "error": "insufficient TRX balance for gas fee. required: 4.235, available: 0",
                          "createdAt": "2026-01-14T10:59:52.763Z",
                          "updatedAt": "2026-01-14T10:59:58.184Z"
                        },
                        {
                          "id": "6fb8205f-0307-5937-95cf-3b5a69d0a979",
                          "sequenceId": "14d7ca44-afad-4d08-97d2-e98de10dfaf-55",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "",
                          "externalId": "",
                          "amount": "20.00",
                          "networkFee": "0.00",
                          "token": "USDT_TRC20",
                          "currency": "USDT",
                          "network": "TRC20",
                          "type": "send",
                          "status": "failed",
                          "destinationType": "EXTERNAL",
                          "sourceAddress": "a0c829c9-ce1f-4123-9b1d-096b475c3b09",
                          "destinationAddress": "TP8iP5xDUaSu92gViDEaz2Ps6aAinRn6iX",
                          "destinationTag": "",
                          "sourceVaultId": "a0c829c9-ce1f-4123-9b1d-096b475c3b09",
                          "destinationVaultId": "",
                          "apiKey": "90c0cce7fb5cb8820f516fe7afe447fc",
                          "countryCode": "NG",
                          "travelRuleData": {
                            "firstName": "James",
                            "lastName": "Falola"
                          },
                          "error": "insufficient TRX balance for gas fee. required: 4.235, available: 0",
                          "createdAt": "2026-01-14T10:48:13.300Z",
                          "updatedAt": "2026-01-14T10:48:16.236Z"
                        },
                        {
                          "id": "78514c1a-4b37-57e9-a074-eb60ff315062",
                          "sequenceId": "4ea8b29a-9862-43ee-a39c6-bd4c450c346d",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "iFHKf2sjqWgpARiY48hMhb9SrHrwsuGXgajzU3a92HgQeatX82pvXe4XYzH5K2YSVxjif9fEQgT7H5vHTXbDvwS",
                          "externalId": "cb74acfc-5559-4e47-9c0e-f79501482ddf",
                          "amount": "0.50",
                          "networkFee": "0.002049582",
                          "token": "USDC_SOL",
                          "currency": "USDC",
                          "network": "SOL",
                          "type": "send",
                          "status": "complete",
                          "destinationType": "INTERNAL",
                          "sourceAddress": "840e884c-c194-42d1-9d7e-924eac2a6520",
                          "destinationAddress": "8wqBZXYJqEaAV6adSb1aF1eCX2xJKCdH6HKJ57tPsaZv",
                          "destinationTag": "",
                          "sourceVaultId": "840e884c-c194-42d1-9d7e-924eac2a6520",
                          "destinationVaultId": "cab7c80e-66b3-420d-acd0-5ef4b3930e1a",
                          "apiKey": "a228b6b2a07ee85c980d43edad8a3695",
                          "countryCode": "",
                          "travelRuleData": {},
                          "error": "",
                          "createdAt": "2026-01-12T16:11:04.457Z",
                          "updatedAt": "2026-01-12T16:11:16.851Z"
                        },
                        {
                          "id": "7ad95972-7db5-56fd-9440-cb7f6fdb50d6",
                          "sequenceId": "3b0c3f2a-281e-51b2-9995-c40c17235477",
                          "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                          "transactionHash": "",
                          "externalId": "3b0c3f2a-281e-51b2-9995-c40c17235477",
                          "amount": "1.00",
                          "networkFee": "",
                          "token": "SOL_SOL",
                          "currency": "SOL",
                          "network": "SOL",
                          "type": "receive",
                          "status": "complete",
                          "destinationType": "INTERNAL",
                          "sourceAddress": "9B5XszUGdMaxCZ7uSQhPzdks5ZQSmWxrmzCSvtJ6Ns6g",
                          "destinationAddress": "3iJJmbUw6hYHxsztdrpnkTzhuvVaKDkXvmDyse9UQ3Mg",
                          "destinationTag": "",
                          "sourceVaultId": "",
                          "destinationVaultId": "",
                          "apiKey": "",
                          "countryCode": "",
                          "travelRuleData": {},
                          "error": "",
                          "createdAt": "2026-01-12T16:09:51.466Z",
                          "updatedAt": "2026-01-12T16:09:51.466Z"
                        }
                      ],
                      "pagination": {
                        "pageSize": 10,
                        "nextCursor": "WzE3NjgyMzQxOTE0NjYsIjdhZDk1OTcyLTdkYjUtNTZmZC05NDQwLWNiN2Y2ZmRiNTBkNiJd",
                        "total": 12
                      }
                    }
                  }
                }
              }
            },
            "description": "OK"
          },
          "201": {
            "description": "Create Send Transaction",
            "headers": {
              "Date": {
                "schema": {
                  "type": "string"
                }
              },
              "Content-Length": {
                "schema": {
                  "type": "integer"
                }
              },
              "Connection": {
                "schema": {
                  "type": "string"
                }
              },
              "CF-RAY": {
                "schema": {
                  "type": "integer"
                }
              },
              "x-amzn-requestid": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-origin": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amz-apigw-id": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-trace-id": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-credentials": {
                "schema": {
                  "type": "boolean"
                }
              },
              "cf-cache-status": {
                "schema": {
                  "type": "string"
                }
              },
              "Set-Cookie": {
                "schema": {
                  "type": "string"
                }
              },
              "Strict-Transport-Security": {
                "schema": {
                  "type": "string"
                }
              },
              "expect-ct": {
                "schema": {
                  "type": "string"
                }
              },
              "referrer-policy": {
                "schema": {
                  "type": "string"
                }
              },
              "x-content-type-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-frame-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-xss-protection": {
                "schema": {
                  "type": "integer"
                }
              },
              "X-Hiring": {
                "schema": {
                  "type": "string"
                }
              },
              "Server": {
                "schema": {
                  "type": "string"
                }
              }
            },
            "content": {
              "application/json": {
                "examples": {
                  "": {
                    "summary": "",
                    "value": {
                      "id": "f16f278b-1313-50eb-a511-46ed296c68ec",
                      "sequenceId": "14d7ca44-afad-4d08-97d2-e98de10dfaf-04",
                      "partnerId": "06b3054b-1ac5-42c6-8687-d2195c1f0e4b",
                      "amount": 10,
                      "networkFee": 0,
                      "token": "USDT_TRC20",
                      "countryCode": "NG",
                      "type": "send",
                      "status": "created",
                      "destinationAddress": "9343af1f-cca4-448c-b460-b178c6dbe34f",
                      "destinationType": "INTERNAL",
                      "destinationVaultId": "9343af1f-cca4-448c-b460-b178c6dbe34f",
                      "sourceAddress": "15f62532-a28d-42fd-9997-cdc2876cce13",
                      "sourceVaultId": "15f62532-a28d-42fd-9997-cdc2876cce13",
                      "createdAt": 1761868420068,
                      "updatedAt": 1761868420068
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "name": {
                      "type": "string",
                      "description": "id"
                    },
                    "sequenceId": {
                      "type": "string"
                    },
                    "partnerId": {
                      "type": "string"
                    },
                    "amount": {
                      "type": "integer"
                    },
                    "networkFee": {
                      "type": "integer"
                    },
                    "token": {
                      "type": "string"
                    },
                    "currency": {
                      "type": "string"
                    },
                    "network": {
                      "type": "string"
                    },
                    "type": {
                      "type": "string"
                    },
                    "status": {
                      "type": "string"
                    },
                    "destinationAddress": {
                      "type": "string"
                    },
                    "destinationType": {
                      "type": "string"
                    },
                    "destinationVaultId": {
                      "type": "string"
                    },
                    "sourceAddress": {
                      "type": "string"
                    },
                    "sourceVaultId": {
                      "type": "string"
                    },
                    "createdAt": {
                      "type": "string",
                      "format": "date-time"
                    },
                    "updatedAt": {
                      "type": "string",
                      "format": "date-time"
                    }
                  }
                }
              }
            }
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "ValidationError"
                    },
                    "message": {
                      "type": "string",
                      "example": "vault id not found"
                    }
                  }
                },
                "examples": {
                  "Bad Request": {
                    "summary": "Bad Request",
                    "value": {
                      "code": "ValidationError",
                      "message": "vault id not found"
                    }
                  }
                }
              }
            },
            "description": "Bad Request"
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "operationId": "get_sends",
        "parameters": [
          {
            "in": "query",
            "name": "vaultId",
            "schema": {
              "type": "string",
              "default": "f9fa9aef-449e-46af-a677-3eabda0d1598"
            },
            "required": false,
            "description": "Returns transactions where the vault appears on either side — as the source or destination. Use this for a complete view of a vault's activity."
          },
          {
            "in": "query",
            "name": "sourceVaultId",
            "schema": {
              "type": "string",
              "default": "f9fa9aef-449e-46af-a677-3eabda0d1598"
            },
            "description": "Narrows results to transactions that originated from this specific vault."
          },
          {
            "in": "query",
            "name": "destinationVaultId",
            "schema": {
              "type": "string",
              "default": "f9fa9aef-449e-46af-a677-3eabda0d1598"
            },
            "description": "Narrows results to transactions where funds were sent to this specific vault."
          },
          {
            "in": "query",
            "name": "startDate",
            "schema": {
              "type": "string",
              "format": "date",
              "default": "2025-01-01T00:00:00.000Z"
            },
            "description": "Returns transactions created on or after this timestamp. \n"
          },
          {
            "in": "query",
            "name": "endDate",
            "schema": {
              "type": "string",
              "default": "2025-01-01T00:00:00.000Z"
            },
            "description": "Returns transactions created on or before this timestamp. "
          },
          {
            "in": "query",
            "name": "token\t",
            "schema": {
              "type": "string",
              "default": "USDT_TRC20"
            },
            "description": "Filters by the asset token used in the transaction. \n"
          },
          {
            "in": "query",
            "name": "status",
            "schema": {
              "type": "string",
              "default": "complete",
              "enum": [
                "created",
                "processing",
                "complete",
                "failed"
              ]
            },
            "description": "Filters by the current transaction status."
          },
          {
            "in": "query",
            "name": "sourceAddress",
            "schema": {
              "type": "string",
              "default": "TMSkxBZpzhEQJHtSoz9QLwTf75LbVsC3ar"
            },
            "description": "Filters by the on-chain wallet address from which the transaction was sent."
          },
          {
            "in": "query",
            "name": "pageSize",
            "schema": {
              "type": "string",
              "default": "15"
            },
            "description": "Number of transactions to return per page. Defaults to 15, maximum is 100.\n"
          },
          {
            "in": "query",
            "name": "cursor",
            "schema": {
              "type": "string",
              "default": "WzE3NjgyMzQxOTE0NjYsIjdhZDk1OTcyLTdkYjUtNTZmZC05NDQwLWNiN2Y2ZmRiNTBkNiJd"
            },
            "description": "Opaque pagination token returned in pagination.nextCursor from the previous response. Pass this value to retrieve the next page of results."
          }
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Get Send Transaction

# Get Send Transaction

This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.

A successful POST request typically returns a `200 OK` or `201 Created` response code.

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/sends/{id}": {
      "get": {
        "summary": "Get Send Transaction",
        "tags": [
          "Transactions"
        ],
        "responses": {
          "200": {
            "description": "Get Send Transaction",
            "headers": {
              "Date": {
                "schema": {
                  "type": "string"
                }
              },
              "Transfer-Encoding": {
                "schema": {
                  "type": "string"
                }
              },
              "Connection": {
                "schema": {
                  "type": "string"
                }
              },
              "Content-Encoding": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-requestid": {
                "schema": {
                  "type": "integer"
                }
              },
              "access-control-allow-origin": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amz-apigw-id": {
                "schema": {
                  "type": "string"
                }
              },
              "x-amzn-trace-id": {
                "schema": {
                  "type": "string"
                }
              },
              "access-control-allow-credentials": {
                "schema": {
                  "type": "boolean"
                }
              },
              "cf-cache-status": {
                "schema": {
                  "type": "string"
                }
              },
              "Strict-Transport-Security": {
                "schema": {
                  "type": "string"
                }
              },
              "expect-ct": {
                "schema": {
                  "type": "string"
                }
              },
              "referrer-policy": {
                "schema": {
                  "type": "string"
                }
              },
              "x-content-type-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-frame-options": {
                "schema": {
                  "type": "string"
                }
              },
              "x-xss-protection": {
                "schema": {
                  "type": "integer"
                }
              },
              "X-Hiring": {
                "schema": {
                  "type": "string"
                }
              },
              "Set-Cookie": {
                "schema": {
                  "type": "string"
                }
              },
              "Server": {
                "schema": {
                  "type": "string"
                }
              },
              "CF-RAY": {
                "schema": {
                  "type": "integer"
                }
              }
            },
            "content": {
              "application/json": {
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": {
                      "partnerId": "7882e37a-51c7-4e6f-80cc-4d9ca99e39ae",
                      "sourceAddress": "ec96d00e-67d3-4da0-8022-cf267f7e67e5",
                      "currency": "USDT",
                      "destinationType": "EXTERNAL",
                      "status": "complete",
                      "createdAt": "2025-10-31T17:41:38.833Z",
                      "sequenceId": "14d7ca44-afad-4d08-97d2-e98de10dfaf-22",
                      "network": "TRC20",
                      "externalId": "6b4778ab-e65d-531d-8bbe-373ae6edef18",
                      "token": "USDT_TRC20",
                      "updatedAt": "2025-10-31T17:44:11.042Z",
                      "destinationAddress": "TP8iP5xDUaSu92gViDEaz2Ps6aAinRn6iX",
                      "sourceVaultId": "ec96d00e-67d3-4da0-8022-cf267f7e67e5",
                      "amount": 15,
                      "networkFee": 3.08424,
                      "id": "ec409418-d074-527b-bee3-f37df419811c",
                      "transactionHash": "c2e903292295d8fd05a31b8b4e746426e613e57d6fa61517b28afb8ad415e152",
                      "type": "send"
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "amount": {
                      "type": "integer",
                      "example": 15,
                      "default": 0
                    },
                    "createdAt": {
                      "type": "string",
                      "example": "2025-10-31T17:41:38.833Z"
                    },
                    "currency": {
                      "type": "string",
                      "example": "USDT"
                    },
                    "destinationAddress": {
                      "type": "string",
                      "example": "TP8iP5xDUaSu92gViDEaz2Ps6aAinRn6iX"
                    },
                    "destinationType": {
                      "type": "string",
                      "example": "EXTERNAL"
                    },
                    "destinationVaultId": {
                      "type": "string"
                    },
                    "externalId": {
                      "type": "string",
                      "example": "6b4778ab-e65d-531d-8bbe-373ae6edef18"
                    },
                    "id": {
                      "type": "string",
                      "example": "ec409418-d074-527b-bee3-f37df419811c"
                    },
                    "network": {
                      "type": "string",
                      "example": "TRC20"
                    },
                    "networkFee": {
                      "type": "number",
                      "example": 3.08424,
                      "default": 0
                    },
                    "partnerId": {
                      "type": "string",
                      "example": "7882e37a-51c7-4e6f-80cc-4d9ca99e39ae"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "14d7ca44-afad-4d08-97d2-e98de10dfaf-22"
                    },
                    "sourceAddress": {
                      "type": "string",
                      "example": "ec96d00e-67d3-4da0-8022-cf267f7e67e5"
                    },
                    "sourceVaultId": {
                      "type": "string",
                      "example": "ec96d00e-67d3-4da0-8022-cf267f7e67e5"
                    },
                    "status": {
                      "type": "string",
                      "example": "complete"
                    },
                    "token": {
                      "type": "string",
                      "example": "USDT_TRC20"
                    },
                    "type": {
                      "type": "string",
                      "example": "send"
                    },
                    "updatedAt": {
                      "type": "string",
                      "example": "2025-10-31T17:44:11.042Z"
                    }
                  }
                }
              }
            }
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "code": {
                      "type": "string",
                      "example": "InternalServerError"
                    },
                    "message": {
                      "type": "string",
                      "example": "something went wrong"
                    }
                  }
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "description": "This is a POST request, submitting data to an API via the request body. This request submits JSON data, and the data is reflected in the response.\n\nA successful POST request typically returns a `200 OK` or `201 Created` response code.",
        "parameters": [
          {
            "in": "path",
            "name": "id",
            "schema": {
              "type": "string"
            },
            "required": true,
            "description": "Unique identifier of the sent trasaction."
          }
        ]
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Get travel rule config

# Get travel rule config

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/travel-rule/config": {
      "get": {
        "description": "",
        "responses": {
          "200": {
            "description": "",
            "content": {
              "application/json": {
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": {
                      "id": "config-550e8400-e29b-41d4-a716-446655440000",
                      "countryCode": "NG",
                      "minAmount": 1000,
                      "status": "ACTIVE",
                      "timeoutAction": "PROCEED",
                      "counterPartyRepair": "outgoing",
                      "repairWaitTime": 30,
                      "repairCount": 3,
                      "dataFields": [
                        {
                          "displayName": "Sender Full Name",
                          "fieldType": "string",
                          "required": true,
                          "payloadName": "senderName"
                        },
                        {
                          "displayName": "Sender Date of Birth",
                          "fieldType": "date",
                          "required": true,
                          "payloadName": "senderDob"
                        }
                      ]
                    }
                  }
                },
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "default": "Unique identifier for this travel rule configuration."
                    }
                  },
                  "required": [
                    "id"
                  ]
                }
              }
            }
          }
        },
        "parameters": [
          {
            "in": "query",
            "name": "countryCode",
            "schema": {
              "type": "string",
              "default": "ISO country code to retrieve the travel rule configuration for (e.g. NG, ZA, KE, US)."
            },
            "required": true
          }
        ],
        "operationId": "get_travel-rule-config",
        "summary": "Get travel rule config"
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Create Sub Wallet

# Create Sub Wallet

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/sub-wallets": {
      "post": {
        "description": "",
        "responses": {
          "201": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "example": "6959f27c-9886-536b-a276-e1f4c2e632db"
                    },
                    "partnerId": {
                      "type": "string",
                      "example": "d7fbe40a-6d50-4607-8648-9827a54947c3"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "6fb07a60-a2c2-5eb6-bb4b-6a91b04962b1"
                    },
                    "name": {
                      "type": "string",
                      "example": "USD Secondary III"
                    },
                    "metadata": {
                      "type": "object",
                      "properties": {}
                    },
                    "currency": {
                      "type": "string",
                      "example": "USD"
                    },
                    "status": {
                      "type": "string",
                      "example": "active"
                    },
                    "createdAt": {
                      "type": "integer",
                      "example": 1770719129967,
                      "default": 0
                    },
                    "updatedAt": {
                      "type": "integer",
                      "example": 1770719129967,
                      "default": 0
                    },
                    "availableBalance": {
                      "type": "integer",
                      "example": 0,
                      "default": 0
                    },
                    "virtualAccount": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "string",
                          "example": "4e6b711b-8952-4f83-a2ac-cff122082cb2"
                        },
                        "subwalletId": {
                          "type": "string",
                          "example": ""
                        },
                        "provider": {
                          "type": "string",
                          "example": "erebor"
                        },
                        "currency": {
                          "type": "string",
                          "example": "USD"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "37212851507366"
                        },
                        "routingNumber": {
                          "type": "string",
                          "example": "125109161"
                        },
                        "accountName": {
                          "type": "string",
                          "example": "Demo Business Checking"
                        },
                        "bankName": {
                          "type": "string",
                          "example": "Erebor Bank"
                        },
                        "bankAddress": {
                          "type": "string",
                          "example": ""
                        },
                        "swiftCode": {
                          "type": "string",
                          "example": ""
                        },
                        "status": {
                          "type": "string",
                          "example": "ACTIVE"
                        },
                        "depositInstructions": {
                          "type": "object",
                          "properties": {
                            "swift": {
                              "type": "object",
                              "properties": {
                                "memoTemplate": {
                                  "type": "string",
                                  "example": "FFC <account holder name> <account number>"
                                },
                                "memo": {
                                  "type": "string",
                                  "example": "FFC Demo Business Checking 37212851507366"
                                },
                                "bankName": {
                                  "type": "string",
                                  "example": "Erebor Bank. N.A"
                                },
                                "accountNumber": {
                                  "type": "string",
                                  "example": "2908175093"
                                },
                                "bic": {
                                  "type": "string",
                                  "example": "CHASUS33"
                                },
                                "bankAddress": {
                                  "type": "string",
                                  "example": "500 Neil Ave, Ste 140 Columbus, OH 43215 US"
                                }
                              }
                            }
                          }
                        },
                        "virtualAccountType": {
                          "type": "string",
                          "example": "third_party"
                        },
                        "recordType": {
                          "type": "string",
                          "example": "viban"
                        },
                        "createdAt": {
                          "type": "string",
                          "example": "2026-07-14T18:10:59.033Z"
                        },
                        "updatedAt": {
                          "type": "string",
                          "example": "2026-07-14T18:10:59.033Z"
                        }
                      }
                    }
                  }
                },
                "examples": {
                  "Created": {
                    "summary": "Created",
                    "value": {
                      "id": "6959f27c-9886-536b-a276-e1f4c2e632db",
                      "partnerId": "d7fbe40a-6d50-4607-8648-9827a54947c3",
                      "sequenceId": "6fb07a60-a2c2-5eb6-bb4b-6a91b04962b1",
                      "name": "USD Secondary III",
                      "metadata": {},
                      "currency": "USD",
                      "status": "active",
                      "createdAt": 1770719129967,
                      "updatedAt": 1770719129967,
                      "availableBalance": 0,
                      "virtualAccount": {
                        "id": "4e6b711b-8952-4f83-a2ac-cff122082cb2",
                        "subwalletId": "",
                        "provider": "erebor",
                        "currency": "USD",
                        "accountNumber": "37212851507366",
                        "routingNumber": "125109161",
                        "accountName": "Demo Business Checking",
                        "bankName": "Erebor Bank",
                        "bankAddress": "",
                        "swiftCode": "",
                        "status": "ACTIVE",
                        "depositInstructions": {
                          "swift": {
                            "memoTemplate": "FFC <account holder name> <account number>",
                            "memo": "FFC Demo Business Checking 37212851507366",
                            "bankName": "Erebor Bank. N.A",
                            "accountNumber": "2908175093",
                            "bic": "CHASUS33",
                            "bankAddress": "500 Neil Ave, Ste 140 Columbus, OH 43215 US"
                          }
                        },
                        "virtualAccountType": "third_party",
                        "recordType": "viban",
                        "createdAt": "2026-07-14T18:10:59.033Z",
                        "updatedAt": "2026-07-14T18:10:59.033Z"
                      }
                    }
                  }
                }
              }
            },
            "description": "Created"
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "Bad Request": {
                    "summary": "Bad Request",
                    "value": {
                      "code": "ValidationError",
                      "message": "wallet with sequenceId james-uuid-test-3 and currency NGN already exists"
                    }
                  }
                }
              }
            },
            "description": "Bad Request"
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "parameters": [],
        "operationId": "post_sub-wallets",
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "Wallet name. e.g. NGN Trading ",
                    "default": "NGN Trading"
                  },
                  "sequenceId": {
                    "type": "string",
                    "default": "6fb07a60-a2c2-5eb6-bb4b-6a91b04962b1",
                    "description": "Unique wallet identifier / idempotency key"
                  },
                  "currency": {
                    "type": "string",
                    "description": "YC Supported fiat currency. e.g. NGN, KES",
                    "default": "NGN"
                  },
                  "createVirtualAccount": {
                    "type": "boolean",
                    "default": "false",
                    "description": " When true, creates a virtual bank account linked to the sub-wallet"
                  }
                },
                "required": [
                  "sequenceId",
                  "name",
                  "currency"
                ]
              },
              "examples": {
                "New Example": {
                  "summary": "New Example",
                  "value": {
                    "name": "USD Secondary III",
                    "currency": "USD",
                    "sequenceId": "6fb07a60-a2c2-5eb6-bb4b-6a91b04962b1"
                  }
                }
              }
            }
          }
        },
        "summary": "Create Sub Wallet"
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

List Sub Wallets

# List Sub Wallets

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/sub-wallets": {
      "get": {
        "description": "",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": {
                      "subwallets": [
                        {
                          "id": "550e8400-e29b-41d4-a716-446655440000",
                          "partnerId": "partner-123",
                          "sequenceId": "customer-123",
                          "name": "Customer NGN Wallet",
                          "currency": "NGN",
                          "status": "active",
                          "availableBalance": 1500.5,
                          "metadata": {
                            "customerId": "12345"
                          },
                          "createdAt": "2024-01-15T10:30:00Z",
                          "updatedAt": "2024-01-15T14:25:00Z",
                          "virtualAccount": {
                            "id": "va-550e8400-e29b-41d4-a716-446655440000",
                            "userId": "partner-123",
                            "subwalletId": "550e8400-e29b-41d4-a716-446655440000",
                            "currency": "USD",
                            "accountNumber": "1234567890",
                            "routingNumber": "021000021",
                            "accountName": "Partner Corp",
                            "bankName": "Example Bank",
                            "bankAddress": "123 Main St, New York, NY 10001",
                            "swiftCode": "EXAMUS33",
                            "status": "ACTIVE",
                            "createdAt": "2024-01-15T10:30:00Z",
                            "updatedAt": "2024-01-15T14:25:00Z"
                          }
                        }
                      ],
                      "pagination": {
                        "pageSize": 10,
                        "nextCursor": "WzE3NjgyMzQxOTE0NjYsIjdhZDk1OTcyLTdkYjUtNTZmZC05NDQwLWNiN2Y2ZmRiNTBkNiJd",
                        "total": 12
                      }
                    }
                  }
                }
              }
            },
            "description": "OK"
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "parameters": [
          {
            "in": "query",
            "name": "withVirtualAccount\t",
            "schema": {
              "type": "boolean",
              "default": "false"
            },
            "description": "Set to true to include the linked virtual bank account details on each sub-wallet in the response.\n"
          },
          {
            "in": "query",
            "name": "pageSize",
            "schema": {
              "type": "string",
              "default": "15"
            },
            "description": "Number of transactions to return per page. Defaults to 15, maximum is 100."
          },
          {
            "in": "query",
            "name": "cursor",
            "schema": {
              "type": "string"
            },
            "description": "Opaque pagination token returned in pagination.nextCursor from the previous response. Pass this value to retrieve the next page of results."
          }
        ],
        "summary": "List Sub Wallets",
        "operationId": "get_sub-wallets"
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Get Sub Wallet by ID

# Get Sub Wallet by ID

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/sub-wallets/{id}": {
      "get": {
        "description": "",
        "responses": {
          "200": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "id": {
                      "type": "string",
                      "example": "6fb07a60-a2c2-5eb6-bb4b-6a91b04962b1"
                    },
                    "partnerId": {
                      "type": "string",
                      "example": "9b821520-52d4-4e91-990c-b2f5452cbc2d"
                    },
                    "sequenceId": {
                      "type": "string",
                      "example": "james-uuid-test-3"
                    },
                    "name": {
                      "type": "string",
                      "example": "NGN Primary"
                    },
                    "metadata": {
                      "type": "object",
                      "properties": {}
                    },
                    "currency": {
                      "type": "string",
                      "example": "NGN"
                    },
                    "status": {
                      "type": "string",
                      "example": "active"
                    },
                    "createdAt": {
                      "type": "integer",
                      "example": 1768578971832,
                      "default": 0
                    },
                    "updatedAt": {
                      "type": "integer",
                      "example": 1768578971832,
                      "default": 0
                    },
                    "availableBalance": {
                      "type": "integer",
                      "example": 0,
                      "default": 0
                    },
                    "virtualAccount": {
                      "type": "object",
                      "properties": {
                        "id": {
                          "type": "string",
                          "example": "d7fbe40a-6d50-4607-8648-9827a54947c3"
                        },
                        "subwalletId": {
                          "type": "string",
                          "example": "6959f27c-9886-536b-a276-e1f4c2e632db"
                        },
                        "provider": {
                          "type": "string",
                          "example": "erebor"
                        },
                        "currency": {
                          "type": "string",
                          "example": "USD"
                        },
                        "accountNumber": {
                          "type": "string",
                          "example": "1234567890"
                        },
                        "routingNumber": {
                          "type": "string",
                          "example": "125108405"
                        },
                        "swiftCode": {
                          "type": "string",
                          "example": "12345"
                        },
                        "accountName": {
                          "type": "string",
                          "example": "Primary Account Number"
                        },
                        "bankName": {
                          "type": "string",
                          "example": "Erebor Bank"
                        },
                        "bankAddress": {
                          "type": "string",
                          "example": ""
                        },
                        "status": {
                          "type": "string",
                          "example": "PENDING"
                        }
                      },
                      "description": "Returned if `withVirtualAccount` is true"
                    }
                  }
                },
                "examples": {
                  "OK": {
                    "summary": "OK",
                    "value": {
                      "id": "6fb07a60-a2c2-5eb6-bb4b-6a91b04962b1",
                      "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                      "sequenceId": "james-uuid-test-3",
                      "name": "NGN Primary",
                      "metadata": {},
                      "currency": "NGN",
                      "status": "active",
                      "createdAt": 1768578971832,
                      "updatedAt": 1768578971832,
                      "availableBalance": 0,
                      "virtualAccount": {
                        "id": "d7fbe40a-6d50-4607-8648-9827a54947c3",
                        "subwalletId": "6959f27c-9886-536b-a276-e1f4c2e632db",
                        "provider": "erebor",
                        "currency": "USD",
                        "accountNumber": "1234567890",
                        "routingNumber": "125108405",
                        "swiftCode": "12345",
                        "accountName": "Primary Account Number",
                        "bankName": "Erebor Bank",
                        "bankAddress": "",
                        "status": "PENDING"
                      }
                    }
                  }
                }
              }
            },
            "description": "OK"
          },
          "201": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "Success": {
                    "summary": "Success",
                    "value": {
                      "id": "6fb07a60-a2c2-5eb6-bb4b-6a91b04962b1",
                      "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                      "sequenceId": "james-uuid-test-3",
                      "name": "NGN Primary",
                      "metadata": {},
                      "currency": "NGN",
                      "status": "active",
                      "createdAt": 1768578971832,
                      "updatedAt": 1768578971832,
                      "availableBalance": 0
                    }
                  }
                }
              }
            },
            "description": "Created"
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "Bad Request": {
                    "summary": "Bad Request",
                    "value": {
                      "code": "ValidationError",
                      "message": "invalid wallet id"
                    }
                  }
                }
              }
            },
            "description": "Bad Request"
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "parameters": [
          {
            "in": "path",
            "name": "id",
            "schema": {
              "type": "string"
            },
            "required": true
          },
          {
            "in": "query",
            "name": "withVirtualAccount",
            "schema": {
              "type": "boolean",
              "default": "false"
            },
            "description": "When true, includes virtual bank account data for the sub-wallet in the response"
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "Wallet name. e.g. NGN Trading ",
                    "default": "NGN Trading"
                  },
                  "sequenceId": {
                    "type": "string",
                    "default": "6fb07a60-a2c2-5eb6-bb4b-6a91b04962b1",
                    "description": "Unique wallet identifier / idempotency key"
                  },
                  "currency": {
                    "type": "string",
                    "description": "YC Supported fiat currency. e.g. NGN, KES",
                    "default": "NGN"
                  }
                },
                "required": [
                  "sequenceId",
                  "name",
                  "currency"
                ]
              },
              "examples": {}
            }
          }
        },
        "summary": "Get Sub Wallet by ID",
        "operationId": "get_sub-wallets-id"
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```

Update Sub Wallet

# Update Sub Wallet

# OpenAPI definition

```json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Custody as a Service",
    "version": "1.0.0",
    "description": "Custody as a Service provides a simple API for managing vaults and generating addresses. This collection demonstrates how to perform basic CRUD operations and interact with the custody service endpoints.\n\n## 📋 API Endpoints Overview\n\n| Method | Path | Name | Description |\n| --- | --- | --- | --- |\n| POST | /vaults | Create Vault | Submits JSON data to create a new vault. |\n| GET | /vaults | Get Vaults | Retrieves a list of vaults. |\n| GET | /vaults/{id} | Get Vault by ID | Retrieves details of a specific vault by its ID. |\n| POST | /addresses | Generate Address | Generates a new address. |"
  },
  "servers": [
    {
      "url": "https://sandbox.api.yellowcard.io/business"
    }
  ],
  "paths": {
    "/sub-wallets/{id}": {
      "patch": {
        "description": "",
        "responses": {
          "201": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "Created": {
                    "summary": "Created",
                    "value": {
                      "id": "6fb07a60-a2c2-5eb6-bb4b-6a91b04962b1",
                      "partnerId": "9b821520-52d4-4e91-990c-b2f5452cbc2d",
                      "sequenceId": "james-uuid-test-3",
                      "name": "NGN Primary",
                      "metadata": {},
                      "currency": "NGN",
                      "status": "active",
                      "createdAt": 1768578971832,
                      "updatedAt": 1768578971832,
                      "availableBalance": 0
                    }
                  }
                }
              }
            },
            "description": "Created"
          },
          "400": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "Bad Request": {
                    "summary": "Bad Request",
                    "value": {
                      "code": "ValidationError",
                      "message": "wallet with sequenceId james-uuid-test-3 and currency NGN already exists"
                    }
                  }
                }
              }
            },
            "description": "Bad Request"
          },
          "500": {
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {}
                },
                "examples": {
                  "Internal Server Error": {
                    "summary": "Internal Server Error",
                    "value": {
                      "code": "InternalServerError",
                      "message": "something went wrong"
                    }
                  }
                }
              }
            },
            "description": "Internal Server Error"
          }
        },
        "parameters": [
          {
            "in": "path",
            "name": "id",
            "schema": {
              "type": "string"
            },
            "required": true
          }
        ],
        "requestBody": {
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "name": {
                    "type": "string",
                    "description": "Wallet name. e.g. NGN Trading ",
                    "default": "NGN Trading"
                  }
                },
                "required": [
                  "name"
                ]
              },
              "examples": {
                "Update Wallet": {
                  "summary": "Update Wallet",
                  "value": "{\n  \"name\": \"NGN Primary\",\n}"
                }
              }
            }
          }
        },
        "summary": "Update Sub Wallet",
        "operationId": "patch_sub-wallets-id"
      }
    }
  },
  "components": {
    "securitySchemes": {
      "Authorization": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
      },
      "Timestamp": {
        "type": "apiKey",
        "in": "header",
        "name": "X-YC-Timestamp"
      }
    }
  },
  "x-readme": {},
  "security": [
    {
      "Timestamp": [],
      "Authorization": []
    }
  ]
}
```