# Pizza Express API
Welcome to the Pizza Express API Backend. This backend service is designed to streamline the process of handling pizza delivery orders, providing a seamless experience for both customers and administrators.
## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [API Documentation](#api-documentation)

---

## Introduction

Pizza Express API is a backend service built with FastAPI and PostgreSQL, designed to handle pizza delivery orders. It provides a set of APIs for creating, retrieving, and managing pizza orders, as well as user authentication.

---

## Features

- User authentication and authorization
- Create, retrieve, and update pizza orders
- Integration with a payment gateway for online payments
- Secure handling of user data and order information
- Error handling and validation checks for input data

---

## Technologies

- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT for authentication

---

## Setup and Installation

1. Clone the repository.
2. Set up a virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Set up the PostgreSQL database and update the connection string in `config.py`.
6. Start the FastAPI application using `uvicorn main:app --reload`.

---

## Usage

- Register a new user and obtain an authentication token.
- Use the token to make authenticated requests to the API.
- Create new pizza orders, retrieve order details, and update order status.

---

## API Endpoints

| Method | URL | Description | Access |
| --- | --- | --- | --- |
| POST | `/auth/signup/` | Register new user | All users |
| POST | `/auth/login/` | Login user | All users |
| POST | `/orders/order/` | Place an order | All users |
| PUT | `/orders/order/update/{order_id}/` | Update an order | All users |
| PUT | `/orders/order/status/{order_id}/` | Update order status | Superuser |
| DELETE | `/orders/order/delete/{order_id}/` | Delete/Remove an order | All users |
| GET | `/orders/user/orders/` | Get user's orders | All users |
| GET | `/orders/orders/` | List all orders made | Superuser |
| GET | `/orders/orders/{order_id}/` | Retrieve an order | Superuser |
| GET | `/orders/user/order/{order_id}/` | Get user's specific order | All users |
| GET | `/docs/` | View API documentation | All users |

---

## API Documentation

The API is documented using Swagger UI, which provides an interactive interface for exploring and testing the endpoints.

To access the API documentation, run the FastAPI application and navigate to [http://localhost:8000/docs](http://localhost:8000/docs) in your web browser.


© 2023 Pizza Express API. All Rights Reserved.

---
