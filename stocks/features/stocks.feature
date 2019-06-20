Feature: Verify stocks prices

  In order to communicate effectively to the stocks functionality
  As a development team
  I want to test Onboarding endpoints and make sure its working as expected with UI

  Scenario: verify access to stocks endpoint		 
    Given the api service is for : "SNAP,fb" stocks
    When the service method is "GET"
    Then the response code should be "200"
    And  it should return the datafor "2" company
    And  verify required fields


  Scenario: verify NASA api aginst NASA ui 
    Given we have the data from the api 
    Then the UI should have the same data as the api
    