Feature: Verify Asteroids

  In order to communicate effectively to the asteroids functionality
  As a development team
  I want to test Onboarding endpoints and make sure its working as expected with UI

  Scenario: verify access to NASA asteroids endpoint		 
    Given the api service is: "asteroids"
    When the service method is "GET"
    Then the response code should be "200"
    And  "element_count" should match the total result
    And  verify required fields


  Scenario: verify NASA api aginst NASA ui 
    Given we have the data from the api 
    Then the UI should have the same data as the api