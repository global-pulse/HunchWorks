Feature: Hunches
  In order to see a list of hunches
  people need to be able to create and edit them

  Scenario: Getting to the new hunch page
    When I go to the hunches page
    And I follow "Create a Hunch"
    Then I should see a "Create" button

  Scenario: Creating a hunch
    Given I go to the hunches page
    And I follow "Create a Hunch"
    When I fill in "Title" with "Drought in Sudan"
    And I fill in "Description" with "Hungry season is lasting longer than usual."
    And I fill in "Geographical area" with "Sudan"
    And I fill in "sector" with "food"
    And I press "Create"
    Then I should see "Drought in Sudan"
    And I should be on the hunches page
  
