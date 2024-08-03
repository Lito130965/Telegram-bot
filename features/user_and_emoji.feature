Feature: Operations with adding new user, set and change emoji
  As a common user
  I want to set and change my emoji

  Scenario: New users should be add to database
    Given a new discovered user
    And i have three users in database
    When bot adding user to a database
    Then i should have four users in database

  Scenario: Set or change user's emoji
    Given i have one user in database
    When user set new emoji
    Then user emoji should be changed

  Scenario: Get all documents from database collection
    Given i have three users in database
    When bot getting documents from database
    Then i should have list with len equals three

  Scenario: Get all user's id from database collection
    Given i have three users in database
    When bot getting user's id from database
    Then i should have list with len equals three

