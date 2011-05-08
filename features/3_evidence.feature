Feature: Evidences
  In order to determine whether a hunch is supported
  people need to be able to add evidence to it
  
  Background: Make sure that we have a hunch
    Given I go to the hunches page
    And I follow "New Hunch"
    And I fill in "Title" with "Drought in Sudan"
    And I fill in "Description" with "Hungry season is lasting longer than usual."
    And I press "Create"
    
  Scenario: viewing evidence already added
    When I go to the hunches page
    Then I should see "0 evidence"
    
  Scenario: getting to the new evidence page
    When I go to the hunches page
    And I follow "New evidence"
    Then I should see an "Add evidence" button
    
  Scenario: Adding new evidence to a hunch
    Given I go to the hunches page
    And I follow "Add evidence"
    When I fill in "Evidence" with "There's a drought in Northern Uganda too"
    And I fill in "Description" with "Farmers here are starting to tweet about water problems."
    And I fill in "Rating" with "+3"
    And I press "Add evidence"
    Then I should see "Drought in Sudan"
    And I should be on the hunches page
    And I should see "1 evidence"
    And I should see "rating +3"
  