# Food Vendor Management System

![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57)
![OOP](https://img.shields.io/badge/OOP-Object--Oriented-green)
![CRUD](https://img.shields.io/badge/CRUD-Application-orange)
![Portfolio Project](https://img.shields.io/badge/Portfolio-Project-purple)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow)

A Python-based food ordering and management application built to demonstrate object-oriented programming, relational database design, CRUD operations, user authentication, automated receipt generation, and multi-class application architecture.

The project was originally developed as a software development capstone and later documented as a portfolio project to showcase the engineering process behind building, testing, and debugging a complete backend application.

---

## Documentation

- [Application Architecture](docs/architecture.md)
- [Database Schema](docs/database-schema.md)
- [Lessons Learned](docs/lessons-learned.md)
- [Screenshots](docs/screenshots.md)

---

## Overview

The Food Vendor Management System simulates the core operations of a small food business.

Customers can log in, place orders, redeem reward points, update their profiles, and view their most recent order receipt. Guest users can place orders without creating an account. Administrative users can manage customer and employee accounts and modify the food menu.

The application uses an in-memory SQLite database populated from tab-separated data files. It runs through a command-line interface and generates formatted text receipts for completed orders.

---

## Features

### Customer functionality

* Customer authentication
* Food ordering by category
* Optional side-item selection
* Reward-point redemption
* Reward-point accumulation
* Profile updates
* Order-history retrieval
* Credit-card masking on receipts

### Guest functionality

* Guest checkout without an account
* Payment and contact-information collection
* Food ordering and receipt generation

### Administrative functionality

* Administrator authentication
* Customer and employee account creation
* Account-profile management
* Account deletion
* New menu-item creation
* Menu price updates
* Menu description updates
* Menu availability management

### Order processing

* Menu-category navigation
* Item availability validation
* Side-option selection
* Price calculation
* Reward discount calculation
* Estimated preparation-time calculation
* Receipt-number generation
* Text-file receipt creation

---

## Technologies and Concepts

* Python
* SQLite
* Object-oriented programming
* Inheritance
* Relational database design
* CRUD operations
* Parameterized SQL queries
* File input and output
* User authentication
* Input validation
* Unit testing
* Integration testing
* Incremental development
* Debugging across multiple classes

---

## Project Structure

```text
food-vendor-management-system/
├── data/
│   ├── menu.tsv
│   └── user.tsv
├── docs/
│   ├── architecture.md
│   ├── database-schema.md
│   └── lessons-learned.md
├── receipts/
│   └── FoodVendorReceipt1001.txt
├── src/
│   ├── DbManager.py
│   ├── FoodVendor.py
│   └── Users.py
├── tests/
│   └── ...
├── LICENSE
├── README.md
└── requirements.txt
```

The exact test-file collection may vary depending on the version of the repository.

---

## Application Architecture

The project separates application behavior, user behavior, and database operations across multiple classes.

### `FoodVendor`

Controls the primary application flow, including:

* database initialization
* customer and administrator login
* guest and member ordering
* receipt generation
* order-history display
* customer menus
* the main application menu

### `User`

Provides the shared base attributes used by customer and administrator accounts.

### `Customer`

Extends `User` and adds:

* credit-card information
* billing address
* reward points
* order history
* customer-profile updates

### `Admin`

Extends `User` and adds:

* employee identification
* account-management operations
* food-menu management
* administrator menu navigation

### `DbManager`

Encapsulates SQLite operations, including:

* database connection management
* table creation
* record insertion
* record retrieval
* record updates
* record deletion
* menu queries
* customer and administrator lookup

---

## Database Design

The application uses two primary tables.

### User table

Stores:

* username
* account type
* first and last name
* email address
* phone number
* password
* employee ID
* credit-card information
* billing address
* reward points
* order history

### Menu table

Stores:

* category
* item name
* description
* price
* preparation time
* availability status

The database is created in memory when the application starts and is populated from `user.tsv` and `menu.tsv`.

---

## Running the Application

### Requirements

* Python 3
* No third-party packages are required

### Start the program

From the project directory, run:

```bash
python3 FoodVendor.py
```

The application will display the main menu:

```text
Welcome to the Food Vendor!
Choose an option to begin.
    Customer login - Enter 1
    Place an order as a guest - Enter 2
    Manage system (admin sign-in required) - Enter 3
    Leave the Food Vendor - Enter 4
```

Follow the terminal prompts to log in, place an order, manage the system, or exit.

---

## Example Workflow

A guest user can:

1. Select the guest-ordering option.
2. Choose a food category.
3. Select a menu item.
4. Add an optional side item.
5. Continue ordering or check out.
6. Enter payment and contact information.
7. Receive a generated text receipt.

A registered customer can also redeem reward points and accumulate new points after completing an order.

An administrator can log in to manage user accounts and modify menu data.

---

## Receipt Generation

Completed orders generate text files using the following naming convention:

```text
FoodVendorReceipt1001.txt
FoodVendorReceipt1002.txt
FoodVendorReceipt1003.txt
```

Receipts include:

* business name
* customer information
* receipt number
* date and time
* ordered items
* item prices
* subtotal
* redeemed rewards
* total cost
* masked credit-card number
* reward points earned
* estimated wait time
* thank-you message

---

## Testing

The application was tested through a combination of:

* method-level unit tests
* database validation queries
* interactive command-line tests
* branch testing
* end-to-end integration tests

Examples of tested workflows include:

* successful and unsuccessful login attempts
* guest checkout
* customer checkout
* reward redemption
* customer-profile updates
* order-history retrieval
* food-price updates
* food-description updates
* food-availability updates
* administrator navigation
* customer navigation
* empty-order exit behavior
* drink ordering without side options

To run an individual test file:

```bash
python3 test_order_food.py
```

or, when tests are organized inside a `tests` directory:

```bash
python3 tests/test_order_food.py
```

---

## Engineering Challenges

### Coordinating state across classes

The application required customer data, menu data, order data, and database state to remain synchronized across several classes.

### Database access

Some methods were called directly while others were reached through menu-routing methods. Managing access to the correct database instance became one of the most important architectural concerns in the project.

### Automated testing assumptions

The application behaved correctly during local unit and integration testing, but some hidden automated tests initialized objects and database dependencies differently. Investigating those differences reinforced the importance of clear method contracts, dependency management, and controlled debugging.

### Preserving working functionality

As the project grew, changing one method could unintentionally affect several others. A known-good checkpoint and one-change-at-a-time debugging process helped protect working code while isolating defects.

---

## Lessons Learned

This project reinforced that software development involves much more than writing syntax.

The most valuable lessons included:

* Clear requirements reduce downstream development risk.
* Database dependencies should be explicit and consistent.
* Local testing and automated testing may expose different assumptions.
* Unit tests help isolate failures before full-system integration.
* Integration testing is necessary to verify that individually working methods cooperate correctly.
* Debugging should be treated as an experiment: change one variable, observe the result, and preserve a known-good version.
* A working application is not finished until its behavior, architecture, and limitations are documented.

The debugging and integration work ultimately provided as much educational value as the original implementation.

---

## Current Limitations

* The application uses a command-line interface rather than a graphical frontend.
* The SQLite database is stored in memory and resets when the program closes.
* Passwords are stored as plain text for educational purposes.
* Input validation is intentionally limited in some areas.
* The application is designed as a learning project rather than a production-ready ordering platform.
* Some administrative database-mutation behavior may differ under external automated test environments.

---

## Future Improvements

Potential future enhancements include:

* Web-based frontend
* REST API
* Persistent SQLite or PostgreSQL database
* Secure password hashing
* Session-based authentication
* Improved form validation
* Automated test suite using `unittest` or `pytest`
* Structured application logging
* Error handling for missing receipt files
* Search and filtering for menu items
* Order-cart editing
* Multiple-order history
* Docker containerization
* Cloud deployment
* Responsive administrator dashboard

---

## Project Progression

The engineering concepts practiced in this project directly support the development of more advanced CRUD applications.

The next stage of this progression is a timeline-management application for writers. That project applies similar principles to a different domain:

* customers become writers
* food items become story events
* menu categories become plotlines or character tracks
* orders become timeline arrangements
* receipts become timeline exports

The Food Vendor Management System therefore serves as both a completed backend project and a foundation for future full-stack software development.

---

## Author

**Vanisha Renee Pierce**

Software developer, instructional designer, and founder of god-Tier Storytelling.

---
